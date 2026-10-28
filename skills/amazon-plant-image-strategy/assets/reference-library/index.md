# 内置植物设计参考库

234个卡片入口，143条图像记录，138个内置成图参考。配图只提供版式或指定视觉效果；导入不等于逐图目视或Lovart实测。

供agent按需读取，无需用户翻译。完整卡片/图像用 `scripts/library_catalog.py show ID` 读取；模板质量与配图可用性分别记录；无内置图的已审核文字模板仍可使用，不声称本轮看过缺失图片。

原库快照SHA-256：`9bb0ab1f939a65963be10f6ea2ca75cbfeac2a60813d386d7aebf61e6cc42a28`。

## 按交付角色检索

| 分类 | 本地图片 | 用途 | 检索参数 |
|---|---|---|---|
| A+图 | 64 | APLUS | `--design-group aplus` |
| 尺寸与细节设计图 | 14 | DIM01 / DETAIL01 | `--design-group dimensions-details` |
| 场景图 | 60 | SCENE | `--design-group scenes` |

尺寸与细节共用版式池；`show IMG-ID --asset-role DIM01/DETAIL01`读取独立适配分支。分类不合并A+产品身份；仍按具体图片核对内容和来源。

| ID | 名称 | 图类 | 内置预览 |
|---|---|---|---|
| QUAL-09 | 花环门板近景 · 枝叶硬投影 | 场景图 | [预览1](previews/assets/collected/09-door-wreath.png) |
| QUAL-26 | 上下场景拼版 · 中间文案带 | A+图 | [预览1](previews/assets/collected/26-two-scene-panel.png) |
| DIM-01 | 白底尺寸 · 全貌＋双圆形细节 | 尺寸图 | [预览1](previews/assets/dimensions/01-white-two-circles.png) |
| DIM-02 | 白底尺寸 · 正视＋俯视＋单花三视图 | 尺寸图 | [预览1](previews/assets/dimensions/02-three-views.png) |
| DIM-03 | 暖米色尺寸 · 主束＋多色套装分栏 | 尺寸图 | [预览1](previews/assets/dimensions/03-warm-assortment.png) |
| DIM-04 | 白底尺寸 · 全貌＋三圆形结构细节 | 尺寸图 | [预览1](previews/assets/dimensions/08-white-three-circles-yellow.png) |
| DIM-05 | 深绿弧形尺寸 · 主束＋圆窗卖点 | 尺寸图 | [预览1](previews/assets/dimensions/05-dark-green-curve.png) |
| DIM-06 | 绿色分栏尺寸 · 主束＋三格矩形细节 | 尺寸图 | [预览1](previews/assets/dimensions/06-green-detail-panels.png) |
| DIM-07 | 橙色尺寸 · 单束测量＋手持整包 | 尺寸图 | [预览1](previews/assets/dimensions/07-orange-handheld-pack.png) |
| SETREF-B07ZCBVV19-G02 | 门廊四盆纵深 | 场景图 | [预览1](previews/assets/collected/6bc344ab57d2809dc6cd70468d8c35201697bfe03a122068df5ac8fb0ea7aa24.jpg) |
| SETREF-B07ZCBVV19-G03 | 窗边前后双瓶与顶部标题 | 场景图 | [预览1](previews/assets/collected/5bab4f4015af2e8cfe65d5e7338a4b2ffcb246afd76920dff7b112312d802222.jpg) |
| SETREF-B07ZCBVV19-G04 | 木桶花簇近景 | 细节图 | [预览1](previews/assets/collected/a157d5e5805c3ec6cbd137ba43065a6d8bc21cd0c7c2b4c296abd993c79cdaac.jpg) |
| SETREF-B07ZCBVV19-G06 | 台阶三盆三角构图 | 场景图 | [预览1](previews/assets/collected/acd8f482f2f0a6b5436eb85fc545f051859a6a0a1522808ba9db179515705dfa.jpg) |
| SETREF-B0D5HKDBDN-G06 | 左主枝右四圆细节 | 细节图 | [预览1](previews/assets/dimensions/0a38211f36ce7abd152096bf163028813217812f6b1544288142dd9670c3d7df.jpg) |
| SETREF-B0FNBSD73T-G02 | 灯树高度与右侧功能栏 | 尺寸图 | [预览1](previews/assets/collected/6cfbd1d2e5227f254f177c5b031415a91aa6d15b88eb9d4e041216b5b36f0988.jpg) |
| SETREF-B0FNBSD73T-G03 | 同机位日夜对照与操作窗 | 对比图 | [预览1](previews/assets/collected/bb00ace05e86e194d4071b6ba6be650626ada1540c0bf5e7fda2bcbad05a3ecf.jpg) |
| SETREF-B0FNBSD73T-G04 | 主灯树与四级状态圆窗 | 对比图 | [预览1](previews/assets/collected/b3a56f67ef258d8e72e00bae396282882fea8ab8233614bd0ee30c5df3a67572.jpg) |
| SETREF-B0FNBSD73T-G06 | 室外蓝调夜景与功能板 | 场景图 | [预览1](previews/assets/collected/a98d64d46c3226e6e4bc1c33774ff7e8dd55a858f4d8ccbf02171f2e3bbdf212.jpg) |
| SETREF-B0GCN4M8ZB-G02 | 色块标题加三圆尺寸细节 | 尺寸图 | [预览1](previews/assets/dimensions/083d6b1ba0096f674c460c040ceb9c3e2dc36669c76796563a40ccd44b209620.jpg) |
| SETREF-B0GCN4M8ZB-G03 | 灰木墙白窗箱近景 | 场景图 | [预览1](previews/assets/collected/1d823fe99cb881a395c3a804e81aed6788214226d1e1af9ddb78098ab116a256.jpg) |
| SETREF-B0GCN4M8ZB-G06 | 风化木栏长箱纵深 | 场景图 | [预览1](previews/assets/collected/5abcd7125f0a9b2ee67e5b80fcb271838fa69fb13aac5ed57da096e510fd3d29.jpg) |
| SETREF-B0GCN4M8ZB-G07 | 黑双门前左右对称盆 | 场景图 | [预览1](previews/assets/collected/c2bf7287ba170fb0fc56c2c3618d2cbb9527bb53b746634c7f4d775e205d14f7.jpg) |
| SETREF-B0DP8JBCC1-G02 | 右完整枝左三圆与弧形分割 | 尺寸图 | [预览1](previews/assets/dimensions/acbc3c7ae7753d65eeccdbbcc14b8a079ec3c7326bcfc76f7991621b8bb93524.jpg) |
| SETREF-B0DP8JBCC1-G03 | 四景用途加中央单枝圆窗 | 场景图 | [预览1](previews/assets/collected/18d6a1bc0a626ec21076a99d83a66a126d1a06e95ab5843ca9b636dabf89af07.jpg) |
| SETREF-B0DP8JBCC1-G04 | 整栋白房前双盆 | 场景图 | [预览1](previews/assets/collected/6efc99400f4f093969bfabefb14395d09b5fd5cff89247fa7dfb5095940f30e0.jpg) |
| SETREF-B0DP8JBCC1-G08 | 砖墙白百叶窗箱 | 场景图 | [预览1](previews/assets/collected/1c33b81be09eaa6868ca89f0a522b694a16c0745f2a07e7284bf083a4303d744.jpg) |
| SETREF-B0H2VDTZYT-G06 | 四组配色数量清单 | 数量图 | [预览1](previews/assets/dimensions/32df8834d5f8b0dc6dca6e1c3efeb2f29a510699f75f35eda943b5c96a0715a8.jpg) |
| SETREF-B0H2VDTZYT-G07 | 右整枝左双矩形尺寸 | 尺寸图 | [预览1](previews/assets/dimensions/2b3aaf42b5723a5104e3167d5ad3e8e50f13fd19427bc2d8b0b8a6015eeb412e.jpg) |
| SETREF-B0H2VDTZYT-G08 | 四格近拍配底部色条 | 细节图 | [预览1](previews/assets/collected/8df86ba93fd33b8e3261f6dbfd4f115d1c2997f983fab6085038e48d64298ccf.jpg) |
| SETREF-B0H2VDTZYT-G09 | 白扶手前单盆与南瓜 | 场景图 | [预览1](previews/assets/collected/07a5f71b27007e695c398c6c78f397fdf735b2eede12a93eb345b5ae8daba210.jpg) |
| SETREF-B0H5J4K825-G03 | 上方数量与下方扇形清单 | 数量图 | [预览1](previews/assets/dimensions/aed9ad2c4f825159ef266cb1fcee88a6d05e3a569ae704afcaf4701f43ac1ab4.jpg) |
| SETREF-B0H5J4K825-G04 | 大场景加底部四细节 | 细节图 | [预览1](previews/assets/collected/d1d7aca4b0f730f4ad7c43cc65309ac05db1069230159ba807ffd45ed83f7bb9.jpg) |
| SETREF-B0H5J4K825-G05 | 白栏金秋长花箱 | 场景图 | [预览1](previews/assets/collected/335f75081805f6d91f136c0450cebaa67d4b8778596c21a935b71504e8e921eb.jpg) |
| SETREF-B0H5J4K825-G06 | 单吊篮与铁艺支架 | 场景图 | [预览1](previews/assets/collected/10bf1ac26aae5b7d8cd541961324aa00e1c782e9a53dfdc66cb5a159077da749.jpg) |
| KEEP-01 | 通用保真底句 | 通用优化 | 无内置图；文字模板可用 |
| KEEP-02 | 只改背景，保留商品视角 | 通用优化 | 无内置图；文字模板可用 |
| KEEP-03 | 只改善摄影，不升级商品 | 通用优化 | 无内置图；文字模板可用 |
| KEEP-04 | 以原图恢复走样 | 通用优化 | 无内置图；文字模板可用 |
| FRAME-01 | 端正正面视角 | 通用优化 | 无内置图；文字模板可用 |
| FRAME-02 | 轻微俯视且保留盆身 | 通用优化 | 无内置图；文字模板可用 |
| FRAME-06 | 商品拍近一点 | 通用优化 | 无内置图；文字模板可用 |
| FRAME-07 | 稍拉远，保留使用环境 | 通用优化 | 无内置图；文字模板可用 |
| FRAME-08 | 完整植株居中 | 通用优化 | 无内置图；文字模板可用 |
| FRAME-09 | 主体偏左，右侧留白 | 通用优化 | 无内置图；文字模板可用 |
| FRAME-10 | 主体偏右，左侧留白 | 通用优化 | 无内置图；文字模板可用 |
| FRAME-11 | 自然中等背景虚化 | 通用优化 | 无内置图；文字模板可用 |
| FRAME-12 | 纠正广角拉伸 | 通用优化 | 无内置图；文字模板可用 |
| FRAME-13 | 只扩背景，不延长植物 | 通用优化 | 无内置图；文字模板可用 |
| FRAME-14 | 花箱正面清楚，上口少量可见 | 通用优化 | 无内置图；文字模板可用 |
| FUSION-01 | 商品植株融入花箱场景 | 场景图 | 无内置图；文字模板可用 |
| FUSION-02 | 商品植株融入道具花盆 | 场景图 | 无内置图；文字模板可用 |
| FUSION-03 | 商品与吊篮自然融合 | 场景图 | 无内置图；文字模板可用 |
| FUSION-04 | 长花箱融合 · 保留实际枝量 | 场景图 | 无内置图；文字模板可用 |
| FUSION-05 | 完整盆栽融入住宅场景 | 场景图 | 无内置图；文字模板可用 |
| FUSION-06 | 裸枝花束放入道具花瓶 | 场景图 | 无内置图；文字模板可用 |
| FUSION-07 | 保留随货内盆的套盆展示 | 场景图 | 无内置图；文字模板可用 |
| FUSION-09 | 商品与住宅环境尺度匹配 | 场景图 | 无内置图；文字模板可用 |
| FUSION-10 | 左右双摆位住宅场景 | 场景图 | 无内置图；文字模板可用 |
| FUSION-11 | 固定住宅布局 · 只替换内容物 | 场景图 | 无内置图；文字模板可用 |
| DETAIL-01 | 花瓣真实近景 | 细节图 | 无内置图；文字模板可用 |
| DETAIL-02 | 叶脉与叶面细节 | 细节图 | 无内置图；文字模板可用 |
| DETAIL-03 | 枝杆连接特写 | 细节图 | 无内置图；文字模板可用 |
| DETAIL-04 | 花盆外部纹理 | 细节图 | 无内置图；文字模板可用 |
| DETAIL-05 | 吊篮绳索与挂点 | 细节图 | 无内置图；文字模板可用 |
| DETAIL-06 | 三格真实细节拼版 | 细节图 | 无内置图；文字模板可用 |
| DETAIL-07 | 全貌＋两处特写 | 细节图 | 无内置图；文字模板可用 |
| DETAIL-08 | 低清细节只做有限改善 | 细节图 | 无内置图；文字模板可用 |
| MAIN-01 | 完整带盆商品白底 | 白底图 | 无内置图；文字模板可用 |
| MAIN-02 | 裸枝 / 花束无道具主图 | 白底图 | 无内置图；文字模板可用 |
| MAIN-03 | 主图完整度修复 | 白底图 | 无内置图；文字模板可用 |
| MAIN-05 | 主图颜色与实拍一致 | 白底图 | 无内置图；文字模板可用 |
| MAIN-06 | 主图保持真实数量 | 白底图 | 无内置图；文字模板可用 |
| INFO-01 | 真实尺寸信息图 | 尺寸图 | 无内置图；文字模板可用 |
| INFO-02 | 尺寸＋真实细节 | 尺寸+细节图 | 无内置图；文字模板可用 |
| INFO-03 | 卖点图：已有英文原文 | 卖点图 | 无内置图；文字模板可用 |
| INFO-04 | 中文需求指导无字卖点底图 | 卖点图 | 无内置图；文字模板可用 |
| INFO-05 | 已有无字底图添加文字 | 卖点图 | 无内置图；文字模板可用 |
| INFO-06 | A+ 无字场景横幅 | A+图 | 无内置图；文字模板可用 |
| INFO-07 | A+ 全貌＋结构特写 | A+图 | 无内置图；文字模板可用 |
| INFO-08 | 移动端文字可读性修正 | 通用优化 | 无内置图；文字模板可用 |
| ASSET-01 | 真实透明抠图 | 中间素材 | 无内置图；文字模板可用 |
| ASSET-02 | 清空花箱并移除旧影 | 中间素材 | 无内置图；文字模板可用 |
| ASSET-03 | 去除原图非商品背景 | 中间素材 | 无内置图；文字模板可用 |
| ASSET-04 | 清理背景杂物 | 中间素材 | 无内置图；文字模板可用 |
| ASSET-05 | 保留干净场景待合成 | 中间素材 | 无内置图；文字模板可用 |
| LIVE-01 | 保持实际苗龄 / 成熟度 | 通用优化 | 无内置图；文字模板可用 |
| LIVE-02 | 保持真实自然差异 | 通用优化 | 无内置图；文字模板可用 |
| LIVE-03 | 真实交付状态展示 | 包装图 | 无内置图；文字模板可用 |
| LIVE-04 | 养护图不猜资料 | 养护图 | 无内置图；文字模板可用 |
| ART-01 | 保留仿真材料外观 | 通用优化 | 无内置图；文字模板可用 |
| ART-02 | 枝叶展开但数量不变 | 通用优化 | 无内置图；文字模板可用 |
| ART-03 | 保留真实轻微工艺差异 | 通用优化 | 无内置图；文字模板可用 |
| ART-04 | 不凭外观加耐晒防水 | 通用优化 | 无内置图；文字模板可用 |
| LIGHT-01 | 中性自然日光 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-02 | 左前方柔和侧光 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-03 | 右前方柔和侧光 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-04 | 接近正面的均匀柔光 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-05 | 侧面光增加层次 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-06 | 逆光加正面补光 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-07 | 小幅增加边缘分离 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-08 | 明亮窗边漫射光 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-09 | 增强日照，保留高光细节 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-10 | 去掉过暖光影 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-11 | 去掉过冷蓝灰色调 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-12 | 提亮暗部但不变灰 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-13 | 压回过曝白花 / 浅盆 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-14 | 叶片适度光泽 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-15 | 织物花瓣柔和质感 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-16 | 哑光盆表面 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-17 | 釉面盆克制反射 | 场景图 | 无内置图；文字模板可用 |
| LIGHT-18 | 商品与场景曝光匹配 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-01 | 盆底轻接触阴影 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-02 | 重接触，轻远端 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-03 | 柔和短投影 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-04 | 柔和长投影 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-05 | 清晰日光投影 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-06 | 叶片投影落在墙上 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-07 | 叶片投影落在盆身 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-08 | 同一光向统一投影 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-09 | 远离墙面，影子稍柔 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-10 | 降低阴影浓度 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-11 | 提高阴影存在感 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-12 | 去掉双重阴影 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-13 | 清除旧植物投影 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-14 | 阴天低对比阴影 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-15 | 窗框光影一致 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-16 | 吊篮墙影与承重一致 | 场景图 | 无内置图；文字模板可用 |
| SHADOW-17 | 花瓶口内部遮光 | 场景图 | 无内置图；文字模板可用 |
| RATIO-02 | 约 2:1 · 温和立体感 | 场景图 | 无内置图；文字模板可用 |
| RATIO-05 | 明亮商品＋克制背景 | 场景图 | 无内置图；文字模板可用 |
| RATIO-06 | 硬边＋低反差 | 场景图 | 无内置图；文字模板可用 |
| FIX-01 | 修白边与杂色 | 通用优化 | 无内置图；文字模板可用 |
| FIX-02 | 修重复叶片 / 花朵 | 通用优化 | 无内置图；文字模板可用 |
| FIX-03 | 修断枝与连接 | 通用优化 | 无内置图；文字模板可用 |
| FIX-04 | 修盆口穿模 | 通用优化 | 无内置图；文字模板可用 |
| FIX-05 | 修悬浮盆底 | 通用优化 | 无内置图；文字模板可用 |
| FIX-06 | 修局部过曝 | 通用优化 | 无内置图；文字模板可用 |
| FIX-07 | 修局部过暗 | 通用优化 | 无内置图；文字模板可用 |
| FIX-08 | 修局部文字错字 | 通用优化 | 无内置图；文字模板可用 |
| FIX-09 | 修尺寸数字 / 单位 | 尺寸图 | 无内置图；文字模板可用 |
| FIX-10 | 修局部色偏 | 通用优化 | 无内置图；文字模板可用 |
| FIX-11 | 修锐化光晕 | 通用优化 | 无内置图；文字模板可用 |
| FIX-12 | 修抹平 / 蜡感 | 通用优化 | 无内置图；文字模板可用 |
| FIX-13 | 只让道具盆变新 | 通用优化 | 无内置图；文字模板可用 |
| FIX-14 | 只让道具盆矮一点 | 通用优化 | 无内置图；文字模板可用 |
| SCENE-01 | 真实美式客厅 | 场景图 | 无内置图；文字模板可用 |
| SCENE-02 | 真实乡村住宅 | 场景图 | 无内置图；文字模板可用 |
| SCENE-03 | 地中海浅石墙 | 场景图 | 无内置图；文字模板可用 |
| SCENE-04 | 真实入户玄关 | 场景图 | 无内置图；文字模板可用 |
| SCENE-05 | 窗边小盆栽 | 场景图 | 无内置图；文字模板可用 |
| SCENE-06 | 餐桌花卉 | 场景图 | 无内置图；文字模板可用 |
| SCENE-07 | 书房办公桌 | 场景图 | 无内置图；文字模板可用 |
| SCENE-08 | 开放书架垂吊 | 场景图 | 无内置图；文字模板可用 |
| SCENE-09 | 门廊吊篮 | 场景图 | 无内置图；文字模板可用 |
| SCENE-10 | 阳台木平台 | 场景图 | 无内置图；文字模板可用 |
| SCENE-11 | 庭院石材背景 | 场景图 | 无内置图；文字模板可用 |
| SCENE-12 | 仅环境季节氛围 | 场景图 | 无内置图；文字模板可用 |
| QUAL-01 | 庭院石材盆 · 大占比日照图 | 场景图 | 无内置图；文字模板可用 |
| QUAL-02 | 花束尺寸 · 单花＋顶部＋全貌 | 尺寸图 | 无内置图；文字模板可用 |
| QUAL-03 | 四格细节 · 圆角卡片与统一文案条 | 细节图 | 无内置图；文字模板可用 |
| QUAL-04 | 窗台长花箱 · 正面建筑与花材 | 场景图 | 无内置图；文字模板可用 |
| QUAL-05 | 单吊篮近景 · 清楚商品与模糊门廊 | 场景图 | 无内置图；文字模板可用 |
| QUAL-06 | 入口高低错落 · 不改变销售数量 | 场景图 | 无内置图；文字模板可用 |
| QUAL-07 | 栏杆平台近景 · 轻俯视与落地感 | 场景图 | 无内置图；文字模板可用 |
| QUAL-08 | 门廊全景 · 吊挂位置与建筑尺度 | 场景图 | 无内置图；文字模板可用 |
| QUAL-10 | 带铃花环 · 真实附件与悬挂 | 场景图 | 无内置图；文字模板可用 |
| QUAL-11 | 花环细节尺寸 · 全貌＋圆形特写 | 尺寸+细节图 | 无内置图；文字模板可用 |
| QUAL-12 | 秋季入户全景 · 商品与环境分工 | 场景图 | 无内置图；文字模板可用 |
| QUAL-13 | 双吊篮前后景深 · 近大远小 | 场景图 | 无内置图；文字模板可用 |
| QUAL-14 | 室内桌面花材 · 柔光与浅墙线脚 | 场景图 | 无内置图；文字模板可用 |
| QUAL-15 | 节日盆栽近景 · 盆身叶影 | 场景图 | 无内置图；文字模板可用 |
| QUAL-16 | 深色枝叶白底 · 完整与层次 | 白底图 | 无内置图；文字模板可用 |
| QUAL-17 | 红色花材日照 · 饱和但不溢色 | 场景图 | 无内置图；文字模板可用 |
| QUAL-18 | 门口单盆中景 · 容器与环境尺度 | 场景图 | 无内置图；文字模板可用 |
| QUAL-19 | 挂架单吊篮 · 柱面投影与远景 | 场景图 | 无内置图；文字模板可用 |
| QUAL-20 | 台阶前后双盆 · 横向留白 | 场景图 | 无内置图；文字模板可用 |
| QUAL-21 | 秋季窗台花箱 · 阳光与花影 | 场景图 | 无内置图；文字模板可用 |
| QUAL-22 | 秋色壁挂吊篮 · 挂架完整入镜 | 场景图 | 无内置图；文字模板可用 |
| QUAL-23 | 花材套装清单 · 分组＋尺寸＋操作 | 尺寸+细节图 | 无内置图；文字模板可用 |
| QUAL-24 | 暖阳门廊组合 · 悬挂与落地层次 | 场景图 | 无内置图；文字模板可用 |
| QUAL-25 | 混合吊篮近景 · 主花配材与下垂 | 细节图 | 无内置图；文字模板可用 |
| QUAL-27 | 傍晚阳台 · 天光与串灯平衡 | 场景图 | 无内置图；文字模板可用 |
| QUAL-28 | 窄长叶盆栽 · 前后摆位与数量标签 | 场景图 | 无内置图；文字模板可用 |
| AMZ-01 | 完整白底 · 宽展轮廓与内部空隙 | 白底图 | 无内置图；文字模板可用 |
| AMZ-02 | 室内中景 · 主体与背景层级 | 场景图 | 无内置图；文字模板可用 |
| AMZ-08 | 主件与附件 · 分区信息布局 | 套装图 | 无内置图；文字模板可用 |
| AMZ-12 | 主件与外容器 · 独立组件关系 | 套装图 | 无内置图；文字模板可用 |
| AMZ-13 | 横展主体 · 浅盆与支撑面 | 白底图 | 无内置图；文字模板可用 |
| AMZ-14 | 多层底部 · 盆与托盘分离 | 白底图 | 无内置图；文字模板可用 |
| AMZ-16 | 装饰盆外观 · 图案与体积分离 | 白底图 | 无内置图；文字模板可用 |
| AMZ-18 | 弧形轮廓 · 支撑杆与留白 | 白底图 | 无内置图；文字模板可用 |
| AMZ-23 | 疏朗枝条 · 不填满自然空隙 | 白底图 | 无内置图；文字模板可用 |
| AMZ-31 | 组合托盘 · 组件边界清楚 | 套装图 | 无内置图；文字模板可用 |
| AMZ-32 | 多件白底 · 等尺度分隔 | 套装图 | 无内置图；文字模板可用 |
| AMZ-34 | 侧窗日光 · 叶层与墙地关系 | 场景图 | 无内置图；文字模板可用 |
| AMZ-35 | 落地中景 · 完整主体与环境尺度 | 场景图 | 无内置图；文字模板可用 |
| AMZ-38 | 高低台阶 · 前后支撑关系 | 场景图 | 无内置图；文字模板可用 |
| AMZ-39 | 多件悬挂 · 错位留白 | 套装图 | 无内置图；文字模板可用 |
| AMZ-44 | 半圈装饰 · 留白与实部平衡 | 白底图 | 无内置图；文字模板可用 |
| AMZ-45 | 环形白底 · 完整外缘与内孔 | 白底图 | 无内置图；文字模板可用 |
| AMZ-49 | 冠部特写 · 真实重叠与裁切 | 细节图 | 无内置图；文字模板可用 |
| AMZ-52 | 散件清单 · 左侧阵列＋顶部特写＋右侧杆件 | 细节图 | 无内置图；文字模板可用 |
| AMZ-54 | 细枝瓶插 · 保留透气留白 | 白底图 | 无内置图；文字模板可用 |
| AMZ-55 | 开盒展示 · 内容物与盒沿 | 包装图 | 无内置图；文字模板可用 |
| AMZ-56 | 高调窗边 · 真实容器与承托 | 场景图 | 无内置图；文字模板可用 |
| AMZ-58 | 手持展示 · 握持与相对尺度 | 场景图 | 无内置图；文字模板可用 |
| AMZ-60 | 商品与实包装 · 分区展示 | 套装图 | 无内置图；文字模板可用 |
| AMZ-62 | 手持与分离视图 · 相对尺度 | 场景图 | 无内置图；文字模板可用 |
| AMZ-67 | 开盒总览与单件 · 左上包装＋右侧下方细节 | 细节图 | 无内置图；文字模板可用 |
| AMZ-74 | 规则阵列 · 留出独立边界 | 套装图 | 无内置图；文字模板可用 |
| AMZ-76 | 多束白底 · 三角空间布局 | 套装图 | 无内置图；文字模板可用 |
| AMZ-77 | 地插套装 · 斜向错位 | 套装图 | 无内置图；文字模板可用 |
| AMZ-81 | 长花箱斜视 · 前侧面分离 | 白底图 | 无内置图；文字模板可用 |
| AMZ-87 | 全貌与使用场景 · 小图层级 | A+图 | 无内置图；文字模板可用 |
| AMZ-90 | 节日室内 · 主体与建筑尺度 | 场景图 | 无内置图；文字模板可用 |
| AMZ-92 | 单场景与控制器小窗 · 真实状态展示 | 卖点图 | 无内置图；文字模板可用 |
| AMZ-93 | 闭盒包装 · 真实印刷与折面 | 包装图 | 无内置图；文字模板可用 |
| AMZ-94 | 包裹礼品 · 织物与容器分层 | 包装图 | 无内置图；文字模板可用 |
| AMZ-99 | 单件放大与套装 · 尺度区分 | 套装图 | 无内置图；文字模板可用 |
| AMZ-100 | 细枝表面 · 保留真实附着物 | 细节图 | 无内置图；文字模板可用 |
| AMZ-102 | 双状态示意 · 不推断功能 | 卖点图 | 无内置图；文字模板可用 |
| AMZ-103 | 装饰吊篮 · 前后错位 | 套装图 | 无内置图；文字模板可用 |
| AMZ-104 | 填充顶饰 · 支架与连接 | 白底图 | 无内置图；文字模板可用 |
| AMZ-105 | 桌面花艺 · 底托与已有配件 | 白底图 | 无内置图；文字模板可用 |
| AMZ-108 | 桌面低照度 · 轮廓与点光 | 场景图 | 无内置图；文字模板可用 |
| AMZ-115 | 垂挂发光 · 上下层次 | 场景图 | 无内置图；文字模板可用 |
| SETREF-B0D5HKDBDN-G05 | 白底扇形数量核对 | 数量图 | 无内置图；文字模板可用 |
| SETREF-B0D5HKDBDN-G07 | 左整枝右俯视与单花三尺度 | 尺寸图 | 无内置图；文字模板可用 |
| SETREF-B0H5J4K825-G02 | 左整枝右圆窗与俯视 | 尺寸图 | 无内置图；文字模板可用 |
| LAYOUT-BENCH | 庭院长凳 · 横向花艺与背景纵深 | 场景图 | 无内置图；文字模板可用 |
| LAYOUT-DIM1 | 单枝尺寸 · 全貌与独立外侧高度线 | 尺寸图 | 无内置图；文字模板可用 |
| LAYOUT-DET4 | 全貌＋四格细节 · 左整右四窗 | 细节图 | 无内置图；文字模板可用 |
| LAYOUT-MOS3-SCENE | 三景拼版 · 上双景下横景 | 场景图 | 无内置图；文字模板可用 |
| LAYOUT-BUNDLE | 单束包含物 · 一件全貌与清楚数量说明 | 包含物图 | 无内置图；文字模板可用 |

