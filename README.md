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

## Amazon 视频前期制作 · v5.5.0

调用 `$amazon-video-generation`，源码见 [SKILL.md](skills/amazon_video_generation/SKILL.md)。花卉承接已生成并精修选定的11张最终套图，也可从部分产品图开始；默认16:9、25–30秒综合展示：相机环绕、空间尺寸、1–2个动态细节、多次插花/整理、多场景和成品收尾。环绕时花器与花卉不自转，背景有真实视差；细节采用微风或轻抚等响应，生活场景有真实机位移动或动作，避免静图缩放轮播。

内置11种展示台背景提示词及室外衍生方案，按产品配色适配开场；插花默认3次，可从已有花材继续，也可先在手中整理成束后一次插入。

新增[双参考六维英文逆推与适配模板](skills/amazon_video_generation/references/reverse-video-prompts.md)：保留两片逐镜报告，并将镜头、动作、材质、风格光照、音景和技术规格整合为可替换SKU的模块。原片观察与复现建议分开，最终仍交完整中文即梦执行词。

通过3–4轮弹窗收敛，按实际一段/两段交付C01/C02文件夹，每段只放该段draft.txt和全部上传图；根目录仅分析说明书.md、README.md和shot-list.csv。上传图包含详细分镜表、带格下说明的宫格故事板及精选产品图；所有图片高度至少350像素，宽高比0.6–1.6且优先1:1。优先复用套图，缺少动作或角度画面时使用Codex内置图像工具补成。

优先整片生成。当前用户Seedance 2.0 Mini全能参考单次15秒，较长方案交前后两段自足词与衔接；更换Seedance 2.5后按实际入口核实整片能力。默认英文卖点与尺寸标注、轻音乐、无旁白，文字出错提供后期修正说明。视频由用户提交即梦生成，草木保留原有展示、安装和灯效路线。

详见[展示台背景库](skills/amazon_video_generation/references/display-background-library.md)、[动态导演规则](skills/amazon_video_generation/references/dynamic-flower-direction.md)、[花卉整片工作流](skills/amazon_video_generation/references/flower-showcase-workflow.md)、[双参考逐帧研究](skills/amazon_video_generation/references/research/2026-10-31-two-reference-showcase.md)及[分镜输出规范](skills/amazon_video_generation/references/flower-storyboard-package.md)。

示例：使用 $amazon-video-generation，把我的花卉套图做成30秒综合展示方案；交C01/C02文件夹，各含本段draft.txt和全部上传图，根目录仅分析说明书、README与分镜CSV，图片优先正方形。

版本均以本地提交/标签保存，详见[中文版本历史与回滚索引](docs/AMAZON-VIDEO-VERSION-HISTORY.zh-CN.md)。v5.5.0保持两类PNG同源与稳定镜号，新增精简目录和全量上传图片规格校验，分段执行词与本段文件夹附件对应。

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
