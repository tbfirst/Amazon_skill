# 可观察的反推与独立Lovart提示词

先按[参考反推与设计改造](reference-redesign.md)区分源图分析与新设计。反推准确性与改造充分性分别审查，不交只换商品、其余照搬的生产提示词。

## 从参考到可执行方向

每个选中来源建一条观察卡：URL/ASIN/变体/图片顺序或视频时间戳、实际查看方式、画布比例、任务、区块坐标、视图/窗口数量与形状、产品覆盖、机位/透视、背景/道具、文字分层、配色、光与影、层级/阅读顺序。不可辨部分写unknown，不凭缩略图猜小字或材质。

另写迁移卡：retained、replaced、removed、adapted、why。结构保留和新品真实适配可以并存，但必须具体解释差异：例如参考是多尺寸横表，本品只有一尺寸，因此保留上方测量示意与下方信息区，改成一个有证据的选择卡，不能复制六列虚构SKU。

跨类目来源只有布局/表达关系可迁移，按本图买家问题判断是否合适：同为“看清销售内容”的平铺结构可借鉴，但餐具件数不转为文具件数；服装叠放不要求刚性商品弯曲；电器的发光特效不能用于证明普通容器的保温。保留原图布局不等于照搬其物理行为、商品事实或固定背景。先解决这些差异，再写一条确定方向。

把观察与提案分开。视频只取支持静态任务的关键帧或相邻状态：记录真实timestamp；组步骤图须逐步有证据。没有关键帧只读过文字时，可生成“由文字启发的原创布局提案”，不能号称忠实重建原镜头。

反推不保证知道作者的原始提示词，不复制品牌标志、人物身份、私有照片、未经证实的评论/徽章或数据表。参考图作为layout输入时只控制已列结构；本品图作为identity输入只控制商品，避免竞品轮廓和功能串入。

## 提示词块

以下为编写结构，不是已完成的可复制成品。每张必须把变量替换为实际已解决内容；缺必需事实放blocked而非交模板。

```text
ASSET / OUTPUT
Create one [role] image, [width] × [height] px, [ratio], for [marketplace and task].

REFERENCE INPUTS — UPLOAD IN THIS ORDER
1. [exact filename]: identity reference; preserve [visible SKU attributes].
2. [exact filename]: dimension/detail/state evidence for [specific part].
3. [exact filename if used]: layout only; retain [named relationships]. Do not transfer its product, brand, claims or measurements.

PRODUCT IDENTITY AND SALE CONTENT
[Exact SKU appearance, relevant form/material/pattern/label or parts, sale unit, included contents/accessories, unchanged markings, supported state and restrictions.]

LAYOUT BLUEPRINT
[One resolved composition: regions in normalized coordinates, margins/gutters, main view, detail-window count/shapes, scale, reading order, background and whitespace. Explain exact retained and changed source features.]

REFERENCE-INSPIRED REDESIGN
[Name the useful information relationships retained, then specify the exact new composition, palette, typography, camera, setting or subordinate props used where appropriate. Remove source-specific brand expression and copied advertising text. Keep the target product identity unchanged. Do not merely replace the source product.]

PHYSICAL SCALE AND ACTION
[Applicable dimensions/specifications and measurement state; relevant scale basis, support/contact, material deformation, fit/connection or action; sale quantity, contents and prop boundaries. Omit inapplicable mechanisms.]

CAMERA, MATERIAL AND LIGHT
[Evidence-supported angle, perspective, visible details, realistic material response, key-light direction/softness, contact/cast shadows and depth.]

EXACT VISIBLE COPY AND TYPE
[Every approved string verbatim, line breaks, text zone, type style, size/weight, alignment, color and background treatment; or explicitly no added text.]

PRODUCT PROTECTION AND FINAL CHECK
[Do not alter the actual structure, fit, count, color, markings or supported mechanism. Keep text/effects clear of the complete silhouette and critical joints. List this asset's concrete failure points and required output.]
```

需要字体时给出字体或明确风格与fallback，不谎称字体文件已加载。精确文字不能只写“add a strong headline”；无字与native-only不残留“add labels”。DIM采用尺寸线时每条需轴、端点、测量状态、数字、单位；采用确认的其他规格表达时写精确数据与含义，不加虚构尺寸线；不可让生成器重新计算。多个状态/视图明确是同一SKU，不表示多件装。

身份锁按形态表达：刚性商品锁轮廓/厚度/零件位置；柔性商品锁版型/缝线/图案/材料与有据形变，而非要求平铺轮廓在穿戴时完全不变；包装商品锁可见标签/规格，不推造内容物。no-added-text不能抹去商品原有标签，也不能把看不清的标签交给模型自由补字。若拟近拍的关键印字缺清晰来源，只阻塞该特写或改用可辨视角。

独立性不等于整份技能复制11遍：每张包含与本图有关的全部约束即可。省略无关分支，保留影响画面质量的光影、尺度、材料、布局和文案细节，不为缩短提示词丢掉决定。

## Consistency pass

核对画布/比例在decisions、brief、manifest、prompt一致；主次区域+间距不超画布；参考文件和上传顺序一致；只选择一个确定结构，不混入“方案A或B”。图片要求与提示词冲突时先解决，再交付。

本SKU事实、参考构图、文字锁与图像模型的能力分开：缺失视角不能靠negative prompt补齐，静态校验不能证明生成图已保持结构。用户回传生成图后才能做实际结构/比例/文字/版式QA，修改时保留原版和明确的新revision。
