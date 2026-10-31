# 项目文件与manifest约定

输出在`outputs/<product-slug>/`，同项目恢复时先读当前记录；重要修改保留revision，不覆盖用户原图。

|文件|内容|
|---|---|
|design-strategy.md|中文主文档：商品画像摘要、SKU事实与买家任务、逐竞品/跨竞品分析、三平台洞察/限制、整套叙事、每个ID完整brief；研究子文件不能替代正文分析|
|discovery.md|输入、商品画像与实际触发模块、参考路线/主套/程度及状态、实际提问与原始回答/委托范围、冲突、必需/可选缺口及依赖资产、stage/activeAssetIds/pendingQuestions/nextQuestion；不适用模块无需逐项填表|
|layout-decisions.md|逐图买家问题→有据答案→表达方式、源ASIN/变体/区段/图序→目标ID映射、保留/修改项，以及layout/sceneDetails/canvas/copyMode/copySource/fontChoice分别的状态、原答/委托、原文与最终文案、roleAdaptation理由|
|evidence-ledger.md|P/V/R/S/D/POL来源、证明范围、矛盾、限制及受影响资产|
|research/amazon/<ASIN>.md/.json|逐竞品有序视觉与评论分析、区段检查点、恢复记录|
|research/competitor-inputs.json|采集前登记全部原始链接及规范站点/ASIN；独立于成功采集结果，用于范围审计|
|research/social/<ID>.md|平台与内容类型、身份、实际观看/文字覆盖、时间戳和可迁移信息|
|research-coverage.md|画像导出的检索与候选筛选、直接竞品/替代品/纯布局参考分类、三平台尝试与结果、逐区段coverage、计数/去重/来源一致性检查；不能把受限改成完成|
|research-audit.md|离线研究检查报告或等价人工核对；不代表真实观察、覆盖完成或用户已回答|
|set-refresh-map.md|仅刷新模式：旧→新、参考→新、范围与保留/改变项|
|prompt-index.md|每图状态、需上传的确切文件/顺序、执行条件、A+模块/原生文字与平台待核项|
|prompts/<ID>.txt|每张READY/PROVISIONAL独立完整英文提示词|
|prompts/blocked/<ID>.txt|依赖缺口与条件草案，不是可执行指令|
|prompt-manifest.json|确定的范围、状态、画布、原文路径、参考角色和条件|
|all-prompts.md/.txt|从单图原文编译的两份可复制合集，BLOCKED仅列缺口，不含条件正文|

不是PDF、控制器或让Lovart自行想11张布局的总提示词。两份合集是同一组资产的额外文件视图，不增加图片数。

商品画像放在discovery.md中即可，按[画像约定](product-profile.md)选择相关字段，不为了形式再建一堆空文件。跨属性商品同时记录相关模块；未列类目由任务与属性建档，不等待新增全局分支。资产必需事实与项目希望了解的事实分开：例如未核耐水性阻塞耐水卖点图，不阻塞已有资料足够的尺寸/包装/表面图。

每图brief记录`buyerQuestion`、`supportedAnswer`、`visualMethod`，以及`requiredFacts`、`optionalFacts`和实际缺口。原图身份未足够时不能READY；已足够的事实不会因为其他模块未知被降成全套BLOCKED。角色调整只改变该ID的信息任务，不能洗掉缺口；缺口和未回答买家问题仍在策略中可见。

