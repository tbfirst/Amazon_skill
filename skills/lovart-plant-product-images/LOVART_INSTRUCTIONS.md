<!-- Generated from SKILL.md and its referenced modules. Edit the sources, then rebuild. -->

These standalone instructions contain the full workflow for a loaded Lovart custom skill. Use only the sections relevant to the current task; no external module files are required.

# Lovart Plant Product Images

Turn everyday requests and reference images into faithful product imagery. Prioritize product identity, physical integration, and controllable composition. Interpret the request, build a focused prompt, and execute when Lovart tools are available. Ask only about missing facts, unclear targets, or necessary delivery settings. If the user requests discussion, analysis, or prompts only, stay within that scope.

## Execution context

Read Lovart execution (section below) when establishing access, choosing an execution route, or resolving tool/settings limitations. Installation supplies instructions, not a Lovart connection or image model. Without usable Lovart access, deliver the prepared prompt and reference mapping, and state that no image was generated. Do not silently switch platforms.

Reuse the user's confirmed output dimensions, count, and format; infer aspect ratio from known width and height. Use current platform settings only when actually visible. If necessary settings remain unknown, ask together once. Do not invent a default resolution, quantity, or format. Internal intermediate assets do not require another round of final-delivery questions. Prompt-only work and photography advice can proceed without file specifications.

V1 covers individual functions, combinations needed to complete them, and user-requested candidates of the same kind. Full Amazon image-set planning and production are future work. Reply in the user's language, Chinese when unspecified; Amazon US image copy defaults to English unless the user requests otherwise.

## Understand this task

Infer these from the conversation and images; do not make the user complete a form:

1. **What is sold:** real or artificial plant, included container/accessories, actual unit count. Ask about sale scope only when it changes this operation; a pot in a photo does not prove it is included.
2. **What each reference supplies:** product identity, details/another view of the same SKU, container, editing base, scene, composition, feasible arrangement, lighting, or style. Follow current image labels and selections. Multiple angles do not imply a multipack.
3. **What changes now:** target, operation, region, degree, position, and preserved properties. Resolve ambiguous selections before editing the wrong object.
4. **What image is needed:** white-background MAIN, lifestyle secondary, close-up, dimensions/details graphic, individual A+ asset, or intermediate compositing asset.

Use one operation for a simple request. Split work when simultaneous arrangement, viewpoint, integration, and lighting edits would compromise identity; do not expand the requested deliverable count.

## Shared product protections

- Preserve species/product type, flower and leaf shapes, colors, textures, key branches, actual flower/stem quantities, container identity, and included accessories. Artificial plants retain their real material appearance. Do not upgrade a living plant's bloom, fruit, health, or maturity.
- Preserve arrangement by default. When explicitly requested, allow physically feasible bending, spreading, orientation, drape, and stem placement while retaining component identity and quantities. Do not duplicate flowers or leaves to create fullness. Check bendability only when the operation depends on it and it is unknown.
- Protect included pots. Decorative pots, outer cachepots, and other props may change within the request. An outer pot must fit the real included pot; it does not replace it.
- Add other decorative flowers only when explicitly requested. Keep merchandise distinguishable from styling materials; decoration cannot replace or complete the actual product. MAIN images show actual sale contents.
- Style, composition, and competitor references contribute only their assigned attributes, never another product's identity, branding, specifications, or performance. Restore missing structure only when genuine source material supports it; do not invent unseen backs, roots, interiors, drainage holes, or accessories.
- Without measured dimensions, visual scale matching is allowed in scenes. Do not turn estimates into inches or centimeters. Dimension graphics require real values, units, and measurement endpoints.
- A new instruction replaces an older target for the same attribute; unrelated protections remain. If a request conflicts with confirmed sale facts, clarify the concrete conflict, such as a decorative pot versus an included product pot.
- Choose references as needed rather than attaching every historical image mechanically. Product facts come from genuine sources and user confirmation; generated defects never become the new truth.

