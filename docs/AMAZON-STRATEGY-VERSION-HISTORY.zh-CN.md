# Amazon植株图片策略：中文版本沿革与Git注释索引

整理日期：2026-10-29。技能版本仍为v1.29.0；本文件整理历史，不新增技能功能版本。

已核对Git历史、历史ZIP、冻结入口快照、版本署名维护报告与行为案例。从v1.1.0到v1.29.0共29个主线版本，另找到6个实际补丁版本，共35条记录。并非35份独立完整源码，也并非35条历史提交。未找到足以单独确认v1.8.1变更的资料；不根据版本号推测其内容，其他仅出现在示例/未来计划中的版本不列为已发布。

现有9条相关Git提交承载这些累计改动；更早f6487f4为另一个Lovart单图技能，未把策略v1.1–1.8倒填到该提交。v1.1–1.9归属首个纳入策略技能的9d469e6，v1.10–1.20归属3693b83，v1.21–1.23归属543c666，v1.28与1.29归属0683ead；此归属不是各版发布日期。

中文注释使用`refs/notes/commits`，不改写既有提交。查看：`git log --show-notes=commits`；单条查看：`git notes show 提交号`。Notes不是原始commit message的一部分，普通clone/push通常不会自动携带此引用；本轮仅本地写入，未推送远端或强推。维护证据位于outputs/dist的部分文件不随普通源码克隆，已在本索引记录摘要和证据范围。