参考选择和设计细节按 [参考选择弹窗](discovery-layout.md#采集后的参考选择弹窗) 记录实际回答/委托。相关决定尚为proposed/pending的图只交brief或BLOCKED条件草案，列清未决项，不放入READY/PROVISIONAL可执行合集；待确认设计不能伪装成“上传条件”。用户已明确自主设计或授权代选则照其范围落实，无需重复询问。编译器不读取这些沟通记录，交付前必须另行核对，不能以脚本通过宣称弹窗已执行。

按[多轮循环](discovery-layout.md#多轮沟通循环)核对每图各决定，而非只有一列全图confirmed。文案记录按[专门问答](copy-typography.md)区分是否要字、原文/AI拟写和字体；SCENE按[场景问答](scene-types.md)保存分配、逐图像素和类型细项。原答已覆盖则直接复用，修订回答要同步下游brief与prompt；交互尚在进行时保存当前状态与下一问题，不假称整套已交付。

discovery/layout-decisions另保存referenceRoute、真实主套或ORD-SET、库版本/逐图模板、继承强度、实际观察或text-only性质，以及逐元素文字地图。证据账本按[证据链](research-evidence.md)保留评论样本分母、关键词来源/意图、买家任务/拟用主张和风险；不要只交一句“已分析竞品”。主策略正文包括逐套有序图谱、共性/差异、买家疑问与范围、选源/选图理由、整套节奏以及每张有据答案。

## manifest

下面是字段说明示例，不是可直接运行的完整11图manifest；actual数据必须填齐，不能将占位图交READY。

```json
{
  "schemaVersion": 1,
  "campaignMode": "new-set",
  "scopeOverrideReason": "",
  "targetAssetIds": ["DIM01", "DETAIL01", "SCENE01", "SCENE02", "SCENE03", "SCENE04", "APLUS01", "APLUS02", "APLUS03", "APLUS04", "APLUS05"],
  "assets": [
    {
      "id": "DIM01", "status": "READY", "file": "prompts/DIM01.txt",
      "canvas": {"width": 1600, "height": 1600},
      "references": [
        {"filename": "sku-front.jpg", "role": "identity", "path": "inputs/sku-front.jpg"},
        {"filename": "sku-dimensions.jpg", "role": "dimension", "path": "inputs/sku-dimensions.jpg"}
      ],
      "conditions": [], "gaps": [], "policyReview": "verified", "uploadReview": "not-applicable"
    }
  ]
}
```

schemaVersion=1；campaignMode为new-set/set-refresh；targetAssetIds非空、唯一、按交付顺序。new-set默认11ID，明确改范围时scopeOverrideReason记录用户决定（不能靠脚本字段自行授权）。set-refresh必须显式给出范围。

canvas为最终整图像素；非方图SCENE必须有记录用户明确变更的canvasOverrideReason。A+明确变更画布也写入决策而非标错尺寸。references按上传顺序，每条有filename（用户实际上传名）、role和path（项目内相对路径或可读绝对路径），path只供本地检查，不复制进Lovart指令。保留原图，可从现有位置引用，避免为校验盲目复制隐私资料。

READY/PROVISIONAL必须至少有一个identity引用，所有引用实际存在。PROVISIONAL必须列conditions，例如账户图位或平台核查尚待完成；**不可把未知承重/净空/材料作为“请确认后用”的PROVISIONAL事实**。BLOCKED必须列gaps，草案文件置于blocked目录，引用可以是已有的部分资料。

policyReview与uploadReview允许verified/pending/not-applicable；pending只能PROVISIONAL/BLOCKED，不能READY。没有检查平台不能填verified；verified也不表示平台已经审核通过。无需A+图位的附图可uploadReview=not-applicable。

## 编译与实际验收

### v2交付字段与参考附件检查

新项目在manifest增加`handoffVersion: 2`及全局`referenceRoute`，逐图可覆盖为competitor-derived/hybrid/library-template/original。旧项目可保留v1用于历史读取；重新交付时按实际已定路线升级，不编造历史回答。

每张竞品或含视觉来源的混合资产（READY/PROVISIONAL）增加：

```json
"visualTransfer": {
  "mode": "reference-replace",
  "delivery": "visual",
  "sourceReference": "competitor-ASIN-G02.jpg",
  "retained": ["upper complete-object view and lower two detail windows", "right window light and leftward floor shadow"]
}
```

sourceReference指向该图references中实际存在的role=layout文件，且英文prompt上传段明确同名；主源需是清晰整图，不能用联系表缩略图或身份图充数。混合项目中只用内置文字的资产将其referenceRoute写library-template；不可因全局hybrid随意塞一个无关竞品。

实际无法传源图且用户明确接受文字适配时，delivery=text-only，保留mode/retained，并写sourceLocator、reason、authorization；正文清楚说明text-only adaptation。不把缺图改称视觉复刻，也不因编译通过就认定该授权真实存在。缺必需身份/设计仍BLOCKED。

编译器检查上述字段、附件存在与正文引用；不会识别图像内容或判断保真。人工另核源图→prompt关系、使用对象/动作、道具与图形选择、可用多角度及跨图差异。研究审计须带`--inputs research/competitor-inputs.json`，否则只能核已有记录，不能发现漏掉的用户链接。

```powershell
python "<skill-root>/scripts/build_prompt_summary.py" "<project-root>/outputs/<product-slug>"
```

脚本先检查所有记录再重建两份合集；校验失败不改写旧合集。写盘期间的系统错误不属于校验保障，需修复后重新编译。读取UTF-8；单图文本保留每个字符/换行，合集外层附状态、参考顺序与条件。BLOCKED只有缺口索引。它能发现结构性不一致，不能识别编造卖点、提示词的全部矛盾、图片内容或用户是否真实授权。

人工核对manifest↔layout-decisions↔brief↔prompt的全部规格、文案、机制与数量；数值/事实逐条有P证据。覆盖不足的研究可以通过结构检查，但报告必须保留不足。未实际生图时只报告规划与静态校验通过；实际保真、文字渲染、平台接收仍未验证。
