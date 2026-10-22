# Lovart 提示词交接

交付的是用户可复制的工作指令，不是 Lovart API 调用。用户仍需上传对应原图；不声称本地路径或证据编号会自动传给 Lovart。不固定模型，不把第三方技能中的模型名称、密钥或推广生图网址带入提示词。

## Consistency pass

交付前按每个资产独立检查，不用堆叠更多否定词掩盖冲突：

- **来源**：提示词的附件名称、角色及顺序与 manifest 一致。不要沿用聊天中的“图2”来指代该条的第1个附件。只引用这张图实际会上传的素材；布局样例与商品身份分开。
- **全貌与局部**：依据已确认的素材角色选图，用本张附件序号＋真实文件名＋画面特征定位。DIM01默认只附完整商品视图与所需测量资料；有局部窗才附相关特写，并限定其使用区域。每条尺寸绑定对象、端点、状态与成图视图；整体尺寸不得落到局部放大窗。角色或端点有歧义时先弹框澄清，不由生成器猜测。
- **布局**：明确百分比相对于整张画布还是某一分区，面板总宽＋间距＋两侧边距不能超过100%。圆窗直径采用画布宽度时，也验算其高度与标签空间。用等比例缩放、取景和短文案适配，不能挤压商品形状。
- **文案**：只保留一个明确的位置、字形层级、行数和确切文本。先移到真实背景留白或精简，再考虑有理由的底板。替换旧模板中的色条要求，不同时留下“增加色条”和“禁止色条”。无文案的场景保持无文案，艺术字体不强加到数字/单位。
- **尺度与光影**：区分实测尺寸、假设的家具尺寸、入瓶遮挡与画面占比；35 in 枝条插入花瓶后的露出高度不会自动等于35 in。接触阴影必须有真实接触面，壁面枝影取决于光源和墙距，不能为了“有阴影”凭空添加。
- **版本与边界**：整套 SKU 的颜色锁和某一张改色授权分开。改提示词不代表已重生成或验收图片。按 manifest 重建 Markdown/TXT 合集，避免合集与单条不一致。

## 文件与就绪状态

固定使用 DIM01.txt、DETAIL01.txt、SCENE01.txt–SCENE04.txt、APLUS01.txt–APLUS05.txt，共 11 份。每个文件只对应一张图；A+ 模块映射另写，不因多图模块或移动端需求静默增加文件。用户显式改变范围时再调整。

无关紧要的研究缺口不必阻断保守画面。商品身份来源或需要绘制/用于尺度判断的实物尺寸缺失时，受影响文件放入`prompts/blocked/`，开头写`CONDITIONAL DRAFT — NOT READY TO GENERATE`，列明缺项和安全替代。默认附图1600×1600、桌面A+1464×600是已知制作值；仅未知账号资格/槽位时，继续默认画布方案，上传就绪标PROVISIONAL/待核。无数据时不填看似真实的数字、ASIN、证明句或文件名。

例外仅限用户明确授权的测试规格选择：可写具体画布和暂拟图位，标明 `PROVISIONAL — TEST CANVAS; ACCOUNT UPLOAD SPECS PENDING`，不使用未解析占位符，也不借此补造商品事实。

## 每条 prompt 必须自包含

以下结构用于编写，不是可直接交付的空模板。成品文件用真实已知内容代替字段。缺事实就删除相应要求或标 blocked，不能留尖括号让用户误以为可直接执行。

