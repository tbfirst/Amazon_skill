"""Build compact, image-bound planning prompts from reviewed visible layouts."""
import copy
import json
from prompt_contracts import FONT_POLICY, PRODUCT_SOURCE_GATE, SCENE_PROP_FIT, TEXT_INTEGRATION

REVISION = 'scene-product-container-fit-20261028-r1'


def prompt_for(layout, role):
    canvas = ('1464 x 600 px by default' if role == 'APLUS' else
              'the project-selected square pixels' if role == 'SCENE' else
              '1600 x 1600 px by default')
    parts = [
        f'AGENT PLANNING TEMPLATE: {role}, one image, {canvas}; explicit user settings override defaults. '
        'Resolve this template into one self-contained English prompt before handoff.',
        'VISIBLE REFERENCE STRUCTURE\n' + layout['layoutEn'],
    ]
    if role in {'DIM01', 'DETAIL01'}:
        parts.append('ROLE ADAPTATION\n' + layout[
            'dimensionAdaptation' if role == 'DIM01' else 'detailAdaptation'])
    parts.append(
        'PROJECT INPUTS\nOpen the selected full reference when available; otherwise label this as '
        'a text-only adaptation of recorded layout notes, without claiming a current image view. '
        'Name the actual uploaded SKU photos and '
        'any layout attachment separately. Confirm measurements/endpoints, sale contents, supported '
        'views and placement before using them. Reference quantities, colors, materials, functions '
        'and claims do not establish current-SKU facts. Repeated pots/panels require an explicit '
        'contents map; use documented stem/support geometry and genuine detail views. '
        'Pause only the dependent asset when essential evidence is missing.')
    if layout.get('requiredEvidence'):
        parts.append('SPECIFIC EVIDENCE NEEDED\n' + layout['requiredEvidence'])
    parts.append('OLD-SET INPUTS\n' + PRODUCT_SOURCE_GATE)
    if role in {'SCENE', 'APLUS'}:
        parts.append('SETTING AND PROP FIT\n' + SCENE_PROP_FIT)
    if layout.get('copyMode') == 'none':
        parts.append('COPY\nPreserve the unlettered layout. Add text only after an explicit project '
                     'choice and a corresponding layout revision.')
    else:
        parts.append('COPY\nReplace source wording with exact project-approved English. Preserve '
                     'the selected text zones and backplates; specify one readable font family, '
                     'hierarchy, color and bounds clear of the product. Source slogans, icons and '
                     'numbers are not approved claims. Resolve any no-copy adaptation in planning.')
        parts.append('TEXT INTEGRATION\n' + TEXT_INTEGRATION)
    parts.append(
        'DESIGN PROPOSAL TO RESOLVE\nSpecify final zones, framing, palette and scene-motivated '
        'lighting with shadows on actual receiving surfaces. Treat exact light positions, lens '
        'settings and layout percentages as proposed design choices unless independently measured; '
        'do not report them as source facts. Preserve SKU color, scale and visible texture. '
        'Output only this asset\'s resolved instructions, exact copy and canvas; remove this planning '
        'preamble and unresolved options. No invented product details or generation-test claims.')
    return '\n\n'.join(parts)


