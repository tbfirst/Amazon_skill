---
name: amazon-video-generation
description: "Turn final Amazon flower image campaigns or product photos into 15–30 second Jimeng showcase packages through iterative popup direction. Deliver a complete Chinese film prompt, analysis manual, captioned grid storyboard PNG and matching detailed shot table PNG for Jimeng upload, plus MD/CSV, and selected upload references. Reuse final images and generate missing storyboard states. Prefer whole-film generation; split into two connected parts when the selected model requires it. Also retain foliage display, assembly and lighting planning. Does not submit or generate videos automatically."
metadata:
  version: "5.4.0"
---

# Amazon Video Generation

把最终商品套图转为可执行的视频展示方案。用户把详细分镜表图片、带格下说明的宫格故事板图片、完整或分段提示词及精选产品图提交即梦生成视频；本技能完成前期策划、必要分镜补图、排版和交接。仅研究或修改本技能时不为未知商品自动生图。

## 方向与入口

- **花卉 flowers**：鲜切、干花、仿真花枝、花束、固定插花。先读[花卉整片工作流](references/flower-showcase-workflow.md)，默认F07综合展示，25–30秒，允许15–30秒按信息量调整，16:9。新流程优先于旧花卉项目中的F01、固定5秒开场、一镜一生成及无故事板约定。
- **草木 foliage**：绿植、盆栽、树、圣诞树。继续用[草木路线](references/foliage-video-workflow.md)，保留展示、整形、安装和灯效能力；不强行迁移花卉的摄影偏好；新项目共用下述四项核心交付与编号规则。按该路线读取素材承接、分镜、输出和交付参考。
- 旧项目按已明确约定继续，用户要求迁移时再改；不恢复弃用素材或覆盖旧交付。

花卉优先承接 `amazon-plant-image-strategy` 规划后**实际生成、精修并选定的11张最终图片**及同SKU事实。图片策略本身交付提示词，不等于成图已经存在。用户可在Codex用这些提示词完成生图/精修；视频阶段只读取实际选定版本，不能仅据提示词假称已看11张成品。也接受产品原图或部分最终图，不要求为启动视频重新制作11张。11张资产不是11个视频镜头，精选少量承担身份、细节、尺寸和场景职责。

## 花卉多轮弹窗

通常3–4轮，每轮1–3个关键问题，已有答案/委托直接复用：

1. 素材与卖点：确认SKU、最终文件版本、真实售卖内容及影响镜头的事实缺口。
2. 结构与模块：展示具体时间线，比较同一综合主线下的两种侧重；选择空间展示模块和时长，不重新要求用户从零决定主线。
3. 场景、人物与动作：按商品配色选择室内/室外展示台、后续用途、人物范围；插花默认3次，或采用先在手中整理成束再一次插入，明确容器起态、构图和转场。
4. 分镜预览微调：展示实际画面分镜板与详细分镜表，按稳定S-ID修改，并同步提示词和上传清单。

使用可用的异步文本弹窗；每次选择影响下一轮。未答、关闭或预选不算同意；与答案无关的素材盘点可继续。上传图片在普通对话请求，不能让文本弹窗收图片。不为流程凑轮数，也不把总风格选择当成所有具体镜头已确认。

用户已选默认：**相机环绕→空间尺寸→1–2个动态细节卖点→多次插花/整理摆放→2–3个动态生活场景→成品收尾**。三种空间模块均可选：相机空间绕行与尺寸线、售卖花枝/套装分组悬浮、真实可调整结构。跨场以匹配构图和运动方向的剪辑为主，必要时遮挡转场。默认简短英文卖点、准确尺寸标注、轻音乐、无旁白；文字先在即梦生成，出错提供后期修正方案。具体商品不适用的模块须说明替代，不硬造结构。

分镜与写词必读[花卉动态导演规则](references/dynamic-flower-direction.md)：环绕时花器和花卉整体在空间中固定，背景随相机位移产生真实透视与视差；尺寸段同样用相机空间绕行，不让主体自转。细节用适合材质的微风、轻抚等连续响应；逐次插花默认3次可辨认的插入—落位—松手，容器可预先已有部分花材；也可选“手中整理部分花材→成束一次插入→落位松手”的完整替代。多色/多花型按实际售卖组合累积。每个场景必须有真实相机位移或画内事件，禁止以静图缩放轮播代替生活展示。