```text
ASSET: asset ID and image purpose
Create one image for the stated Amazon placement.

REFERENCE INPUTS
Attach these actual source files in this order:
1. Filename — product identity and permitted view.
2. Filename — detail/measurement/scene/style role, if needed.
Use product references for the merchandise. A style or composition reference
must never supply another product's leaves, flowers, pot, branding or claims.
Separate identity, measurement metadata, process evidence and visual-style roles.
For each attachment, identify whether it shows the complete product or a named
part. State its permitted output region and use. Upload order alone does not
establish its role. Use a close-up only for its identified part/detail inset;
never substitute it for the whole-product dimension view.
For every dimension, bind the verified value and unit to a named object,
measurement condition, start/end points and one specific output view.
Overall dimensions belong only to the matching full-product view. A part inset
may carry only independently supported part dimensions with visible endpoints.
Do not render an instruction card, SKU screenshot or reference brand as artwork.

PRODUCT IDENTITY
State the verified SKU, live/artificial identity, silhouette, proportions,
color, flower/leaf characteristics, branching/density, visible material,
included container, sold unit count and accessories.
Repeat all applicable protected attributes in this prompt.
Describe permitted rearrangement and its limits, if any.

IMAGE TASK AND LAYOUT — LAYOUT BLUEPRINT
State one specific buyer question and the concrete scene or diagram that
answers it. Specify panel/zone arrangement, subject frame coverage,
subject and text positions, whitespace, safe margins, detail insets and callouts.
Implement the selected layout skeleton explicitly: number and order of panels,
their bounds, full-product versus detail-window size and shape, reading order,
dimension-line positions and typography hierarchy. Preserve the chosen campaign
rules while using this SKU, supported source details and original approved copy.
Do not replace a specified multi-panel layout with a generic single photograph.
Use normalized layout zones when useful; these are design targets, not measurements.
Describe view, shot distance, perspective, depth of field, credible scale,
contact/support, background and crop limits.
Use only supported views and details. Distinguish styling props from sale contents.
For scenes, name the target market, compatible occasion and two or three
recognizable architectural cues. Specify foreground, product plane and background.
Describe the intended new background explicitly; the identity photo's white
backdrop and its original cast shadow are not automatically part of the result.
Keep physical product-to-door/furniture scale separate from frame coverage.

SCALE AND FOCAL PRIORITY
State the real merchandise dimension, measurement axis/endpoints and condition.
Name one primary scale anchor, its dimension and measured/confirmed/design-assumed
basis; identify comparable axes, relative depth and any perspective limitation.
Give the physical/projected ratio, then derive compatible framing from the anchor.
Do not independently enlarge product coverage, shrink furniture, or stretch the
product to fill a layout rectangle. Same merchandise size across scenes does not
mean identical pixel coverage. Foreground props are not coplanar measuring rulers.
List only selected supporting props and their purpose, placement and visual rank.
Merchandise remains the first visual subject; reduce/reposition competing props
instead of making the actual product larger. Off-center composition is permitted.

LIGHTING AND SHADOWS
Specify a scene-motivated light source, its direction relative to the camera,
height and apparent size; identify the lit face, readable dark face, contrast,
fill purpose and warm/cool balance without changing product color.
Describe self-shading, contact shadows, product cast shadows and any environmental
shadow separately when present. Name receiving planes, direction, length and
edge softness, including distance-related changes. Window patterns require
plausible windows; hanging objects need wall/support shadows, not pot-base ellipses.
Rebuild shadows for the new scene. Use material-appropriate highlights;
avoid floating merchandise, duplicate old shadows or invented gloss.

VISUAL STYLE
Repeat this asset's actual palette, lighting, background family, typography
and hierarchy. Spell out the selected design principles; do not tell Lovart
to open competitor URLs or copy an unseen competitor image.
Assign dominant, supporting and accent color roles with approximate design
proportions where useful; preserve the merchandise's actual colors.
Specify type family, relative size/weight, line count, alignment and text zone.
Integrate copy directly into quiet areas of the actual background by default.
Prefer no separate colored caption strips, cards, pills or boxes. Adapt a source's
caption band into integrated typography while preserving its information order.
Retain a panel only for a concrete readability need or an explicit project choice.
For actual typesetting, load an available suitable font only with a real rendering
tool; record its file and permitted use. A font name in this prompt is not loading.
Keep text clear of foliage, bows, dimension endpoints and other critical details.
If suitable, use expressive display lettering for a short mood headline only;
keep facts, quantities and units in a readable text face. Specify the chosen style,
not an automatic calligraphy requirement or an unsupported claim of loaded fonts.
Protect the complete merchandise silhouette plus a small breathing buffer from
text, swashes, glow, blur, frosted panels and gradients. Never wash out, defocus,
erase or fade any product part to make lettering readable. Restrict any backdrop
softening to background-only regions; move copy or remove the effect if it overlaps.

EXACT VISIBLE COPY
Headline: exact approved English words, or NONE.
Proof/supporting copy: exact approved English words, or NONE.
Other labels: exact measurements/callouts, or NONE.
Render only this listed copy. Do not add marketing claims or evidence IDs.
Keep Amazon native module text outside the generated image when specified.

OUTPUT
One image. State known pixel dimensions, aspect ratio, color space and format,
distinguishing requested settings from settings that still need export verification.
Default: secondary images 1600 x 1600 px (1:1); desktop A+ images 1464 x 600 px
(61:25), sRGB target. Repeat this asset's actual setting; later explicit project
overrides take precedence. A production canvas is not verified account-slot acceptance.

DO NOT CHANGE / DO NOT ADD
State asset-specific identity and compliance constraints, missing accessories
that must not appear as sold, unsupported performance implications, and forbidden copy.

CHECK BEFORE DELIVERY
Check the supplied references against product identity, quantity, scale,
all exact text and measurements, placement requirements and output settings.
Check projected size against genuinely comparable anchor endpoints, merchandise
salience versus props/type, and every product edge near a text effect at full size.
Report actual returned pixels separately from the requested export dimensions.
Report unresolved discrepancies; do not silently invent missing product details.
```

