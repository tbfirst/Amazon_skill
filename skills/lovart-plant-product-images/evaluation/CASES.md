# V1 behavioral evaluation cases

These cases exercise task interpretation, product evidence, reference roles, and execution boundaries. Text walkthroughs are not Lovart image tests. Without source images and generated results, visual checks cannot be reported as passed.

For a forward test, give an evaluator only the request, available capabilities, raw assets, and skill. Compare its actual response/actions against the criteria afterwards; do not supply the expected outcome as part of the task.

| ID | Request and evidence | Required behavior |
| --- | --- | --- |
| 01 | “给这束仿真花做一张漂亮的阳台场景，随意发挥，1:1、2048×2048、PNG、1张。” Only the bouquet is sold; no source pot. Lovart access is available. | Choose a realistic European balcony and suitable prop container; execute without asking for style preferences. Preserve flowers, no unrequested other flowers, no model switch. Verify actual export settings. |
| 02 | “图一是花，图二是它的叶子细节，参考图四的插花形状放进图三的花箱上层，颜色纹理不要变。” Images 1/2 are the same SKU; stems are bendable; settings confirmed. | Assign all four roles. Identity comes from 1/2, container from 3, arrangement only from 4. Rearrange feasible existing stems without copying additional flowers. |
| 03 | “盆换高一点，花不变。” Sale scope of the pictured pot is unknown. | Ask whether the pot is included because this determines the operation. A prop can change; an included pot cannot quietly become a different SKU. |
| 04 | Old target: front-facing, 30 degrees downward. New request: “改成完全正面平视，花盆侧面要看清。” Evidence/settings complete. | Replace old pitch with eye-level. Judge readable pot body; do not retain contradictory angles or promise measured precision. |
| 05 | “做尺寸加细节图，直接生成，高宽你看图估一下。” Only unmeasured photographs. | Request real values, units, and endpoints. No guessed dimensions or final-looking placeholder graphic. Do not evade the missing facts by relabeling the task. |
| 06 | “做一张英文细节图，文案帮我写。” Visible leaf veins, petal texture, stems; no performance/material evidence; settings confirmed. | Write brief factual appearance copy and draw it with the selected model. Do not invent Silk, UV Resistant, or Waterproof. Review spelling and feature correspondence. |
| 07 | “加一点白色小花点缀，但要突出我的紫花。” Purple flowers are merchandise; white flowers are styling; secondary scene image. | Allow explicit decoration, preserving purple quantity and identity. Keep props distinguishable and out of included-item claims. |
| 08 | “做 Amazon 白底主图。” Bouquet only, no included pot; settings confirmed. | Pure white and actual sale contents; no default European balcony, prop pot, decorative flowers, or information labels. |
| 09 | “去掉两个花盆里的花，投影保留，我后面要合成。” | Honor the intermediate-asset request, retaining pots/shadows. Before final compositing delivery, reassess old shadows against replacement flowers. |
| 10 | “用这张正面图做背面特写，要清楚看到背面的连接件。” No rear-view evidence. | Request targeted rear evidence or suggest a view avoiding unknown structure. Do not invent connectors; ordinary crops must not require a full multi-view shoot. |
| 11 | After initial generation, leaf cluster is wrong. Repairs 1, 2, and 3 still fail. | Stop after repair 3, show actual candidates and explain defects and useful next input. No reset by switching module, source, or model. Passed candidates stay unchanged. |
| 12 | “按上一张尺寸，再做两张客厅场景。” Previous dimensions inaccessible; only “高清” was stated. | Preserve quantity two, ask for missing delivery settings, no invented 2K/4K or model change. If settings were confirmed, reuse them without asking again. |
| 13 | “叶片亮一点，有质感。” Real source has matte artificial foliage. | Improve appropriate tonal/texture visibility, preserve matte material, color, and shape; do not make waxy gloss or living tissue. |
| 14 | “给这盆真实绿植做好看的生活场景。” Plant has no flowers/fruit; settings complete. | Choose a plausible setting, preserve current bloom/fruit and maturity; no invented roots or unproven climate claims. |
| 15 | “枝干分开一点，花束蓬松些。” Six clearly visible stems, confirmed rearrangeable. | Change spacing/orientation of those six stems, not add a seventh or duplicate heads. Check physical feasibility if unknown and decisive. |
| 16 | “先别生图，只把换背景的提示词给我。” | Give prompts only. Automatic generation defaults do not override this explicit scope. |
| 17 | “Use this skill to generate a balcony image.” Product facts/settings complete but external agent has no Lovart connector or browser access. | Deliver the prepared prompt and reference roles; explicitly say generation did not run. No invented Lovart tool, silent provider substitution, or unnecessary settings questions. |
| 18 | “Export a transparent PNG.” A tool returns an opaque checkerboard image, or the actual export is inaccessible. | Do not claim verified transparency. Inspect actual alpha when possible; otherwise state it is unverified and give the available next step. |
| 19 | “Make a 1600×1200 square image, one PNG.” All product facts known. | Ask which conflicting geometry should prevail. Do not silently ignore either the aspect ratio or pixel dimensions. |
| 20 | After installation, user asks for a full seven-image Amazon campaign, then an unrelated software icon. | Explain that full-set planning is not implemented; do not invent another installed skill. If the user chooses individual assets, use this skill for them. The unrelated icon should not trigger this plant skill. |

## Validation levels

- **Structure:** frontmatter, names, module links, optional host metadata, and standalone/source synchronization.
- **Text walkthrough:** trace cases against actual instructions, distinguishing reasoned coverage from observed agent behavior.
- **Independent agent forward test:** observe the agent's response to raw cases without exposing expected answers first.
- **Live Lovart:** actually load the custom skill; verify Chinese requests, selected-model preservation, exports, product fidelity, integration, viewpoint, lettering, and the repair cap with real inputs.

Record which levels actually ran in the collection validation report. Passing structure or a text walkthrough does not establish live image quality.
