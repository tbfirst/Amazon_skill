# 有文案图片：融入真实背景

仅适用于已确定有图内文案的图片；不改变是否加字、准确文案、字体选择与用户已明确的授权。无字图保持无字，A+ native-only仍交原生字段。本规则覆盖模板或参考中默认继承文字底板的约定；用户明确要求保留某个底板/信息分区时按其范围保留，不重复询问已确定的偏好。

## 默认排版

`text_surface: natural-background`、`backplate: NONE`。标题、辅助句和标签优先直接排在同一真实场景的安静背景中，例如墙面、天空或桌面留白。保持材质纹理、空间纵深、原有光照与投影连续，不另划纯色半幅、底部横条、悬浮卡片、磨砂块或白雾层专门承载文案。维持参考的阅读顺序、字体层级与对齐关系，源图有底板不等于目标必须沿用；将“源底板→同位置自然背景落字”等适配写入brief。四宫格、步骤窗等任务本身需要的画面分区仍可保留，不把这些分区误当文字底板删除。

可读性不足依次尝试：移动文字到更安静的真实背景、压缩获准可编辑的文案、调整换行/字重/字号/字色，再微调有依据的构图和背景曝光。保持必要事实及锁定词句。不要自动用大色板或全图白雾补救；确需独立文字面板或局部羽化时，先说明原因并取得用户该项选择，已明确授权的具体例外不重问。

## 光影融合与产品保护

字色与背景局部亮度、环境冷暖协调，保留清楚对比。默认是清晰的平面排字，不把“融合”误读成把文案印到产品上、制造实体招牌或给文字强加立体投影。若选择极轻的字影/细描边，明确其范围、颜色、强度及与场景主光的一致性，不用粗发光、厚描边或模糊底层割裂背景。只有用户选择实体墙字/招牌时才使用相应表面透视和真实投影，不能扭曲普通文字造成难读。

完整主产品轮廓及适当缓冲区是禁入区，包含花叶/枝梢/花瓣、盆器、附件、开合部件与关键操作点。文字、字影、长笔画、引线、装饰和所有效果边缘均不得压住产品，也不得擦除、虚化、降透明度或改变产品尺度来腾位置。商品接触影和关键结构须保持可辨。必要尺寸线放在外围，端点指向测量对象，不横穿商品。

## 每图交付与检查

brief及独立英文prompt明确：准确文案和换行、文字区域坐标、字体/字号/字重/字色、实际背景材质与光向、产品保护范围；`backplate: NONE`时不再填写底板圆角/填充等矛盾要求。有例外则记录用户决定及适用ID。

可采用以下执行句，再加入本图唯一的具体参数，不把它当成完整prompt：

“Place the exact copy directly in the quiet negative space of the continuous photographed background. Preserve the background texture, depth, lighting and existing shadows. No separate text panel, banner, card, frosted patch or white veil. Keep all lettering, flourishes and text effects outside the complete product silhouette and its clearance area. Use legible flat typography with colors coordinated to the local background; do not print the added copy on the product.”

审查参考→brief→prompt是否一致，排除继承模板中遗留的底板、羽化与强投影指令；检查全套有字图是否默认融合、是否保护完整商品。生成前只称提示词检查；实际出图后才核验遮挡、文字可读性、纹理和光影连续性。