不要写“同上一张”“沿用前面的身份锁”“参考 P03”作为唯一说明。提示词需包含可执行的事实，证据 ID 只在外部设计文档中用于追溯。选择本张实际需要的原图，不机械要求上传全部历史图片。

将竞品/图库启发写成完整执行指令，例如“左侧全貌区x=6–57%，右侧两个圆窗自上而下，标题在顶部6–15%，尺寸线在商品外沿且不穿过花叶；所有标注使用统一细线和短无衬线文字”。在Brief和layout-decisions解释已观察来源、用户选择及适配；prompt不能只说“仿照ASIN第2张”或“LIB-DIM-01”。没有目视来源时区分模板文字与原创建议。坐标、光向与区域百分比是我方设计，不是竞品实测参数。

以版式接近为目标逐项检查：分区/窗格数量与位置、完整商品/特写的比例、标题与标注层级、阅读路线，以及全套共同的色板/边距/线条规范。相同背景和花色不足以证明排版相似；选定两圆窗就不能在prompt里变成四格。需因证据或比例调整时同步更新决策和Brief，不虚构细节填空。

## 分图注意事项

**默认无 MAIN**：竞品主图可以分析，但不生成我方主图 prompt。尺寸图和细节图也不能被误标为白底主图。

**四张场景**：分别写出任务、摆放关系、景别/机位、道具、光线与阴影，四张须有实质用途差异，保持统一产品身份与视觉风格。植物尺寸与家具关系真实。不要“make it bigger/lusher”来表达更有存在感；通过机位、留白和合理构图突出实际产品。未包含的套盆、托盘等不要暗示随货。

按[场景拓展](scene-expansion.md)从合适的候选场所/节日中选择，逐条写入本张确定的环境，而不是让生成器自由猜测欧美房间。固定圣诞装饰可拓展圣诞期间不同使用任务，不为跨节日删掉原配饰。住宅方向、建筑锚点、位置及观看距离要具体；不把四图统一写成米色墙+边桌，也不对所有图套同一柔光。更多版式和光影选择见[视觉指导](visual-art-direction.md)。

需要更多灵感时由本技能在策略阶段检索并筛选，prompt写最终选中的结果，不将“自己上网找场景”当作唯一场景指令。保留类别适配的生活/节庆小物，不统一禁杯子、书、画或烛台，也不把它们列成每图必需品。按[尺度校验](scale-and-composition.md)复述本图自洽比例与透视，不仅说“realistic scale”。

**细节**：用真实近景或原图裁切来源。没有内部照片就不要求生成根系/剖面。对未知材料描述外观而不是猜材料名。

**尺寸/步骤**：写明测量端点、实测数值、单位和产品状态。尺寸箭头不得覆盖重要特征。已确认需要双单位时保留核算过的值，不能让图像模型自行换算。没有真实操作证据不编造三步安装。

DIM01全貌/特写的来源和每条尺寸的目标视图必须明确写进本张prompt；选定版式、特写位置及尺寸线位置仍按多轮弹框讨论，不以规定上传顺序替代澄清。布局未决可保留草案，不能以“请模型自行选择”作为最终交接。用户上传成图后，检查整体尺寸箭头是否连到完整商品端点、局部窗是否误挂整体值；未看到成图不能声称检查通过。

**五张 A+**：每张各自一条完整 prompt，写清图位和哪些文字走原生字段；按五张图预算匹配模块。若选择原生文字优先，就把图中文字设为 NONE 并规划留白；若确需绘字，给出完整准确英文，生成后必须检查拼写和可读性。

分别落实五张的叙事角色及适配版式；一个原生三图模块使用三个文件，一张内含三场景的位图则只是一张文件，不能混淆。不要把原生文字路线解释为每张画面都应有巨大空白；不要把参考图的品牌、手作/材质词或9张手机适配直接继承为本项目任务。桌面、移动端有不同图槽时先核对范围，再提出重排需求。

## 交付给用户的简短说明

可从 `all-prompts.md` / `all-prompts.txt` 总汇或prompt-index选择一条可执行资产，按列出的文件名上传本张原图，再复制完整英文prompt到Lovart。总汇是11份单图提示词的可复制视图，不是让Lovart自行拆11张的总控制词，也不输出PDF。汇总必须从最新单张TXT同步，BLOCKED只在独立缺口区列出。制作命令与manifest格式见[交付规范](deliverables.md)。逐张使用，保留相同产品参考和视觉规范。图片出炉后按对应brief检查；本技能只完成规划与提示词预检。

如果用户随后上传生成图请求复核，可依据 brief 指出具体差异并修订该图 prompt；更新版本与受影响事实。除非用户另行要求执行，不自动打开 Lovart 或调用图像生成工具。
