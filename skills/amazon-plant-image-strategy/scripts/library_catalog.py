"""Search reference text independently of local media; import portable snapshots."""
import argparse
import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / 'assets/reference-library/catalog.json'
SELECTED_IDS = {'INFO-06', 'QUAL-26', 'AMZ-87', 'SHADOW-01', 'LIGHT-02', 'QUAL-09'}


def reusable(record):
    observation = record.get('observation') or {}
    return (record.get('reuseEligible') is True
            and record.get('visualStatus', '').startswith('observed')
            and observation.get('reuseDecision') not in {'reject', 'hold'}
            and (observation.get('legacyReview') or {}).get('displayEligible') is not False)


def text_searchable(record):
    publication = record.get('publication') or {}
    return (reusable(record) and publication.get('status', 'published') == 'published'
            and 'text' in publication.get('scopes', ['text']))


def filter_recipe(recipe, eligible_ids):
    """Keep actual source identities and branches; never substitute another image."""
    result = copy.deepcopy(recipe)
    ids = [i for i in recipe.get('sourceImageIds', []) if i in eligible_ids]
    result.update(sourceImageIds=ids, sourceCount=len(ids))
    variants = result.get('promptVariants')
    if isinstance(variants, dict):
        result['promptVariants'] = {i: v for i, v in variants.items() if i in ids}
    elif isinstance(variants, list):
        result['promptVariants'] = [v for v in variants if v.get('imageId') in ids]
    return result


def retired(card):
    return card['id'].startswith('DSTYLE-')


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inside(root, relative):
    root = Path(root).resolve()
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or path == root:
        raise ValueError(f'Path outside library: {relative}')
    return path


def check_cards(data):
    cards = data['cards']
    ids = [c['id'] for c in cards]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError('Empty catalog or duplicate card IDs')
    for c in cards:
        if not isinstance(c.get('prompt'), str) and not c.get('promptSourceImageId'):
            raise ValueError(f"Missing recipe: {c['id']}")
    return cards


def references(card):
    refs = card.get('references', [])
    if not refs and card.get('reference'):
        refs = [card['reference']]
    return refs


def authored_extension(destination, source_cards):
    """Preserve the installed outdoor text pack when refreshing imported media."""
    path = Path(destination) / 'authored-outdoor.json'
    if not path.is_file():
        return [], []
    data = read_json(path)
    cards = copy.deepcopy(check_cards(data))
    source_ids = {c['id'] for c in source_cards}
    for card in cards:
        if card['id'] in source_ids:
            raise ValueError(f"Authored/source card ID conflict: {card['id']}")
        if (card.get('provenance', {}).get('kind') != 'skill-authored'
                or references(card) or card.get('bundledPreviews') or card.get('layoutSketch')):
            raise ValueError(f"Authored extension must be original text only: {card['id']}")
        card['bundledPreviews'] = []
    return cards, [dict(file=path.name, revision=data.get('revision'), cardCount=len(cards))]


