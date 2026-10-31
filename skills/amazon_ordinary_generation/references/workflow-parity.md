# 植株流程对应与通用化边界

普通产品沿用植株版的完整工作流程；差别在商品事实模块、适用环境/交互、尺度核算对象和内置模板。运行时自包含，不要求另外安装或读取植株技能。维护对照基准：amazon-plant-image-strategy 1.29.1；背景文字融合的已定规则继续优先。

|植株流程|普通产品对应执行与可查结果|
|---|---|
|判新套/旧图刷新、保持范围|campaignMode、targetAssetIds、set-refresh；默认11ID，无隐增MAIN或A+模块|
|检查上传、身份与必要事实|product-profile/product-truth/product-states；按用途选择规格、内容、接触、状态；不把花叶/花器/剪茎门槛带入无关产品|
|全部竞品核身份→分区盘点→原图/原评→跨套比较|competitor-inputs.json保留全部原始链接及规范身份；每ASIN独立检查点；输入范围审计能发现少了哪一个，失败保留不冒充成功|
|初批可见参考展示并选路线，继续其他来源研究|discovery-layout；候选必须有真实画面/有序覆盖，联系表只做导航；不得首批成功后静默结束其余来源|
|具体套图/图序→继承强度→逐图映射|reference-fidelity；展示源图后用“照着做/重新布景”弹窗，分开source selection与transfer mode；不得自动structure-adapt|
|整体→局部→整体反推|complex-layout-analysis；记录分区、主体比例、道具/使用对象、图形、机位、文字、明暗与投影，不只概括卖点|
|主动场景、合适花器、支撑/插入关系|scene-props/scene-expansion/spatial-placement；换为产品—使用对象—配套物—环境适配；保留实际使用叙事，区分事实缺口与可自由选择的布景|
|按证据拓展场景/光影/角度|跨SCENE与A+对照任务、动作、构图、机位、环境和光线；在身份可见范围内选择差异，不一律前右侧+浅墙+柔光|
|多轮骨架→文字模式→文案输入→字体/文字地图|discovery-layout/scene-types/copy-typography/text-layouts；问未决项，实际答复/明确委托才确认，不把默认预选当回答|
|竞品/内置/具名混合|reference-library：200条普通商品模板与8套配方，逐ID角色分支；文字蓝图如实标text-only，不能覆盖已选竞品|
|逐图独立prompt+真实身份/参考附件|reverse-prompts/deliverables；身份图控制商品、竞品整图控制所选画面关系；附件和prompt一致，降级文字适配须有明确决定|
|正反向审查、合集编译与状态隔离|research_audit --inputs检查范围，build_prompt_summary检查附件/继承记录，人工核使用/道具/多样性/文字/尺度；脚本不证明真实看图或成图效果|

不通过减少事实要求来制造“多样性”，也不因事实未知就将所有生活用途删掉。缺口只约束依赖它的图，提出补证与可行替代供选择。维持参考继承强度时，不为凑差异破坏已选画面；源套本身重复则展示替代图/来源并让用户选择。
