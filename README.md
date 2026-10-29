# Amazon Product Visual Skills

A collection of three Agent Skills, with a [Chinese guide](README.zh-CN.md): individual Lovart plant imagery, Amazon plant image strategy, and product video preproduction for Jimeng.

**Status:** local source collection, updated 2026-10-27. Strategy skill v1.22.0 adds finished-set refresh: analyze competitor sets/reviews, map old images to new layouts and styling, and request clear same-SKU details when needed. New sets default to 11 assets; refreshes use an explicit scope. Text uses intact scene surfaces or deliberate editorial panels rather than automatic blurred white mats. The 200 independent templates and 138 bundled images remain available. See the [validation scope](docs/AMAZON-STRATEGY.zh-CN.md); image generation remains unverified.

## Available skills

| Skill | Use |
| --- | --- |
| [lovart-plant-product-images](skills/lovart-plant-product-images/SKILL.md) | Turn everyday requests and product references into faithful Lovart plant imagery: preparation, integration, scenes, composition, refinement, lighting, individual information images, and review |
| [amazon-plant-image-strategy](skills/amazon-plant-image-strategy/SKILL.md) | Parallel research of 3–6 competitors; 1 dimension + 1 detail + 4 lifestyle + 5 A+ image plans; Chinese design-strategy and independent English Lovart prompts with layout, lighting and shadows |
| [amazon-video-generation](skills/amazon_video_generation/SKILL.md) | Four connected 10-second Chinese Jimeng prompts in 21:9, detailed text shot tables and clean closing space for later copy |

The image skills support real and artificial plant merchandise. The video skill supports product video preproduction, including botanical products. The image strategy skill produces plans and prompts for the user to execute in Lovart.

## Amazon 视频前期制作 · v3.1.0

调用 `$amazon-video-generation`，源码见 [SKILL.md](skills/amazon_video_generation/SKILL.md)。默认21:9、四条各10秒、顺序衔接的中文即梦提示词：特写与缓推、空间多角度展示、有依据的卖点、右侧商品与左侧后期文案留白。

交付详细文字分镜表（镜号、顺序、全局/段内时间、时长、景别、角度、运镜、画面、依据和接缝）及CSV，不生成故事板或编辑页。最后10秒为固定无人连续单镜头，不生成文字、Logo、数字或按钮。21:9为创作母版，Amazon具体版位的发布规格另核实。

新增 [植物商品运镜库](skills/amazon_video_generation/references/camera-movement-library.md)：慢推拉、横移视差、短弧环绕、升降和前景揭示，按商品资料与镜头目的选用。附提示词片段、角度覆盖、失败简化方案及[研究边界](skills/amazon_video_generation/references/research/2026-10-29-camera-movements.md)。

内置 [T01/T02模板](skills/amazon_video_generation/references/builtin-video-templates.md)，承接同SKU事实，保留旧项目已明确约定。[行为案例](skills/amazon_video_generation/evaluation/CASES.md)覆盖新流程；旧故事板工具仅保留历史兼容。

示例：使用 $amazon-video-generation，根据我的商品图制作21:9的四段10秒视频方案，交详细分镜表与四条完整中文提示词，尾段留白供后期加字，不生成故事板。

## Use the campaign strategy skill

Load the complete [amazon-plant-image-strategy](skills/amazon-plant-image-strategy/SKILL.md) folder through your host's supported skill installation mechanism, then invoke `$amazon-plant-image-strategy`. State what the product is, upload original measurements/photos, and supply 3–6 unique competitor URLs or ASINs. Finished listing/A+ images are not required inputs. The skill uses independent browser sessions/tabs concurrently when supported, and asks only consequential unanswered questions. Defaults: Amazon US, Chinese discussion and documents, English image copy and prompts.

Direct-fetch failures trigger documented browser/public-search recovery before asking for exports. Missing evidence is labeled, not invented. Outputs include the substantive multi-competitor `design-strategy.md`, per-ASIN research files, evidence/decision records, a prompt index and one independent `.txt` prompt per scoped asset (11 by default for new sets). Refreshes also include an old-to-new map and an explicit target manifest. A+ assets are allocated to actual modules within the selected image budget (five for new sets). Incomplete production prompts are kept under `prompts/blocked/`.

After visual research, the skill compares actual competitor layouts with the bundled library, presents concrete options and asks layout questions using the available text popup tool. Each asset records its selected blueprint. Extra `all-prompts.md` and `all-prompts.txt` collections preserve the exact executable per-image prompt text and ordered upload references, with blocked gaps separate; no PDF or all-in-one inferred-layout controller is produced.

