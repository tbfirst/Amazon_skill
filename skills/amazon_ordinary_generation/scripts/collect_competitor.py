#!/usr/bin/env python3
"""Collect visible Amazon gallery/A+ media into a project directory using Playwright."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse


def product_url(value, marketplace):
    if re.fullmatch(r'[A-Za-z0-9]{10}', value):
        return f'https://www.{marketplace}/dp/{value.upper()}'
    parsed = urlparse(value)
    if parsed.scheme != 'https' or parsed.hostname not in {'amazon.com', 'www.amazon.com', 'amazon.co.uk', 'www.amazon.co.uk', 'amazon.de', 'www.amazon.de', 'amazon.ca', 'www.amazon.ca'}:
        raise ValueError('Use an HTTPS Amazon product URL or a 10-character ASIN')
    match = re.search(r'/(?:dp|gp/product)/([A-Za-z0-9]{10})(?:/|$)', parsed.path)
    if not match:
        raise ValueError('Product URL must contain /dp/ASIN or /gp/product/ASIN')
    return f'https://{parsed.hostname}/dp/{match[1].upper()}'


def output_root(value):
    root = Path(value).resolve()
    skill = Path(__file__).resolve().parents[1]
    if root == skill or skill in root.parents or any(p.name in {'skills', '.agents'} for p in [root, *root.parents]):
        raise ValueError('Media output must be outside skill directories')
    return root


async def collect(args):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        raise RuntimeError('DEPENDENCY_MISSING: install playwright and its Chromium browser; no capture attempted')
    url = product_url(args.product, args.marketplace)
    root = output_root(args.out)
    asin = url.rsplit('/', 1)[-1]
    run = root / asin / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    run.mkdir(parents=True, exist_ok=False)
    report = {'requestedUrl': url, 'asin': asin, 'status': 'partial', 'viewed': 0,
              'coverage': 'Visible DOM candidates only; manual variant, module and completeness review required',
              'media': [], 'errors': [], 'nativeText': []}
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=not args.headed, chromium_sandbox=True, executable_path=args.browser_executable)
            context = await browser.new_context(viewport={'width': 1440, 'height': 1000})
            page = await context.new_page()
            await page.goto(url, wait_until='domcontentloaded', timeout=45000)
            await page.wait_for_timeout(1500)
            report['title'] = await page.title()
            if await page.locator('form[action*="validateCaptcha"]:visible, input#captchacharacters:visible, input#ap_email:visible').count():
                raise RuntimeError('ACCESS_REQUIRED: CAPTCHA or login page; capture stopped')
            report['resolvedUrl'] = page.url
            report['title'] = await page.title()
            report['variant'] = await page.locator('#ASIN').get_attribute('value') if await page.locator('#ASIN').count() else None
            if not await page.locator('#productTitle').count():
                raise RuntimeError('PRODUCT_PAGE_UNCONFIRMED: no product title; do not interpret as empty gallery')
            candidates = []
            async def gallery_image(index):
                data = await page.locator('#landingImage, #imgBlkFront').first.evaluate('''el => ({url:el.getAttribute('data-old-hires') || el.currentSrc || el.src, alt:el.alt})''')
                candidates.append(dict(data, section='gallery', moduleIndex=0, imageIndex=index))
            if await page.locator('#landingImage, #imgBlkFront').count():
                await gallery_image(0)
            thumbs = page.locator('#altImages li.imageThumbnail')
            for i in range(await thumbs.count()):
                try:
                    await thumbs.nth(i).hover(timeout=4000)
                    await thumbs.nth(i).click(timeout=4000)
                    await page.wait_for_timeout(400)
                    await gallery_image(i + 1)
                except Exception as exc:
                    report['errors'].append(f'gallery[{i}]: {exc}')
            # Bounded normal scrolling triggers lazy loading without hidden endpoints.
            for _ in range(35):
                bottom = await page.evaluate('window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 5')
                if bottom:
                    break
                await page.evaluate('window.scrollBy(0, 800)')
                await page.wait_for_timeout(200)
            containers = page.locator('#aplus_feature_div, #aplusBrandStory_feature_div')
            if not await containers.count():
                containers = page.locator('#aplus')
            for i in range(await containers.count()):
                block = containers.nth(i)
                await block.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)
                items = await block.evaluate('''el => Array.from(el.querySelectorAll('img')).map((im,i) => ({url:im.currentSrc || im.src, alt:im.alt, imageIndex:i, section:im.closest('#aplusBrandStory_feature_div, .aplus-brand-story') ? 'brand_story' : 'aplus', moduleIndex:Array.from(el.querySelectorAll('.aplus-module')).indexOf(im.closest('.aplus-module'))}))''')
                candidates.extend(items)
                report['nativeText'].append(await block.inner_text())
            files = {}
            seen = set()
            for item in candidates:
                key = (item['url'], item['section'], item['moduleIndex'], item['imageIndex'])
                if key in seen:
                    continue
                seen.add(key)
                item['status'] = 'discovered'
                report['media'].append(item)
                parsed = urlparse(item['url'])
                if parsed.scheme != 'https' or not parsed.hostname or not parsed.hostname.endswith(('.media-amazon.com', '.ssl-images-amazon.com', '.images-amazon.com')):
                    item['error'] = 'Unsupported media host or URL'
                    continue
                try:
                    if item['url'] not in files:
                        response = await context.request.get(item['url'], timeout=20000)
                        kind = response.headers.get('content-type', '').split(';')[0]
                        extensions = {'image/jpeg': '.jpg', 'image/png': '.png', 'image/webp': '.webp', 'image/gif': '.gif'}
                        if not response.ok or kind not in extensions:
                            raise RuntimeError(f'HTTP {response.status}, content type {kind}')
                        body = await response.body()
                        if not body:
                            raise RuntimeError('Empty media response')
                        name = hashlib.sha256(body).hexdigest() + extensions[kind]
                        (run / name).write_bytes(body)
                        files[item['url']] = name
                    item.update(file=files[item['url']], status='downloaded', visualReview='pending')
                except Exception as exc:
                    item['error'] = str(exc)
            report['downloadedFiles'] = len(set(files.values()))
            if not files:
                report['status'] = 'failed'
            await context.close()
            await browser.close()
    except Exception as exc:
        report['status'] = 'blocked'
        report['errors'].append(str(exc))
    finally:
        (run / 'manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'manifest': str(run / 'manifest.json'), 'status': report['status'], 'downloaded': report.get('downloadedFiles', 0)}, ensure_ascii=False))
    return 0 if report.get('downloadedFiles', 0) else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('product', nargs='?')
    parser.add_argument('--out')
    parser.add_argument('--marketplace', default='amazon.com', choices=['amazon.com', 'amazon.co.uk', 'amazon.de', 'amazon.ca'])
    parser.add_argument('--headed', action='store_true')
    parser.add_argument('--browser-executable', help='Explicit existing Chromium executable; browser compatibility must be checked')
    parser.add_argument('--check', action='store_true', help='Check Python Playwright and Chromium availability without network')
    args = parser.parse_args()
    try:
        if args.check:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as pw:
                executable = Path(args.browser_executable or pw.chromium.executable_path)
                print(json.dumps({'playwright': True, 'chromiumExists': executable.exists(), 'executable': str(executable)}))
                return 0 if executable.exists() else 2
        if not args.product or not args.out:
            parser.error('product and --out are required unless --check is used')
        product_url(args.product, args.marketplace)
        output_root(args.out)
        import asyncio
        return asyncio.run(collect(args))
    except (ImportError, ValueError, RuntimeError) as exc:
        print(f'Capture unavailable: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