|版本|对应累计提交|证据范围|中文变更摘要|
|---|---|---|---|
|v1.1.0|`9d469e6`|归档包可核对；首个纳入Git的累计版本为1.9.0|固定为尺寸1张、细节1张、场景4张及A+5张，共11张附图/A+；从原始产品资料与3–6竞品启动，增加竞品并行浏览、独立布局与光影分析，不新增MAIN。|
|v1.2.0|`9d469e6`|归档包可核对；没有独立Git版本提交|研究按身份、图库/A+盘点、目视与评论采样分轮执行；新增逐ASIN JSON检查点、研究记录规范及离线审计，明确失败恢复、覆盖口径和续跑。|
|v1.3.0|`9d469e6`|维护记录；非独立源码快照|新增本地优秀套图研究、场景/场合扩展与美术指导；把构图、配色、字体和光影迁移接入策略、Brief及独立提示词。|
|v1.3.1|`9d469e6`|维护记录；非独立源码快照|按花卉、盆栽、树木、花环等商品分支推导场景与支撑，避免圣诞花环案例成为全部品类默认；区分策略技能与另行授权生图。|
|v1.4.0|`9d469e6`|维护记录；非独立源码快照|增加实物尺度/投影比例与画幅占比的分离检查、参照物和算术助手；强调四场景任务差异、商品免受字效遮挡，以及制作画布与账户槽位分开。|
|v1.5.0|`9d469e6`|维护记录与行为案例；非独立源码快照|增加整套有序图谱、逐图版式弹窗与选择记录；接入便携参考库，并从独立TXT编译Markdown/TXT合集，保持原文一致及BLOCKED隔离。|
|v1.6.0|`9d469e6`|版本署名维护报告|强化图文融合与字体规则；接入可选变体图库采集manifest，保存来源/变体/图序；建立Agent内部知识索引、去重与项目内增量积累，移除翻译服务依赖。|
|v1.6.1|`9d469e6`|版本署名维护报告；历史测试结果不代表本轮重跑|修复观察覆盖、透明度去重、导入前语义校验、JSON逐文件原子写入、坏manifest兼容及像素别名丢失关联；增加真实故障回归并校正提示词附件和布局一致性。|
|v1.7.0|`9d469e6`|版本署名维护报告|新增approved-only收录门槛、受限参考默认隐藏、布局家族查询和便携快照刷新；对新增图库筛选并保留拒绝原因，审核未过图片字节不进入可复用库。|
|v1.8.0|`9d469e6`|版本署名行为案例；无法据此证明真实页面全部执行通过|加强A+来源与主要产品身份识别；保留模块出现位置、原生文字和图像分支；同布局/品牌/父ASIN不再授权合并不同产品模板。|
|v1.8.2|`9d469e6`|有入口快照；补丁精确变更边界未恢复|确认存在1.8.2入口快照，包含A+产品模板、整套布局选择、内部图库/集成文字等当时规则；缺少1.8.0→1.8.1→1.8.2逐补丁完整对照，不能独断各项首次引入版本。|
|v1.9.0|`9d469e6`|独立Git源码快照及发布候选记录|发布精选便携库：保留290条文字模板、735条历史图像记录、46配方及6套有序系列入口，提供110张已审核成图；按实际安装目录检索，保留缺口和附件真实性。|
|v1.10.0|`3693b83`|归档/维护记录；累计纳入1.20.0提交|增加完整图库构建器、不可变manifest、轻量索引与逐图详细记录；默认搜索677条已审核文字/61源系列，离线精选不再限制完整文字检索，媒体发布范围单独控制。|
|v1.11.0|`3693b83`|冻结快照与发布候选记录；累计纳入1.20.0提交|增加远程HTTPS索引同步与指定记录/预览/原图按需获取、独立哈希缓存、凭据来源隔离、撤回过滤及断网回退；私有测试不等于真实云账号接入或公开stable发布。|
|v1.12.0|`3693b83`|维护行为案例；非独立Git快照|增加散枝入容器分段尺度与剪裁状态核算；明确多产品/多颜色、每容器分配和一包总数，不复制整包或将替代用途当同时陈列。|
|v1.13.0|`3693b83`|维护行为案例；非独立Git快照|增加商品事实和可见细节门槛；材料名、竞品和设计委托不补足缺失纹理/结构/视角，及时追问或请求最小补图，只阻塞相关资产，并迁移旧模板事实规则。|
|v1.14.0|`3693b83`|维护记录；非独立Git快照|竞品视觉研究后选择新竞品反推、内置或混合路线，并绑定具体套图/逐图来源；适用短标题主动落实展示字，保护商品，避免默认回退库模板。|
|v1.15.0|`3693b83`|版本署名检查记录；非独立Git快照|新增基础文案输入/真实空白/AI生成/无字区分、Apple等字体菜单与层级；询问4类场景张数和逐图方图像素，四宫格/步骤/对比与A+画布分别处理。|
|v1.16.0|`3693b83`|维护记录；非独立Git快照|新增24条室外文字方向并接入检索、场景问答和提示词适配；按本品使用范围筛选室外场景，不把文字模板当已观察成图或性能证据。|
|v1.17.0|`3693b83`|维护记录；非独立Git快照|细化保义、自然英文、版面适配三遍编辑；增加分图类篇幅、8种文字布局和逐元素文字地图，保持准确文案/断行/区域/层级贯通到prompt。|
|v1.18.0|`3693b83`|维护记录；后续1.28–1.29已增加完整继承例外|默认单图字族统一；增加具体竞品套图选择、逐图迁移与实际风格附件交接；区分实拍密度、展示数量和售卖数量，保留协调底板/彩色文字。|
|v1.19.0|`3693b83`|维护记录；非独立Git快照|逐场景选择字色/底板与非随货花器，不再默认同一棕白配色/玻璃瓶；增加跨容器口沿以上高度、露茎、主体与容器关系的对照核算。|
|v1.20.0|`3693b83`|独立Git源码快照|增加已审核来源套图及逐图入口，扩展A+主要产品组与离线原图；允许适配的5张A+均为室外，仍核对实际暴露、支撑、数量与来源图位。|
|v1.21.0|`543c666`|维护记录；累计纳入1.23.0提交|按用户三类目录维护138张保留图，修复移图引用、不恢复已删图；为14张尺寸/细节源图分别编写DIM与DETAIL角色分支，排除维护标注资源。|
|v1.21.1|`543c666`|维护记录；后续修复关系明确|对活动库作大幅精简与分支去重，正文集中到图像记录并清理无配图入口；此版的缺图统一删除策略后被1.21.2纠正，不能只描述为无风险清理。|
|v1.21.2|`543c666`|维护记录；累计纳入1.23.0提交|纠正缺图统一删除：恢复并重写193条误删卡片及独立布局/A+分支，保留200个独立任务；集中维护具体任务与准入，合格文字模板不必强绑图片。|
|v1.22.0|`543c666`|维护记录；累计纳入1.23.0提交|增加set-refresh：盘点旧成图、按明确目标资产清单更新，支持范围内MAIN；区分局部编辑/布局重建，旧图细节不足及时补图，并扩展合集脚本的范围/顺序校验。|
|v1.23.0|`543c666`|独立Git源码快照|增加文字节制、局部羽化与竞品画面继承规则；允许保留画面只替换真实商品及有依据文案/配色，应用于尺寸、细节、场景和A+，需实际参考附件。|
|v1.24.0|`0b24d2e`|独立Git源码快照|逐图落实是否有字、少量标题或必要标注，未回答与真实空白/委托分开；精简生图正文与代理流程内容，同时保留关键产品、布局、光影和文字约束。|
|v1.24.1|`302f73e`|独立Git源码快照|将提示词优化目标改为质量与可控性优先，不以字数压缩为成功；复杂场景/尺寸/参考替换保留独立控制信息，无字也不等于省略空间光影。|
|v1.25.0|`ffc339a`|独立Git源码快照；1.26.0继续泛化|新增复杂版式分析参考，覆盖曲线分区、空间/图层归属与表现字体，将观察关系落实为具体prompt并接入入口与文字/参考迁移流程。|
|v1.26.0|`d04b26a`|独立Git源码快照|将视觉结构分析泛化为元素、归属、几何、对齐、嵌套、重复、跨区、层级、空间支撑与文字关系；按真实复杂度展开，不预设曲线或某类场景配方。|
|v1.27.0|`42effcb`|独立Git源码快照|联合检查目标市场住宅/远景、产品—场景、容器—场景、产品—容器；容纳算术之外增加轮廓、口部过渡、露茎和视觉重量判断，保留固定容器身份。|
|v1.28.0|`0683ead`|维护记录与本会话改动；与1.29.0合并提交|旧套图默认大幅重建；增加完整画面替换与排版结构适配两种继承强度，拆分商品来源/新设计来源/实际底图；解决字体/底板默认冲突，限制茶壶等非常规花器，并做旧→新和来源→方案双重检查。|
|v1.29.0|`0683ead`|独立Git源码快照；当前发布技能版本|完整继承也默认允许有限设计自由度：调整未锁定道具花器颜色、适度改变有素材支持的机位、少量装饰增添/类似替换；保留主要布局、空间关系、层级与光影，明确选定结果而非交给模型随机发挥。|

