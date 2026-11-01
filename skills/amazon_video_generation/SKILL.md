---
name: amazon-video-generation
description: "Plan Jimeng showcase videos for Amazon products across categories, from product photos or selected image campaigns. Direct scenes, camera paths, mechanisms, human interactions and prop continuity; retain dedicated flower and foliage workflows. Deliver only C01/C02 folders with self-contained Chinese draft prompts and all upload images, plus an analysis Markdown, README and shot CSV. Each segment has at most nine upload images; storyboard pages have fixed 3x3 slots and tables use ten director columns. Upload images are preferably square, at least 350 px high, with width/height between 0.6 and 1.6. Reuse selected images and generate missing storyboard states when needed. Does not submit or generate videos automatically."
metadata:
  version: "6.5.0"
---

# Amazon Video Generation

面向各类Amazon商品的视频前期策划与即梦交接。花卉是最初使用场景，不是主产品范围限制。用户上传详细分镜表、带格下说明的宫格故事板、精选产品图，并复制本段提示词生成视频。本技能策划、补必要预演帧、排版及检查，不自动提交即梦或付费生成视频；仅修改技能时不为未知SKU生图。

## 通用主流程与专用路线

所有商品先读[通用商品工作流](references/product-video-workflow.md)，按实际用途、形态、结构、材质、可动部件和交互任务选镜；编镜必读[物理空间与实体连续性](references/physical-continuity.md)及[商品与镜头保真](references/reference-and-shot-fidelity.md)。先保留商品结构、镜头展示目标与已选运动，再增加动态描述；逐张排除身份/场景/状态图冲突，不能仅凭“以主图为准”放行错误图。默认15–30秒、16:9，按信息量/已核入口调整，旧项目已明确约定优先。

- **general 通用商品**：家具、宠物用品、电子、家居器具、穿戴、包装及其他商品均可进入；未列类目直接按任务分析。不硬套插花、环绕、固定场景数或植物模板。使用`--profile general`检查。
- **flowers 花卉**：鲜切/干花/仿真花枝、花束、固定插花追加[花卉整片工作流](references/flower-showcase-workflow.md)与[花卉动态导演](references/dynamic-flower-direction.md)。保留用户已选F07、优先25–30秒综合主线和动作偏好，仅在本分支应用。
- **foliage 草木**：绿植、盆栽、树/圣诞树追加[草木路线](references/foliage-video-workflow.md)，保留展示、整形、安装和灯效，不强加花卉插入动作。花盆/容器为售卖主角时按该SKU任务进入general。

接受实际选定的最终套图、产品原图或部分素材。可承接`amazon-ordinary-generation`或`amazon-plant-image-strategy`，但计划/提示词不等于成图已存在；不要求启动前重新做11张，也不把资产数当作镜头数。同SKU多角度/状态绑定同一物件，不从竞品继承结构与功能。

## 干净场景与三维动态演绎

商品实拍仅提取身份/结构，默认重建干净用途场景或按配色选[文字展台库](references/display-background-library.md)，不沿用杂乱实拍背景；用户明确选定的干净最终场景可复用。尺寸展示优先洁白影棚/白色无缝空间，保持轮廓、承重与尺度，不让白底抹掉白色商品边缘。

生活场景优先一个与用途相关的细微画内事件，并写可见响应：如动物自然抬头/眨眼、手指按键带来相应屏幕变化、柔性部分随轻风微动。按已选主体及材质设计，不硬塞人物/动物，不让刚性商品为动而动；固定机位也可真实，单纯静图横移不作为生活场景默认。编镜时读[三维场景演绎](references/volumetric-scene-direction.md)：把参考图展开为空间、可达机位路径、可见面/遮挡变化与连续事件；整图平移缩放、景深模糊或分层视差不能独自冒充三维动态。人物动作与物体响应写清触发、进行及暂停后的状态；光影只按真实驱动改变。多机位按信息需要选用，不强制每镜移动或为未知侧面补造结构。

## 按决定推进的弹窗

