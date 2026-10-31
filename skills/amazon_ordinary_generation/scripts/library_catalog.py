"""Search ordinary-product planning templates; never browse or generate images."""

import argparse
import json
from pathlib import Path
import re
import sys

DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / 'assets/reference-library/catalog.json'
GROUPS = ('dimensions-details', 'scenes', 'aplus')


def role_family(role):
    if role in {'DIM01', 'DETAIL01', 'MAIN01'}:
        return role
    if re.fullmatch(r'(?:SCENE|APLUS)(?:\d{2})?', role or ''):
        return 'SCENE' if role.startswith('SCENE') else 'APLUS'
    raise ValueError(f'Unsupported asset role: {role}')


def load_catalog(path=DEFAULT_CATALOG):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if data.get('schemaVersion') != 1:
        raise ValueError('Unsupported catalog schema')
    templates, series = data.get('templates'), data.get('series')
    if not isinstance(templates, list) or not isinstance(series, list):
        raise ValueError('Catalog needs templates and series lists')
    seen = set()
    for card in templates:
        if not isinstance(card, dict) or not isinstance(card.get('id'), str) or card['id'] in seen:
            raise ValueError('Template IDs must be unique strings')
        seen.add(card['id'])
        if card.get('templateKind') not in {'operation', 'lighting', 'layout'} or not card.get('taskEn'):
            raise ValueError(f'{card["id"]}: missing task or kind')
        if not card.get('targetRoles') or not isinstance(card.get('designGroups'), list):
            raise ValueError(f'{card["id"]}: missing role classification')
    for recipe in series:
        if not isinstance(recipe, dict) or not isinstance(recipe.get('id'), str) or recipe['id'] in seen:
            raise ValueError('Recipe IDs must be unique strings')
        seen.add(recipe['id'])
        slots = recipe.get('slots', [])
        slot_ids = [s.get('assetId') for s in slots if isinstance(s, dict)]
        if len(slot_ids) != len(slots) or not slots or len(set(slot_ids)) != len(slots):
            raise ValueError(f'{recipe["id"]}: invalid or repeated asset slots')
        by_id = {t['id']: t for t in templates}
        for slot in slots:
            card = by_id.get(slot.get('templateId'))
            if card is None or role_family(slot['assetId']) not in card['targetRoles']:
                raise ValueError(f'{recipe["id"]}: missing or incompatible slot template')
    if data.get('templateCount') != len(templates) or data.get('seriesCount') != len(series):
        raise ValueError('Catalog counts do not match records')
    for collection in ('productProfiles', 'materialProfiles'):
        profiles = data.get(collection, {})
        if not isinstance(profiles, dict):
            raise ValueError(f'{collection} must be an object')
        for key, profile in profiles.items():
            if not isinstance(profile, dict) or not all(
                    isinstance(profile.get(field), str) and profile[field].strip()
                    for field in ('title', 'promptEn')):
                raise ValueError(f'{collection}/{key}: missing title or prompt')
    return data