def render_index(data):
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', ' ')
    lines = ['# 内置植物设计参考库\n\n',
             f"{data['cardCount']}个卡片入口，{len(data.get('images', []))}条图像记录，{data['bundledPreviewCount']}个内置成图参考。",
             '配图只提供版式或指定视觉效果；导入不等于逐图目视或Lovart实测。\n\n',
             '供agent按需读取，无需用户翻译。完整卡片/图像用 `scripts/library_catalog.py show ID` 读取；',
             '模板质量与配图可用性分别记录；无内置图的已审核文字模板仍可使用，不声称本轮看过缺失图片。\n\n',
             f"原库快照SHA-256：`{data['source']['sha256']}`。\n\n"]
    for extension in data.get('authoredExtensions', []):
        lines.append(f"另含{extension['cardCount']}条原创文字模板（`{extension['file']}`，"
                     f"版本`{extension['revision']}`），已计入模板总数；无新增成图或竞品观察，须适配SKU后使用。\n\n")
    if data.get('designGroups'):
        lines.extend(['## 按交付角色检索\n\n',
                      '| 分类 | 本地图片 | 用途 | 检索参数 |\n|---|---|---|---|\n'])
        for group, spec in data['designGroups'].items():
            lines.append(f"| {cell(spec['label'])} | {spec['count']} | {cell(' / '.join(spec['roles']))} | "
                         f"`--design-group {group}` |\n")
        lines.append('\n尺寸与细节共用版式池；`show IMG-ID --asset-role DIM01/DETAIL01`读取独立适配分支。'
                     '分类不合并A+产品身份；仍按具体图片核对内容和来源。\n\n')
    lines.extend([
             '| ID | 名称 | 图类 | 内置预览 |\n|---|---|---|---|\n']
    )
    for card in data['cards']:
        previews = ' / '.join(f"[预览{i}]({r['file']})" for i, r in enumerate(card['bundledPreviews'], 1)) or '无内置图；文字模板可用'
        lines.append(f"| {cell(card['id'])} | {cell(card.get('title', ''))} | {cell(' / '.join(card.get('imageTypes', [])))} | {previews} |\n")
    if data.get('series'):
        lines.extend(['\n## 套图索引（保留缺失图位）\n\n',
                      '以 `search --kind series` 检索，`show SET-ID` 按源图序读取；缺口不是已核实全套。\n\n',
                      '| SET ID | 商品/变体 | 已内置图库 | 已内置A+ |\n|---|---|---|---|\n'])
        for series in data['series']:
            members = series['members']
            lines.append(f"| {cell(series['id'])} | {cell(series.get('title', ''))} / {cell(series.get('variant', ''))} | "
                         f"{sum(m.get('bundled', False) and m['section'] == 'gallery' for m in members)} | "
                         f"{sum(m.get('bundled', False) and m['section'] == 'aplus' for m in members)} |\n")
    bundled_images = [r for r in data.get('images', []) if r.get('bundled')]
    if bundled_images:
        lines.extend(['\n## 已内置成图索引\n\n',
                      '先按标题/图类定位，再打开原图；`show IMG-ID` 读取该图观察与反推提示词。\n\n',
                      '| 图像 ID | 已记录标题 | 图类 | 成图 |\n|---|---|---|---|\n'])
        for record in bundled_images:
            observation = record.get('observation') or {}
            lines.append(f"| {record['id']} | {cell(observation.get('title', ''))} | "
                         f"{cell(' / '.join(observation.get('imageTypes', [])))} | [查看]({record['file']}) |\n")
    return ''.join(lines)


