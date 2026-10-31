# 可观察的反推与独立Lovart提示词

有图内文案时先执行 [背景融合规则](background-copy.md)：默认在真实背景留白直接排字；下文继承底板、羽化或独立信息面的规则仅用于用户明确选择的例外。保留图像任务所需的分区及文字层级，不自动为文字新增背景层。

先按[参考来源路线](reference-library.md)和[继承强度](reference-fidelity.md)落实竞品/内置/混合以及具体逐图分支，再按[参考改造](reference-redesign.md)区分观察与设计。内置文本不是源图观察，不能把模板原样当成可执行prompt。按已选来源保留有效结构并展开确定的局部改动，不强制重做成功构图。

## 从参考到可执行方向

先读 [空间摆放](spatial-placement.md) 与 [场景和道具](scene-props.md)。每个选中来源建一条观察卡：URL/ASIN/变体/图片顺序或视频时间戳、实际查看方式、画布比例、任务、区块坐标、视图/窗口数量与形状、产品覆盖、机位/透视、背景/道具、文字分层、配色、光与影、层级/阅读顺序。不可辨部分写unknown，不凭缩略图猜小字或材质。

按[通用视觉结构分析](complex-layout-analysis.md)检查元素角色、区域归属、边界交接、图层遮挡与对齐关系，再返回整体核阅读顺序。分析深度随图复杂度变化，观察到的数值和我方布局目标分开；不能只写物件包围框而丢失区域之间的关系。图内有字时，按[文字地图](text-layouts.md)逐元素指定准确字符串、语义断行、区域、字形/字号/字重、行距/对齐、颜色、强调和保护区。

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
3. [actual selected competitor full-image filename, required for visual competitor-derived work]: layout reference controlling the selected composition, setting, props/interaction relationships, camera, typography hierarchy and lighting at the resolved transfer strength. Do not transfer its product identity, brand, claims or measurements.

PRODUCT IDENTITY AND SALE CONTENT
[Exact SKU appearance, relevant form/material/pattern/label or parts, sale unit, included contents/accessories, unchanged markings, supported state and restrictions.]

LAYOUT BLUEPRINT
[One resolved composition: regions in normalized coordinates, margins/gutters, main view, detail-window count/shapes, scale, reading order, background and whitespace. Explain exact retained and changed source features.]

REFERENCE ADAPTATION — RETAIN AND CHANGE
[Name the observed source composition, spatial setting, hierarchy and lighting to retain. Replace the source product with the exact target SKU. Specify only the selected bounded changes to viewpoint, subordinate props, copy and palette; preserve successful layout relationships rather than inventing a new composition. Remove source branding and unsupported claims.]

PHYSICAL SCALE AND ACTION
[Applicable dimensions/specifications and measurement state; relevant scale basis, support/contact, material deformation, fit/connection or action; sale quantity, contents and prop boundaries. Omit inapplicable mechanisms.]
SPATIAL PLACEMENT
[Support plane, product orientation relative to walls/table edges, camera viewpoint independently of product rotation, coherent horizon/vanishing relationships, clearance, contact points, scale basis and prop fit. Use the applicable resolved spatial blueprint.]

USE, PROPS AND GRAPHIC ACCENTS
[This asset's resolved use subject and supported pose/action; compatible physical props with position, scale and sale role; selected subordinate graphic motif with bounds/style/color, or none as deliberately chosen. Do not let no-added-text erase a selected graphic, or apply no-people/no-props across unrelated assets.]

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

策划核查与生成正文分开。来源研究、用户问答、选择理由、证据ID、状态和“先检查/先询问/等待”等工作流留在brief/索引；执行正文只写本图唯一画面、实际附件、构图、事实、光影和准确文字。不要同时保留“全部机位道具不变”和本图已定的机位/道具调整。无字只省文字层，不压缩掉复杂场景需要的信息；没有容纳/穿戴/接口就不加入对应通用禁令。

## Consistency pass

核对画布/比例在decisions、brief、manifest、prompt一致；主次区域+间距不超画布；参考文件和上传顺序一致；只选择一个确定结构，不混入“方案A或B”。图片要求与提示词冲突时先解决，再交付。

先对“实际参考→用户选择/委托→逐图决定→具体指令与附件”逐项正向核对，再反查每条指令的本品证据或设计依据；骨架、图层、尺度/数量、光向/受影面、材质、文字地图和销售边界都在链中。内置模板的角色分支不代替该图问答与事实核实。未答选择不得通过PROVISIONAL进入可执行合集。

本SKU事实、参考构图、文字锁与图像模型的能力分开：缺失视角不能靠negative prompt补齐，静态校验不能证明生成图已保持结构。用户回传生成图后才能做实际结构/比例/文字/版式QA，修改时保留原版和明确的新revision。

竞品路线不允许把“source provenance: ASIN/G02”当唯一迁移指令，再说“no competitor image required”。完整源图必须在本图上传顺序和manifest.references中，role=layout，并在正文说明控制哪些关系。实际身份图/细节图不能代替布局图。缺原图则先补采；确需文字适配时按reference-fidelity记录并披露已选降级，不宣称视觉替换。

无字仅省文字层；不要顺手加no icons/no decorations/no interaction等未选限制。身份锁只约束商品本身与有据状态，不能将同一机位、同一房间、相同光向或无使用对象误写成产品身份。最终反查所选用途、布景、图形、机位与明暗是否都进入正文，不能只写禁止项而遗漏正向画面指令。