## Select relevant modules

Read only modules needed for the current task.

| Need | Module |
| --- | --- |
| Photography advice, missing views, white background, cutouts, detail/intermediate assets | Asset preparation (section below) |
| Place plants in containers/scenes, replace contents, combine references | Product integration (section below) |
| Choose or replace environments, European homes, seasons, background assets | Scenes and backgrounds (section below) |
| Distance, viewpoint, placement, frame coverage, cropping, outpainting | Composition (section below) |
| Local fixes, props, feasible reshaping, local text correction | Local refinement (section below) |
| Exposure, shadows, color temperature, material appearance | Lighting and color (section below) |
| Dimensions, details, selling points, individual A+ images | Information images (section below) |

For every generated result, apply Quality and repair (section below). The initial generation is followed by at most **three automatic repair rounds shared across this task**, not three per module, region, or candidate.

## Translate everyday language into an executable prompt

Include only relevant parts: **task and image type → reference roles → protected facts and permitted changes → placement/composition → physical integration/light → text and delivery settings**. Remove superseded instructions. Do not pad prompts with irrelevant photographic settings.

| Everyday request | Interpretation |
| --- | --- |
| “P 到第二张里” / put it into image two | Identify the product source, destination, replaced object, and protected scene |
| “拍大一点” / bring it closer | Increase frame coverage or move the camera, preserving actual proportions |
| “稍微俯视，还能看到盆” / slight top view, keep the pot visible | Gentle downward viewpoint with a clearly readable pot body and rim |
| “俯视太多，改正面” / too overhead, make it front-on | Replace the previous pitch target; distinguish horizontal facing from vertical pitch |
| “有光泽、有质感” / glossy and detailed | Show material-appropriate reflections and texture; do not gloss every surface |
| “枝干分开一点，更蓬松” / spread stems, make it fuller | Rearrange feasible existing stems without multiplying components |
| “高级一点，随意发挥” / make it premium, your choice | Improve styling and photography in a realistic European setting, retaining product facts |
| “只改这里” / change only here | Identify the edit region and preservation boundary; inspect for changes outside it |

Execute without requiring line-by-line prompt approval. Explain significant choices briefly; show the full prompt if requested. Never claim exact angle measurements or immutable outside-mask pixels from a generative prompt alone.

## Delivery

Show actual generated candidates and briefly describe completed changes and remaining issues. Claim dimensions, transparency, and visual checks only when observed. If execution or inspection is unavailable, say which step remains unperformed and preserve the useful prompt. Stop automatic repair after three rounds and explain unresolved defects in text. Use Lovart's existing history and selection records.

---

# Lovart execution

Use this module to distinguish native Lovart use from an external agent installation.

## Inside Lovart

Use the generation, editing, canvas, and export tools actually available in the current session. The user selects the image model in Lovart's interface; preserve that selection. Model names and controls may change, so do not hard-code a model/version or infer availability from these instructions.

The standalone LOVART_INSTRUCTIONS.md contains all modules for a native custom skill; no local file access is needed after it is loaded. Select only relevant sections mentally. Saving and selecting a custom skill is separate from pasting a prompt into a normal conversation.

## In an external agent

Inspect the available, authorized Lovart tools or browser session. A text skill does not install a connector, create credentials, or make a Lovart API available. Use documented capabilities actually exposed by the current environment. Do not invent tool names, endpoints, model IDs, or a connection to the user's canvas.

If usable Lovart access exists, execute within the requested scope and retain the user's settings where the interface supports them. An API route may not inherit the web canvas's model or export settings: resolve required settings from confirmed task information rather than pretending the web selection transferred.

If access is unavailable, finish the useful preparation: give the ready-to-paste prompt, identify which reference is used for each role, and list only genuinely missing input. Clearly state that generation has not run. Do not silently substitute another image provider.

## Output settings and evidence

