---
name: lovart-plant-product-images
description: Create or refine plant product images in Lovart from everyday requests and reference photos. Use for real or artificial plants, wreaths, bouquets, potted plants, and flower boxes, including compositing, framing, retouching, and individual Amazon US information images. Also prepare prompts for these Lovart tasks; not a full listing image campaign planner.
metadata:
  version: "1.0.0"
---

# Lovart Plant Product Images

Turn everyday requests and reference images into faithful product imagery. Prioritize product identity, physical integration, and controllable composition. Interpret the request, build a focused prompt, and execute when Lovart tools are available. Ask only about missing facts, unclear targets, or necessary delivery settings. If the user requests discussion, analysis, or prompts only, stay within that scope.

## Execution context

Read [Lovart execution](references/lovart.md) when establishing access, choosing an execution route, or resolving tool/settings limitations. Installation supplies instructions, not a Lovart connection or image model. Without usable Lovart access, deliver the prepared prompt and reference mapping, and state that no image was generated. Do not silently switch platforms.

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
| Photography advice, missing views, white background, cutouts, detail/intermediate assets | [Asset preparation](references/assets.md) |
| Place plants in containers/scenes, replace contents, combine references | [Product integration](references/fusion.md) |
| Choose or replace environments, European homes, seasons, background assets | [Scenes and backgrounds](references/scenes.md) |
| Distance, viewpoint, placement, frame coverage, cropping, outpainting | [Composition](references/composition.md) |
| Local fixes, props, feasible reshaping, local text correction | [Local refinement](references/refinement.md) |
| Exposure, shadows, color temperature, material appearance | [Lighting and color](references/lighting.md) |
| Dimensions, details, selling points, individual A+ images | [Information images](references/information.md) |

For every generated result, apply [Quality and repair](references/quality.md). The initial generation is followed by at most **three automatic repair rounds shared across this task**, not three per module, region, or candidate.

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