选择开场展示台时读[背景参考与提示词库](references/display-background-library.md)：内置11张用户参考对应的布景卡及室外衍生方案，按产品配色适配环境、不改变商品颜色。以用户最终产品图为身份依据，用图像工具放入合适主位，前几秒相机环绕，再接尺寸、细节、插花及其他场景；已有合适成图可复用。参考中的异种花材、品牌和陈列数量不继承为SKU内容。

## 整片提示词与实际入口

借鉴用户两段参考片时读[六维逆推与模板库](references/reverse-video-prompts.md)：内含两片完整逐镜英文复现建议和可替换SKU的适配模板。原片时间码、人物、材质、动作和音轨核实程度属于研究记录；现行花卉规则优先，不能迁移玩具折叠/机洗、恢复主体自转或把原片混合花材当本SKU。英文库用于分析与学习，项目最终仍交完整中文即梦执行词；原片的镜头数与总长不决定生成任务数或本片时长。

读[整片提示词与即梦交接](references/full-film-prompt.md)。S-ID表示镜头，C-ID表示一次生成任务；**一个C-ID可以包含多个镜头和多个场景**。主提示词写全片顺序、节奏、运镜、动作、切镜、字和声音，不再只给散落的逐镜短词。

本次用户入口是 **Seedance 2.0 Mini / 全能参考 / 单次15秒**，来源为用户2026-10-31说明。优先一份完整脚本，目标超过实际时长时分前后两段，分别给自足执行词、局部时间线、对应详细分镜表PNG和宫格故事板PNG及素材映射，明确接缝。允许用户在提示词成熟后选更贵的Seedance 2.5；单次可用时长/参考数量/声音能力仍按实际入口核实，不能从模型名或参考片标题推定。不要把30秒总脚本标成Mini可直接一次运行，也不要无理由退回每镜一个任务。

## 画面、事实与交付

读[分镜板与输出包](references/flower-storyboard-package.md)。四项核心交付为：①足够详细且可上传即梦的分镜表PNG（另附MD/CSV）；②每格下方有简短中文说明的宫格故事板PNG；③自足的整段或分段中文提示词TXT；④中文分析说明书。另附精选产品图与有序上传清单。分段时每个C-ID各有表、板、执行词和产品图映射。两类PNG从同一份镜头数据生成；S-ID全片稳定，分页/分段不重编号，同镜多格以S05/start、S05/key、S05/end对应同一表行。格下说明和表内导演信息不作为成片字幕。PNG必须实际产出并查看，不用文字表或空框代替画面分镜板。

优先复用最终套图；缺少的动作起止或角度画面按 `imagegen` 技能，用内置图像工具和实际产品参考补成，再排版。生成图是预演，不新增商品事实；角度推断标明，隐藏结构/尺寸缺失要补事实，不能用生图“证明”。程序可排版、加编号和文字，不能以色块或手绘假商品冒充真实画面。不自动建网站/编辑器，不提交即梦或自动付费生成视频。

卖点查[证据规范](references/claims-and-evidence.md)；运镜按需查[运镜库](references/camera-movement-library.md)和[机位覆盖](references/multi-angle-coverage.md)。每镜分别写相机移动、主体动作、环境响应及空间视差，给起中终状态、主路径与稳定读图时间。花器固定指世界坐标中的落点和朝向，不是冻结屏幕中的透视；真实摆放/整理动作另行描述。花枝布局可因真实操作改变，身份、花型、颜色、数量与售卖内容须一致。固定成品不擅自拆成散枝，不从竞品继承功能。

实际镜头起止、附件顺序、表行与格下编号/状态说明、字幕、TXT与清单版本一致；插删镜头保留已有S-ID，以顺序字段控制播放次序。详细执行信息须在上传表图可读，不能仅藏在MD/CSV。按[分镜板与输出包](references/flower-storyboard-package.md)的同源排版命令生成两类图片，并按实际上传缩放检查可读性。静态分镜验收、提示词齐备、视频生成、动态验收与发布是不同状态。参考片的逐帧序列结论见[双参考研究](references/research/2026-10-31-two-reference-showcase.md)；它提炼拍法，不证明模型成功率或销售效果。

CSV运镜与时长检查：`python scripts/check_camera_plan.py shot-list.csv --profile flowers --flower-format F07 --max-generation-seconds 15 --strict`；仅在实际选定入口支持更长时填写相应上限。此脚本不核实模型能力、不检查商品真伪，也不代替时间轴/画面验收。修改技能后运行技能校验及受影响脚本测试，源码与`.agents/skills/amazon-video-generation`安装副本同步。
