# Amazon Product Visual Skills

A collection of four Agent Skills, with a [Chinese guide](README.zh-CN.md): individual Lovart plant imagery, Amazon plant image strategy, non-botanical Amazon image campaigns, and product video preproduction for Jimeng.

**Status:** local source collection, updated 2026-10-27. Strategy skill v1.22.0 adds finished-set refresh: analyze competitor sets/reviews, map old images to new layouts and styling, and request clear same-SKU details when needed. New sets default to 11 assets; refreshes use an explicit scope. Text uses intact scene surfaces or deliberate editorial panels rather than automatic blurred white mats. The 200 independent templates and 138 bundled images remain available. See the [validation scope](docs/AMAZON-STRATEGY.zh-CN.md); image generation remains unverified.

## Available skills

| Skill | Use |
| --- | --- |
| [lovart-plant-product-images](skills/lovart-plant-product-images/SKILL.md) | Turn everyday requests and product references into faithful Lovart plant imagery: preparation, integration, scenes, composition, refinement, lighting, individual information images, and review |
| [amazon-plant-image-strategy](skills/amazon-plant-image-strategy/SKILL.md) | Parallel research of 3–6 competitors; 1 dimension + 1 detail + 4 lifestyle + 5 A+ image plans; Chinese design-strategy and independent English Lovart prompts with layout, lighting and shadows |
| [amazon-ordinary-generation](skills/amazon_ordinary_generation/SKILL.md) | Image campaigns across non-botanical product categories, driven by each SKU's use, form, fit, contents and supported functions; Amazon/TikTok/YouTube research, observed-layout reverse prompting, 11-asset campaigns or scoped refreshes, Chinese strategy and independent English Lovart prompts |
| [amazon-video-generation](skills/amazon_video_generation/SKILL.md) | Flower showcase packages: complete Jimeng prompt, analysis manual, visual and detailed storyboard PNGs, with whole-film or two-part execution |

The plant image skills support real and artificial botanical merchandise. The ordinary-generation skill handles non-botanical product campaigns independently, with source files in `skills/amazon_ordinary_generation/` and invocation `$amazon-ordinary-generation`. Image strategy skills produce plans and prompts for the user to execute in Lovart; social video sources are research inputs, not a request to produce videos. The video skill handles its own video preproduction workflow.

## Amazon 通用商品视频前期制作 · v6.7.0

调用 `$amazon-video-generation`，源码见[SKILL.md](skills/amazon_video_generation/SKILL.md)。面向各类Amazon商品，按用途、结构、可动部件和交互任务策划视频；花卉与草木保留专门路线，花卉初始用例不再限制整个技能范围。接受产品原图、部分成图或已选最终套图，不要求先凑11张。

[通用主流程](skills/amazon_video_generation/references/product-video-workflow.md)与[物理连续性](skills/amazon_video_generation/references/physical-continuity.md)区分相机运动、主体运动和部件操作：先核空间可达性与真实连接，再设计接触、受力、移动、遮挡与结果。合理透视收缩不是结构变形；刚性结构、同一活动件和柔性道具的连接关系分别验收，不把所有商品锁成静止。

[执行词规范](skills/amazon_video_generation/references/full-film-prompt.md)要求TXT、上传表图和宫格说明仅写本SKU及真实上传附件；模板溯源、原片禁用清单、未试听声明和平台文件规则留在分析说明书/README。独立两段采用自足音景描述，同词不保证同旋律；需要统一音轨时规划实际共同输入或后期，不假定模型记得前段。

默认15–30秒、16:9，按已核入口决定一段或两段；用户既有Mini全能参考单次15秒设置仅在相同入口复用。只交C01/C02文件夹（各含本段draft.txt和全部上传图），根目录仅分析说明书.md、README.md及shot-list.csv。所有上传图高度≥350px，宽高比0.6–1.6，优先1:1；表与宫格保持同源S-ID和格下说明。

