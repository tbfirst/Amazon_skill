# Lovart 提示词交接

适用模式：下文固定11图、4张SCENE和5张A+均为`new-set`默认。`set-refresh`先按[旧套图更新](set-refresh.md)记录的目标清单执行，SCENE数量为N、A+为M；类型分配合计N，没有该角色则不追加或强问。已明确的选择与规格沿用，角色/数量/画布有歧义时才澄清。

交付的是用户可复制的工作指令，不是 Lovart API 调用。用户仍需上传对应原图；不声称本地路径或证据编号会自动传给 Lovart。不固定模型，不把第三方技能中的模型名称、密钥或推广生图网址带入提示词。

写相关最终prompt前执行[文案/字体弹窗](copy-typography.md)与[场景类型分配/方图尺寸弹窗](scene-types.md)。本轮用户基础文案只做保义润色；明确提交空白则AI生成。字体提供Apple等基础选项，明确跳过则AI选择。SCENE固定1:1，先问四类在4张内的张数分配，再逐图选择1600/2000/2048方图。将这些选择在策划阶段解决，不让Lovart再替用户选。

## 策划检查与执行正文分开

交付前核对实际附件角色、SKU与尺度、已选来源骨架、逐图文案回答、准确文字、画布与就绪状态。事实缺口按[商品事实](product-truth-compliance.md)处理；布局、文字效果分别按[参考迁移](reference-fidelity.md)和[文字布局](text-layouts.md)处理。研究、问答、证据ID、选择理由、审批与渲染状态留在Brief/索引，不复制进生图正文。

## 以成图质量为目标优化正文

优化目标是信息准确、指令清晰、画面可控，不以字数或压缩率衡量成功。复杂场景、尺寸/细节图和高保真竞品替换可以使用较长正文。删除一句前判断它是否控制了独立的视觉结果；若删除会让模型猜测产品、布局、光影或文字，应保留或改写得更具体。无字仅表示没有文字层，不代表场景描述也要简略。

每条只写本图要画什么、怎么构图、哪些必须保留。相同要求只写一次；删去泛化品质词、长篇禁止清单、重复身份锁、与本图无关的安装/容器/多色规则，以及“请先询问用户/查资料/通过审核”等代理工作流。需要澄清的事在交付前完成，不能转交生图模型。

源模板是策划材料，不直接原样粘贴。按本图实际需要展开字段：无字图一句说明即可，无需字体/文字地图；单景不写窗格规则；无容器不写入瓶几何。参数图保留数值、单位、端点，局部图保留真实部位来源；不能为缩短删除这些关键约束。每条独立可用，不引用上一条提示词。

### 必要画面信息覆盖检查

以下按本图需要展开，不机械塞满所有字段。具体内容必须进入执行正文，不能只留在内部Brief，也不能以“高质量、真实、参考原图”代替：

| 画面目标 | 必须保留的控制信息 |
| --- | --- |
| 商品准确 | 实际附件与SKU对应、可见颜色/形态/结构/纹理、数量、随货与道具边界；整体与局部来源分别绑定 |
| 继承优秀参考 | 指定主参考附件，明确保持的机位、取景、背景、道具位置、图文分区与光影；单列替换商品、文案、配色及必要适配 |
| 构图与空间 | 主体位置/占比、前中后景、必要留白、支撑和遮挡关系；多格图的分区、窗格形状/数量、间距和统一坐标基准 |
| 尺度可信 | 实测对象/端点/状态及同平面比例；涉及入瓶时保留插入深度、露茎、花材主体与容器关系，不能压缩成realistic scale |
| 光影与质感 | 光源方向、软硬、明暗/冷暖关系；接触影与投影的实际承接面；保留实物色和有依据的纹理，白色/亮面不丢细节 |
| 融合自然 | 商品与环境的透视、曝光、白平衡和清晰度协调；轮廓无剪贴白边，接触处落地；景深突出主体而不糊掉关键细节 |
| 文字可读 | 逐图弹窗确认结果；有字时写准确字符串、必要断行、位置、字族、大小/字重、字色；底板边界/内边距或羽化范围完整避开商品 |
| 输出完整 | 实际画布、比例、完整商品或有意局部取景；仅保留本图容易出错且有依据的约束 |

复核采用“已确认画面决定 → 最终正文中的具体指令”逐项对应。缺少关键指令就补回；相互冲突就解决，不靠末尾追加一串禁令。收到成图后再对照商品保真、参考继承、构图光影、融合和文字逐项修词；未生成图片时只报告提示词检查，不保证一次生成即可达到目标质量。

## 文件与就绪状态