Use explicit current instructions first, then confirmed settings for this task, then observable current controls. Resolve contradictory width/height and aspect ratio before final generation. A ratio alone is not evidence of actual pixel dimensions.

When an exact requested size or format cannot be produced directly, use available export/resizing capabilities if they can meet the request without distorting the product. Otherwise explain the limitation and ask about the specific alternative; do not silently deliver a different specification. A flattened image is not an editable layered PSD.

Use actual export/file inspection to substantiate pixel dimensions, format, or alpha. A prompt saying “transparent PNG” and a rendered checkerboard do not prove transparency. A successful generation status does not establish product fidelity. If the result cannot be viewed, report that visual review is incomplete and avoid blind repair calls.

History and selected versions remain in Lovart. Reference selection is task-dependent; factual checks remain anchored to real product evidence.

## Native custom skill setup

Lovart's documentation describes Thinking Mode, a project conversation, then Skill Book → Create a Skill → My Skills. Later, select the saved skill in a new chat; instructions and examples can be edited. Use the supplied standalone instructions as the workflow material and check what was saved after creation.

Do not claim that Lovart directly imports a GitHub Agent Skills directory or automatically loads this skill merely from its name. Verify such a capability in the current product before promising it. Setup UI steps may change.

Source checked 2026-10-14: [Lovart Agent Skills and Custom Skills](https://www.lovart.ai/docs/how-to-prompt/agent-skills).

---

# Asset preparation

Use for input assessment, photography guidance, white-background images, transparent cutouts, genuine details, and intermediate compositing assets. Choose only operations needed for the request.

## Inputs and photography

Prefer clear real photos or user-verified restored material. Identify whether images show one SKU, different views of one unit, or different products.

Give targeted reshoot guidance when needed: a front view with topmost foliage and pot base, a side view for spread and pot depth, a top view for branching, or flower/leaf/stem close-ups for textures and connections. Request measurement evidence only when true dimensions are required. Use neutral lighting and faithful color; avoid filters, severe backlight, occlusion, and clipped edges. Arrange stems only within real physical limits.

Proceed when the current task has enough evidence. A background replacement does not inherently need a complete multi-angle shoot. Indistinct low-resolution details remain unknown.

## White-background MAIN images

Keep the actual sale contents complete against pure white, with a clear viewpoint, restrained contact shadow, and intact leaf tips/base. Target strong frame coverage; Amazon's general guidance describes at least 85% product fill, subject to applicable category rules. Do not crop required parts to force a numerical target or claim measured coverage without checking it.

Do not add non-included containers, decorative flowers, packaging, props, text, dimension lines, badges, or borders. Multiple source views do not justify showing multiple units. If “main image with a lifestyle background” means a secondary scene image, use that type; if explicitly destined for Amazon MAIN, explain the conflict and clarify the image type.

Prefer retaining the photographed product and editing background, edges, and exposure. White is not transparent. These instructions do not certify marketplace acceptance; check current category requirements when preparing an upload.

## Transparent subjects and components

Use an actual available background-removal/export capability. Preserve thin stems, leaf tips, translucent petal edges, and natural holes. Inspect halos, fringe color, hollowed leaves, and background residue. An exported transparent asset requires alpha; confirm it only when the file can be inspected.

Obtain leaf, flower, and stem details from visible real regions or genuine alternate views, using crops where appropriate. Do not invent cross-sections, unseen joins, or separate components. Isolated visual assets must not imply that parts detach or ship separately.

## Intermediate assets

Prepare empty pots/flower boxes, backgrounds with subjects removed, standalone environments, and explicitly requested retained shadows for later integration.

“Remove the flowers but keep the shadow” is valid when explicitly requested as an intermediate asset. Label its purpose. Once a new plant is inserted, check the old shadow against the new shape and placement; an orphaned old flower shadow is not a finished product scene.

## Review

Compare product type, shapes, colors, component counts, containers, and edge completeness with genuine sources. Confirm that the result matches the white, transparent, or intermediate target. Mark unsupported details as unverifiable.

Reference checked 2026-10-14: [Amazon product image requirements](https://sellercentral.amazon.com/help/hub/reference/external/G1881).

---

# Product integration

Determine **what goes where, what it replaces, and what must stay** for compositing, container changes, and multi-reference work.

## Reference roles

Identify product identity, same-product detail/alternate view, target container, destination scene, and arrangement reference. One image may have multiple explicit roles. Use the current input order, not stale image numbers.

In a multi-image task, flower color/texture, leaf details, container structure, and feasible arrangement can come from separate assigned sources. Change arrangement only as requested. An arrangement reference cannot supply extra flower heads, stem counts, or another species.

## Product and container

- **Container is the merchandise:** preserve its shape, texture, color, proportions, and actual accessories; handle plants within confirmed styling scope.
- **Plant sold with a pot:** preserve the included pot. A suitable outer cachepot or stand can decorate it without replacing the actual product.
- **Bouquet/bare stems sold separately:** remove a source prop pot if needed and place the real stems into the destination with credible depth and orientation.
- **Replace existing destination plants:** remove their visible foliage, stems, and mismatching shadows while retaining the destination container and protected scene.
- **No container specified:** choose a realistic European-style prop appropriate to use. A specified background, carrier, or location takes precedence.

Ask about sale scope only if unknown and decisive for the edit. If the user wants to change the actual included pot's specifications, resolve whether the real product has changed before presenting it as the same SKU.

## Physical integration

1. Align contact position, scale, camera, and perspective. The base rests on a support surface; with no dimensions, match visually without claiming measurements.
2. Establish insertion and occlusion. Stems enter the container; its front rim hides appropriate portions. Railings, basket rims, and hanging chains have coherent depth order.
3. Match key-light direction, color temperature, and shadow softness without changing product identity colors or material.
4. Remove white halos, old background remnants, double contours, and abrupt sharpness differences while retaining fine foliage and petals.

These are judgment priorities, not mandatory separate model calls.

## Multiple displays and decoration

“Put my plant in both pots” specifies two scene placements, not necessarily a two-pack. Distinguish repeated styling instances from the actual sale quantity. MAIN images and included-item claims use the real quantity.

Additional decorative flowers require an explicit request and must not obscure the merchandise or appear included. Otherwise create depth using distinguishable containers, surfaces, or architectural materials.

## Review

Use real product evidence for identity and quantity. Assess silhouette changes against explicitly permitted arrangement changes. Check that the correct container survived; stems do not float, pierce walls, or pass through the base; shadows and occlusion agree; replaced plants leave no remnants. Repair the observed failure rather than redoing everything by default.

---

# Scenes and backgrounds

Use for lifestyle scenes, background replacement, seasonal ambiance, style references, and background-only assets. Defaults suit European and North American customers using realistic European residential settings.

## Decision priority

Explicit user setting and protected regions → assigned reference setting → confirmed product use → freely chosen European scene.

Do not let the default override an American home, specified room, or locked background. When scene and carrier are unspecified, choose them without repeated preference questions. Match product scale, display method, intended indoor/outdoor use, and image purpose. A setting must not imply unverified extreme-weather suitability.

## Flexible inspiration

French plaster walls, wood window trim, linen and matte timber; British painted joinery, brick and modest courtyards; Mediterranean mineral walls, terracotta and pale stone; European country stonework, wood and everyday domestic furnishings are possible directions. Other credible European styles are welcome.

Keep materials coherent and spaces livable. Do not hard-code a door design, pot color, focal length, color temperature, season, or text-space percentage. White-background MAIN requests use their own background rules.

## Reality checks

- Wall/floor junctions, window depth, railing joints, furniture sizes, and walking space must be plausible. Wreaths and hanging baskets need credible hanging points and support.
- Keep the product prominent. Let shot distance determine how much environment is shown; do not dwarf the product with enormous architecture.
- Restrained wear and texture may enrich the background, but do not transfer dirt or damage to a new product.
- Weather, daylight, and time must agree. Overcast conditions favor diffuse light; hard sunlight requires compatible shadows. Window patterns require a plausible occluding frame.
- Seasonal changes affect environment and props, not product flower color, fruit, foliage, or material. Other flower additions still require an explicit request.
- “This feeling” usually borrows palette, materials, light, and spatial organization. “Keep image two, replace only the plant” protects its scene and framing.

## Review

Check product identity and prominence first, then scale, intended use, contact, light, perspective, and environmental realism. For multiple requested settings, vary clear scene features while preserving the same product facts.

---

# Composition

Treat shot distance, viewpoint, subject position, frame coverage, and focus target as independent controls.

## Distance and completeness

| Target | Visible outcome |
| --- | --- |
| Wide environmental shot | More surroundings, readable product location and plausible scale; preserve the complete product unless directed otherwise |
| Full/medium product shot | Include top foliage through the base and required hanging chains or supports |
| Close-up/detail | Focus on the requested flower, leaf, pot, stem, or texture; crop to a genuine region without inventing microscopic structure |

For framing instructions, describe coverage using the subject bounding box relative to the matching frame edge; for details, use the focus region. This is a composition aid, not an Amazon compliance measurement. Coverage, focal lengths, and angle numbers are visual targets, not guaranteed physical measurements.

“Closer” or “larger in frame” changes framing first. “Make the pot taller” changes object geometry and requires product/prop classification. “More scene” means pull back or outpaint, not change the real product's proportions.

## Viewpoint and references

Distinguish horizontal facing from vertical pitch: front-facing with a 15-degree downward view can be coherent; straight-on at eye level removes downward pitch.

“A little overhead, but keep the pot visible” means a gentle downward view, slightly more visible crown, and readable pot body. Judge that visible effect rather than inventing precise measured angles.

“Too overhead” reduces pitch; “eye-level now” replaces the old target. Remove conflicting old viewpoint instructions from the execution prompt.

For crops, outpainting, or positioning at the same viewpoint, the current base may suffice. If a new angle exposes unknown important structure, use genuine alternate views or request the specific missing evidence; offer a composition that avoids exposing it. Small supported adjustments from one image are acceptable, but cannot prove unseen backs, roots, or interiors.

## Position and outpainting

Identify whether the camera, merchandise, or focal region moves. Moving a pot from a table to the floor also changes contact, shadow, and perspective. Moving it within the frame does not change its aspect ratio.

Extend space, material, and illumination coherently. Preserve the original product; do not create a second plant or distracting new props. Reserve text space only for requested copy or an information layout that needs it.

## Review and feedback

Check completeness/allowed cropping, visible pot body, frame coverage, location, background extent, and perspective. After a failed viewpoint edit, describe the observed problem—still too overhead, still sideways, too close—and update the instruction instead of repeating it unchanged.

---

# Local refinement

Use for edges, stem connections, container intersections, local shadows, prop changes, feasible rearrangement, and local lettering errors.

## Edit boundary

Identify the selected image, user marking, or described object. Define the target region, observed defect, desired change, and preserved properties. Clarify only if ambiguity risks editing the wrong target.

Use local selection, Touch Edit, Quick Edit, or layers only when actually available. Otherwise express the boundary with the supported editing tool. Do not claim a mask was drawn or pixels locked when they were not.

Prioritize product identity and physical relationships, then edge quality and aesthetic details. Related defects may be repaired together.

## Operations

- **Edges:** remove halos, ghosting, and background residue; retain slender stems and natural openings.
- **Connections:** restore joins supported by actual product views; do not invent hidden components.
- **Arrangement:** on explicit request, change physically feasible orientation, bend, spacing, or stem placement without duplicating/removing flowers for fullness or symmetry.
- **Props:** modify decorative pots, objects, and placement within the request. Keep included product parts factual. Adding other flowers requires an explicit request.
- **Removal:** remove the target, reconstruct exposed background, and update its shadows. Honor an explicit intermediate-asset request to retain shadows and label that purpose.
- **Local light:** specify the shadow caster, receiving surface, and direction, such as flower shadows on the upper pot only; protect the rest of the scene.
- **Text:** correct to the confirmed wording, numbers, and units; keep the label attached to the intended feature without damaging the product.

## References and recovery

Choose the current image, original photo, or earlier reliable candidate as appropriate. If the current image has product drift, recover from factual evidence rather than polishing the incorrect structure.

## Review

Compare before and after: did the defect resolve; did unrequested regions change; did colors, quantities, texture, containers, and text remain faithful; are there patch edges, holes, smears, or double contours?

Masks and markings guide edits but do not guarantee unchanged outside pixels. The skill does not depend on source-project pixel-compositing code. Use the task-wide three-round repair budget, not separate budgets per region.

---

# Lighting and color

Use for exposure, color temperature, cast/contact shadows, matching a scene, and showing genuine material.

## Interpret the target

- “Brighter” or “less warm”: adjust exposure or temperature without changing shape, scene, or viewpoint.
- “Sunlight from the left”: establish coherent left-side key light across plant, container, ground, and walls.
- “Flower shadows only on the pot”: limit the receiving region; follow actual light direction without changing the entire weather.
- “Glossy, clear, textured”: show highlights and texture appropriate to the actual material. Fabric, matte plastic, and glazed ceramic require different treatment; preserve real hue.

## Shadow relationships

Distinguish contact shadow, self-shadow, and shadows cast onto surroundings. Maintain contact beneath pots, plausible load-bearing hooks/chains, and consistent wall/ground shadow directions.

Shadow contours depend on the real subject, occlusion, and distance. After plant replacement, do not preserve a clearly incompatible old plant shadow. Translucency and highlights must respect material; artificial foliage should not acquire living-tissue detail.

## Color and environment

Lighting can carry ambiance without changing product variant colors. Warm light must not turn white flowers into a yellow SKU; brightening must not bleach green foliage.

Overcast/misty scenes favor diffuse illumination. Direct sun and crisp shadows need compatible weather. Match subject/background white balance, light softness, and exposure range while retaining highlight texture and shadow detail.

Borrow a color reference's temperature, contrast, and tonal relationships, not its product color. Prefer suitable non-generative adjustment tools when available; inspect model-based adjustments for shape/texture drift. Natural-language color edits are not deterministic LUT processing.

## Review

Check identity colors, material, light direction, receiving surfaces, grounding, clipped highlights, blocked shadows, oversaturation, sharpening halos, and abrupt local illumination. Faithfulness matters more than stronger gloss or darker shadows.

---

# Information images

Use for individual Amazon US dimension, detail, combined dimension/detail, selling-point, and A+ images. Follow user-specified delivery settings. Do not expand into a full listing set or invent A+ module dimensions.

## Facts and copy

By default, the selected image model draws text, callouts, and icons directly. Preserve supplied copy and its intended meaning. When detail copy is missing, write short English descriptions of visible appearance: leaf veins, petal texture, color, form, and visible connections.

Dimensions, composition/material, package count, installation method, UV resistance, waterproofing, fade resistance, certifications, flexibility, detachability, and living-plant care requirements need confirmed evidence. Visible texture alone does not prove a material or performance claim. Without supported selling points, organize the image around visible features.

Do not list an unconfirmed pot, decorative flower, tray, or chain under “What's included.” Explain non-included styling briefly where needed; small print cannot cure a misleading portrayal.

## Dimension graphics

Require real values, units, and corresponding endpoints. Distinguish overall height including pot, bare-stem length, crown width, spread, pot height, opening diameter, and wreath outside diameter.

Ask for missing values or ambiguous endpoints. Do not estimate dimensions, fabricate placeholders, or present an empty dimension graphic as finished. Preserve supplied values and units; convert only when requested and verify the calculation without silently changing rounding.

Match arrows to actual measured parts and avoid covering the product. Additional views must come from genuine source photos or crops, not fabricated backs. Visual scene matching is not measurement evidence.

## Details and combined layouts

Select a few real regions that answer the current buyer question: flower/leaf/stem texture, pot/base, verified construction/accessories, actual packaging, or arrival state.

Main subject and details must show the same product. Keep copy short and readable. If installation information is absent, show visible parts; if interior evidence is absent, show exterior details. Do not invent freshness, quality, care, or shipping-state promises for live plants.

Combined dimension/detail layouts inherit all measurement requirements. Fit the layout to aspect ratio and information density; do not fix arbitrary left/right percentages or add unrequested panels.

## Individual A+ and selling-point assets

Develop one requested theme using confirmed facts and dimensions. Keep the product readable, scene credible, and text clear. Allocate space to actual copy needs. Full-set sequencing, competitor analysis, and conversion strategy are future work.

## Review

Check spelling, numbers, units, arrow endpoints, correspondence between text and feature, and factual support for new claims. Inspect at reduced display size for hierarchy and readability. Model-rendered lettering is not automatically correct. Correct errors within the shared three-round budget; after it is exhausted, report unresolved text rather than claiming a finished asset.

If the selected tool cannot make text reliably readable, explain the limitation. An editable text-layer alternative may be offered, but do not silently replace the user's default model-rendered workflow.

---

# Quality and repair

Review every actual result against the current request and product evidence. A generation status or model self-report is not proof of fidelity.

## Review in priority order

1. **Product identity:** type, flower/leaf shapes, key branches, color, texture, quantities, container, markings, and included items. Assess explicitly permitted arrangement changes separately.
2. **Physical integration:** scale, support/contact, insertion depth, occlusion, load-bearing structure, intersections, light, shadows, and replaced-object remnants.
3. **Composition:** shot distance, horizontal facing and pitch, placement, coverage, completeness, and allowed cropping.
4. **Local quality:** halos, ghosting, broken stems, fused shapes, patches, sharpness discontinuities, exposure, and color drift.
5. **Information and delivery:** image type, factual copy, numbers/units, annotation position, requested count and export settings. Confirm alpha only through actual inspection.

Use relevant checks for the image type. Hidden details, tiny unreadable components, and unproven performance remain unverifiable; do not fill gaps with confident claims.

## Shared repair budget

After the initial generation, automatically repair material defects for at most **three rounds**. The initial generation is not a repair round. Deliver sooner if satisfactory.

A round is one targeted repair attempt on each failed candidate in the current task. Candidate batches share at most three review/repair cycles. Leave passed candidates unchanged; each failed candidate gets at most one repair attempt per round.

All modules and regions share the counter. Restarting from a source, revising prompts, or changing edit methods still counts. A failed repair tool call consumes that attempt. Do not reset the counter by relabeling automatic work as a new task. Do not switch the user's model or add candidates to evade the cap.

Before each round, identify the observable failure and choose an appropriate local edit, reframing, or source-based redo. Update the instruction using result feedback rather than repeating it mechanically.

Report service/tool failures as such, not as visual defects. When results cannot be viewed, stop blind automatic repair and explain that visual review is incomplete. A new user-requested modification is a new task; automatic retries are not.

## Stop and deliver

Show actual results. If defects remain after three repair rounds, stop and state the unresolved issue, which candidates are relatively usable, and what specific evidence or user decision would help.

For example, only when actually observed: “After three repair rounds, the right leaf cluster still differs from the product photo. This is not ready as a final image. A clearer photo of that area or a composition that retains the original subject would help.”

Keep history and selections in Lovart. Review is assistance, not a guarantee that every leaf, pixel, or marketplace check passed.