def compact_catalog(data, root):
    """Maintain reviewed layouts and useful text templates; media presence is separate."""
    review = json.loads((root / 'reviewed-layouts.json').read_text(encoding='utf-8'))
    dimensions = json.loads((root / 'classified-layouts.json').read_text(encoding='utf-8'))
    notes = {r['imageId']: r for r in review['layouts']}
    dim_notes = {r['imageId']: r for r in dimensions['dimensionLayouts']}
    images = [r for r in data['images'] if r.get('bundled') or r['id'] in notes or r['id'] in dim_notes]
    by_id = {r['id']: r for r in images}
    by_sha = {r['sha256']: r for r in images}
    for record in images:
        is_dim = record['id'] in dim_notes
        layout = (dim_notes if is_dim else notes).get(record['id'])
        if not layout or (layout.get('sha256') and layout['sha256'] != record['sha256']):
            raise ValueError(f'Missing or mismatched reviewed layout: {record["id"]}')
        group = 'dimensions-details' if is_dim else layout['designGroup']
        roles = ['DIM01', 'DETAIL01'] if is_dim else ['APLUS' if group == 'aplus' else 'SCENE']
        record.update(designGroups=[group], targetRoles=roles)
        record['planningPrompts'] = {role: dict(
            revision=REVISION, role=role, sourceImageId=record['id'],
            referenceFile=record['file'] if record.get('bundled') else None, textOnlyUsable=True,
            layoutZh=layout.get('layoutZh'), layoutEn=layout['layoutEn'],
            prompt=prompt_for(layout, role),
            status='planning-template; current-SKU facts and full-image inspection required',
        ) for role in roles}
        observation = record.setdefault('observation', {})
        # Old recipe/transferable fields mixed generic inventions into observations.
        for key in ['recipe', 'recipeZh', 'recipeFamily', 'designPromptRevision',
                    'transferable', 'copyIntegration', 'lighting', 'shadows']:
            observation.pop(key, None)
        observation['overview'] = layout['layoutEn']
        observation['layout'] = layout['layoutEn']
        record['layoutReview'] = dict(revision=REVISION,
            scope=layout.get('reviewScope', 'Dimension layout checked against retained reference'),
            source='classified-layouts.json' if is_dim else 'reviewed-layouts.json',
            limits='Visible layout only; no SKU facts, exact OCR/lighting measurements or generation test.')

    cards = []
    for old in data['cards']:
        if old.get('textOnlyUsable') and old.get('qualityReview'):
            continue  # Regenerated from the maintained text-template source below.
        sources = [by_sha[p['sha256']] for p in old.get('bundledPreviews', [])
                   if p.get('sha256') in by_sha]
        if old.get('promptSourceImageId') in by_id:
            sources = [by_id[old['promptSourceImageId']]]
        if len(sources) != 1:
            continue
        record = sources[0]
        # Preserve existing IDs as navigation aliases, not duplicated prompt bodies.
        card = {k: copy.deepcopy(old[k]) for k in [
            'id', 'title', 'category', 'tags', 'productTypes', 'imageTypes', 'source',
            'bundledPreviews', 'references', 'reference', 'designGroups', 'targetRoles',
            'layoutImageTypes'] if k in old}
        card.update(promptSourceImageId=record['id'], status='image-bound navigation alias',
                    description=record['observation']['layout'])
        if not record.get('bundled'):
            card.update(bundledPreviews=[], references=[], reference=None)
        cards.append(card)

    from curated_templates import load_templates
    curated = load_templates(root)
    overridden = {c['id'] for c in curated}
    cards = [c for c in cards if c['id'] not in overridden] + curated

    recipes = []
    for old in data.get('layoutRecipes', []):
        # Layout-family defaults were not faithful to their many different sources.
        if not old['id'].startswith('APLUS-PRODUCT-'):
            continue
        ids = [i for i in old.get('sourceImageIds', []) if i in by_id
               and 'aplus' in by_id[i]['designGroups']]
        if not ids:
            continue
        recipe = {k: copy.deepcopy(old[k]) for k in [
            'id', 'title', 'category', 'imageTypes', 'productTypes', 'productKey',
            'principalProduct', 'sourceAsins'] if k in old}
        recipe.update(sourceImageIds=ids, sourceCount=len(ids), designGroups=['aplus'],
                      targetRoles=['APLUS'], requiresImageSelection=True,
                      promptRevision=REVISION, promptVariants={})
        for image_id in ids:
            image = by_id[image_id]
            recipe['promptVariants'][image_id] = dict(
                imageId=image_id, promptSourceImageId=image_id,
                referenceFile=image['file'] if image.get('bundled') else None,
                title=image['observation'].get('title'),
                copyMode=notes[image_id]['copyMode'])
        recipes.append(recipe)

    kept_series = []
    for series in data.get('series', []):
        if not any(m.get('imageId') in by_id for m in series['members']):
            continue
        for member in series['members']:
            if member.get('imageId') not in by_id:
                member.update(file=None, bundled=False, designGroups=[], status='excluded-or-missing')
        kept_series.append(series)
    for image in images:
        image['cardIds'] = [c['id'] for c in cards if c.get('promptSourceImageId') == image['id']]
        image['recipeIds'] = [r['id'] for r in recipes if image['id'] in r['sourceImageIds']]
        image['seriesIds'] = [s['id'] for s in kept_series
                              if any(m.get('imageId') == image['id'] for m in s['members'])]
    data.update(images=images, cards=cards, cardCount=len(cards), layoutRecipes=recipes,
                series=kept_series, authoredExtensions=[], libraryVersion='2026.10.27-set-refresh-1',
                scope='Quality-reviewed image layouts and independent text templates; media presence is not a quality verdict.')
    for key in ['promptTextReview', 'headlineLetteringReview']:
        data.pop(key, None)
    data['promptPolicy'] = dict(revision=REVISION, requireLocalReference=False,
        canonicalPrompt='images[].planningPrompts for source layouts; curated-templates.json for independent design tasks',
        maintenance='Retain admitted text templates without bundled media. Retire by explicit quality decision, duplication, scope or user instruction; never by missing preview alone.')
    data['agentPolicy']['textPlacement'] = TEXT_INTEGRATION
    data['agentPolicy']['typography'] = FONT_POLICY
    data['agentPolicy']['oldSetInputs'] = PRODUCT_SOURCE_GATE
    data['agentPolicy']['sceneProductContainerFit'] = SCENE_PROP_FIT
    data['agentPolicy']['classifiedLayoutRouting'] = (
        'Use role-specific image layouts or independently quality-reviewed text templates. '
        'A+ groups require an explicit source branch. Inspect available images; a text-only '
        'design remains usable but cannot be described as an image observed this run. '
        'Template quality and local media availability are separate decisions.')
    return data