花卉分支保留F07综合展示、3次逐次插入或整理成束后1次插入、展示台适配等既定偏好；一般商品不被要求插花或强制环绕。前期图/词检查不等于视频实际通过，生成后的几何、数量、接触与道具连续性仍需验片。研究与能力边界见[本轮一手资料记录](skills/amazon_video_generation/references/research/2026-11-01-general-product-video.md)。

新增终态倒推：先选定好看的真实完成态，再设计基础布置与逐步补入，按正常动作顺序展示。多场景明确空间变化与用途，主体、柔性部件和可见光影按真实驱动联动；可手持细节优先稳定小转，触摸/弯折以材质为依据。规则见[终态倒推与真实运动](skills/amazon_video_generation/references/terminal-state-and-motion.md)。

v6.2固定每张宫格3×3九槽，前页填满才续页；每段全部上传图最多9张。详细分镜表按横向十列输出，台词与字幕分列。新增BG12–BG18通用配色展台及WHITE01洁白尺寸空间，生活场景优先轻微画内动作与因果响应。assets参考图已文字化并从当前树移除，历史研究截图按用户选择保留，编辑器模板迁至scripts/templates；旧素材可从v6.1.0恢复。

v6.4在回退后的v6.2基础上新增[三维场景演绎](skills/amazon_video_generation/references/volumetric-scene-direction.md)：每镜落实空间关系、可达相机路径、可见面/遮挡变化，以及持续动作的触发与响应。整图平移缩放和分层滑动不作为三维演示；按任务选机位，不强制人物或环绕，不虚构未知背面，也不强制光影闪动。规则直接映射到现有表/板/TXT，未恢复整套v6.3规则。

v6.5针对真实回归新增[商品与镜头保真](skills/amazon_video_generation/references/reference-and-shot-fidelity.md)：保留细节的部件定位与原有任务；逐张排除身份/状态/场景图结构冲突；检查每一步操作能否达到下一态；已选环绕与主体摆动不静默替换为微横移。TXT合并字段重复，终态落实轮廓、局部覆盖与落位关系。调查证据与未证实原因见[回归记录](skills/amazon_video_generation/evaluation/v65-regression-findings.md)，不是已完成视频修复的声明。

v6.6清理草木、版位及其引用模板中的旧分段与额外交付要求；将实体连续性、终态步骤、机位光影分工维护。按镜头任务验收：商品阅读镜可静止，空间/动作镜检查相应变化，已选动态保留。继续保留v6.5四项有效规则、15字段接口、十列表、九槽九图和精简目录；TXT合并重复表达，不为填字段制造运动。101项既有测试及独立文字试用通过，尚未验证即梦成片效果。

v6.7在本地`meng`分支加入[商品蒙太奇](skills/amazon_video_generation/references/montage-for-product-video.md)，覆盖顺叙、交叉、平行、重复、时间压缩和匹配接切，以商品信息、实际状态与时空关系选用。直接读取两份官方手册并加入[即梦2.0/2.5适配](skills/amazon_video_generation/references/jimeng-model-adaptation.md)：绑定实际素材、补齐格间动作、区分普通生成/延长/编辑，能力升级不覆盖九图与同镜多状态约定。核实[Amazon写实AI人物元数据](skills/amazon_video_generation/references/amazon-synthetic-performer.md)，标签适用于相应最终发布图片/视频，不泛化到所有AI商品图，也不混入画面提示词。默认服务欧美商品详情页，保留精简交付。101项测试、技能校验及独立文字试用通过；未生成即梦成片或实际改写发布文件元数据。

每个明确版本独立本地提交并附中文说明，详见[版本历史与回滚索引](docs/AMAZON-VIDEO-VERSION-HISTORY.zh-CN.md)。示例：使用 $amazon-video-generation，为我的家具、器具、穿戴或花卉商品设计两段视频方案，先确认真实结构和用途，再交精简分段包。

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
