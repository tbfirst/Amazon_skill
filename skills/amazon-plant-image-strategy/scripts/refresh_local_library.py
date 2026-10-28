"""Reconcile a classified portable library with its existing image bytes; no downloads."""
import argparse
import copy
import json
from pathlib import Path

from library_catalog import DEFAULT_CATALOG, digest, inside, read_json, render_index


REVISION = 'classified-layouts-20261026-r1'
GROUPS = {
    'aplus': dict(folder='Aplus', label='A+图', roles=['APLUS'],
                  guide='classified-reference-layouts.md#aplus'),
    'dimensions-details': dict(folder='dimensions', label='尺寸与细节设计图',
                              roles=['DIM01', 'DETAIL01'],
                              guide='classified-reference-layouts.md#dimensions-details'),
    'scenes': dict(folder='collected', label='场景图', roles=['SCENE'],
                   guide='classified-reference-layouts.md#scenes'),
}


def planning_prompt(record, layout, role):
    """Use the shared compact prompt writer for both dimension/detail roles."""
    from grounded_prompts import prompt_for
    return prompt_for(layout, role)


def reconcile(catalog_path, overlay_path=None):
    catalog_path = Path(catalog_path).resolve()
    root = catalog_path.parent
    data = read_json(catalog_path)
    overlay_path = Path(overlay_path) if overlay_path else root / 'classified-layouts.json'
    overlay = read_json(overlay_path)
    layouts = {r['imageId']: r for r in overlay['dimensionLayouts']}
    assets = {}
    groups_by_hash = {}
    for group, spec in GROUPS.items():
        folder = inside(root, 'previews/assets/' + spec['folder'])
        for path in sorted(folder.rglob('*')):
            if not path.is_file():
                continue
            if path.is_symlink() or not path.resolve().is_relative_to(folder):
                raise ValueError(f'Image escapes classified folder: {path}')
            if path.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp'}:
                raise ValueError(f'Unexpected file in image folder: {path}')
            sha = digest(path)
            if sha in assets:
                raise ValueError(f'Duplicate image bytes across classified files: {path}')
            assets[sha] = dict(file=path.relative_to(root).as_posix(), sha256=sha,
                               kind='classified-local-reference', designGroup=group)
            groups_by_hash[sha] = group
    old_assets = {a['sha256']: a for a in data.get('bundledAssets', [])}
    known_hashes = set(old_assets) | {i.get('sha256') for i in data.get('images', [])}
    if set(assets) - known_hashes:
        raise ValueError('Unreviewed new image bytes need visual admission before refresh')
    for sha, asset in assets.items():
        previous = old_assets.get(sha, {})
        asset['sourceFile'] = previous.get('sourceFile', previous.get('file'))
    by_id = {}
    removed_ids = []
    for record in data.get('images', []):
        by_id[record['id']] = record
        asset = assets.get(record.get('sha256'))
        previously_bundled = record.get('bundled', False)
        record['bundled'] = bool(asset)
        for key in ['designGroups', 'targetRoles', 'planningGuide', 'planningPrompts']:
            record.pop(key, None)
        if asset:
            group = asset['designGroup']
            if 'sourceFile' not in record:
                record['sourceFile'] = record.get('file')
            record.update(file=asset['file'], bundledFile=asset['file'],
                          designGroups=[group], targetRoles=GROUPS[group]['roles'],
                          planningGuide=GROUPS[group]['guide'])
            if group == 'dimensions-details':
                if record['id'] not in layouts:
                    raise ValueError(f'Dimension/detail source lacks reviewed layout: {record["id"]}')
                layout = layouts[record['id']]
                record['planningPrompts'] = {role: dict(
                    revision=REVISION, role=role, sourceImageId=record['id'],
                    referenceFile=asset['file'], layoutZh=layout['layoutZh'],
                    prompt=planning_prompt(record, layout, role),
                    status='planning-template; current-SKU inputs and final image review required',
                ) for role in ['DIM01', 'DETAIL01']}
        elif previously_bundled:
            removed_ids.append(record['id'])
            record['previousBundledFile'] = record.pop('bundledFile', record.get('file'))
            record['file'] = record.get('sourceFile') or record['previousBundledFile']
    for card in data['cards']:
        refs = []
        for previous in card.get('bundledPreviews', []):
            asset = assets.get(previous.get('sha256'))
            if asset:
                refs.append(copy.deepcopy(asset))
        card['bundledPreviews'] = refs
        if refs:
            original_refs = card.get('references') or ([card['reference']] if card.get('reference') else [])
            card.setdefault('sourceReferences', copy.deepcopy(original_refs))
            card['references'] = [dict(file=a['file'], kind=a['kind']) for a in refs]
            card['reference'] = refs[0]['file']
        groups = sorted({a['designGroup'] for a in refs})
        if groups:
            card['designGroups'] = groups
            card['targetRoles'] = sorted({r for g in groups for r in GROUPS[g]['roles']})
        else:
            card.pop('designGroups', None)
            card.pop('targetRoles', None)
        if groups == ['dimensions-details']:
            card['layoutImageTypes'] = ['尺寸图', '细节图']
            records = [r for r in by_id.values() if r.get('sha256') in {a['sha256'] for a in refs}]
            card['planningPromptsByImage'] = {r['id']: copy.deepcopy(r['planningPrompts']) for r in records}
            # One actual source is unambiguous; multi-source cards retain explicit branches.
            if len(records) == 1:
                card['prompt'] = records[0]['planningPrompts']['DIM01']['prompt']
                card['promptZh'] = layouts[records[0]['id']]['layoutZh'] + '。DIM01/DETAIL01共用版式池，按角色读取独立分支。'
                card['promptRevision'] = REVISION
        else:
            card.pop('layoutImageTypes', None)
            card.pop('planningPromptsByImage', None)
    for recipe in data.get('layoutRecipes', []):
        ids = recipe.get('sourceImageIds', [])
        groups = sorted({g for i in ids for g in by_id.get(i, {}).get('designGroups', [])})
        recipe['designGroups'] = groups
        recipe['targetRoles'] = sorted({r for g in groups for r in GROUPS[g]['roles']})
        recipe['planningPromptsByImage'] = {i: copy.deepcopy(by_id[i]['planningPrompts'])
                                          for i in ids if by_id.get(i, {}).get('planningPrompts')}
        if recipe['planningPromptsByImage']:
            recipe['layoutImageTypes'] = ['尺寸图', '细节图']
    for series in data.get('series', []):
        for member in series['members']:
            image = by_id.get(member.get('imageId'), {})
            member['bundled'] = bool(image.get('bundled') and member.get('status') == 'approved')
            member['file'] = image['file'] if member['bundled'] else None
            member['designGroups'] = image.get('designGroups', [])
    by_name = {Path(a['file']).name: a['file'] for a in assets.values()}
    def relocate_branches(node):
        if isinstance(node, dict):
            if node.get('referenceFile'):
                previous = node['referenceFile']
                relocated = by_name.get(Path(previous.replace('\\', '/')).name)
                if relocated:
                    node['referenceFile'] = relocated
                else:
                    node.setdefault('sourceReferenceFile', previous)
                    node['referenceFile'] = None
            for value in node.values():
                relocate_branches(value)
        elif isinstance(node, list):
            for value in node:
                relocate_branches(value)
    for key in ['cards', 'layoutRecipes']:
        relocate_branches(data[key])
    # Keep historical reference/alias paths as provenance; only active bundled pointers move.
    data['bundledAssets'] = sorted(assets.values(), key=lambda a: a['file'])
    data['bundledPreviewCount'] = len(assets)
    data['missingSelectedPreviews'] = []
    data['designGroups'] = {g: dict(spec, count=sum(a['designGroup'] == g for a in assets.values()))
                            for g, spec in GROUPS.items()}
    data['classificationRevision'] = REVISION
    selection = copy.deepcopy(data.get('selection') or {})
    selection.update(mediaSelectionPolicy='existing-classified-files',
                     imageIds=sorted(i for i, r in by_id.items() if r.get('bundled')),
                     allowedMediaSha256s=sorted(assets),
                     classifiedPathsBySha256={sha: a['file'] for sha, a in sorted(assets.items())})
    data['selection'] = selection
    data['libraryVersion'] = '2026.10.26-classified-layouts-1'
    data['scope'] = 'User-classified portable references; historical text/provenance retained. Only existing selected bytes are bundled.'
    data['agentPolicy']['classifiedLayoutRouting'] = (
        'Use designGroups for asset-role routing and observed imageTypes for source content. '
        'DIM01 and DETAIL01 share the dimensions-details layout pool and have separate planning prompts. '
        'A+ remains grouped by principal product, not by folder. Open the selected actual image. '
        'Historical text is searchable when media is absent; never claim this run viewed it.')
    if (root / 'reviewed-layouts.json').is_file():
        from grounded_prompts import compact_catalog
        data = compact_catalog(data, root)
    return data, dict(counts={g: spec['count'] for g, spec in data['designGroups'].items()},
                      removedImageIds=removed_ids, bundledFiles=len(assets),
                      dualRoleSources=sum(len(i.get('planningPrompts', {})) > 1 for i in by_id.values()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=DEFAULT_CATALOG)
    parser.add_argument('--check', action='store_true', help='Compare without modifying any files')
    args = parser.parse_args()
    data, report = reconcile(args.catalog)
    root = args.catalog.resolve().parent
    if args.check:
        if read_json(args.catalog) != data or (root / 'index.md').read_text(encoding='utf-8') != render_index(data):
            parser.exit(1, 'Classified catalog/index need refresh\n')
    else:
        args.catalog.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (root / 'index.md').write_text(render_index(data), encoding='utf-8')
        (root / 'selection.json').write_text(json.dumps(data['selection'], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