def planning_prompt(card, asset_role=None, product_profile=None, material_profile=None):
    role = role_family(asset_role) if asset_role else None
    if role and role not in card['targetRoles']:
        raise ValueError(f'{card["id"]} does not support {asset_role}')
    parts = [
        'AGENT PLANNING TEMPLATE — NOT A READY GENERATION PROMPT\n'
        'Resolve this selected task through the recorded dialogue into one independent English '
        'instruction. Use actual filenames, canvas and literal copy. The template does not '
        'confirm user choices, supply product facts, authorize generation or add assets.',
        'TASK AND VISIBLE RESULT\n' + card['taskEn'],
    ]
    if card.get('artDirectionEn'):
        parts.append('PROPOSED VISUAL DIRECTION\n' + card['artDirectionEn'] + '\n'
                     'This is a starting proposal. Retain already selected reference relationships '
                     'and user decisions; resolve one concrete composition before handoff. Do not '
                     'combine incompatible alternatives or turn proposed placement into a fact.')
    parts.append(
        'PRODUCT IDENTITY\nUse genuine same-SKU visual evidence for shape, dimensions, finish, '
        'print, labels, parts, contents and supported states. Keep rigid geometry fixed; for '
        'soft goods preserve construction, seams, pattern and supported deformation. Packaging '
        'does not establish unseen contents. Use the actual interfaces, operating method and '
        'sale quantity; omit mechanisms irrelevant to this product.')
    if product_profile:
        parts.append('SELECTED PRODUCT FORM\n' + product_profile['promptEn'])
    if material_profile:
        parts.append('SELECTED MATERIAL RESPONSE\n' + material_profile['promptEn'] + '\n'
                     'Name the evidenced part this applies to; this selector supplies lighting '
                     'guidance, not proof of material composition. Preserve the other parts\' finishes.')
    parts.append(
        'SOURCES AND SCOPE\nThis is an authored text recipe without a source image. Distinguish '
        'identity inputs, selected visual layout references and an actual edit base. For refresh, '
        'use only clear supported product regions from old artwork; rebuild or edit within the '
        'chosen scope. A historical template ID never proves a current competitor observation.')
    if card['templateKind'] == 'operation':
        parts.append('EDIT BOUNDARY\nFor an edit, name the actual base and changed regions. Preserve '
                     'correct areas outside the chosen task; rebuild dependent occlusion, '
                     'illumination and shadows. Do not apply preserve-all-background wording '
                     'when the selected task rebuilds that background. For a new composition, '
                     'carry forward only the applicable identity or construction instruction; '
                     'do not invent an edit base or request repair of a nonexistent defect.')
    elif card['templateKind'] == 'lighting':
        parts.append('LIGHTING BOUNDARY\nKeep resolved viewpoint, environment and geometry. '
                     'Specify the source direction and size, lit and shaded faces, fill, '
                     'contact and cast-shadow receiving surfaces. Ratios are visual intent, '
                     'not measured photometry; do not imply unsupported material performance.')
    else:
        parts.append('LAYOUT\nResolve regions, ownership, reading order, scale, perspective, '
                     'margins, windows and layers as needed. Use the selected reference transfer '
                     'mode and exact bounded changes; do not stretch the product to fit a recipe.')
    if role == 'DIM01':
        parts.append('DIM01 BRANCH\nMake verified size/specification/fit information primary. '
                     'Bind each value to its exact object, endpoints and state. Preserve any '
                     'confirmed role adaptation; a detail crop does not inherit an overall value.')
    elif role == 'DETAIL01':
        parts.append('DETAIL01 BRANCH\nMake one supported visible detail task primary, with '
                     'genuine source crops and clear relation to the whole item. Do not add '
                     'dimension lines unless relevant, or invent microscopic texture or performance.')
    elif role == 'SCENE':
        parts.append('SCENE BRANCH\nUse the recorded type allocation, this asset\'s square '
                     'pixel selection and resolved single/grid/operation/comparison content. '
                     'A recipe does not silently confirm these decisions or the copy mode.')
    elif role == 'APLUS':
        parts.append('APLUS BRANCH\nRecompose for the resolved wide canvas and actual module '
                     'mapping. Keep native fields separate; do not stretch a square source, '
                     'invent a cross-sell range or expand the five-image budget.')
    elif role == 'MAIN01':
        parts.append('MAIN SCOPE\nUse only when this existing main image is explicitly in '
                     'set-refresh scope or the user explicitly changes scope. Check current '
                     'marketplace/category rules; never add a new main by selecting this template.')
    parts.extend([
        'SETTING AND PHYSICS\nWhen applicable, resolve the actual use location, support, '
        'scale anchor, fit and operating state. Actively propose the real use subject and '
        'supported interaction for products that have one; missing fit/action facts trigger '
        'a focused evidence question, not a campaign-wide empty-product default. Separately '
        'resolve compatible physical props and optional subordinate graphic motifs, their '
        'positions and sale roles, or a task-specific reason for none. No-copy does not '
        'automatically ban selected graphics. Choose an evidenced camera height, side and '
        'shot scale for this task; the identity photo does not lock every campaign viewpoint. '
        'Compare setting, use, framing and light with other assets to avoid merely renaming '
        'the same scene. Preserve selected reference fidelity and deliberate comparison '
        'invariants; do not force variety quotas. Do not add an unsupported container, '
        'installation, electric effect or home setting.',
        'COPY AND TYPOGRAPHY\nUse the confirmed per-asset copy mode and source. No-copy means '
        'no added text or text effects; preserve genuine product print. For visible copy, '
        'write exact strings, semantic line breaks, bounded zones, chosen type, size, weight '
        'and color. Default to lettering on the intact real background with no added backplate '
        'or veil; use a panel only within an explicit scoped exception. Keep all treatments '
        'outside the complete product and its clearance. Native-only text stays outside the bitmap.',
        'HANDOFF\nResolve pending decisions before final executable text. Write only this '
        'asset\'s selected visible result and concrete failure constraints; remove this planning '
        'preamble, internal IDs, alternatives and research instructions. Report design checks '
        'separately from actual rendered-image validation. Lead the final prompt with the visible '
        'result, followed by actual inputs, product locks, layout, physical scene, light and exact '
        'copy. Merge overlapping constraints once and omit irrelevant product/material branches. '
        'Choose a single principal task; lighting and repair helpers modify that asset rather '
        'than introducing extra panels, steps, products or deliverables.'
    ])
    return '\n\n'.join(parts)


