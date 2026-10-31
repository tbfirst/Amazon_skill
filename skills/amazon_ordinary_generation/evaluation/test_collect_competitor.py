import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'collect_competitor.py'
spec = importlib.util.spec_from_file_location('collector', SCRIPT)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


class CollectorBoundaryTests(unittest.TestCase):
    def test_product_identity(self):
        self.assertEqual(collector.product_url('b012345678', 'amazon.com'), 'https://www.amazon.com/dp/B012345678')
        self.assertEqual(collector.product_url('https://www.amazon.de/gp/product/B012345678?ref=test', 'amazon.com'), 'https://www.amazon.de/dp/B012345678')

    def test_reject_non_product_or_untrusted_urls(self):
        for url in ['http://www.amazon.com/dp/B012345678', 'https://amazon.com.evil.example/dp/B012345678', 'https://www.amazon.com/s?k=chairs']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                collector.product_url(url, 'amazon.com')

    def test_media_cannot_enter_skill_package(self):
        for root in [SCRIPT.parent.parent, SCRIPT.parent.parent / 'assets', '/tmp/skills/another-skill/images']:
            with self.subTest(root=root), self.assertRaises(ValueError):
                collector.output_root(str(root))
        self.assertEqual(collector.output_root('/tmp/ordinary-project/media'), Path('/tmp/ordinary-project/media').resolve())


# Offline browser fixture exercises the actual collection flow, not live Amazon.
import asyncio
import json
import tempfile
import types
from unittest.mock import AsyncMock, patch


class CollectionRecoveryTests(unittest.TestCase):
    def run_capture(self, *, broken_aplus=False, fail_download=False, fail_hires=False):
        media_url = 'https://m.media-amazon.com/images/I/example.jpg'

        class Locator:
            def __init__(self, selector):
                self.selector = selector

            @property
            def first(self):
                return self

            def nth(self, i):
                return self

            async def count(self):
                return int(self.selector in {'#productTitle', '#landingImage, #imgBlkFront',
                                             '#altImages li.imageThumbnail',
                                             '#aplus_feature_div, #aplusBrandStory_feature_div'})

            async def evaluate(self, expression):
                if self.selector == '#landingImage, #imgBlkFront':
                    return {'url': media_url, 'urls': [media_url, 'https://m.media-amazon.com/images/I/display.jpg'], 'alt': 'Example product'}
                return [{'url': 'https://m.media-amazon.com/images/I/aplus.jpg', 'alt': '',
                         'section': 'aplus', 'moduleIndex': 0, 'imageIndex': 0}]

            async def scroll_into_view_if_needed(self, **kwargs):
                if broken_aplus:
                    raise RuntimeError('A+ container is hidden')

            async def inner_text(self, **kwargs):
                return 'A+ native copy'

            async def hover(self, **kwargs):
                pass

            async def click(self, **kwargs):
                pass

        page = types.SimpleNamespace(url='https://www.amazon.com/dp/B012345678',
                                     goto=AsyncMock(), wait_for_timeout=AsyncMock(),
                                     title=AsyncMock(return_value='Product title'),
                                     locator=Locator, evaluate=AsyncMock(return_value=True))
        response = types.SimpleNamespace(ok=True, status=200, headers={'content-type': 'image/jpeg'},
                                         body=AsyncMock(return_value=b'fixture image bytes'))
        request = types.SimpleNamespace(get=AsyncMock(return_value=response))
        if fail_hires:
            async def fetch(url, **kwargs):
                if url == media_url:
                    raise RuntimeError('High-resolution URL unavailable')
                return response
            request.get.side_effect = fetch
        if fail_download:
            request.get.side_effect = RuntimeError('Media request failed')
        context = types.SimpleNamespace(new_page=AsyncMock(return_value=page), request=request, close=AsyncMock())
        browser = types.SimpleNamespace(new_context=AsyncMock(return_value=context), close=AsyncMock())

        class Playwright:
            chromium = types.SimpleNamespace(launch=AsyncMock(return_value=browser))

            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                pass

        module = types.ModuleType('playwright.async_api')
        module.async_playwright = Playwright
        with tempfile.TemporaryDirectory() as tmp, patch.dict('sys.modules', {
            'playwright': types.ModuleType('playwright'), 'playwright.async_api': module
        }):
            args = types.SimpleNamespace(product='B012345678', marketplace='amazon.com',
                                         out=tmp, headed=False, browser_executable=None)
            result = asyncio.run(collector.collect(args))
            manifest_path = next(Path(tmp).rglob('manifest.json'))
            manifest = json.loads(manifest_path.read_text())
            for item in manifest['media']:
                if item['status'] == 'downloaded':
                    self.assertTrue((manifest_path.parent / item['file']).is_file())
            context.close.assert_awaited()
            browser.close.assert_awaited()
            return result, manifest

    def test_aplus_failure_preserves_and_downloads_gallery(self):
        result, manifest = self.run_capture(broken_aplus=True)
        self.assertEqual(result, 0)
        self.assertEqual(manifest['status'], 'partial')
        self.assertEqual(manifest['downloadedFiles'], 1)
        self.assertEqual(manifest['media'][0]['section'], 'gallery')
        self.assertTrue(any('A+ container is hidden' in e for e in manifest['errors']))
        self.assertEqual(manifest['viewed'], 0)

    def test_main_and_first_thumbnail_are_one_gallery_entry(self):
        _, manifest = self.run_capture()
        self.assertEqual(len([m for m in manifest['media'] if m['section'] == 'gallery']), 1)
        self.assertEqual(len([m for m in manifest['media'] if m['section'] == 'aplus']), 1)

    def test_download_failure_retains_candidates(self):
        result, manifest = self.run_capture(fail_download=True)
        self.assertEqual(result, 2)
        self.assertEqual(manifest['status'], 'failed')
        self.assertEqual(len(manifest['media']), 2)
        self.assertTrue(all(m['status'] == 'discovered' for m in manifest['media']))

    def test_high_resolution_failure_falls_back_to_display_image(self):
        result, manifest = self.run_capture(fail_hires=True)
        self.assertEqual(result, 0)
        gallery = next(m for m in manifest['media'] if m['section'] == 'gallery')
        self.assertEqual(gallery['status'], 'downloaded')
        self.assertTrue(gallery['downloadedUrl'].endswith('/display.jpg'))
        self.assertEqual(len(gallery['downloadAttempts']), 2)
        self.assertIn('error', gallery['downloadAttempts'][0])

    def test_european_product_domains_preserve_marketplace(self):
        for domain in ('amazon.fr', 'amazon.it', 'amazon.es', 'amazon.nl', 'amazon.com.be', 'amazon.ie'):
            with self.subTest(domain=domain):
                url = f'https://www.{domain}/dp/B012345678'
                self.assertEqual(collector.product_url(url, 'amazon.com'), url)
                self.assertEqual(collector.product_url('B012345678', domain), url)

if __name__ == '__main__':
    unittest.main()