## 套图索引（保留缺失图位）

以 `search --kind series` 检索，`show SET-ID` 按源图序读取；缺口不是已核实全套。

| SET ID | 商品/变体 | 已内置图库 | 已内置A+ |
|---|---|---|---|
| SET-B0C42XHLS7-B0C42XHLS7 | alyptus Fake Flowers Yellow Fall Flowers for Outdoors - 8 Bundles Artificial Mums UV Resistant for Home Garden Window Fall Decor / Yellow | 0 | 1 |
| SET-B0C42XHLS7-B0FBGYSMHX | alyptus Fake Flowers Yellow Fall Flowers for Outdoors - 8 Bundles Artificial Mums UV Resistant for Home Garden Window Fall Decor / Orange | 0 | 1 |
| SET-B0C42XHLS7-B0FBGDHC5N | alyptus Fake Flowers Yellow Fall Flowers for Outdoors - 8 Bundles Artificial Mums UV Resistant for Home Garden Window Fall Decor / Dusty Green Leaves | 0 | 1 |
| SET-B0C42XHLS7-B0D584G412 | alyptus Fake Flowers Yellow Fall Flowers for Outdoors - 8 Bundles Artificial Mums UV Resistant for Home Garden Window Fall Decor / Multi Color | 0 | 1 |
| SET-B0C42XHLS7-B0HBQ4HL4M | alyptus Fake Flowers Yellow Fall Flowers for Outdoors - 8 Bundles Artificial Mums UV Resistant for Home Garden Window Fall Decor / Light Red | 8 | 1 |
| SET-B0C42XHLS7-B0FBGB7NDD | alyptus Fake Flowers Yellow Fall Flowers for Outdoors - 8 Bundles Artificial Mums UV Resistant for Home Garden Window Fall Decor / Red | 0 | 1 |
| SET-B0C42XHLS7-B0CHVXJFC9 | alyptus Fake Flowers Yellow Fall Flowers for Outdoors - 8 Bundles Artificial Mums UV Resistant for Home Garden Window Fall Decor / White Artificial Flowers for Outdoors | 0 | 1 |
| SET-B0C42XHLS7-B0FBGC28CH | alyptus Fake Flowers Yellow Fall Flowers for Outdoors - 8 Bundles Artificial Mums UV Resistant for Home Garden Window Fall Decor / Fall Leaves | 0 | 1 |
| SET-B0C42XHLS7-B0D583WDC1 | alyptus Fake Flowers Yellow Fall Flowers for Outdoors - 8 Bundles Artificial Mums UV Resistant for Home Garden Window Fall Decor / Colorful | 0 | 1 |
| SET-B0C42XHLS7-B0C42YV732 | alyptus Fake Flowers Yellow Fall Flowers for Outdoors - 8 Bundles Artificial Mums UV Resistant for Home Garden Window Fall Decor / Light Orange | 2 | 1 |
| SET-B0C42XHLS7-B0F92G176Y | alyptus Fake Flowers Yellow Fall Flowers for Outdoors - 8 Bundles Artificial Mums UV Resistant for Home Garden Window Fall Decor / Orang Red Yellow 12 Bundles | 0 | 1 |
| SET-B0C42XHLS7-B0FBG1PS3F | alyptus Fake Flowers Yellow Fall Flowers for Outdoors - 8 Bundles Artificial Mums UV Resistant for Home Garden Window Fall Decor / Green Leaves | 0 | 1 |
| SET-B0C42XHLS7-B0CN5JCJVH | alyptus Fake Flowers Yellow Fall Flowers for Outdoors - 8 Bundles Artificial Mums UV Resistant for Home Garden Window Fall Decor / Eucalyptus | 0 | 1 |
| SET-B0CDH12X3Z-B0CDH12X3Z | Artificial Flowers Outdoors, Artificial Geraniums for Outdoors, Fake Geranium Flowers, UV Resistant Faux Outdoor Plants for Planters, Artificial Flowers for Indoor Home Decor, Pink 4PCS / Pink-4 | 0 | 1 |
| SET-B0CDH12X3Z-B0DSHP47BN | Artificial Flowers Outdoors, Artificial Geraniums for Outdoors, Fake Geranium Flowers, UV Resistant Faux Outdoor Plants for Planters, Artificial Flowers for Indoor Home Decor, Pink 4PCS / Rose Red-8 | 0 | 1 |
| SET-B0CDH12X3Z-B0B9JYQD3R | Artificial Flowers Outdoors, Artificial Geraniums for Outdoors, Fake Geranium Flowers, UV Resistant Faux Outdoor Plants for Planters, Artificial Flowers for Indoor Home Decor, Pink 4PCS / Yellow-4 | 0 | 1 |
| SET-B0CDH12X3Z-B0B9K1RPXJ | Artificial Flowers Outdoors, Artificial Geraniums for Outdoors, Fake Geranium Flowers, UV Resistant Faux Outdoor Plants for Planters, Artificial Flowers for Indoor Home Decor, Pink 4PCS / Red-4 | 0 | 1 |
| SET-B0CDH12X3Z-B0DSHMLXZX | Artificial Flowers Outdoors, Artificial Geraniums for Outdoors, Fake Geranium Flowers, UV Resistant Faux Outdoor Plants for Planters, Artificial Flowers for Indoor Home Decor, Pink 4PCS / Pink-8 | 0 | 1 |
| SET-B0CDH12X3Z-B0DSHLC4NJ | Artificial Flowers Outdoors, Artificial Geraniums for Outdoors, Fake Geranium Flowers, UV Resistant Faux Outdoor Plants for Planters, Artificial Flowers for Indoor Home Decor, Pink 4PCS / Red-8 | 0 | 1 |
| SET-B0CDH12X3Z-B0DSHN4JJT | Artificial Flowers Outdoors, Artificial Geraniums for Outdoors, Fake Geranium Flowers, UV Resistant Faux Outdoor Plants for Planters, Artificial Flowers for Indoor Home Decor, Pink 4PCS / White-8 | 0 | 1 |
| SET-B0CDH12X3Z-B0B9JZWDV9 | Artificial Flowers Outdoors, Artificial Geraniums for Outdoors, Fake Geranium Flowers, UV Resistant Faux Outdoor Plants for Planters, Artificial Flowers for Indoor Home Decor, Pink 4PCS / White-4 | 0 | 1 |
| SET-B0CDH12X3Z-B0DSHQJ2DY | Artificial Flowers Outdoors, Artificial Geraniums for Outdoors, Fake Geranium Flowers, UV Resistant Faux Outdoor Plants for Planters, Artificial Flowers for Indoor Home Decor, Pink 4PCS / Yellow-8 | 0 | 1 |
| SET-B0CDH12X3Z-B0B9JWTGLJ | Artificial Flowers Outdoors, Artificial Geraniums for Outdoors, Fake Geranium Flowers, UV Resistant Faux Outdoor Plants for Planters, Artificial Flowers for Indoor Home Decor, Pink 4PCS / Rose Red-4 | 6 | 1 |
| SET-B0D5HKDBDN-B0D5HKDBDN | Daisy Artificial Flowers for Outdoors Fall Autumn Decoration, 6 Bundles Fake Mums Yellow Silk Flowers for Outside Look Real UV Resistant Faux Flowers Plants for Planter Front Door Home Indoor Porch / Yellow | 7 | 11 |
| SET-B0D5HKDBDN-B0D5HMC3PC | Daisy Artificial Flowers for Outdoors Fall Autumn Decoration, 6 Bundles Fake Mums Yellow Silk Flowers for Outside Look Real UV Resistant Faux Flowers Plants for Planter Front Door Home Indoor Porch / Orange | 0 | 11 |
| SET-B0D5HKDBDN-B0DK96HCYR | Daisy Artificial Flowers for Outdoors Fall Autumn Decoration, 6 Bundles Fake Mums Yellow Silk Flowers for Outside Look Real UV Resistant Faux Flowers Plants for Planter Front Door Home Indoor Porch / White-6 Bundles | 0 | 11 |
| SET-B0D5HKDBDN-B0D5HK6FD7 | Daisy Artificial Flowers for Outdoors Fall Autumn Decoration, 6 Bundles Fake Mums Yellow Silk Flowers for Outside Look Real UV Resistant Faux Flowers Plants for Planter Front Door Home Indoor Porch / Dark Red | 0 | 11 |
| SET-B0D5HKDBDN-B0F5W97V25 | Daisy Artificial Flowers for Outdoors Fall Autumn Decoration, 6 Bundles Fake Mums Yellow Silk Flowers for Outside Look Real UV Resistant Faux Flowers Plants for Planter Front Door Home Indoor Porch / Mixed Colors(3 Yellow, 3 Orange) | 0 | 11 |
| SET-B0D5HKDBDN-B0DP1XNBF4 | Daisy Artificial Flowers for Outdoors Fall Autumn Decoration, 6 Bundles Fake Mums Yellow Silk Flowers for Outside Look Real UV Resistant Faux Flowers Plants for Planter Front Door Home Indoor Porch / Red | 0 | 11 |
| SET-B0D5HKDBDN-B0DP1XDLB8 | Daisy Artificial Flowers for Outdoors Fall Autumn Decoration, 6 Bundles Fake Mums Yellow Silk Flowers for Outside Look Real UV Resistant Faux Flowers Plants for Planter Front Door Home Indoor Porch / Purple | 0 | 11 |
| SET-B0D5HKDBDN-B0D5HHGMSR | Daisy Artificial Flowers for Outdoors Fall Autumn Decoration, 6 Bundles Fake Mums Yellow Silk Flowers for Outside Look Real UV Resistant Faux Flowers Plants for Planter Front Door Home Indoor Porch / Mixed Colors | 0 | 11 |
| SET-B0D5HKDBDN-B0D8BCV27K | Daisy Artificial Flowers for Outdoors Fall Autumn Decoration, 6 Bundles Fake Mums Yellow Silk Flowers for Outside Look Real UV Resistant Faux Flowers Plants for Planter Front Door Home Indoor Porch / Sunflowers | 0 | 11 |
| SET-B0D5HKDBDN-B0GQMFQ8SV | Daisy Artificial Flowers for Outdoors Fall Autumn Decoration, 6 Bundles Fake Mums Yellow Silk Flowers for Outside Look Real UV Resistant Faux Flowers Plants for Planter Front Door Home Indoor Porch / White | 0 | 11 |
| SET-B0FNBSD73T-B0FNBSD73T | PABIPABI Birch Tree with LED Lights, 6ft Lighted Christmas Trees Outdoor / 6ft x2 | 9 | 12 |
| SET-B0H4G2PXX5-B0H4G2PXX5 | HyeFlora Artificial Fall Faux Mums Flowers Outdoor Plants for Decoration, 6 Bundles Fake Silk Yellow Gerbera Daisy Flowers UV Resistant Look Real for Planter Outside Front Door Porch Patio Balcony / Yellow-gerbera | 0 | 8 |
| SET-B0H4G2PXX5-B0D1FSC421 | HyeFlora Artificial Fall Faux Mums Flowers Outdoor Plants for Decoration, 6 Bundles Fake Silk Yellow Gerbera Daisy Flowers UV Resistant Look Real for Planter Outside Front Door Porch Patio Balcony / Dark Pink | 0 | 8 |
| SET-B0H4G2PXX5-B0D1DYBDTT | HyeFlora Artificial Fall Faux Mums Flowers Outdoor Plants for Decoration, 6 Bundles Fake Silk Yellow Gerbera Daisy Flowers UV Resistant Look Real for Planter Outside Front Door Porch Patio Balcony / Fuchsia | 0 | 8 |
| SET-B0H4G2PXX5-B0FZJ5SS76 | HyeFlora Artificial Fall Faux Mums Flowers Outdoor Plants for Decoration, 6 Bundles Fake Silk Yellow Gerbera Daisy Flowers UV Resistant Look Real for Planter Outside Front Door Porch Patio Balcony / Melon Red+red | 6 | 8 |
| SET-B0H4G2PXX5-B0H4FXTCFC | HyeFlora Artificial Fall Faux Mums Flowers Outdoor Plants for Decoration, 6 Bundles Fake Silk Yellow Gerbera Daisy Flowers UV Resistant Look Real for Planter Outside Front Door Porch Patio Balcony / White-gerbera | 0 | 8 |
| SET-B0H4G2PXX5-B0D1DT3CCV | HyeFlora Artificial Fall Faux Mums Flowers Outdoor Plants for Decoration, 6 Bundles Fake Silk Yellow Gerbera Daisy Flowers UV Resistant Look Real for Planter Outside Front Door Porch Patio Balcony / White | 0 | 8 |
| SET-B0H4G2PXX5-B0FZJ695J8 | HyeFlora Artificial Fall Faux Mums Flowers Outdoor Plants for Decoration, 6 Bundles Fake Silk Yellow Gerbera Daisy Flowers UV Resistant Look Real for Planter Outside Front Door Porch Patio Balcony / Red+fuchsia | 0 | 8 |
| SET-B0H4G2PXX5-B0D1DT2XYD | HyeFlora Artificial Fall Faux Mums Flowers Outdoor Plants for Decoration, 6 Bundles Fake Silk Yellow Gerbera Daisy Flowers UV Resistant Look Real for Planter Outside Front Door Porch Patio Balcony / Red | 0 | 8 |
| SET-B0H4G2PXX5-B0D1FK1SBK | HyeFlora Artificial Fall Faux Mums Flowers Outdoor Plants for Decoration, 6 Bundles Fake Silk Yellow Gerbera Daisy Flowers UV Resistant Look Real for Planter Outside Front Door Porch Patio Balcony / Pink | 0 | 8 |
| SET-B0H4G2PXX5-B0H4FT74HH | HyeFlora Artificial Fall Faux Mums Flowers Outdoor Plants for Decoration, 6 Bundles Fake Silk Yellow Gerbera Daisy Flowers UV Resistant Look Real for Planter Outside Front Door Porch Patio Balcony / Orange-gerbera | 1 | 8 |
| SET-B0H4G2PXX5-B0D1DNDB3T | HyeFlora Artificial Fall Faux Mums Flowers Outdoor Plants for Decoration, 6 Bundles Fake Silk Yellow Gerbera Daisy Flowers UV Resistant Look Real for Planter Outside Front Door Porch Patio Balcony / Hotpink | 0 | 8 |
| SET-B0H5J4K825-B0H5J4K825 | Artificial Fall Fake Mums Flowers Plants for Outdoor Decoration, 6 PCS Faux Silk Orange Gerbera Daisy UV Resistant No Fade Realistic for Planter Pot Outside Porch Patio Balcony Garden Yard Home Decor / Orange Mums | 8 | 9 |
| SET-B0H5J4K825-B0CNK6FWYR | Artificial Fall Fake Mums Flowers Plants for Outdoor Decoration, 6 PCS Faux Silk Orange Gerbera Daisy UV Resistant No Fade Realistic for Planter Pot Outside Porch Patio Balcony Garden Yard Home Decor / White | 0 | 9 |
| SET-B0H5J4K825-B0D7VCBQMN | Artificial Fall Fake Mums Flowers Plants for Outdoor Decoration, 6 PCS Faux Silk Orange Gerbera Daisy UV Resistant No Fade Realistic for Planter Pot Outside Porch Patio Balcony Garden Yard Home Decor / A Red | 0 | 9 |
| SET-B0H5J4K825-B0H5J4GHHC | Artificial Fall Fake Mums Flowers Plants for Outdoor Decoration, 6 PCS Faux Silk Orange Gerbera Daisy UV Resistant No Fade Realistic for Planter Pot Outside Porch Patio Balcony Garden Yard Home Decor / White Mums | 0 | 9 |
| SET-B0H5J4K825-B0G414P7K9 | Artificial Fall Fake Mums Flowers Plants for Outdoor Decoration, 6 PCS Faux Silk Orange Gerbera Daisy UV Resistant No Fade Realistic for Planter Pot Outside Porch Patio Balcony Garden Yard Home Decor / Melon Red+red | 1 | 9 |
| SET-B0H5J4K825-B0CNK77XY2 | Artificial Fall Fake Mums Flowers Plants for Outdoor Decoration, 6 PCS Faux Silk Orange Gerbera Daisy UV Resistant No Fade Realistic for Planter Pot Outside Porch Patio Balcony Garden Yard Home Decor / Pink | 0 | 9 |
| SET-B0H5J4K825-B0CNK6GYD1 | Artificial Fall Fake Mums Flowers Plants for Outdoor Decoration, 6 PCS Faux Silk Orange Gerbera Daisy UV Resistant No Fade Realistic for Planter Pot Outside Porch Patio Balcony Garden Yard Home Decor / Purple | 0 | 9 |
| SET-B0H5J4K825-B0CNK75DZ2 | Artificial Fall Fake Mums Flowers Plants for Outdoor Decoration, 6 PCS Faux Silk Orange Gerbera Daisy UV Resistant No Fade Realistic for Planter Pot Outside Porch Patio Balcony Garden Yard Home Decor / Hotpink | 0 | 9 |
| SET-B0H5J4K825-B0CNK7C4DP | Artificial Fall Fake Mums Flowers Plants for Outdoor Decoration, 6 PCS Faux Silk Orange Gerbera Daisy UV Resistant No Fade Realistic for Planter Pot Outside Porch Patio Balcony Garden Yard Home Decor / Yellow | 0 | 9 |
| SET-B0H5J4K825-B0G413ZG8Y | Artificial Fall Fake Mums Flowers Plants for Outdoor Decoration, 6 PCS Faux Silk Orange Gerbera Daisy UV Resistant No Fade Realistic for Planter Pot Outside Porch Patio Balcony Garden Yard Home Decor / Purple+fuchsia | 0 | 9 |
| SET-B0H5J4K825-B0G418LNMV | Artificial Fall Fake Mums Flowers Plants for Outdoor Decoration, 6 PCS Faux Silk Orange Gerbera Daisy UV Resistant No Fade Realistic for Planter Pot Outside Porch Patio Balcony Garden Yard Home Decor / Red +Fuchsia | 0 | 9 |
| SET-B0H5J4K825-B0CNK7GYJ4 | Artificial Fall Fake Mums Flowers Plants for Outdoor Decoration, 6 PCS Faux Silk Orange Gerbera Daisy UV Resistant No Fade Realistic for Planter Pot Outside Porch Patio Balcony Garden Yard Home Decor / Pink 2 | 0 | 9 |
| SET-B0H5J4K825-B0H5JLLMP4 | Artificial Fall Fake Mums Flowers Plants for Outdoor Decoration, 6 PCS Faux Silk Orange Gerbera Daisy UV Resistant No Fade Realistic for Planter Pot Outside Porch Patio Balcony Garden Yard Home Decor / Yellow Mums | 0 | 9 |
| SET-B07ZCBVV19-B07ZCBVV19 | AXYLEX Artificial Mums for Outdoors, Fake Fall Flowers (Red Orange) / Red Orange | 4 | 3 |
| SET-B0GCN4M8ZB-B0GCN4M8ZB | lovemoon 8 Pcs Geraniums Artificial Flowers for Outdoor Decor, Rose Red / Rose Red / 8 | 4 | 2 |
| SET-B0DP8JBCC1-B0DP8JBCC1 | 18"Artificial Geraniums for Outdoors 2-Pack Pink Silk Flowers / Pink | 4 | 5 |
| SET-B0H2VDTZYT-B0H2VDTZYT | Artificial Mums for Outdoors Fall Flowers Artificial for Decoration, 12 Bundles Fake Mums Realistic UV Resistant Fall Plants Faux Mums for Outdoor Planters Patio Porch Yard Front Door Gardens Indoor / 12 Bundles Multi-color (3 Orange, 3 Burgundy, 3 Yellow, 3 Brown) | 4 | 8 |

