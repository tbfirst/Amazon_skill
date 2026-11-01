# 外部模板提取与商品事实适配

当用户给提示词仓库、参考skill或要求提取方法时使用。先阅读实际原文，记录仓库/文件/模板ID/案例ID及固定版本；只提取解决当前视频问题的结构。模板是写词方法来源，既不证明商品事实，也不等于已观察到竞品视频。

## 已筛选的来源

仓库：[freestylefly/awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2)，核对日期2026-10-27；本次固定提交 `63e6176fa01be51c000108dacd72716d3e46784b`。读取其SKILL、结构化模板/案例索引和模板正文后，选用以下概念作我方改写。未安装其skill、运行其代码、下载示例图库或验证其生成效果。

- [外部SKILL](https://github.com/freestylefly/awesome-gpt-image-2/blob/63e6176fa01be51c000108dacd72716d3e46784b/agents/skills/gpt-image-2-style-library/SKILL.md)：按任务、风格、场景筛选，再读案例原文；字段是内部检查线索，不要求用户另选固定数量方案。
- [结构化模板索引](https://github.com/freestylefly/awesome-gpt-image-2/blob/63e6176fa01be51c000108dacd72716d3e46784b/data/style-library.json)：保留精确ID和适用条件，不能只按标签或封面继承默认案例。
- 相关源文件哈希：`data/style-library.json`、`data/cases.json`、`docs/templates.md`可在具体项目的来源记录保存；不要求后续每次重新下载整个库。

| 来源模板/案例 | 只提取的组织方法 | 转成植物商品视频 |
| --- | --- | --- |
| [product-commerce-visual](https://github.com/freestylefly/awesome-gpt-image-2/blob/63e6176fa01be51c000108dacd72716d3e46784b/docs/templates.md#tpl-product) | 主商品、环境与辅助物分层 | 每镜有商品主信息，道具不抢主体、不暗示随货；删价格贴、促销icon和静态版块 |
| [realistic-photography](https://github.com/freestylefly/awesome-gpt-image-2/blob/63e6176fa01be51c000108dacd72716d3e46784b/docs/templates.md#tpl-photo) | 机位、光、质感分别说明 | 操作段让接触清楚，氛围段再柔化背景；表面只写我方资料可见内容，不堆虚构材质或污渍 |
| [scene-storytelling](https://github.com/freestylefly/awesome-gpt-image-2/blob/63e6176fa01be51c000108dacd72716d3e46784b/docs/templates.md#tpl-scene)与[character-design-sheet](https://github.com/freestylefly/awesome-gpt-image-2/blob/63e6176fa01be51c000108dacd72716d3e46784b/docs/templates.md#tpl-character) | 场所/事件明确，身份约束前置 | 人脸/服装锚点改为枝形、颜色、连接、容器/底座与比例；不要求生成角色表、多视图或动作宫格 |
| [案例519](https://github.com/freestylefly/awesome-gpt-image-2/blob/63e6176fa01be51c000108dacd72716d3e46784b/data/cases.json#L620)、[案例342](https://github.com/freestylefly/awesome-gpt-image-2/blob/63e6176fa01be51c000108dacd72716d3e46784b/data/cases.json#L4513) | 商品身份先于场景变化 | 保持同SKU固有特征，场景用切镜更换；不照搬品牌、颜色、2×2网格或产品重设计 |
| [案例419](https://github.com/freestylefly/awesome-gpt-image-2/blob/63e6176fa01be51c000108dacd72716d3e46784b/data/cases.json#L2830)、[案例422](https://github.com/freestylefly/awesome-gpt-image-2/blob/63e6176fa01be51c000108dacd72716d3e46784b/data/cases.json#L2762) | 关键事件有序推进，先列共享环境锚点 | 面板关系改为起始→接触/动作→结果→下一镜；同场容器/桌面/光向连续，不继承格数、时长、题材与运镜清单 |
| [案例487](https://github.com/freestylefly/awesome-gpt-image-2/blob/63e6176fa01be51c000108dacd72716d3e46784b/data/cases.json#L1313) | 整片调性、商品锁与声音方向分层 | 音乐服务过程和结尾，已知接触音不抢主体；不搬护肤功效、人物要求、品牌或固定镜头规格。其商业片式文案不证明实际视频存在 |

以上均为转述与改写，不把整段原提示词、图库、原品牌/音乐装入我方执行包。仓库署名与MIT许可见 [第三方许可](third-party/awesome-gpt-image-2-LICENSE.txt)；案例原发布者信息以源索引记录为准，不宣称仓库许可已验证所有社区媒体权利。

## 先适配事实，再适配拍法

1. **保留当前约定**：用途、时长、色款、真实步骤、单次/分段与字音选择不被模板默认覆盖。模板缺字段不妨碍现有方案；空材质/参数/品牌不能靠模板填造。
2. **分清固定、可变、未知**：固定SKU颜色/分叉结构/数量/连接/比例等；可变项仅经确认的整理姿态、手动作、相机或切场；未知部位仍标缺口。整理会改变枝条姿态，不能同时要求整形前后每根枝条的位置完全不变；结构与身份不能随之增减。
3. **写小型空间锚点**：同场只记影响连续性的台面/落点、花瓶或底座、线缆/盒体、主光相对方向。镜头可近可远，物理比例和支撑不能跟着重置。新场景明确切换，不强制额外制作地图或空间板。
4. **把静态面板变成时间事件**：删除格数、边框、表头、箭头、左上/右下和均分时长指令；按本片操作可读性重排。按方向与约30秒预算分配事件；花卉F01保留5秒环绕、连续插花与整理完成态，默认一镜一任务，单次≤15秒并交代跨段接续；输出详细文字分镜表，不生成故事板、不逐镜提交视频或自动裁格作为首帧。
5. **按信息控制摄影**：操作镜让手与接触处都清楚，避免过浅景深/运动模糊遮住动作；氛围镜可有克制背景虚化。词中的光色是提案，不从模板推出我方照度、材质或户外能力。

内部可用“任务与商品依据→参考角色→固定/可变/未知→空间与事件时序→光色/字音→结尾/检查”组织，四条中文提示词分别按自然叙事写全并重复相关身份/场景锁，不向用户交一堆需要自行拼装的槽位或外部模板ID。

## 适配结果与验收

需要留来源时在项目 `template-adaptation.md` 写：`版本/模板或案例ID → 提取概念 → 我方事实/适用SKU → 具体S-ID及改写 → 舍弃项/缺口`。它是解释记录，不是第二条执行提示词；README解释其用途。轻量任务可合并到既有brief/研究文件，不强制新增文件。

检查总词、分镜、参考包和说明一致；未知内部、多角度或变体信息没有被静态模板补成事实；固定数量/分屏/示例品牌/产品重设计没有漏进正文。原参考图与已确认事实优先于品牌气质；不照搬“产品服从品牌环境”等会改写实物的要求。

本技能的竞品研究继续按 [实际视频风格流程](video-style-analysis.md) 进行。模板提取不能替代那项研究，也不新增自动安装、付费、生图、提交或发布步骤。