Research runs in staged batches: identity verification, image inventory, actual visual/review inspection, then comparison. Per-ASIN JSON checkpoints support resuming; the [offline audit helper](skills/amazon-plant-image-strategy/references/research-records.md) checks counts and evidence structure without browsing. Passing it does not prove source truth or research completeness.

The repository's `skills/` folder is source packaging. Project-local image-strategy and video skill copies exist under `.agents/skills`; keep them synchronized with the source. Discovery in a running session depends on the host's reload behavior. Current [official Codex documentation](https://learn.chatgpt.com/docs/build-skills) describes local discovery. See [strategy design and validation](docs/AMAZON-STRATEGY.zh-CN.md) for the image strategy's synchronization and testing status.

Each skill lives in its own directory. Supporting modules are resources within that skill, not separately installed skills. Installed metadata helps a compatible agent select the relevant skill; actual discovery and activation depend on the host. Cloning this collection alone does not register it with every agent.

## Install into an agent

Use a host that supports the [Agent Skills format](https://agentskills.io/specification). Install the whole skill directory, including references. Installation provides workflow instructions; generating in Lovart still requires a usable, authorized Lovart integration or browser session.

With Node.js/npm and the third-party [skills CLI](https://github.com/vercel-labs/skills), run these commands from the collection root. They preview or install locally; installation prompts select the target agent:

```sh
npx skills add . --list
npx skills add . --skill lovart-plant-product-images
```

After this collection has a real GitHub URL, replace OWNER/REPOSITORY below with it. These are publication templates, not an existing repository:

```sh
npx skills add OWNER/REPOSITORY --list
npx skills add OWNER/REPOSITORY --skill lovart-plant-product-images
npx skills add OWNER/REPOSITORY --skill '*'
```

The last command selects every skill currently present; it does not automatically install future additions. Retain interactive target selection. Alternatively, copy each complete skill folder into the host's documented skill directory and reload/rescan as that host requires. No custom collection router or fabricated connector manifest is necessary.

This package includes optional agents/openai.yaml UI metadata with implicit selection enabled. Host support varies; the portable entrypoint remains SKILL.md. No installer or authenticated Lovart session was executed during packaging.

## Use in Lovart itself

The [standalone instructions](skills/lovart-plant-product-images/LOVART_INSTRUCTIONS.md) include all functional modules without local file dependencies.

Lovart documents Thinking Mode and a project conversation, followed by Skill Book → Create a Skill → My Skills. Use the standalone text as workflow material in that conversation, save the custom skill, and check/edit its saved instructions. Then select it in a new chat and supply your images and request. The full procedure and an example starter message are in the [Chinese guide](README.zh-CN.md). Direct GitHub/SKILL.md import into Lovart is not established by the documentation. [Lovart documentation](https://www.lovart.ai/docs/how-to-prompt/agent-skills)

Example request:

> Use the plant product image skill. Place my bouquet in a realistic European balcony scene. Only the bouquet is sold. Keep its flowers and colors unchanged. One 2048 × 2048 PNG.

The requested dimensions are an example, not a default. The user controls Lovart's selected model. English rules still accept Chinese and other natural-language requests; reply in the user's language.

## Maintain and verify

Edit SKILL.md and references, then regenerate the standalone delivery file with Python 3.10+ (standard library only):

```sh
python skills/lovart-plant-product-images/scripts/build_lovart_instructions.py
python skills/lovart-plant-product-images/scripts/build_lovart_instructions.py --check
```

[Behavioral cases](skills/lovart-plant-product-images/evaluation/CASES.md) cover product facts, reference roles, execution boundaries, and repair behavior. [Validation status](docs/VALIDATION.md) separates structural checks from unperformed Lovart image tests. [Design and roadmap](docs/DESIGN.zh-CN.md) records accepted requirements and future image-set work.

Add future skills under skills/<skill-name>/ with distinct descriptions only when implemented. Do not turn roadmap ideas into discoverable empty skills.

## Publication status

The collection is versioned in a local Git repository; the user will configure the remote and push. Generated archives in dist/ are kept locally and excluded from Git. Decide the license and repository identity before public distribution. There is intentionally no LICENSE file or license frontmatter field. The absence of a license is not an open-source grant. No Git initialization, commit, history rewrite, account installation, or publication is performed by the bundled build script.