通常3–4轮，每轮1–3个关键问题；已有答案或委托复用，不凑轮数：

1. 确认SKU与最终素材、售卖内容、用途/卖点，以及会影响拍摄的结构/连接/尺寸缺口。
2. 给具体时间线，比较两种有意义侧重，明确镜头和生成任务的区别；不要求用户从零写导演脚本。
3. 确认场景空间、人物范围、要展示的真实动作和关键道具；检查相机可达范围、同一部件的动作与连接、握持/遮挡/落位。通用商品不默认三次动作。
4. 展示实际表图与宫格，按稳定S-ID修改，同步TXT、CSV和README附件映射。

用可用的异步文本弹窗；未答/关闭/预选不算同意。缺商品事实时只暂停依赖该事实的镜头，其他工作继续。图片上传在普通对话请求，不用文本弹窗收图片。素材/决定/缺口合并到分析说明书，不额外产生过程文档。

## 身份、空间与动作的通用约束

从本SKU参考确认关键实体身份、数量、固定/可动关系与允许变化。每镜分开写相机路径、主体/部件动作、环境响应；相机位移不是主体自转。固定的是世界中的结构与落点，透视投影随视角合理变化：斜视梯形不必然是错误；正面读形节点须明确机位条件。角落环绕先检查相机是否会穿墙或暴露无参考的面，再决定可达弧段或匹配剪辑。

操作明确初态→接触/支撑→移动→结果，同一个活动件持续保持身份及真实连接。道具也需管理：柔性绳/带允许弯曲与松垂，但已核端点、环、扣具与归属不能凭空变化。遮挡后的再现是同一物件；真正切分/倒出/装入等已核变化按动作记录，不能机械禁止一切数量变化。

复杂接触优先清楚、稳定的观察机位，减少无信息价值的同时动作。细节镜保留必要的邻接/连接参照、清楚的起终构图和可读停留；不为写孔壁/视差丢失原有定位信息。补图只覆盖必要角度/状态，生成预演不证明隐藏结构。无论提示词多详细，静态起终图正确都不代表中间视频物理一致；按[连续性验收](references/physical-continuity.md)检查实际过程，失败时简化具体事件/补参考/调整机位或切镜。

涉及装配/布置、中间态、多场景或手持细节时，读[终态倒推与真实运动](references/terminal-state-and-motion.md)：先确定完成态，按真实可操作关系倒推基础态及步骤，逐对检查新增组件与落位是否足以得到下一态，再正向展示；多场景写清空间证据，主体/柔性部分/投影按真实驱动联动；可手持件优先小幅转看，触摸或弯折以材料依据为限。

## 研究说明与执行内容分开

按[整段提示词与交接](references/full-film-prompt.md)编写。研究来源、模板代号、原片禁用元素、未试听声明、平台/文件规则属于agent和用户的说明，留在分析说明书/README。**最终TXT、上传分镜表文字、宫格简述只含当前SKU、实际上传素材及本段画面/声音要求**；不把未上传底层模板作为模型已知上下文。

参考片可按[六维逆推库](references/reverse-video-prompts.md)提炼拍法；该库是内部研究资料，T04/T05等花卉模块不自动套给其他商品。新研究及适用边界见[通用商品研究记录](references/research/2026-11-01-general-product-video.md)。优先具体正向动作，必要的本项目限制仍可保留，不用无关黑名单或全局禁词替代商品事实。

S-ID表示镜头，C-ID表示生成任务；一个C-ID可含多个镜头/场景。每段独立说明身份、附件、动作、节奏、切镜、文案和声音，不写“同上”或让用户拼词。秒段是导演预算，复杂动作按事件顺序与相对节奏表达，不承诺模型精确按时点执行。

用户2026-10-31说明的入口是Seedance 2.0 Mini/全能参考/单次15秒。可用设置按实际入口核实，不从更贵型号、API或源片标题推定。优先整片，超实际上限才拆前后两段；两段仍容不下时弹窗决定，不默默增段。保留轻音乐、无旁白与简短英文文案的已选偏好，具体项目可改。**两次独立生成相同音乐词连同旋律也不能保证**；每段写自足风格目标，同一连续音轨的后期方案留在说明书，不假定模型记得前段，不默认新增音频交付。