def import_catalog(source_root, destination, selection=None):
    source = Path(source_root).resolve()
    dest = Path(destination).resolve()
    if dest == source or dest.is_relative_to(source) or source.is_relative_to(dest):
        raise ValueError('Snapshot destination must be separate from source library')
    source_json = source / 'prompts.json'
    data = read_json(source_json)
    knowledge_path = source / 'agent-index.json'
    knowledge = read_json(knowledge_path) if knowledge_path.is_file() else {}
    cards = [copy.deepcopy(c) for c in check_cards(data) if not retired(c)]
    extra_cards, extensions = authored_extension(dest, cards)
    selection = read_json(selection) if selection else {}
    missing = []
    bundled = {}

    def bundle(relative, kind):
        normalized = Path(relative).as_posix().replace('\\', '/')
        if normalized.startswith('assets/layouts/'):
            raise ValueError(f'Retired layout preview: {relative}')
        original = inside(source, relative)
        if not original.is_file():
            raise ValueError(f'Selected source file missing: {relative}')
        if original.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp', '.svg'}:
            raise ValueError(f'Unsupported preview file: {relative}')
        raw = original.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        if selection.get('allowedMediaSha256s') is not None and sha not in selection['allowedMediaSha256s']:
            return None
        target_relative = selection.get('classifiedPathsBySha256', {}).get(sha, 'previews/' + normalized)
        target = inside(dest, target_relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        record = {'file': target_relative, 'sourceFile': relative,
                  'sha256': sha, 'kind': kind}
        bundled[target_relative] = record
        return record

    for card in cards:
        # Only use references explicitly assigned by the exported source catalog.
        card['bundledPreviews'] = []
        selected = card['id'].startswith('DIM-') or card['id'] in SELECTED_IDS
        candidates = [(r['file'], r.get('kind', 'source-preview')) for r in references(card)] if selected else []
        if selected and card.get('layoutSketch'):
            candidates.append((card['layoutSketch'], 'layout-sketch'))
        for relative, kind in candidates:
            original = inside(source, relative)
            if not original.is_file():
                missing.append({'card': card['id'], 'file': relative})
                continue
            record = bundle(relative, kind)
            if record is not None:
                card['bundledPreviews'].append(record)
    images = copy.deepcopy(knowledge.get('images', []))
    by_id = {i['id']: i for i in images}
    source_series = read_json(source / 'series-index.json').get('series', []) if (source / 'series-index.json').is_file() else []
    series_by_id = {s['id']: s for s in source_series}
    chosen_series = []
    image_ids = set(selection.get('imageIds', []))
    for series_id in selection.get('seriesIds', []):
        if series_id not in series_by_id:
            raise ValueError(f'Unknown selected series: {series_id}')
        series = copy.deepcopy(series_by_id[series_id])
        series.update({k: v for k, v in selection.get('seriesMetadata', {}).get(series_id, {}).items()
                       if k in {'titleZh', 'tags'}})
        for member in series['members']:
            record = by_id.get(member.get('imageId'))
            member['bundled'] = bool(member.get('status') == 'approved' and record and reusable(record))
            if member['bundled']:
                if member.get('sha256') and member['sha256'] != record.get('sha256'):
                    raise ValueError(f'Series/image hash mismatch: {series_id}')
                image_ids.add(record['id'])
            else:
                member['file'] = None
        chosen_series.append(series)
    for image_id in sorted(image_ids):
        record = by_id.get(image_id)
        if not record or not reusable(record):
            raise ValueError(f'Selected image is unknown or not reviewed for reuse: {image_id}')
        asset = bundle(record['file'], 'reviewed-finished-reference')
        if asset is None:
            image_ids.discard(image_id)
            continue
        if record.get('sha256') and record['sha256'] != asset['sha256']:
            raise ValueError(f'Source image hash changed: {image_id}')
        record.update(sourceFile=record['file'], bundledFile=asset['file'], file=asset['file'])
    for record in images:
        record['bundled'] = record['id'] in image_ids
    # Selection controls media bundling, not which series can be discovered as text.
    chosen_series = copy.deepcopy(source_series)
    for series in chosen_series:
        series.update({k: v for k, v in selection.get('seriesMetadata', {}).get(series['id'], {}).items()
                       if k in {'titleZh', 'tags'}})
        for member in series['members']:
            record = by_id.get(member.get('imageId'))
            member['bundled'] = bool(record and record['id'] in image_ids
                                     and member.get('status') == 'approved' and reusable(record))
            if member['bundled']:
                member['file'] = record['file']
            else:
                member['file'] = None
    recipes = (read_json(source / 'layout-recipes.json').get('recipes', [])
               if (source / 'layout-recipes.json').is_file() else [])
    for record in images:
        record['recipeIds'] = [r['id'] for r in recipes if record['id'] in r.get('sourceImageIds', [])]
        record['seriesIds'] = [s['id'] for s in chosen_series if any(m.get('imageId') == record['id'] for m in s['members'])]
    cards.extend(extra_cards)
    result = {
        'schemaVersion': 2,
        'source': {'root': source.as_posix(), 'file': 'prompts.json',
                   'sha256': digest(source_json), 'version': data.get('version'),
                   'date': data.get('date'),
                   'importedAt': datetime.now(timezone.utc).isoformat()},
        'scope': 'Text recipes and selected previews; no fresh visual validation or SKU evidence.',
        'authoredExtensions': extensions,
        'cardCount': len(cards), 'bundledPreviewCount': len(bundled),
        'missingSelectedPreviews': missing, 'cards': cards,
        'bundledAssets': list(bundled.values()), 'series': chosen_series,
        'selection': selection, 'retiredCardIds': [c['id'] for c in data['cards'] if retired(c)],
        'audience': 'agents', 'agentPolicy': knowledge.get('policy', {}),
        'images': images,
        'aplusNativeText': copy.deepcopy(knowledge.get('aplusNativeText', [])),
        'layoutRecipes': recipes,
        'sourceKnowledgeSha256': digest(knowledge_path) if knowledge_path.is_file() else None,
    }
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'catalog.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if (dest / 'classified-layouts.json').is_file():
        from refresh_local_library import reconcile
        result, _ = reconcile(dest / 'catalog.json')
        (dest / 'catalog.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (dest / 'index.md').write_text(render_index(result), encoding='utf-8')
    return dict({k: result[k] for k in ['cardCount', 'bundledPreviewCount', 'missingSelectedPreviews']},
                seriesCount=len(chosen_series), bundledImageCount=len(image_ids))


def search_series(series, query='', limit=8):
    if limit < 1:
        raise ValueError('limit must be positive')
    terms = query.casefold().split()
    results = []
    for entry in series:
        body = json.dumps({k: entry.get(k) for k in ['id', 'title', 'titleZh', 'variant', 'tags', 'requestedAsin']}, ensure_ascii=False).casefold()
        if all(t in body for t in terms):
            members = [m for m in entry['members'] if m.get('available', m.get('bundled', False))]
            results.append(dict({k: entry.get(k) for k in ['id', 'title', 'titleZh', 'variant', 'requestedAsin', 'variantAsin', 'scope']},
                                bundledGallery=sum(m['section'] == 'gallery' for m in members),
                                bundledAplus=sum(m['section'] == 'aplus' for m in members),
                                textImageCount=sum(bool(m.get('textSearchable')) for m in entry['members']),
                                imageTypes=sorted({m.get('imageType', 'unknown') for m in members})))
    return results[:limit]


def resolve_image(record, root, portable=False):
    if record is None:
        return None
    result = copy.deepcopy(record)
    media = record.get('media') or {}
    media_states = {}
    for kind in ['preview', 'original']:
        asset = media.get(kind) or {}
        candidate = inside(root, asset['path']) if asset.get('path') else None
        media_states[kind] = bool(candidate and candidate.is_file()
                                  and asset.get('sha256') == digest(candidate))
    selected = next((media[k] for k in ['original', 'preview'] if media_states[k]), None)
    path = inside(root, selected['path']) if selected else (inside(root, record['file']) if record.get('file') else None)
    legacy_allowed = not portable or record.get('bundled') is True
    available = bool(selected or (not media and legacy_allowed and path and path.is_file()
                                  and (not record.get('sha256') or digest(path) == record['sha256'])))
    result.update(available=available, localAvailable=available,
                  resolvedFile=str(path) if available else None,
                  previewAvailable=media_states['preview'],
                  originalAvailable=media_states['original'] or (available and not media),
                  textSearchable=text_searchable(record), fetchable=False,
                  observedThisRun=False,
                  mediaStatus='local' if available else 'text-only')
    if not available:
        for branch in result.get('planningPrompts', {}).values():
            if branch.get('textOnlyUsable'):
                if branch.get('referenceFile'):
                    branch['sourceReferenceFile'] = branch['referenceFile']
                branch['referenceFile'] = None
                branch['referenceStatus'] = 'text-only; no available image attachment'
    return result


def search_cards(cards, query='', image_type=None, limit=8):
    if limit < 1:
        raise ValueError('limit must be positive')
    terms = query.casefold().split()
    matches = []
    for card in cards:
        if image_type and image_type not in card.get('layoutImageTypes', card.get('imageTypes', [])):
            continue
        title = ' '.join([card['id'], card.get('title', ''), card.get('category', ''),
                          *card.get('tags', []), *card.get('productTypes', [])]).casefold()
        identity = json.dumps({k: card.get(k) for k in
                              ['productKey', 'principalProduct', 'sourceAsins', 'promptVariants']},
                              ensure_ascii=False).casefold()
        body = title + ' ' + card.get('promptZh', '').casefold() + ' ' + card.get('prompt', '').casefold() + ' ' + identity
        if not all(t in body for t in terms):
            continue
        # Generic categories often contain “尺寸/卖点/A+” on unrelated cards.
        # Prefer the actual image type and title over a shared category label.
        score = sum(
            (20 if t == card['id'].casefold() else 0)
            + (10 if t in card.get('title', '').casefold() else 0)
            + (12 if any(t in v.casefold() for v in card.get('imageTypes', [])) else 0)
            + (6 if any(t in v.casefold() for v in card.get('productTypes', [])) else 0)
            + (2 if any(t in v.casefold() for v in card.get('tags', [])) else 0)
            + (1 if t in body else 0)
            for t in terms)
        matches.append((score, card))
    matches.sort(key=lambda item: (-item[0], item[1]['id']))
    return [{k: card.get(k) for k in ['id', 'title', 'category', 'imageTypes', 'productTypes',
             'status', 'imageStatus', 'layoutSketch', 'bundledPreviews',
             'productKey', 'principalProduct', 'sourceAsins', 'promptZh', 'promptVariants',
             'designGroups', 'targetRoles', 'layoutImageTypes', 'promptSourceImageId', 'description']}
            for _, card in matches[:limit]]


def search_images(images, query='', image_type=None, limit=8, include_restricted=False):
    if limit < 1:
        raise ValueError('limit must be positive')
    matches = []
    for record in images:
        observation = record.get('observation') or {}
        restricted = (record.get('reuseEligible') is False
                      or observation.get('reuseDecision') in {'reject', 'hold'}
                      or (observation.get('legacyReview') or {}).get('displayEligible') is False)
        if restricted and not include_restricted:
            continue
        types = ['尺寸图', '细节图'] if 'dimensions-details' in record.get('designGroups', []) else observation.get('imageTypes', [])
        if image_type and image_type not in types:
            continue
        # Shared policy/negative constraints and hashes are not visual evidence.
        # Otherwise e.g. every 'do not add flowers' record matches 'flowers'.
        status = record.get('visualStatus', 'pending')
        visible = {k: observation.get(k) for k in
                   ['title', 'imageTypes', 'overview', 'layout', 'lighting', 'shadows']}
        body = json.dumps(visible if status.startswith('observed') else {
            'id': record['id'], 'originalName': record.get('originalName')}, ensure_ascii=False).casefold()
        body += ' ' + record['id'].casefold()
        terms = query.casefold().split()
        if not all(t in body for t in terms):
            continue
        score = sum(10 if t in observation.get('overview', '').casefold() else 1 for t in terms)
        matches.append((score + (20 if status.startswith('observed') and not restricted else 0), record, observation))
    matches.sort(key=lambda v: (-v[0], v[1]['id']))
    return [dict(id=r['id'], file=r.get('file'), originalName=r.get('originalName'),
                 status=r.get('visualStatus', 'pending'), imageTypes=o.get('imageTypes', []),
                 layoutImageTypes=['尺寸图', '细节图'] if 'dimensions-details' in r.get('designGroups', []) else o.get('imageTypes', []),
                 designGroups=r.get('designGroups', []), targetRoles=r.get('targetRoles', []),
                 overview=o.get('overview') if r.get('visualStatus', '').startswith('observed') else None,
                 reviewMethod=o.get('reviewMethod'), limitations=o.get('limitations'),
                 restricted=(r.get('reuseEligible') is False or o.get('reuseDecision') in {'reject', 'hold'}
                             or (o.get('legacyReview') or {}).get('displayEligible') is False),
                 selectionUse='Open original before precise layout use' if r.get('visualStatus', '').startswith('observed') else 'Metadata only; no visual layout evidence',
                 cardIds=r.get('cardIds', []), principalProducts=r.get('principalProducts', []),
                 aplusTemplateEligible=r.get('aplusTemplateEligible'),
                 aplusTemplateScope=r.get('aplusTemplateScope'))
            for _, r, o in matches[:limit]]


def search_recipes(recipes, query='', image_type=None, limit=8):
    if limit < 1:
        raise ValueError('limit must be positive')
    terms = query.casefold().split()
    matches = [r for r in recipes if (not image_type or image_type in r.get('layoutImageTypes', r.get('imageTypes', [])))
            and all(t in json.dumps({k: r.get(k) for k in [
                'id', 'title', 'imageTypes', 'layout', 'prompt', 'promptZh', 'promptVariants',
                'productKey', 'principalProduct', 'sourceAsins']},
                                    ensure_ascii=False).casefold() for t in terms)][:limit]
    # Search discovers IDs and scope; read one full prompt through show --image-id.
    return [dict({k: copy.deepcopy(r.get(k)) for k in [
        'id', 'title', 'category', 'imageTypes', 'productTypes', 'productKey',
        'principalProduct', 'sourceAsins', 'sourceCount', 'sourceImageIds', 'promptRevision',
        'designGroups', 'targetRoles', 'layoutImageTypes']},
        layoutSummary=(r.get('layoutZh') or r.get('layout') or '')[:240],
        variantCount=len(variant_summaries(r)), variants=variant_summaries(r)) for r in matches]


def variant_summaries(recipe):
    variants = recipe.get('promptVariants') or {}
    rows = variants.items() if isinstance(variants, dict) else [
        (v.get('imageId'), v) for v in variants if isinstance(v, dict)]
    return [dict(imageId=image_id, **{k: copy.deepcopy(value[k]) for k in
                 ['title', 'sourceSlot', 'referenceFile', 'copyMode', 'outputSpec'] if k in value})
            for image_id, value in rows if isinstance(value, dict)]


def show_recipe(recipe, image_id=None, images=None):
    """Return one independent branch, or a default prompt with compact choices."""
    result = copy.deepcopy(recipe)
    variants = result.pop('promptVariants', None) or {}
    summaries = variant_summaries(recipe)
    if image_id is None:
        result.update(variantCount=len(summaries), variants=summaries)
        return result
    if isinstance(variants, dict):
        selected = variants.get(image_id)
    else:
        selected = next((v for v in variants if isinstance(v, dict) and v.get('imageId') == image_id), None)
    if not variants and image_id in recipe.get('sourceImageIds', []):
        selected = recipe
    if isinstance(selected, dict) and selected.get('promptSourceImageId'):
        image = (images or {}).get(selected['promptSourceImageId'])
        if not image or not image.get('textSearchable'):
            raise ValueError(f'Selected planning reference is not eligible: {image_id}')
        if not image.get('available') and not image.get('planningPrompts', {}).get('APLUS', {}).get('textOnlyUsable'):
            raise ValueError(f'Selected planning reference is not locally available: {image_id}')
        selected = dict(selected, **image['planningPrompts']['APLUS'])
    if not isinstance(selected, dict) or not isinstance(selected.get('prompt'), str):
        raise ValueError(f'Unknown or unavailable image branch: {image_id} for {recipe["id"]}')
    result.update(copy.deepcopy({k: v for k, v in selected.items() if k != 'promptVariants'}))
    result.update(selectedImageId=image_id, sourceImageIds=[image_id], sourceCount=1,
                  variantCount=len(summaries))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    imp = subs.add_parser('import')
    imp.add_argument('--source-root', required=True)
    imp.add_argument('--destination', required=True)
    imp.add_argument('--selection', type=Path, help='Explicit reviewed series/image selection for a portable release')
    for command in ['sync', 'fetch', 'cache']:
        p = subs.add_parser(command)
        p.add_argument('--config', required=True, type=Path, help='User-owned trusted remote source configuration')
        p.add_argument('--cache-dir', type=Path)
        if command in ['sync', 'fetch']:
            p.add_argument('--offline', action='store_true')
        if command == 'sync':
            p.add_argument('--strict', action='store_true', help='Fail instead of returning cached/bundled fallback')
        if command == 'fetch':
            p.add_argument('image_ids', nargs='*')
            p.add_argument('--series')
            p.add_argument('--size', choices=['preview', 'original'], default='preview')
            p.add_argument('--library-version')
            p.add_argument('--limit', type=int, default=8, help='Maximum images for --series')
    for command in ['search', 'show']:
        p = subs.add_parser(command)
        p.add_argument('--catalog', type=Path, default=DEFAULT_CATALOG)
        p.add_argument('--source-root', type=Path)
        p.add_argument('--manifest', type=Path, help='Verified local immutable library manifest (no network sync)')
        p.add_argument('--config', type=Path, help='Read a synced remote index; does not silently sync')
        p.add_argument('--cache-dir', type=Path)
        p.add_argument('--library-version', help='Use a specified already-synced version')
        p.add_argument('--offline', action='store_true', help='Never request uncached selected records')
        if command == 'search':
            p.add_argument('--query', default='')
            p.add_argument('--image-type')
            p.add_argument('--design-group', choices=['aplus', 'dimensions-details', 'scenes'],
                           help='User-classified layout pool; does not replace observed image content')
            p.add_argument('--limit', type=int, default=8)
            p.add_argument('--kind', choices=['template', 'image', 'recipe', 'series', 'all'], default='template')
            p.add_argument('--include-restricted', action='store_true', help='Diagnostics only')
            p.add_argument('--available-only', action='store_true', help='Only references with actual local media')
        else:
            p.add_argument('card_id')
            p.add_argument('--image-id', help='Read one image-specific recipe branch')
            p.add_argument('--asset-role', choices=['DIM01', 'DETAIL01', 'SCENE', 'APLUS'],
                           help='Select the image-bound planning adaptation')
    args = parser.parse_args()
    try:
        client = None
        if args.command == 'import':
            result = import_catalog(args.source_root, args.destination, args.selection)
        elif args.command in ['sync', 'fetch', 'cache']:
            from library_remote import LibraryClient
            client = LibraryClient(args.config, args.cache_dir)
            if args.command == 'sync':
                result = client.sync(args.offline, args.strict)
            elif args.command == 'fetch':
                result = client.fetch(args.image_ids, args.series, args.size, args.library_version, args.offline, args.limit)
            else:
                result = client.cache_status()
        else:
            if sum(bool(v) for v in [args.manifest, args.source_root, args.config]) > 1:
                raise ValueError('--config, --manifest and --source-root are mutually exclusive')
            if args.library_version and not args.config:
                raise ValueError('--library-version requires --config')
            path = args.source_root / 'prompts.json' if args.source_root else args.catalog
            library_source = 'external' if args.source_root else 'local-manifest' if args.manifest else 'bundled'
            remote_entry = None
            fallback_reason = None
            if args.config:
                from library_remote import LibraryClient
                client = LibraryClient(args.config, args.cache_dir)
                try:
                    data, _, path, remote_entry = client.snapshot(args.library_version)
                    library_source = 'synced-cache'
                except (ValueError, OSError, KeyError, TypeError) as exc:
                    if args.library_version:
                        raise
                    # No implicit network request or silent substitution of a pinned version.
                    client = None
                    fallback_reason = str(exc)
                    path = DEFAULT_CATALOG
                    data = read_json(path)
                    library_source = 'bundled-fallback'
            elif args.manifest:
                from library_build import load_manifest
                path = args.manifest
                data, _ = load_manifest(path)
            else:
                data = read_json(path)
                if not args.source_root and data.get('schemaVersion', 1) not in {1, 2}:
                    raise ValueError('Unsupported portable catalog schema')
            cards = [c for c in (check_cards(data) if data.get('cards') else []) if not retired(c)]
            knowledge_path = args.source_root / 'agent-index.json' if args.source_root else None
            knowledge = read_json(knowledge_path) if knowledge_path and knowledge_path.is_file() else data
            images = knowledge.get('images', [])
            recipes = (read_json(args.source_root / 'layout-recipes.json').get('recipes', [])
                       if args.source_root and (args.source_root / 'layout-recipes.json').is_file()
                       else data.get('layoutRecipes', []))
            policy = knowledge.get('policy', knowledge.get('agentPolicy', {}))
            portable = not args.source_root and not args.manifest and not client and data.get('schemaVersion', 1) == 2
            image_root = args.source_root.resolve() if args.source_root else path.resolve().parent
            resolve = (lambda r: client.resolve(r, remote_entry['manifestUrl'], data['libraryVersion'])) if client else (lambda r: resolve_image(r, image_root, portable))
            resolved = {r['id']: resolve(r) for r in images}
            if data.get('promptPolicy', {}).get('requireLocalReference'):
                # Missing/tampered media must not expose a stale planning prompt,
                # even before the maintainer runs refresh_local_library.
                active_ids = {i for i, r in resolved.items() if r['available'] and r['textSearchable']}
                for i, r in resolved.items():
                    if i not in active_ids:
                        r['textSearchable'] = False
                cards = [c for c in cards if c.get('promptSourceImageId') in active_ids]
            eligible_ids = {i for i, r in resolved.items() if r['textSearchable']}
            # Older external text-only exports have no image index to adjudicate.
            if images or not args.source_root:
                recipes = [filter_recipe(r, eligible_ids) for r in recipes]
                recipes = [r for r in recipes if r['sourceImageIds']]
            series = (read_json(args.source_root / 'series-index.json').get('series', [])
                      if args.source_root and (args.source_root / 'series-index.json').is_file()
                      else data.get('series', []))
            for entry in series:
                for member in entry['members']:
                    record = resolved.get(member.get('imageId'))
                    allowed = bool(record and record['textSearchable'] and member.get('status') == 'approved'
                                   and member.get('published', True))
                    member['textSearchable'] = allowed
                    member['available'] = bool(allowed and record['available'])
                    member['resolvedFile'] = record['resolvedFile'] if member['available'] else None
            available_ids = {i for i, r in resolved.items() if r['available']}
            if args.command == 'search':
                selected_cards = [c for c in cards if (not args.design_group or args.design_group in c.get('designGroups', []))
                                  and (not args.available_only or any(
                                      inside(image_root, p['file']).is_file() and
                                      (not p.get('sha256') or digest(inside(image_root, p['file'])) == p['sha256'])
                                      for p in c.get('bundledPreviews', [])))]
                matches = search_cards(selected_cards, args.query, args.image_type, args.limit) if args.kind in ['template', 'all'] else []
                searchable_images = [r for r in images if (args.include_restricted or r['id'] in eligible_ids)
                                     and (not args.design_group or args.design_group in r.get('designGroups', []))
                                     and (not args.available_only or r['id'] in available_ids)]
                searchable_recipes = [r for r in recipes
                                      if (not args.design_group or args.design_group in r.get('designGroups', []))
                                      and (not args.available_only or available_ids.intersection(r.get('sourceImageIds', [])))]
                image_matches = search_images(searchable_images, args.query, args.image_type, args.limit, args.include_restricted) if args.kind in ['image', 'all'] else []
                for match in image_matches:
                    match.update({k: resolved[match['id']][k] for k in [
                        'available', 'localAvailable', 'resolvedFile', 'previewAvailable',
                        'originalAvailable', 'textSearchable', 'fetchable', 'observedThisRun', 'mediaStatus']})
                    if client:
                        match.update({k: resolved[match['id']][k] for k in ['previewFetchable', 'originalFetchable']})
                recipe_matches = search_recipes(searchable_recipes, args.query, args.image_type, args.limit) if args.kind in ['recipe', 'all'] else []
                for match in recipe_matches:
                    match['availableImageIds'] = [i for i in match.get('sourceImageIds', []) if i in available_ids]
                searchable_series = [s for s in series
                                     if (not args.available_only or any(m.get('available') for m in s['members']))
                                     and (not args.design_group or any(args.design_group in m.get('designGroups', []) for m in s['members']))]
                series_matches = search_series(searchable_series, args.query, args.limit) if args.kind in ['series', 'all'] else []
                result = {'catalog': str(path.resolve()), 'agentPolicy': policy,
                          'imageRoot': str(image_root), 'portable': portable,
                          'libraryVersion': data.get('libraryVersion', data.get('source', {}).get('version')),
                          'manifestHash': data.get('manifestHash'),
                          'coverage': dict(totalImages=len(images), textSearchableImages=len(eligible_ids), localImages=len(available_ids)),
                          'designGroups': data.get('designGroups', {}),
                          'matches': matches, 'images': image_matches, 'recipes': recipe_matches, 'series': series_matches}
            else:
                card = next((c for c in cards if c['id'] == args.card_id), None)
                image = next((r for r in images if r['id'] == args.card_id), None)
                if image and data.get('promptPolicy', {}).get('requireLocalReference') and image['id'] not in eligible_ids:
                    raise ValueError('Selected planning reference is not locally available and eligible')
                recipe = next((r for r in recipes if r['id'] == args.card_id), None)
                selected_series = next((s for s in series if s['id'] == args.card_id), None)
                if card is None and image is None and recipe is None and selected_series is None:
                    raise ValueError(f'Unknown card: {args.card_id}')
                if card and card.get('promptSourceImageId'):
                    image = resolved[card['promptSourceImageId']]
                if args.image_id and recipe is None and selected_series is None:
                    raise ValueError('--image-id requires a recipe or series ID')
                if recipe is not None:
                    recipe = show_recipe(recipe, args.image_id, resolved)
                if selected_series is not None and args.image_id:
                    members = [m for m in selected_series['members'] if m.get('imageId') == args.image_id]
                    if not members or not all(m['textSearchable'] for m in members):
                        raise ValueError(f'Unavailable image branch: {args.image_id} for {selected_series["id"]}')
                    selected_series = copy.deepcopy(selected_series)
                    selected_series['members'] = members
                    image = resolved[args.image_id]
                if args.asset_role:
                    source_id = args.image_id or (image or {}).get('id')
                    candidates = ([resolved[source_id]] if source_id in resolved else
                                  [r for r in resolved.values() if card and
                                   r.get('sha256') in {p.get('sha256') for p in card.get('bundledPreviews', [])}])
                    candidates = [r for r in candidates if args.asset_role in r.get('planningPrompts', {})]
                    if len(candidates) != 1:
                        raise ValueError('Asset-role adaptation requires one selected dimension/detail image ID')
                    if (not candidates[0]['textSearchable'] or
                            (not candidates[0]['available'] and not candidates[0]['planningPrompts'][args.asset_role].get('textOnlyUsable'))):
                        raise ValueError('Selected planning reference is not locally available and eligible')
                    planning_template = candidates[0]['planningPrompts'][args.asset_role]
                else:
                    planning_template = None
                if planning_template is None:
                    canonical_id = (card or {}).get('promptSourceImageId') or (image or {}).get('id')
                    canonical = resolved.get(canonical_id, {})
                    branches = canonical.get('planningPrompts', {})
                    if canonical.get('textSearchable') and len(branches) == 1 and (
                            canonical.get('available') or next(iter(branches.values())).get('textOnlyUsable')):
                        planning_template = next(iter(branches.values()))
                # Search reads only summaries; show verifies and loads just the selected detail.
                if image and client:
                    image = client.detail(image, path, remote_entry, args.offline)
                elif image and args.manifest:
                    from library_build import checked_json
                    image = checked_json(image_root, image['record'])
                reference_images = []
                if recipe:
                    for image_id in recipe.get('sourceImageIds', []):
                        r = resolved.get(image_id)
                        if r:
                            reference_images.append({k: r.get(k) for k in [
                                'id', 'file', 'available', 'localAvailable', 'resolvedFile', 'visualStatus',
                                'textSearchable', 'fetchable', 'observedThisRun', 'mediaStatus']})
                    if args.image_id and (images or not args.source_root) and args.image_id not in eligible_ids:
                        raise ValueError(f'Selected recipe image is not eligible: {args.image_id}')
                result = {'catalog': str(path.resolve()), 'agentPolicy': policy,
                          'imageRoot': str(image_root), 'portable': portable,
                          'libraryVersion': data.get('libraryVersion', data.get('source', {}).get('version')),
                          'manifestHash': data.get('manifestHash'),
                          'card': card, 'image': resolve(image) if image else None, 'recipe': recipe,
                          'series': selected_series, 'referenceImages': reference_images,
                          'planningTemplate': planning_template}
            result.update(librarySource=library_source, fallbackReason=fallback_reason)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.command == 'fetch' and result['status'] == 'failed':
            parser.exit(2)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f'{exc}\n')


if __name__ == '__main__':
    main()