new-set固定使用DIM01、DETAIL01、SCENE01–04、APLUS01–05，共11份；set-refresh逐一使用已确定targetAssetIds的TXT。每个文件只对应一张图；A+ 模块映射另写，不因多图模块或移动端需求静默增加文件。用户显式改变范围时再调整。

无关紧要的研究缺口不必阻断保守画面。商品身份来源或需要绘制/用于尺度判断的实物尺寸缺失时，受影响文件放入`prompts/blocked/`，开头写`CONDITIONAL DRAFT — NOT READY TO GENERATE`，列明缺项和安全替代。DIM/DETAIL默认1600×1600、桌面A+默认1464×600是已知制作值；SCENE固定1:1，像素需逐图弹窗选择或明确委托。仅未知账号资格/槽位时，继续已定画布方案，上传就绪标PROVISIONAL/待核。文案、字体、场景分配/像素未答时也保留相关依赖，不用超时/预选伪造确认。无数据时不填看似真实的数字、ASIN、证明句或文件名。

同样的阻塞规则适用于必须呈现却没有依据的材质、纹理、结构、视角或工作状态。先向用户提出具体澄清，而不是仅写BLOCKED或把“请补全真实细节”转交生成器。非必要未知主张可删去，但不能静默改变用户已经选定的图片任务。

例外仅限用户明确授权的测试规格选择：可写具体画布和暂拟图位，标明 `PROVISIONAL — TEST CANVAS; ACCOUNT UPLOAD SPECS PENDING`，不使用未解析占位符，也不借此补造商品事实。

## 每条 prompt 必须自包含

以下结构用于编写，不是可直接交付的空模板。成品文件用真实已知内容代替字段。缺事实就删除相应要求或标 blocked，不能留尖括号让用户误以为可直接执行。

```text
OUTPUT
One image: resolved width × height, aspect ratio and format.

REFERENCES AND PRODUCT
Map actual uploaded filenames to product identity and layout/style roles.
State this asset's SKU, appearance, quantity, sale scope and necessary scale.

COMPOSITION AND LIGHT
Specify the retained reference composition, background, props, camera angle,
product position, light direction and shadows. List only intended changes.
Resolve foreground/midground/background, subject scale and support, focus,
light softness and contrast, contact/cast-shadow receiving surfaces, and
faithful visible texture wherever they affect this image. Match perspective,
exposure and edge integration between the product and its surroundings.
For panels/details/dimensions, give their positions and source/endpoint mapping.
For old-set edits, identify the replacement area and the surroundings to retain.

TEXT (use only the confirmed route)
No added text or text backing; OR exact approved strings, positions, font,
size/weight and color, with the selected direct/feathered/panel treatment.
For visible text, resolve semantic line breaks, alignment and spacing;
for backing, specify panel bounds/padding or the full feathered extent.
Keep the full extent of text and effects outside the product silhouette.

ESSENTIAL LIMITS
Only this image's necessary identity, quantity, scale and accessory constraints.
```

这是编写结构，不是原样提交的模板。最终词填入具体值，只保留已选分支，去掉OR、括号选项、空字段和字段解释。输出规格是要求，验证状态写在索引。

不要写“同上一张”“沿用前面的身份锁”“参考 P03”作为唯一说明。提示词需包含可执行的事实，证据 ID 只在外部设计文档中用于追溯。选择本张实际需要的原图，不机械要求上传全部历史图片。

将竞品/图库启发写成完整执行指令，例如“左侧全貌区x=6–57%，右侧两个圆窗自上而下，标题在顶部6–15%，尺寸线在商品外沿且不穿过花叶；所有标注使用统一细线和短无衬线文字”。在Brief和layout-decisions解释已观察来源、用户选择及适配；prompt不能只说“仿照ASIN第2张”或“LIB-DIM-01”。没有目视来源时区分模板文字与原创建议。坐标、光向与区域百分比是我方设计，不是竞品实测参数。

按[参考迁移约定](reference-fidelity.md)展示源图→方案→prompt对照，记录实际附件传入状态及必要差异；源图ID本身不代表相似性通过。以版式接近为目标逐项检查：分区/窗格数量与位置、完整商品/特写的比例、标题与标注层级、阅读路线，以及全套共同的色板/边距/线条规范。相同背景和花色不足以证明排版相似；选定两圆窗就不能在prompt里变成四格。需因证据或比例调整时同步更新决策和Brief，不虚构细节填空。

## 分图注意事项

**new-set默认无MAIN**：竞品主图可以分析，但不新增我方主图prompt。set-refresh若明确包括已有主图，则按MAIN01更新并遵守对应要求，不另加主图。尺寸图和细节图也不能被误标为白底主图。

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
