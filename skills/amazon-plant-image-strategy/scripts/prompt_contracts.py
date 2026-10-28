"""Shared prompt clauses; keep generated templates and ingestion policy aligned."""

TEXT_INTEGRATION = (
    'Integrate copy into an intact quiet background using aligned margins and a scene-matched '
    'palette. Keep real scene texture, perspective and light continuous behind and around text. '
    'Do not invent a blurred white text mat, frosted patch, feathered white wash or erased backdrop '
    'to make room for copy. If an editorial panel is selected, specify its deliberate boundary, '
    'fill, padding and relation to the photo; preserve approved source bands and cards instead '
    'of applying a blanket panel ban. A source\'s blurred white zone does not automatically '
    'approve that effect: retain its information role while resolving an integrated text surface. '
    'Improve contrast through text color/weight, position or '
    'approved shorter copy before changing the text surface. Keep natural photographic depth '
    'of field separate from graphic text backing, and protect the whole merchandise plus clearance. '
    'An expressly requested localized frosted effect is a recorded exception, not a default.'
)

PRODUCT_SOURCE_GATE = (
    'When the input is an already designed old-set image, separate its old layout/copy from '
    'product identity. Reuse only clear product regions established as faithful to this SKU; '
    'old generated imagery and embedded claims are not independent product evidence. If the '
    'needed petal texture, stem junction, view or other detail is unclear, immediately ask a '
    'focused popup question and/or request the smallest clear same-SKU photo in chat. Keep '
    'dependent assets blocked until the visual gap is resolved; sharpening, competitor details '
    'and design delegation cannot supply missing product structure.'
)

FONT_POLICY = (
    'Use one selected readable font family throughout an image, including facts and dimensions; '
    'vary size, weight, spacing and color. Honor explicit approved mixed-font exceptions. '
    'A prompt font name does not prove a font file was loaded.'
)
