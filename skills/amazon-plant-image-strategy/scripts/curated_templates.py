"""Compile quality-reviewed design/edit templates independently of bundled media."""
import copy
import json
from prompt_contracts import PRODUCT_SOURCE_GATE, TEXT_INTEGRATION


def compile_prompt(template):
    kind = template['templateKind']
    parts = ['AGENT PLANNING TEMPLATE\nResolve this one selected task into the current asset\'s '
             'self-contained English prompt. Name the actual input files, selected canvas and '
             'literal copy before handoff; this template does not authorize extra campaign assets.',
             'TASK AND VISIBLE RESULT\n' + template['taskEn']]
    if kind == 'operation':
        parts.append('EDIT BOUNDARY\nUse the actual target image as the editing base. Preserve '
                     'correct background, camera view, product and text outside the stated change. '
                     'For a background replacement or reframing task, change only the expressly '
                     'named scope and its dependent occlusion, light or shadows. Preserve target '
                     'pixels/aspect unless the project explicitly selects another output.')
    elif kind == 'lighting':
        parts.append('LIGHTING BOUNDARY\nApply this effect to the selected asset\'s resolved '
                     'setting and real receiving surfaces. For a relight, keep viewpoint, geometry '
                     'and environment fixed. Distinguish lit face, open shadow, contact and cast '
                     'shadows; do not add a new room or mirror the product to fake a light change. '
                     'Named light ratios express intended visual contrast, not measured photometry.')
    else:
        parts.append('COMPOSITION AND LIGHT\nResolve the actual panel bounds, margins and '
                     'gutter sizes on the target canvas. Keep the prescribed reading order and '
                     'window/backplate relationships. Specify one scene-motivated key, appropriate '
                     'fill and shadows on real supports. Preserve scale, product color and '
                     'documented surface; reframe a mismatched aspect ratio without stretching.')
    parts.append('PRODUCT INPUTS\nUse verified same-SKU visual sources for appearance, supported views '
                 'and visible details. Confirm required measurements/endpoints, contents, operating '
                 'states and stem/support geometry before using them. External examples supply '
                 'layout or a named visual effect, never current-product facts. Obtain missing '
                 'essential views or facts; do not invent texture, hidden structure or extra units.')
    parts.append('OLD-SET INPUTS\n' + PRODUCT_SOURCE_GATE)
    if template.get('copyMode') == 'approved':
        parts.append('COPY\nUse exact project-approved English and verified measurement strings. '
                     'Specify one readable family, hierarchy, colors and bounded positions. '
                     'Keep labels, backplates and effects clear of the complete product. Resolve '
                     'copy fit before handoff; do not inherit example slogans or feature icons.')
    elif kind in {'operation', 'lighting'}:
        parts.append('COPY\nPreserve correct existing text unless this task explicitly changes it; '
                     'add no new words, badges or claims.')
    else:
        parts.append('COPY\nUse the unlettered layout unless the project explicitly chooses '
                     'copy and resolves its text region. Preserve genuine product marks.')
    if template.get('copyMode') == 'approved' or kind in {'operation', 'lighting'}:
        parts.append('TEXT INTEGRATION WHEN COPY IS PRESENT\n' + TEXT_INTEGRATION)
    parts.append('HANDOFF\nReturn one resolved image instruction with its actual output settings. '
                 'Remove this planning preamble and all unresolved choices. A studied example '
                 'is not automatically a generation attachment or a successful output test.')
    return '\n\n'.join(parts)


def load_templates(root):
    path = root / 'curated-templates.json'
    if not path.is_file():
        return []
    pack = json.loads(path.read_text(encoding='utf-8'))
    cards = []
    seen = set()
    for source in pack['templates']:
        card = copy.deepcopy(source)
        if card['id'] in seen or card['id'].startswith(('OUT-', 'DSTYLE-')):
            raise ValueError(f'Duplicate or retired curated template: {card["id"]}')
        if card.get('qualityReview', {}).get('decision') != 'retain-rewritten':
            raise ValueError(f'Template lacks explicit quality admission: {card["id"]}')
        seen.add(card['id'])
        card.update(prompt=compile_prompt(card), promptZh=card['summaryZh'],
                    promptRevision=pack['revision'], status='quality-reviewed design template; not generation-tested',
                    mediaRequired=False, textOnlyUsable=True, requiresLibraryReference=False,
                    imageStatus='Source study recorded separately; bundled preview is optional',
                    bundledPreviews=[], references=[], reference=None,
                    designGroups=['aplus', 'dimensions-details', 'scenes'],
                    targetRoles=['DIM01', 'DETAIL01', 'SCENE', 'APLUS'])
        if card['templateKind'] == 'layout':
            types = set(card.get('imageTypes', []))
            if card['id'].startswith('MAIN-'):
                card.update(designGroups=[], targetRoles=['REFERENCE_ONLY'],
                            eligibleRefreshRole='MAIN01',
                            roleCondition='MAIN01 only when set-refresh explicitly includes the existing main image; never add a new-set main asset')
            elif card['id'] in {'INFO-06', 'INFO-07', 'INFO-08'} or 'A+图' in types:
                card.update(designGroups=['aplus'], targetRoles=['APLUS'])
            elif types.intersection({'尺寸图', '细节图', '尺寸+细节图', '细节+尺寸图'}):
                card.update(designGroups=['dimensions-details', 'aplus'], targetRoles=['DIM01', 'DETAIL01', 'APLUS'])
            else:
                card.update(designGroups=['scenes', 'aplus'], targetRoles=['SCENE', 'APLUS'])
        cards.append(card)
    return cards
