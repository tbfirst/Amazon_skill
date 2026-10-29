# Amazon 商品视觉 Skill 集合

当前包含三个独立 skill：**lovart-plant-product-images** 负责植株单图制作；**amazon-plant-image-strategy** 负责整套 Amazon 植株图片策略与 Lovart 提示词；**amazon-video-generation** 负责产品视频的需求澄清、详细分镜表和即梦提示词。均支持中文大白话输入。

本目录是独立的本地 Git 仓库，日期为 2026-10-14。第一版本纳入本地初始提交，后续由你配置远程仓库并推送；许可证按你的决定暂缓。生成的 dist/ 压缩包保留在本地，不重复纳入 Git。

## Amazon 视频前期制作 · v3.1.0

调用 `$amazon-video-generation`，源码见 [SKILL.md](skills/amazon_video_generation/SKILL.md)。默认21:9、四条各10秒、顺序衔接的中文即梦提示词：特写与缓推、空间多角度展示、有依据的卖点、右侧商品与左侧后期文案留白。

交付详细文字分镜表（镜号、顺序、全局/段内时间、时长、景别、角度、运镜、画面、依据和接缝）及CSV，不生成故事板或编辑页。最后10秒为固定无人连续单镜头，不生成文字、Logo、数字或按钮。21:9为创作母版，Amazon具体版位的发布规格另核实。

新增 [植物商品运镜库](skills/amazon_video_generation/references/camera-movement-library.md)：慢推拉、横移视差、短弧环绕、升降和前景揭示，按商品资料与镜头目的选用。附提示词片段、角度覆盖、失败简化方案及[研究边界](skills/amazon_video_generation/references/research/2026-10-29-camera-movements.md)。

内置 [T01/T02模板](skills/amazon_video_generation/references/builtin-video-templates.md)，承接同SKU事实，保留旧项目已明确约定。[行为案例](skills/amazon_video_generation/evaluation/CASES.md)覆盖新流程；旧故事板工具仅保留历史兼容。

示例：使用 $amazon-video-generation，根据我的商品图制作21:9的四段10秒视频方案，交详细分镜表与四条完整中文提示词，尾段留白供后期加字，不生成故事板。

## 整套 Amazon 图片策略

2026-10-27 策略 skill 更新至 v1.22.0：新增旧套图更新，基于竞品套图和评论分析迁移布局与搭配，按实际更新范围交付；细节不清时即时弹窗澄清或请求同SKU补图。文字优先融入完整背景或明确编辑区，不默认铺白色模糊底。200个独立模板继续保留，138张内置图未改。验证范围见 [策略技能说明](docs/AMAZON-STRATEGY.zh-CN.md)。

入口：[amazon-plant-image-strategy/SKILL.md](skills/amazon-plant-image-strategy/SKILL.md)。按宿主支持的方式加载完整目录后，可输入：

> 使用 $amazon-plant-image-strategy。我的产品是……，以下是原始实拍、白底、多角度细节与真实尺寸资料，以及 3–6 个不同竞品 ASIN。请并行研究竞品图片、A+和评论，输出 design-strategy，以及尺寸图1张、细节图1张、场景图4张、A+图5张的独立 Lovart 提示词，写清布局、明暗和阴影。

默认美国站；中文引导和策略文档；英文图上文案与提示词。先读原始素材，不要求用户先上传成品附图/A+。研究后弹框比较带来源的尺寸/细节版式、四场景处理与五A+序列，已选或委托的项跳过。独立浏览器会话/标签页并行研究；直链失败后继续实际浏览器、页面状态检查与公开搜索恢复，剩余受限内容才索要最小补充。

新品首套默认交付1张尺寸＋1张细节＋4张场景＋5张A+，共11份Brief和独立TXT，默认不新增主图。旧套图更新接受现有排版成图，按已定旧图范围重排；只有范围内已有主图才更新MAIN01，不自动扩成11张。核心技术文档 `design-strategy.md` 展示逐竞品与跨竞品分析，并说明每张图如何借鉴已观察到的布局、光线和阴影。另有单竞品记录、证据账本、决策记录和提示词索引。A+图按当前范围与真实模块适配，不因模块多图静默扩数；未就绪提示词单列在 `prompts/blocked/`。

用户可直接打开 `all-prompts.md` 或 `all-prompts.txt`，按每张列出的顺序上传原图并复制完整提示词到Lovart；未就绪正文不混进可执行合集。每张包含选定版式骨架，并保持套图的字体、边距、配色与标注规范。这个skill不调用Lovart、不自动生图、不上传Amazon，也不凭空获得评论或关键词工具权限。

竞品研究先核对身份与变体，再盘点图库/A+，逐图目视和抽样读评论，最后横向对比。每区段保存 JSON 检查点；[离线审计工具](skills/amazon-plant-image-strategy/references/research-records.md) 检查图片覆盖数、重复评论及证据字段，不能把一致性通过解释为研究完成。浏览器默认2页并行，按实际稳定性调整。

`skills/` 是源码与分发结构；当前项目已存在 `.agents/skills/amazon-plant-image-strategy/` 加载副本，更新时需同步。[Codex 官方文档](https://learn.chatgpt.com/docs/build-skills) 说明项目内技能发现机制；具体同步与验收状态见设计说明。

## 文件入口

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](skills/lovart-plant-product-images/SKILL.md) | Agent 安装后发现和执行的英文入口 |
| [Amazon 策略 SKILL.md](skills/amazon-plant-image-strategy/SKILL.md) | 整套图的引导、证据、策略与提示词入口 |
| [Amazon 视频 SKILL.md](skills/amazon_video_generation/SKILL.md) | 视频多轮需求拆解、产品事实承接、详细分镜表与即梦提示词 |
| [完整 Lovart 指令](skills/lovart-plant-product-images/LOVART_INSTRUCTIONS.md) | 在 Lovart 内创建自定义 skill 的完整文本，不依赖读取本地模块 |
| [references](skills/lovart-plant-product-images/references/) | 八个功能模块，以及 Lovart 执行适配说明 |
| [设计与后续计划](docs/DESIGN.zh-CN.md) | 已确认决策、集合结构、后期整套 Amazon 图片开发 |
| [验收案例](skills/lovart-plant-product-images/evaluation/CASES.md) | 中文/英文需求及预期行为 |
| [验证状态](docs/VALIDATION.md) | 本轮检查与仍待进行的实图验证 |