## 花卉专用偏好

仅flowers默认：相机环绕→空间尺寸→1–2个动态细节→多次插花/整理摆放→2–3个动态生活场景→成品收尾。可选相机空间绕行/尺寸线、真实售卖分组悬浮或已核可调整结构；固定成品不擅自拆枝。逐次插入默认3次落位松手，先从选定完成态倒推三次补入及基础花材，不等于空瓶插三枝就结束；或先手中整理再成束1次插入，二选一记录。花材随真实操作累积，不将“身份一致”写成每帧排列冻结。

选择展示台时读[背景库](references/display-background-library.md)，按商品配色适配室内/室外环境，产品保色；模板背景中的花材/品牌/数量不继承为SKU事实。BG代号和此迁移说明仅供策划；最终执行内容写实际选择的空间与配色。通用商品优先看库中的BG12–BG18几何展台及WHITE01白棚；BG01–BG11保留为花卉/活动布景文字分支。库内参考图已转为文字，原图可从v6.1.0标签恢复，不作为执行依赖。

## 固定交付与检查

读[精简分镜输出规范](references/flower-storyboard-package.md)。最终仅交`C01/`、需要第二段时的`C02/`、`分析说明书.md`、`README.md`、`shot-list.csv`。每段目录平铺`C01.draft.txt`或`C02.draft.txt`及该段全部详细表PNG、宫格PNG和精选上传图；单段不建空C02。draft是固定文件名，实际齐备状态在README说明。其余总提示词、分镜MD、JSON清单、HTML、音频文件或其他交付均不默认生成，必要中间数据放内存或交付目录外临时区。

所有上传图片（含表、宫格、产品/细节/场景/锚帧）解码并处理EXIF方向后的高度≥350px，`0.6≤宽÷高≤1.6`含边界，优先1:1；这是用户交付约束，不冒称平台普遍规则。视频和格内画面仍可16:9。表/板通过重排、分页和留白达标，不压扁商品或缩成不可读小字。实际图片编辑/补帧按imagegen工作流且使用已查看的本SKU参考；不以画布放大声称低清细节已恢复。

每C-ID全部上传图片合计最多9张（表页、宫格页、产品/场景/锚帧等全部计入），先预算再补图，TXT不占图片数。每张宫格固定3×3九槽，按顺序填充，只有前页填满9槽才开下一页；末页空槽无假图片或假镜号。一格的一个状态不等于一镜，也不单独计作上传文件。详细表固定十列：时间、镜头编号、景别、摄像机角度与运动、画面内容、演员动作、产品展示重点、台词/旁白、音效/音乐、字幕。

两类PNG同源生成；S-ID全片稳定，分页/分段不重编号，同镜多状态为S05/start、S05/key、S05/end，对应同一表行。宫格每格下方有本镜状态简述，详细表的执行信息完整可读。PNG实际产出并逐页查看；表/格说明不是成片字幕。

通用运镜按需查[运镜库](references/camera-movement-library.md)和[机位覆盖](references/multi-angle-coverage.md)，只借工具，不恢复其中植物/旧时长默认。每个卖点须有本SKU依据；植物可另查[证据例库](references/claims-and-evidence.md)，AI画面不能替代商品事实或测试。

运行`python3 scripts/check_camera_plan.py shot-list.csv --profile general --max-generation-seconds 15 --strict`；flowers显式改为`--profile flowers --flower-format F07`，草木用foliage，实际入口更长时才改上限。另运行`python3 scripts/check_delivery_package.py 交付目录`检查层级与所有上传图。脚本不核实商品真实性、几何/道具连续性或音乐匹配，不代替实际视频验收。

修改技能后运行技能校验及受影响测试，源码与`.agents/skills/amazon-video-generation`同步；每次可见版本独立本地提交、中文说明并加版本标签。