## 逐版本依据

- **v1.1.0**：dist/amazon-plant-image-strategy-v1.1.0.zip；与v1.0.0入口差异。
- **v1.2.0**：dist/amazon-plant-image-strategy-v1.2.0.zip；与v1.1.0入口差异；docs/AMAZON-STRATEGY.zh-CN.md。
- **v1.3.0**：docs/AMAZON-STRATEGY.zh-CN.md；references/reference-study.md。
- **v1.3.1**：docs/AMAZON-STRATEGY.zh-CN.md。
- **v1.4.0**：docs/AMAZON-STRATEGY.zh-CN.md；outputs/skill-v140-check/。
- **v1.5.0**：docs/AMAZON-STRATEGY.zh-CN.md；outputs/skill-v150-check/；skills/amazon-plant-image-strategy/evaluation/CASES.md。
- **v1.6.0**：outputs/library-maintenance-20261019/summary.md；skills/amazon-plant-image-strategy/evaluation/CASES.md。
- **v1.6.1**：outputs/skill-robustness-20261019/report.md。
- **v1.7.0**：outputs/library-update-20261020/library-update-report.md。
- **v1.8.0**：skills/amazon-plant-image-strategy/evaluation/CASES.md（1.8.0章节）。
- **v1.8.2**：outputs/portable-library-20261022/before/SKILL.md。
- **v1.9.0**：outputs/portable-library-20261022/release-notes.zh-CN.md；Git tag v1.9.0。
- **v1.10.0**：outputs/library-v1.10.0-20261022/release-notes.zh-CN.md；before/skill/为1.9.0。
- **v1.11.0**：outputs/library-v1.11.0-20261022/release-notes.zh-CN.md；release-snapshot/amazon-plant-image-strategy/SKILL.md。
- **v1.12.0**：skills/amazon-plant-image-strategy/evaluation/CASES.md（1.12.0章节）。
- **v1.13.0**：skills/amazon-plant-image-strategy/evaluation/CASES.md（1.13.0章节）。
- **v1.14.0**：skills/amazon-plant-image-strategy/evaluation/CASES.md（1.14.0章节）；outputs/skill-maintenance-20261023/lettering-text-review.json。
- **v1.15.0**：outputs/skill-v1150-check/validation.md；skills/amazon-plant-image-strategy/evaluation/CASES.md。
- **v1.16.0**：docs/AMAZON-STRATEGY.zh-CN.md；outputs/outdoor-update/validation.md。
- **v1.17.0**：docs/AMAZON-STRATEGY.zh-CN.md；outputs/typography-v1170/validation.md。
- **v1.18.0**：docs/AMAZON-STRATEGY.zh-CN.md；outputs/skill-v1180-check/validation.md。
- **v1.19.0**：docs/AMAZON-STRATEGY.zh-CN.md；outputs/skill-v1190-check/validation.md。
- **v1.20.0**：docs/AMAZON-STRATEGY.zh-CN.md；Git tag v1.20.0。
- **v1.21.0**：docs/AMAZON-STRATEGY.zh-CN.md；skills/amazon-plant-image-strategy/evaluation/CASES.md。
- **v1.21.1**：docs/AMAZON-STRATEGY.zh-CN.md。
- **v1.21.2**：docs/AMAZON-STRATEGY.zh-CN.md。
- **v1.22.0**：docs/AMAZON-STRATEGY.zh-CN.md；references/set-refresh.md。
- **v1.23.0**：skills/amazon-plant-image-strategy/evaluation/CASES.md（v1.23.0章节）；Git提交入口版本。
- **v1.24.0**：skills/amazon-plant-image-strategy/evaluation/CASES.md（v1.24.0章节）；该提交代码差异。
- **v1.24.1**：skills/amazon-plant-image-strategy/evaluation/CASES.md（v1.24.1章节）；该提交代码差异。
- **v1.25.0**：Git ffc339a 的complex-layout-analysis.md及相关差异。
- **v1.26.0**：skills/amazon-plant-image-strategy/evaluation/CASES.md（v1.26.0章节）；该提交代码差异。
- **v1.27.0**：skills/amazon-plant-image-strategy/evaluation/CASES.md（v1.27.0章节）；该提交代码差异。
- **v1.28.0**：docs/AMAZON-STRATEGY.zh-CN.md；skills/amazon-plant-image-strategy/evaluation/CASES.md（v1.28.0章节）。
- **v1.29.0**：docs/AMAZON-STRATEGY.zh-CN.md；skills/amazon-plant-image-strategy/evaluation/CASES.md（v1.29.0章节）。

本轮仅检查版本与注释映射、历史保持、包内容一致性；没有重跑每个历史版本的测试，也不宣称过去所有行为案例均实跑。