## 在 Lovart 中使用

1. 打开项目并启用 Thinking Mode。官方要求本会话至少已有一次 Agent 对话，才可创建自定义 skill。
2. 打开上面的完整指令文件，将正文作为对话中的工作规则提供给 Lovart。可先输入：“请按以下规则处理植株商品图片，之后我会提供商品图和具体要求。”随后粘贴完整英文规则。
3. 上传实拍与必要参考图，完成一个具体任务并检查结果。用户继续在 Lovart 界面选择图像模型；skill 不替你切换。
4. 打开 Skill Book → Create a Skill → 保存到 My Skills。可命名为“植株商品生图”。
5. 查看并编辑保存后的指令，核对商品保护、图源角色、真实尺寸、三轮修复等关键规则没有被自动总结丢失。若当前编辑器允许，可将完整指令作为保存的执行内容；平台长度与附件支持以实际界面为准，未做账户内验证。
6. 新对话中从 Skill Book 选择这个 skill，再上传商品图并输入大白话。

以上流程依据 [Lovart 官方文档](https://www.lovart.ai/docs/how-to-prompt/agent-skills)。本包不承诺 Lovart 能从 GitHub 直接导入通用 SKILL.md，也不承诺只输入名称就已加载 My Skills。

可直接试用的请求：

> 使用植株商品生图。将这束花放在欧式阳台上，花束是售卖商品，花盆只是道具，保持原花材数量、颜色和纹理。略微俯视，但看得清盆身。生成 1 张 2048×2048 的 PNG。

这里的张数、像素与格式只是示例。你实际使用时指定自己的规格，已有确认规格可沿用。

## 在其他 Agent 中安装和选择

集合采用 skills/技能目录/SKILL.md 结构。安装工具将各 skill 注册到目标 Agent 后，支持自动发现的 Agent 可根据名称和描述判断使用哪一项，再按需读取模块。当前有三个独立 skill，各自的 references 模块不需要分别安装。

**把仓库克隆下来不等于完成安装；安装指令也不等于获得 Lovart 生图能力。** Agent 必须实际有可用的 Lovart 工具或浏览器访问能力。没有连接时，会给出可粘贴到 Lovart 的提示词、参考图角色及缺失信息，并说明尚未执行出图。

本地可选用第三方 [skills CLI](https://github.com/vercel-labs/skills)，需要 Node.js/npm。在集合根目录执行：

```sh
npx skills add . --list
npx skills add . --skill lovart-plant-product-images
```

安装时按提示选择目标 Agent。也可以按目标 Agent 的官方安装方式复制完整 skill 文件夹。请保留 references、scripts 等随附资源。本轮只准备安装说明，没有运行安装或改动全局配置。

将来创建 GitHub 仓库后，把 OWNER/REPOSITORY 换成真实仓库标识：

```sh
npx skills add OWNER/REPOSITORY --list
npx skills add OWNER/REPOSITORY --skill lovart-plant-product-images
npx skills add OWNER/REPOSITORY --skill '*'
```

最后一条选择仓库当前所有 skill，由安装器提示选择目标 Agent；不表示今后新增 skill 会自动安装。当前仓库地址与许可证未确定，这些命令是发布后的使用模板。

若在 Codex 项目内使用，完整目录结构为 `项目目录/.agents/skills/技能目录/SKILL.md`，同时保留 references 等资源。本项目图片策略与视频技能已有这个加载副本；源码更新后应一起同步。新技能是否立即出现在当前会话取决于宿主重新发现/加载机制，文件存在不代表当前会话已刷新技能列表。

## 日常工作规则

- 真实植物、仿真植物、花环、花束、盆栽、花箱均支持。
- 未指定场景/道具时，可自主选现实欧式住宅环境；用户明确指定的环境优先。
- 售卖主体和随货配件保留；装饰道具可调整。明确要求时可作实物允许的造型整理，不复制花材增加丰满度。
- 添加其他装饰花材需要明确要求。
- 场景可做视觉比例匹配；尺寸图必须提供真实数值、单位和测量部位。
- 细节图可自动拟写简短英文外观文案，默认模型直接绘字；不得编造性能、成分或随货清单。
- 比例、像素、张数、格式由用户指定；模型沿用用户在 Lovart 的选择。
- 首次生成后最多三轮自动修复，所有模块与候选共用预算；超限后文字说明问题。
- 单图技能仅要求提示词/讨论时不生图。整套规划使用新策略技能；用户在 Lovart 执行对应提示词。

## 更新与验证

维护英文 SKILL.md 和 references 后，在集合根目录运行：

```sh
python skills/lovart-plant-product-images/scripts/build_lovart_instructions.py
python skills/lovart-plant-product-images/scripts/build_lovart_instructions.py --check
```

脚本只使用 Python 3.10+ 标准库，生成/核对完整指令，不连接 Lovart、不生成图片、不进行 Git 操作。不要直接修改生成版后忘记更新源文件。

当前可以进行本地试用。公开发布前再确定仓库地址和许可证；本包未附开源授权。