def search(data, query='', kind='all', design_group=None, limit=5, asset_role=None):
    if limit < 1:
        raise ValueError('limit must be positive')
    role = role_family(asset_role) if asset_role else None
    tokens = query.casefold().split()
    candidates = []
    if kind in {'all', 'template'}:
        candidates.extend(data['templates'])
    if kind in {'all', 'series'}:
        candidates.extend(data['series'])
    results = []
    by_id = {c['id']: c for c in data['templates']}
    for card in candidates:
        members = [by_id[s['templateId']] for s in card['slots']] if 'slots' in card else [card]
        if design_group and not any(design_group in c['designGroups'] for c in members):
            continue
        if role and not any(role in c['targetRoles'] for c in members):
            continue
        haystack = json.dumps(card, ensure_ascii=False).casefold()
        if any(token not in haystack for token in tokens):
            continue
        results.append(card)
    return results[:limit]


def show(data, ident, asset_role=None, product_form=None, material=None):
    card = next((c for c in data['templates'] + data['series'] if c['id'] == ident), None)
    if card is None:
        raise ValueError(f'Unknown template or series: {ident}')
    if 'slots' in card:
        if asset_role or product_form or material:
            raise ValueError('Select a recipe slot template before requesting an asset-role branch')
        return card
    selected = []
    for collection, key in (('productProfiles', product_form), ('materialProfiles', material)):
        profiles = data.get(collection, {})
        if key is not None and key not in profiles:
            raise ValueError(f'Unknown {collection} selection: {key}')
        selected.append(profiles.get(key))
    return dict(card, selectedProductForm=product_form, selectedMaterial=material,
                planningTemplate=planning_prompt(card, asset_role, *selected))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=DEFAULT_CATALOG)
    sub = parser.add_subparsers(dest='command', required=True)
    find = sub.add_parser('search')
    find.add_argument('--kind', choices=('all', 'template', 'series'), default='all')
    find.add_argument('--design-group', choices=GROUPS)
    find.add_argument('--query', default='')
    find.add_argument('--limit', type=int, default=5)
    find.add_argument('--asset-role')
    get = sub.add_parser('show')
    get.add_argument('identifier')
    get.add_argument('--asset-role')
    get.add_argument('--product-form', help='Optional evidenced form; see profiles command')
    get.add_argument('--material', help='Optional evidenced surface; see profiles command')
    sub.add_parser('profiles', help='List available form and material planning branches')
    sub.add_parser('check')
    args = parser.parse_args()
    try:
        data = load_catalog(args.catalog)
        if args.command == 'search':
            result = dict(libraryVersion=data['libraryVersion'], mediaStatus='text-only',
                          matches=search(data, args.query, args.kind, args.design_group,
                                         args.limit, args.asset_role))
        elif args.command == 'show':
            result = show(data, args.identifier, args.asset_role, args.product_form, args.material)
        elif args.command == 'profiles':
            result = dict(productProfiles=data.get('productProfiles', {}),
                          materialProfiles=data.get('materialProfiles', {}))
        else:
            result = dict(libraryVersion=data['libraryVersion'], templates=len(data['templates']),
                          series=len(data['series']), bundledImages=0)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