## 已内置成图索引

先按标题/图类定位，再打开原图；`show IMG-ID` 读取该图观察与反推提示词。

| 图像 ID | 已记录标题 | 图类 | 成图 |
|---|---|---|---|
| IMG-890bf22af487a33f | 花环门板近景 · 枝叶硬投影 | 场景图 | [查看](previews/assets/collected/09-door-wreath.png) |
| IMG-51da6130886f3900 | 上下场景拼版 · 中间文案带 | 场景图 | [查看](previews/assets/collected/26-two-scene-panel.png) |
| IMG-fe6f0ec125d1c36b | 白底尺寸 · 全貌＋双圆形细节 | 尺寸图 / 细节图 | [查看](previews/assets/dimensions/01-white-two-circles.png) |
| IMG-e88c95c18a0ff8a8 | 白底尺寸 · 正视＋俯视＋单花三视图 | 尺寸图 | [查看](previews/assets/dimensions/02-three-views.png) |
| IMG-4b9836deb1740822 | 暖米色尺寸 · 主束＋多色套装分栏 | 尺寸图 | [查看](previews/assets/dimensions/03-warm-assortment.png) |
| IMG-79c94e78fb0099a7 | 深绿弧形尺寸 · 主束＋圆窗卖点 | 尺寸图 / 细节图 | [查看](previews/assets/dimensions/05-dark-green-curve.png) |
| IMG-48d71770d95ca2d3 | 绿色分栏尺寸 · 主束＋三格矩形细节 | 尺寸图 / 细节图 | [查看](previews/assets/dimensions/06-green-detail-panels.png) |
| IMG-e2a934da4dca032d | 橙色尺寸 · 单束测量＋手持整包 | 尺寸图 | [查看](previews/assets/dimensions/07-orange-handheld-pack.png) |
| IMG-2b8df74a164bb64a | 白底尺寸 · 全貌＋三圆形结构细节 | 尺寸图 / 细节图 | [查看](previews/assets/dimensions/08-white-three-circles-yellow.png) |
| IMG-015e68fbba6a50ec | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/015e68fbba6a50ecf6032df09ddf524ced862c240ab5d7661cdeeca1e943d094.jpg) |
| IMG-07a41b46cffe14b4 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/07a41b46cffe14b49e9e86061085131cf95c708b0c1dea6d58d6d2aebec5ef78.jpg) |
| IMG-09b96fc70900ad72 | 深檐下金秋吊篮 | A+图 | [查看](previews/assets/Aplus/09b96fc70900ad72748c206eed699ce43f0266ef8d950a3ce88bf28a98fd8374.jpg) |
| IMG-0a38211f36ce7abd | 左主枝右四圆细节 | 细节图 | [查看](previews/assets/dimensions/0a38211f36ce7abd152096bf163028813217812f6b1544288142dd9670c3d7df.jpg) |
| IMG-0c12e4ba653335d6 | Three-tier arrangement-size guidance | 卖点图 | [查看](previews/assets/collected/0c12e4ba653335d69ac2ba4bbfaa91f62ea8f1e1b734315a91bcf460eb6078cb.jpg) |
| IMG-10bf1ac26aae5b7d | 单吊篮与铁艺支架 | 场景图 | [查看](previews/assets/collected/10bf1ac26aae5b7d8cd541961324aa00e1c782e9a53dfdc66cb5a159077da749.jpg) |
| IMG-136101748b8847e2 | 左门廊右斜切标题区 | A+图 | [查看](previews/assets/Aplus/136101748b8847e29409cd42d9cf2fa78e3d58aa84500c3813715e472364cd9f.jpg) |
| IMG-14b78271129945a5 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/14b78271129945a5f748a60b8ae6df14dabfc5d60f252d646162f6dbaf54d361.jpg) |
| IMG-192b9b7cff1354f2 | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/192b9b7cff1354f2844b29b5f9b3c20b7cd34f54112da0ba6672e7417ad12f6c.jpg) |
| IMG-1ad19a90fa1b201f | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/1ad19a90fa1b201fdca2cc9a52e9c1ea3880205095c9574f56b4a9037ed2cf13.jpg) |
| IMG-1c46f72614abbbd3 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/1c46f72614abbbd33886514553ea3c867043a98436939c31b90f23efd9ac8095.jpg) |
| IMG-1f0042c70aba64c3 | 绿长椅前后三盆 | A+图 | [查看](previews/assets/Aplus/1f0042c70aba64c36e5379a5d47a39ab89ced9de82a1a665237307d2d776ac66.jpg) |
| IMG-2539d6b2447ab1b4 | 炭灰盆与门廊层次 | A+图 | [查看](previews/assets/Aplus/2539d6b2447ab1b4dc9217ff7fa85dcd0c241beb95bef7cb15907f4d01dc51f6.jpg) |
| IMG-255f6d31a0ed5f64 | Horizontal windowbox or railing planter | 场景图 | [查看](previews/assets/collected/255f6d31a0ed5f647ceeba0d72a6c4c6c0e5284cebe5d59c75ef38cfc135d9e6.jpg) |
| IMG-2a55e0ba7b0f4669 | 场景与场景拼版 · 6ft_x2 | 场景图 | [查看](previews/assets/collected/2a55e0ba7b0f4669b09ab6340bb08e528008a53dc2824c8b1e24b2ec744e2ef9.jpg) |
| IMG-31aed85e5c3268e3 | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/31aed85e5c3268e3b28563ba858b6350932bb8f15606e371087ad88a5358b8f0.jpg) |
| IMG-335f75081805f6d9 | 白栏金秋长花箱 | 场景图 | [查看](previews/assets/collected/335f75081805f6d91f136c0450cebaa67d4b8778596c21a935b71504e8e921eb.jpg) |
| IMG-36162841ca027778 | 浅蓝门前多高低盆 | A+图 | [查看](previews/assets/Aplus/36162841ca027778df7fb35f74b15a62af5596fe55e84dc3d33c84a08b322649.jpg) |
| IMG-36939080cbdffc42 | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/36939080cbdffc422917df7564a6e5edf6b55ac7e1d8b927f7ec869db49afd38.jpg) |
| IMG-39a786b319666370 | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/39a786b3196663700c64858503c3e7139cf6a116a355f64300bee5bdd0e8cd95.jpg) |
| IMG-3bb77d69e1838454 | 白阶三盆与椅子 | A+图 | [查看](previews/assets/Aplus/3bb77d69e1838454c9271b5131b64f8de95f24b51b7c20f7f409c4dbe33fe1fe.jpg) |
| IMG-45f74254fc63f012 | 木廊单盆纵深 | A+图 | [查看](previews/assets/Aplus/45f74254fc63f012904697244788d4a0ee43bc0e252242ed7bece2e2d80a0b09.jpg) |
| IMG-45f9e3925377bd5d | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/45f9e3925377bd5de3234b90ae546b5a65c9700ca410b217d0eea11c8036a5e6.jpg) |
| IMG-489de30499bb2117 | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/489de30499bb211732b98fc19b1c1396bf3787b9673ddf42651be5f895e78f58.jpg) |
| IMG-4a9a2be84a7f2f8f | 白栏旁留白木桶 | A+图 | [查看](previews/assets/Aplus/4a9a2be84a7f2f8f43e98f8010a5cc2be20be93d7de15db26553af1c398f0fa5.jpg) |
| IMG-4b8cbe219b216f03 | Living-room floral arrangement with seasonal depth | 场景图 | [查看](previews/assets/collected/4b8cbe219b216f030f3b8cde9e30b89ecedbdf82a877ee1c6861802bacabf1ab.jpg) |
| IMG-4c9561f70b3d861b | Supported hanging basket with architectural depth | 场景图 | [查看](previews/assets/collected/4c9561f70b3d861b4d5f1a00d32ab50d49c03fcaaef4eb0008d5a3c55fa99e3d.jpg) |
| IMG-4cb45329439563d1 | 蓝调廊架与玻璃门夜景 | A+图 | [查看](previews/assets/Aplus/4cb45329439563d19cb57d79056d097a561cdcf5a8e35c7c72ea8f4658c41366.jpg) |
| IMG-52b1ee33d21d71ea | Whole spray plus three rectangular close-ups | 尺寸图 / 细节图 | [查看](previews/assets/collected/52b1ee33d21d71ea9346f75985233fe551841dc1ebe4b3f2d6f99735683ad8d1.jpg) |
| IMG-55237d6cd4d57a1e | Horizontal windowbox or railing planter | 场景图 | [查看](previews/assets/collected/55237d6cd4d57a1e2e35df71cf20af22fac7bfeca3e7dfe882cfb094b309140e.jpg) |
| IMG-56800b5de0571c07 | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/56800b5de0571c073f630288b6c279ac91837e9bb635d49acae9f46af91745f6.jpg) |
| IMG-59ee1899fb0784a6 | 场景与场景拼版 · 6ft_x2 | 场景图 | [查看](previews/assets/collected/59ee1899fb0784a606b31c4900aa174443b1ca97ffb28ed11e4350e5b62b6439.jpg) |
| IMG-625103dc561225b6 | Tabletop or windowsill floral focal point | 场景图 | [查看](previews/assets/collected/625103dc561225b6a8f3442ffd2b9533c3d962a21e54eb30620dd8f786f7224f.jpg) |
| IMG-628b7a80db4b77e5 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/628b7a80db4b77e540e37d9ca03c80e75170afce582c56ec6d3d3268b95b1d9b.jpg) |
| IMG-66ee3c603ed21cab | 农舍有顶木廊暖夜 | A+图 | [查看](previews/assets/Aplus/66ee3c603ed21cabc1acd2b0ddbdc0fcbbd6e62d39b972cab140b15bf0a80fb5.jpg) |
| IMG-68b621a50f4de531 | 石柱旁方木盆 | A+图 | [查看](previews/assets/Aplus/68b621a50f4de5316670528d3f377a11e7ac9be8a8073b75227e26970959fec6.jpg) |
| IMG-68d9a9a819caac4a | 深绿外框加底部核对栏 | A+图 | [查看](previews/assets/Aplus/68d9a9a819caac4a560348207eac8babfb4cc18c490be38fa4d8a2a776080c20.jpg) |
| IMG-691e8318bb1e0217 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/691e8318bb1e0217539bce560c2d207c711f1f52cfcc306d53c0dea1fdf1b65e.jpg) |
| IMG-6aca210e13535b8d | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/6aca210e13535b8de1d2f93bb6d0c23cd4cea8532e6307c791f5d27542a12e43.jpg) |
| IMG-6cfbd1d2e5227f25 | 灯树高度与右侧功能栏 | 尺寸图 | [查看](previews/assets/collected/6cfbd1d2e5227f254f177c5b031415a91aa6d15b88eb9d4e041216b5b36f0988.jpg) |
| IMG-6cfcd1bef6429a62 | 场景与场景拼版 · 6ft_x2 | 场景图 | [查看](previews/assets/collected/6cfcd1bef6429a62894c5d6a004ab62166b55909f1ec71edfc58b9f1b9b15549.jpg) |
| IMG-7b906a13c777852d | Symmetric residential entry display | 场景图 | [查看](previews/assets/collected/7b906a13c777852dfca75917b0264016394763f3bff9e7dce588870038353e5e.jpg) |
| IMG-7d0e9f6fadecb7a2 | Supported hanging basket with architectural depth | 场景图 | [查看](previews/assets/collected/7d0e9f6fadecb7a22632475c498e8546338fdc36af0102b22b3bae6db14c6422.jpg) |
| IMG-7d3dbe9a699564d0 | 六种载体用途等格 | A+图 | [查看](previews/assets/Aplus/7d3dbe9a699564d00efc9db4b0527179aa4fea63f4c9e1cfc7c856b8c9cbecf4.jpg) |
| IMG-8637d7f4cf5ba53d | 木凳与地面三盆 | A+图 | [查看](previews/assets/Aplus/8637d7f4cf5ba53df807da4f206accacdf84ba30789f7b4e0dd4b8625858af9e.jpg) |
| IMG-880f4592b15af043 | Whole spray plus three rectangular close-ups | 尺寸图 / 细节图 | [查看](previews/assets/dimensions/880f4592b15af043d1aa164850fa6abaf56d546de99c465b946cc38a3b8bf7fb.jpg) |
| IMG-8cca38b930560820 | Symmetric residential entry display | 场景图 | [查看](previews/assets/collected/8cca38b930560820e8f1dcd54a983506ff0779e3a933769b82e042b973216879.jpg) |
| IMG-8e3abbb8f9cfd5bf | Symmetric residential entry display | 场景图 | [查看](previews/assets/collected/8e3abbb8f9cfd5bf519fc44fc6acb3b70162518b0fc75475da1b4d81f3f6801a.jpg) |
| IMG-91283c92626a4018 | Whole spray beside a two-by-two detail grid | 尺寸图 / 细节图 | [查看](previews/assets/collected/91283c92626a4018eab64a85d81d4c24c540e348c949db95ec31c2ac87fdee7e.jpg) |
| IMG-94c28e279b6f8279 | Autumn garden bench and long planter | 场景图 | [查看](previews/assets/collected/94c28e279b6f8279cb18a805584cdf737726549169b87eda3f2cd23624a8d954.jpg) |
| IMG-965e58ee248607f5 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/965e58ee248607f500b88bc6084a90b092891158dce8824945a2c77f08f08673.jpg) |
| IMG-97f7c2c8f8f8afb6 | 暖色木桶近景 | A+图 | [查看](previews/assets/Aplus/97f7c2c8f8f8afb6ed662254fc290b9f75d2d942a0cf4efe7aa20d9ad55c6ea0.jpg) |
| IMG-999b998e71e10447 | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/999b998e71e10447e9e9f16fd6de74b3eccb9c308df0f0046641a54e5592487c.jpg) |
| IMG-9a1f2eeb455432da | Hands interacting with a floral arrangement | 卖点图 | [查看](previews/assets/collected/9a1f2eeb455432da2996051a5da8db492940e2758caaca08eed60e8a85429499.jpg) |
| IMG-9d0385d3443d8e5a | 深绿框三栏规格细节 | A+图 | [查看](previews/assets/Aplus/9d0385d3443d8e5aa162660609f89c11aeb08478aeeeb359f0c3c7f9636404b5.jpg) |
| IMG-9f62e0f35c609420 | 砖墙黑栏长箱 | A+图 | [查看](previews/assets/Aplus/9f62e0f35c609420dcd21216898e8f5b54505069b6db0af55067c38d3181f46c.jpg) |
| IMG-a09d369eda14c2f8 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/a09d369eda14c2f8ace57273e39db91c5e0a2645c5c15ad992663b1de5dc192b.jpg) |
| IMG-a1f63575e6921d75 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/a1f63575e6921d754903a3b9af352442e8a83a8dd7b72a9440fcc1365ef2338f.jpg) |
| IMG-a92b1f33d2ceb429 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/a92b1f33d2ceb42902e84ecbb47d3f5b279b9b5640487443352e51db83248c77.jpg) |
| IMG-a94d9ea5055a28c3 | 场景与场景拼版 · 6ft_x2 | 场景图 | [查看](previews/assets/collected/a94d9ea5055a28c305e8b853c2fe9d1f9fd927eaf63090d4d25e0d3fd7f9d6ee.jpg) |
| IMG-a98d64d46c3226e6 | 室外蓝调夜景与功能板 | 场景图 | [查看](previews/assets/collected/a98d64d46c3226e6e4bc1c33774ff7e8dd55a858f4d8ccbf02171f2e3bbdf212.jpg) |
| IMG-a9968094d29723b0 | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/a9968094d29723b0344af0ea67865e0aaba6838269c44814eedba0d6a4598530.jpg) |
| IMG-aed9ad2c4f825159 | 上方数量与下方扇形清单 | 数量图 | [查看](previews/assets/dimensions/aed9ad2c4f825159ef266cb1fcee88a6d05e3a569ae704afcaf4701f43ac1ab4.jpg) |
| IMG-af2f37fe6f13da1a | 场景与场景拼版 · 6ft_x2 | 场景图 | [查看](previews/assets/collected/af2f37fe6f13da1a3a7e18399de8354141cac0194f8d93fced56816940d57d54.jpg) |
| IMG-af43f8f622a20203 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/af43f8f622a20203264e331fb775ede14501218c180f2b563bcfb49006967dea.jpg) |
| IMG-b3a56f67ef258d8e | 主灯树与四级状态圆窗 | 对比图 | [查看](previews/assets/collected/b3a56f67ef258d8e72e00bae396282882fea8ab8233614bd0ee30c5df3a67572.jpg) |
| IMG-b49c7f559c055086 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/b49c7f559c0550864ebe0ebbed055c05f0a654ffa8acb3c7b138b73269d2b9f8.jpg) |
| IMG-b4fb6c8d73fa5cab | Tabletop or windowsill floral focal point | 场景图 | [查看](previews/assets/collected/b4fb6c8d73fa5cab7615a9089556f81ffa32909d6f8bdd4d4f7cc65b80e7b638.jpg) |
| IMG-b9d36ac9ccb6ab92 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/b9d36ac9ccb6ab92c929cff6e87d5d001889cfc2b81a12bf7bdb1fd95e84900e.jpg) |
| IMG-ba7267f67a7498b0 | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/ba7267f67a7498b004385ad58133a7bab56f6e003ae94e86df4cf9fa8baebd9b.jpg) |
| IMG-bb00ace05e86e194 | 同机位日夜对照与操作窗 | 对比图 | [查看](previews/assets/collected/bb00ace05e86e194d4071b6ba6be650626ada1540c0bf5e7fda2bcbad05a3ecf.jpg) |
| IMG-bb609eafb89a0fef | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/bb609eafb89a0fef28795d6ac6a7626a3d042e6e6d13bbe059f557f54f5be4e7.jpg) |
| IMG-c0e24a4f07548d30 | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/c0e24a4f07548d3000970259dcb96991d8421213e82827ffadc802f50ee22a43.jpg) |
| IMG-c2c379bf80a7d942 | 门前灯树与左侧编辑标题 | A+图 | [查看](previews/assets/Aplus/c2c379bf80a7d942e07236734d5a3c13605d2b45d88c3f8548f34048b61eb0de.jpg) |
| IMG-c9ee1eb14d8b7c4f | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/c9ee1eb14d8b7c4f9c0594f3e7d84b5e8244336f20894d13d5af2c528f68c17d.jpg) |
| IMG-ce1fb0ee046ddc1f | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/ce1fb0ee046ddc1f0c852277d530bd17348d5fb02bc89096d97bb949798f6445.jpg) |
| IMG-d1d7aca4b0f730f4 | 大场景加底部四细节 | 细节图 | [查看](previews/assets/collected/d1d7aca4b0f730f4ad7c43cc65309ac05db1069230159ba807ffd45ed83f7bb9.jpg) |
| IMG-d4b266e6f60b6d98 | 石墙红花方盆 | A+图 | [查看](previews/assets/Aplus/d4b266e6f60b6d981978882c4bc719d812074f629d8e47f4383881d78f75ccb7.jpg) |
| IMG-d5a484266d43a6c5 | Potted floral hero in a residential setting | 场景图 | [查看](previews/assets/collected/d5a484266d43a6c55d135be6ac219072e4c992e15c435839cecc59675e4c10cf.jpg) |
| IMG-d790fabff9e4f3b9 | 左信息四卡右六景 | A+图 | [查看](previews/assets/Aplus/d790fabff9e4f3b95fe7f32ac924bb5d26e3c1cc5896f3e7bd83c4071554ed8e.jpg) |
| IMG-db2d994ce410219a | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/db2d994ce410219adfd67aa327429250707a07d047f58c78b833bb59dcab99eb.jpg) |
| IMG-df555a7c6f2f29f4 | 鼠尾草绿长盆与白栅栏 | A+图 | [查看](previews/assets/Aplus/df555a7c6f2f29f44cc98394161e64e52db7a0dc83d1f23918ae5970fc32ed55.jpg) |
| IMG-e1f1f810f8d4f59b | 日落露台餐桌两侧树 | A+图 | [查看](previews/assets/Aplus/e1f1f810f8d4f59b77423050ba94ebf3432820ba97e318a60aab0e07e25c0ab5.jpg) |
| IMG-e3bee4e1785c37b2 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/e3bee4e1785c37b2727d0669b3a9d887e7333b8294c2f71ce0682e90f938ae1b.jpg) |
| IMG-e643debab2c579cd | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/e643debab2c579cdfc543618cf5be280463cb182bd5327cbe0de861167052501.jpg) |
| IMG-e840aefb78f635f3 | 石阶陶盆与白扶手 | A+图 | [查看](previews/assets/Aplus/e840aefb78f635f3aa9cc1f9b9a0b90f7f0b691982b8b22a4c994b1b4332e053.jpg) |
| IMG-e8f3cf0277e79d9f | Supported hanging basket with architectural depth | 场景图 | [查看](previews/assets/collected/e8f3cf0277e79d9f2e4c878a7be18b932c3625d0814f28cbda41eef18f2e2ea4.jpg) |
| IMG-ec24f261809e50c7 | 宽幅 A+ · Aplus | A+图 | [查看](previews/assets/Aplus/ec24f261809e50c7120f3bcafcd1922c93c9b4635febc9d77c90eaa1176ed380.jpg) |
| IMG-ec41904ffa1a1cda | 白栏上的长椰棕花箱 | A+图 | [查看](previews/assets/Aplus/ec41904ffa1a1cdaf150b873e11af03134424dfe71cc2d7abad0367406ae94cb.jpg) |
| IMG-be1f4b9d9a623ef9 | 盆底轻接触阴影 | 场景图 | [查看](previews/assets/collected/20261016-shadow-01-light-contact-shadow.png) |
| IMG-44bb216e1d4bbb10 | 左前方柔和侧光 | 场景图 | [查看](previews/assets/collected/light-front-left.png) |
| IMG-bd05aa0023fa8671 | Reviewed brown-branch A+ 2 | A+图 | [查看](previews/assets/Aplus/bd05aa0023fa867142b652fbf17c8e3a4927e714a5f4c490d837e4972aef9859.jpg) |
| IMG-351eb8f5b26f3848 | Reviewed brown-branch A+ 4 | A+图 | [查看](previews/assets/Aplus/351eb8f5b26f384875664c3864ad6a55b18d880674f4e160251dafb30a73f5e9.jpg) |
| IMG-790e47f059ff8912 | Reviewed brown-branch A+ 1 | A+图 | [查看](previews/assets/Aplus/790e47f059ff8912d4cd0f068553dfebc9ba8c7cd816a86115cbb0ad8359704b.jpg) |
| IMG-12bd9ce6297e93e0 | Reviewed brown-branch A+ 2 | A+图 | [查看](previews/assets/Aplus/12bd9ce6297e93e0b8c553706fc96ad9d7281240ddc80e85c186390456dce676.jpg) |
| IMG-6bc344ab57d2809d | 门廊四盆纵深 | 场景图 | [查看](previews/assets/collected/6bc344ab57d2809dc6cd70468d8c35201697bfe03a122068df5ac8fb0ea7aa24.jpg) |
| IMG-5bab4f4015af2e8c | 窗边前后双瓶与顶部标题 | 场景图 | [查看](previews/assets/collected/5bab4f4015af2e8cfe65d5e7338a4b2ffcb246afd76920dff7b112312d802222.jpg) |
| IMG-a157d5e5805c3ec6 | 木桶花簇近景 | 细节图 | [查看](previews/assets/collected/a157d5e5805c3ec6cbd137ba43065a6d8bc21cd0c7c2b4c296abd993c79cdaac.jpg) |
| IMG-acd8f482f2f0a6b5 | 台阶三盆三角构图 | 场景图 | [查看](previews/assets/collected/acd8f482f2f0a6b5436eb85fc545f051859a6a0a1522808ba9db179515705dfa.jpg) |
| IMG-ec07e36f648058d7 | 门廊与窗边等分双景 | A+图 | [查看](previews/assets/Aplus/ec07e36f648058d7b56e063f8aa2260e65194c9669b0ae563e07307cfafba51d.jpg) |
| IMG-5e4164ceac2d6a2d | 阶前木桶与玻璃廊房双景 | A+图 | [查看](previews/assets/Aplus/5e4164ceac2d6a2db1cca636b512140e050d3dbbf350c3b3221d0a74f792f0d9.jpg) |
| IMG-f58244861a25f2a8 | 密集台阶与开阔门廊双景 | A+图 | [查看](previews/assets/Aplus/f58244861a25f2a8715a091ee498419ec42d983f6d22bba9e93cb405101c7b07.jpg) |
| IMG-083d6b1ba0096f67 | 色块标题加三圆尺寸细节 | 尺寸图 | [查看](previews/assets/dimensions/083d6b1ba0096f674c460c040ceb9c3e2dc36669c76796563a40ccd44b209620.jpg) |
| IMG-1d823fe99cb881a3 | 灰木墙白窗箱近景 | 场景图 | [查看](previews/assets/collected/1d823fe99cb881a395c3a804e81aed6788214226d1e1af9ddb78098ab116a256.jpg) |
| IMG-5abcd7125f0a9b2e | 风化木栏长箱纵深 | 场景图 | [查看](previews/assets/collected/5abcd7125f0a9b2ee67e5b80fcb271838fa69fb13aac5ed57da096e510fd3d29.jpg) |
| IMG-c2bf7287ba170fb0 | 黑双门前左右对称盆 | 场景图 | [查看](previews/assets/collected/c2bf7287ba170fb0fc56c2c3618d2cbb9527bb53b746634c7f4d775e205d14f7.jpg) |
| IMG-36ae408fabd1c687 | 红砖弧形花坛与园门 | A+图 | [查看](previews/assets/Aplus/36ae408fabd1c68746f07e627ef632c2cf66538af1dca6186c7f52d6bb9788d5.jpg) |
| IMG-708a8d4db1b261ae | 石墙吊篮与庭院纵深 | A+图 | [查看](previews/assets/Aplus/708a8d4db1b261aef8eee3032c46d17c63729b883faeb30517d560baa4f5bce8.jpg) |
| IMG-acbc3c7ae7753d65 | 右完整枝左三圆与弧形分割 | 尺寸图 | [查看](previews/assets/dimensions/acbc3c7ae7753d65eeccdbbcc14b8a079ec3c7326bcfc76f7991621b8bb93524.jpg) |
| IMG-18d6a1bc0a626ec2 | 四景用途加中央单枝圆窗 | 场景图 | [查看](previews/assets/collected/18d6a1bc0a626ec21076a99d83a66a126d1a06e95ab5843ca9b636dabf89af07.jpg) |
| IMG-6efc99400f4f0939 | 整栋白房前双盆 | 场景图 | [查看](previews/assets/collected/6efc99400f4f093969bfabefb14395d09b5fd5cff89247fa7dfb5095940f30e0.jpg) |
| IMG-1c33b81be09eaa68 | 砖墙白百叶窗箱 | 场景图 | [查看](previews/assets/collected/1c33b81be09eaa6868ca89f0a522b694a16c0745f2a07e7284bf083a4303d744.jpg) |
| IMG-b2823fdeccfd5813 | 房前双盆与顶部彩条 | A+图 | [查看](previews/assets/Aplus/b2823fdeccfd5813bea61cd930d737767533b9e502c67a4da162a61878e81586.jpg) |
| IMG-2f29cf6adb7c1aa0 | 白柱住宅前对称双盆 | A+图 | [查看](previews/assets/Aplus/2f29cf6adb7c1aa0221dde13dc0c819c3cce95bee82cfefe8c71840de0fadb14.jpg) |
| IMG-0540b251f953df13 | 后院餐桌三壶聚会 | A+图 | [查看](previews/assets/Aplus/0540b251f953df13fa1f58bc0e21ebbae22658378b9ac9387dde2b6117d88bf3.jpg) |
| IMG-08fc25704ae38113 | 前左多层盆组与远宅 | A+图 | [查看](previews/assets/Aplus/08fc25704ae38113b8f8f017ec7f5ec007163828d245b2be8735cd7064bfb415.jpg) |
| IMG-31eb04f516e00ab6 | 红砖白窗长箱 | A+图 | [查看](previews/assets/Aplus/31eb04f516e00ab6a411a290203b661f1a8869ef8e5ded314df2c140e9d47115.jpg) |
| IMG-32df8834d5f8b0dc | 四组配色数量清单 | 数量图 | [查看](previews/assets/dimensions/32df8834d5f8b0dc6dca6e1c3efeb2f29a510699f75f35eda943b5c96a0715a8.jpg) |
| IMG-2b3aaf42b5723a51 | 右整枝左双矩形尺寸 | 尺寸图 | [查看](previews/assets/dimensions/2b3aaf42b5723a5104e3167d5ad3e8e50f13fd19427bc2d8b0b8a6015eeb412e.jpg) |
| IMG-8df86ba93fd33b8e | 四格近拍配底部色条 | 细节图 | [查看](previews/assets/collected/8df86ba93fd33b8e3261f6dbfd4f115d1c2997f983fab6085038e48d64298ccf.jpg) |
| IMG-07a5f71b27007e69 | 白扶手前单盆与南瓜 | 场景图 | [查看](previews/assets/collected/07a5f71b27007e695c398c6c78f397fdf735b2eede12a93eb345b5ae8daba210.jpg) |
| IMG-9c626b70cd05bbe8 | 四种容器门前错落 | A+图 | [查看](previews/assets/Aplus/9c626b70cd05bbe8f1d8772505ce347b888e9ce8d02452850f0bbea37a4e59c6.jpg) |
| IMG-fea61325a4ddbfe5 | 浅石阶三盆三角 | A+图 | [查看](previews/assets/Aplus/fea61325a4ddbfe51ca51b588a4c7b6c3b5ffe7b847f53ec52020738a1fd4d29.jpg) |
| IMG-460f2962e3ef77e0 | 白墙长窗箱侧视 | A+图 | [查看](previews/assets/Aplus/460f2962e3ef77e0187f83a8ccaf419da23bdb048e6853b6b32ced94afb04ad9.jpg) |
| IMG-352aeb49487f6b31 | 白廊架单吊篮 | A+图 | [查看](previews/assets/Aplus/352aeb49487f6b31c03acd08d415955ee2021541328a26cf313bc496e149f142.jpg) |
| IMG-c6ba9da2469f7fe4 | 木廊三盆斜线纵深 | A+图 | [查看](previews/assets/Aplus/c6ba9da2469f7fe4e02f60904f584d57654e0e6acaa695825fcdf0990c8b949b.jpg) |
| IMG-c41185628f5dad93 | 深门前灰盆三角 | A+图 | [查看](previews/assets/Aplus/c41185628f5dad933a7ea857d00493fb867d1dd09df26f12e58e9ba3656635d8.jpg) |
| IMG-dd10aa78620d5d3a | 一大五小六窗用途拼版 | A+图 | [查看](previews/assets/Aplus/dd10aa78620d5d3a1e815d30e9ddfa3d8dc76b51e9b4c62ce923cd5b21b70df3.jpg) |
| IMG-4ed5677975406b0f | 红砖台阶底部对称双盆 | A+图 | [查看](previews/assets/Aplus/4ed5677975406b0f030737a18530dff7e96be011b2ad134088b467442a39722b.jpg) |
