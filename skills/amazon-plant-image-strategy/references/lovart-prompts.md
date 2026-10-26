# Lovart 提示词交接

交付的是用户可复制的工作指令，不是 Lovart API 调用。用户仍需上传对应原图；不声称本地路径或证据编号会自动传给 Lovart。不固定模型，不把第三方技能中的模型名称、密钥或推广生图网址带入提示词。

写相关最终prompt前执行[文案/字体弹窗](copy-typography.md)与[场景类型分配/方图尺寸弹窗](scene-types.md)。本轮用户基础文案只做保义润色；明确提交空白则AI生成。字体提供Apple等基础选项，明确跳过则AI选择。SCENE固定1:1，先问四类在4张内的张数分配，再逐图选择1600/2000/2048方图。将这些选择在策划阶段解决，不让Lovart再替用户选。

## Consistency pass

所有历史库模板（包括OUT室外卡）的文字层都须经过[三遍润色](copy-typography.md#文案润色先保义再自然再适配版面)与[文字布局](text-layouts.md)适配。历史标题只是源内容，不覆盖用户输入、已选字体或当前SKU事实。改编时完整复述已选文字地图，不要求Lovart读取内部TYPE编号。

使用[室外OUT模板](outdoor-scenes.md)时，先将agent改编前言与所有条件分支解析成当前SKU的唯一方案，再交付英文指令。固定实际附件、暴露范围、支撑、件数、步骤/对比条件、准确文案、字体及本张像素；不能直接将模板中的“已选尺寸/按真实方法”等泛称当READY提示词。OUT原始卡片无成图验证，改写不等于效果验收。

先过[事实与细节门槛](product-truth-compliance.md#缺失事实与可见细节门槛)。模板中的“花瓣/叶片/织纹/挂件”都是有条件的任务对象，不证明当前商品存在它们。逐条删改不适用指令，而非在仍要求绘制不存在部位的正文后追加一句“不要编造”。已确认布局需要更换部位或减少窗口时先澄清。

交付前按每个资产独立检查，不用堆叠更多否定词掩盖冲突：

- **来源**：提示词的附件名称、角色及顺序与 manifest 一致。不要沿用聊天中的“图2”来指代该条的第1个附件。只引用这张图实际会上传的素材；布局样例与商品身份分开。
- **全貌与局部**：依据已确认的素材角色选图，用本张附件序号＋真实文件名＋画面特征定位。DIM01默认只附完整商品视图与所需测量资料；有局部窗才附相关特写，并限定其使用区域。每条尺寸绑定对象、端点、状态与成图视图；整体尺寸不得落到局部放大窗。角色或端点有歧义时先弹框澄清，不由生成器猜测。
- **布局**：明确百分比相对于整张画布还是某一分区，面板总宽＋间距＋两侧边距不能超过100%。圆窗直径采用画布宽度时，也验算其高度与标签空间。用等比例缩放、取景和短文案适配，不能挤压商品形状。
- **文案**：对照用户原文/锁定词与最终稿，保留原意和证据边界，只给生成器最终英文，不把原稿和润色稿同时要求绘制。只保留一个明确的位置、字形层级、行数和确切文本；大中小层级、卖点详略、字重/颜色按重要性安排。保持所选参考的文字/底板关系；可在留白中使用协调的非黑色字与填充框，不默认删除底板。用户选择米白区/属性框/步骤底条时去掉与其冲突的禁底板旧词，不能同时要求与禁止。无文案的场景保持无文案，艺术字体不强加到数字/单位。
- **参考路线**：来源符合用户在读取竞品套图后选择的路线；选择刚抓取套图反推时逐图描述实际观察到的骨架、文字层级与光影，不自动回退到内置默认。混合路线逐图指明主来源；内部来源ID放外部文档，执行词仍完整自包含。
- **字体与标题艺术字**：落实用户所选Apple/其他基础字族或自定义字体，不能被艺术字默认覆盖。AI委托时，适用短标题主动给出具体展示字/手写/笔刷/装饰衬线风格并要求绘制准确文案；写清笔画、字色、行数与背景区，避免只写“高级艺术字”。单图所有文字默认同一字族/字形（font_lock），数字、单位与必要说明也在此字族内保持易读；不默认艺术字标题搭另一种黑体。全部笔画、长尾及字效必须在完整商品轮廓加缓冲之外；无字/原生字段/朴素风格选择照常保留。
- **场景类型与规格**：SCENE四类张数合计4且映射到ID；每张固定1:1并有像素回答/委托，prompt只写本图选定尺寸。四宫格逐格给不同风格和商品，安装图逐步给真实动作/顺序，对比图给明确条件/固定项。拼格数量不是资产数量，不给未答图套默认1600提前定稿。
- **尺度与光影**：区分实测尺寸、假设的家具尺寸、入瓶遮挡与画面占比；35 in 枝条插入花瓶后的露出高度不会自动等于35 in。接触阴影必须有真实接触面，壁面枝影取决于光源和墙距，不能为了“有阴影”凭空添加。
- **版本与边界**：整套 SKU 的颜色锁和某一张改色授权分开。改提示词不代表已重生成或验收图片。按 manifest 重建 Markdown/TXT 合集，避免合集与单条不一致。
- **配色与载体变化**：对照逐场景表，写入本图唯一字色/底板色、背景明暗与选择理由；不从示例批量复制棕底白字。只替换道具容器，锁定真实随货盆；写本图造型/材质/口部/底部和H/D依据，不把产品参考照片中的玻璃瓶强制复制到全部场景。
- **分段与容纳**：散枝的总长、主体、下部裸茎分别有端点/依据；逐载体写外高、有效内深、插入量、露茎、主体与摆放总高。不能只写一个整体比，也不能把未剪总长当成穗头长度。剪裁能力与本图采用剪裁的决定分开。见[分段尺度](scale-and-composition.md#散枝入载体分段计算)。
- **数量与密度**：单瓶也核对每包数量、本图分配、完整包/部分展示及经确认的实拍密度锚点；不继承竞品枝数，不靠加枝/放大花头消除稀疏。不可数的成图不能验收为准确数量。
- **组合**：多色/多品类/多载体按[内容表](arrangement-composition.md)确认单一或混放、每瓶配方/数量、同时或替代展示和售卖范围；每附件明确对应哪个产品及载体。未答组合问题不得交给生成器随机决定。

## 文件与就绪状态

固定使用 DIM01.txt、DETAIL01.txt、SCENE01.txt–SCENE04.txt、APLUS01.txt–APLUS05.txt，共 11 份。每个文件只对应一张图；A+ 模块映射另写，不因多图模块或移动端需求静默增加文件。用户显式改变范围时再调整。

无关紧要的研究缺口不必阻断保守画面。商品身份来源或需要绘制/用于尺度判断的实物尺寸缺失时，受影响文件放入`prompts/blocked/`，开头写`CONDITIONAL DRAFT — NOT READY TO GENERATE`，列明缺项和安全替代。DIM/DETAIL默认1600×1600、桌面A+默认1464×600是已知制作值；SCENE固定1:1，像素需逐图弹窗选择或明确委托。仅未知账号资格/槽位时，继续已定画布方案，上传就绪标PROVISIONAL/待核。文案、字体、场景分配/像素未答时也保留相关依赖，不用超时/预选伪造确认。无数据时不填看似真实的数字、ASIN、证明句或文件名。

同样的阻塞规则适用于必须呈现却没有依据的材质、纹理、结构、视角或工作状态。先向用户提出具体澄清，而不是仅写BLOCKED或把“请补全真实细节”转交生成器。非必要未知主张可删去，但不能静默改变用户已经选定的图片任务。

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
For a competitor-derived asset, list the actual selected composition/lighting
image as a separate style-only attachment, alongside our product photographs.
A filename or URL in text does not attach image bytes. If direct attachment is
unavailable, disclose text-only adaptation in the handoff; do not claim a visual
reference was supplied. Never transfer the competitor product, count or copy.
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
State only supported SKU facts and directly resolved appearance: product type,
silhouette, proportions, color, actual parts, density, finish and sale contents.
Distinguish confirmed material composition from visible surface appearance.
Do not fill every attribute merely because this outline lists it.
Repeat all applicable protected attributes in this prompt.
Describe permitted rearrangement and its limits, if any.

EVIDENCE LIMITS
Identify the actual photo and visible region supporting each requested detail.
Use only detail resolved at the source's real resolution. Do not reconstruct
unseen fibers, veins, seams, pores, reflections or hidden geometry from a
material name, category stereotype, competitor or AI-generated reference.
Clarity enhancement may improve existing information, not create product facts.
Before handoff, the planning agent must resolve indispensable gaps with the
user; do not pass unresolved factual decisions to the image generator. If an
attached file is absent, illegible or inconsistent, stop this dependent image
and request that specific input rather than substituting plausible detail.

CONTAINER CONTENTS AND SOURCE MAP (when applicable)
Identify the vessel as fixed merchandise/included hardware or a styling prop.
Keep fixed product containers unchanged. For an approved/delegated styling prop,
state this scene's resolved vessel silhouette, material, opening, footprint,
external height and usable depth, including their measured or design-assumed basis.
Our product photograph may show another prop vase: retain the merchandise only,
and use the specified vessel here. Do not carry its glass vase into every scene.
State the confirmed number, position and depth of containers, and exactly which
products/colors and allocated quantities go into each. Map the actual reference
filenames to each product and container; keep single-type versus mixed contents
explicit. Distinguish simultaneous placements from separate alternative-use views.
Preserve each product's own color, shape, dimensions and sale role. Do not average
colors, substitute heads between products or duplicate one full pack per container.
State what is sold and what is separately sold or a styling prop, using approved
copy where needed. An unresolved identity/allocation is a blocker, not a random
composition instruction. Internal product IDs alone are insufficient for Lovart.

QUANTITY AND DENSITY (for grouped products, including a single vase)
State the verified sale-unit count and this image's shown allocation separately.
Identify the confirmed full-pack density photo, or a clearly planned partial view.
Preserve its supported head-to-stem structure, spacing, overlap and bundle envelope.
Do not borrow the competitor's pack count, add clones, enlarge heads or compress
bare stems to make a sparse arrangement fuller. Multiple simultaneous containers
must conserve the allocated total; separate alternative views are not extra packs.

REFERENCE TRANSFER (for reference-derived layouts)
Name the actual style attachment and its specific preserved properties: panel
count/order/bounds, subject and text positions, type hierarchy/color/backplates,
light direction/softness/contrast and cast-shadow direction/receiving surface.
State only the resolved changes required by our SKU, format or user decisions.
Do not silently replace this structure with a generic lifestyle photograph.

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
For lifestyle scenes/panels, name the target market, compatible occasion and two
or three recognizable architectural cues. Specify foreground, product plane and
background. Process close-ups use a truthful work surface and action framing;
they do not need an invented room/occasion. Same-location comparisons may retain
the same architecture and camera as explicit invariants.
Describe the intended new background explicitly; the identity photo's white
backdrop and its original cast shadow are not automatically part of the result.
Keep physical product-to-door/furniture scale separate from frame coverage.

SCENE STRUCTURE (when applicable)
State the selected single-scene, four-grid, installation/use/care or comparison
structure. A single scene occupies one coherent setting. For a four-grid image,
describe all four distinct-style settings in top-left to bottom-right order,
each with this product, correct scale, light, text and internal bounds. State
whether panels are alternative uses rather than simultaneous sale contents.
For process imagery, give the supported step count, order, actual actions,
hands/tools, completion state and exact step labels; do not invent a method.
For comparison, name changing conditions and fixed merchandise properties,
panel order and divider proportions. Weather requires supported use conditions;
night illumination does not make an unlit product emit light. All panels belong
to this one asset. State panel coordinates relative to the whole canvas or
their named panel explicitly. Do not let the generator choose missing content.

SCALE AND FOCAL PRIORITY
State the real merchandise dimension, measurement axis/endpoints and condition.
For loose stems, separately state supported total, decorative-body and lower bare
stem lengths with their endpoints. Distinguish one seed head from the staggered
decorative envelope of a whole bouquet. For each product-container pairing, give
container external height, usable depth to the actual support, insertion, exposed
bare stem, body projection and tabletop-to-tip height; identify the chosen untrimmed
or supported trimmed state and lower-stem cut length. Preserve the segment ratios,
not just the total silhouette. Lock the container base, rim, body start and tip.
State this scene's numeric above-rim height, exposed bare stem and body-to-vessel
ratio from the scale plan. Changing depth requires recomputing these values; do
not paste an identical exposed bouquet above both a tall and a shallow vessel.
Equal tabletop-to-tip heights can be physically correct when support heights and
stem projections are equal. Preserve the real stem length; never resize it merely
to make total arrangement heights differ. Disclose any supported, selected trim.
Use the calculated scale for each pairing; shorter vessels reveal more bare stem
unless an explicitly chosen, supported lower-stem trim changes the length. Never
enlarge heads, compress bare stems, pass stems through the base or invent a trim
to fit. Explain non-comparable geometry instead of supplying false precision.
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
Use this scene's resolved text and backplate colors from its local background,
lighting and selected reference. Campaign font consistency does not require
identical colors or the same cocoa/ivory card in every room. State actual colors
and fill treatment here, not a menu, a global example palette or an instruction
to let the generator choose. Keep coordinated campaign cues without recoloring
the merchandise or making a contrasting panel compete with it.
Specify one selected type family or coherent letterform style for ALL image copy,
large/medium/small size hierarchy, weight, color emphasis, line count,
alignment and text zone. Preserve the user's selected Apple-style or other
font system. A font-style instruction does not prove a font file was loaded.
Preserve the selected source's text zones and backplate relationships unless a
recorded adaptation changes them. Colored type and coordinated filled circles,
rounded rectangles or panels may improve readability. Specify the chosen text
color, fill/opacity, shape, bounds, padding and any subtle border/shadow. Keep the
whole treatment outside the full product and its buffer; do not default to black
type or add a box to every label. Never remove a selected band by generic rule.
For actual typesetting, load an available suitable font only with a real rendering
tool; record its file and permitted use. A font name in this prompt is not loading.
Keep text clear of foliage, bows, dimension endpoints and other critical details.
When font selection is delegated, for an eligible short image headline choose
one scene-appropriate
expressive style and instruct the image model to render the exact approved words
in that lettering. Describe stroke contrast, restrained connections or terminals,
weight, color, line count, alignment and a bounded quiet background zone.
Fit every glyph and flourish within that zone, outside the complete merchandise
silhouette plus its breathing buffer. Keep the product visually dominant.
Preserve explicit plain/no-copy choices and native-text-only A+ routes; never
add words just to demonstrate lettering. Keep facts, quantities, units and sale
labels readable in the SAME family/style. If the display face cannot do that,
resolve a readable family for the whole image in planning, not an unrelated
sans-serif for labels. Only explicitly approved mixed-font exceptions override. A style description does not claim a font file was loaded.
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

TEXT LAYOUT (omit when visible copy is NONE)
For each listed copy element, state its exact line-by-line text, one bounded
zone with an explicit coordinate basis, the selected typeface or observable
letterform, target size, weight, line height, tracking, alignment and color.
Repeat the image-wide font lock; vary size, weight or color, not unrelated faces.
For each backplate, resolve its shape, fill/opacity, bounds, padding and clearance.
Identify the exact phrase receiving emphasis and its one resolved treatment.
Keep the joined line text identical to the approved string except for spacing.
Keep numbers with units and qualifiers with the words they limit. Preserve
readable sale-content and use-condition labels. Do not print internal field
names or quotation delimiters, invent new text, or rewrite copy to fit.
Resolve text fit and product clearance in planning; the final prompt contains
only the chosen arrangement, not fallback copy, alternative fonts or a menu.

OUTPUT
One image. State known pixel dimensions, aspect ratio, color space and format,
distinguishing requested settings from settings that still need export verification.
DIM01/DETAIL01 default to 1600 x 1600 px. SCENE01-04 use the selected square
size, normally 1600 x 1600, 2000 x 2000 or 2048 x 2048 px, always 1:1 unless
explicitly overridden later. Desktop A+ defaults to 1464 x 600 px (61:25),
including scene-style A+ assets. Use the sRGB target. Repeat only this asset's
actual selected setting, not the option menu; later explicit project overrides
take precedence. A production canvas is not verified account-slot acceptance.

DO NOT CHANGE / DO NOT ADD
State asset-specific identity and compliance constraints, missing accessories
that must not appear as sold, unsupported performance implications, and forbidden copy.

CHECK BEFORE DELIVERY
Check the supplied references against product identity, quantity, scale,
all exact text and measurements, placement requirements and output settings.
Check projected size against genuinely comparable anchor endpoints, merchandise
salience versus props/type, and every product edge near a text effect at full size.
Where applicable, check decorative-body versus exposed-bare-stem proportions,
container insertion/support/clearance and trimmed state, then each container's
contents and simultaneous pack allocation. A correct overall height does not
prove correct head size, insertion depth or multi-product composition.
Report actual returned pixels separately from the requested export dimensions.
Report unresolved discrepancies; do not silently invent missing product details.
```

不要写“同上一张”“沿用前面的身份锁”“参考 P03”作为唯一说明。提示词需包含可执行的事实，证据 ID 只在外部设计文档中用于追溯。选择本张实际需要的原图，不机械要求上传全部历史图片。

将竞品/图库启发写成完整执行指令，例如“左侧全貌区x=6–57%，右侧两个圆窗自上而下，标题在顶部6–15%，尺寸线在商品外沿且不穿过花叶；所有标注使用统一细线和短无衬线文字”。在Brief和layout-decisions解释已观察来源、用户选择及适配；prompt不能只说“仿照ASIN第2张”或“LIB-DIM-01”。没有目视来源时区分模板文字与原创建议。坐标、光向与区域百分比是我方设计，不是竞品实测参数。

按[参考迁移约定](reference-fidelity.md)展示源图→方案→prompt对照，记录实际附件传入状态及必要差异；源图ID本身不代表相似性通过。以版式接近为目标逐项检查：分区/窗格数量与位置、完整商品/特写的比例、标题与标注层级、阅读路线，以及全套共同的色板/边距/线条规范。相同背景和花色不足以证明排版相似；选定两圆窗就不能在prompt里变成四格。需因证据或比例调整时同步更新决策和Brief，不虚构细节填空。

## 分图注意事项

**默认无 MAIN**：竞品主图可以分析，但不生成我方主图 prompt。尺寸图和细节图也不能被误标为白底主图。

**四张场景资产**：按[四类场景](scene-types.md)落实已选张数分配、逐图类型和方图尺寸；四类可为0张但总数为4，四宫格仍一张。各图有新增购买任务，分别写适用的摆放关系/实际步骤/比较条件、景别/机位、道具、光线与阴影，保持统一产品身份与视觉风格。安装图不强加不同房间；同地点昼夜对比不强改地点以制造差异。植物尺寸与家具关系真实。不要“make it bigger/lusher”来表达更有存在感；通过机位、留白和合理构图突出实际产品。未包含的套盆、托盘等不要暗示随货。

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
