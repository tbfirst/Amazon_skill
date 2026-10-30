# 研究种子与可复用反推配方

研究日期：2026-10-29（Asia/Shanghai）。这是建立技能的有界研究，不是任何未来SKU的竞品完成报告。没有用户SKU，本页不提供本品性能结论、需求比例或热销排名。仅一个Amazon A+图已实际打开目视，其余按实际覆盖记录；没有完整观看TikTok/YouTube视频。没有内置11张竞品原图库。

## AMZ-SEED-01：狗笼尺寸选择信息图

- [Amazon商品 B09G4KS7FY](https://www.amazon.com/dp/B09G4KS7FY)，公开页面HTML可读，A+区段定位到一张1464×600图片，随后下载并实际打开查看。这里只核了这个A+视觉，不代表整套gallery或评论已读。
- [实际查看的A+原图](https://m.media-amazon.com/images/S/aplus-media-library-service-media/8d8c4db7-afd7-44c5-88ee-a9b49655c23d.__CR0,0,1464,600_PT0_SX1464_V1___.jpg)，原图来源是该商品的From the manufacturer区段。未来使用前重新核对可访问性与产品适配；本包不包含原图字节。
- 可见结构：白底，上方居中的橙色标题；中上部橙色犬只轮廓与深色水平/垂直测量线；下半部六列尺寸表，浅灰/淡奶油交替列底，各列上方橙色犬轮廓；行标题在表左；外侧宽留白。这里是平面信息设计，不是室内狗笼照片。
- 值得迁移：先教测量，再呈现选择信息，按图示→表格的阅读顺序降低理解负担。
- 限制：不能抄用源表尺寸、犬种适配、系列SKU或品牌文案；六列表格不证明本品有六个尺寸。原图小字密度也是需要适配的弱点，不能仅因参考存在便认为移动端可读。

下段是**观察结构的英文反推练习，不是适用于未知SKU的READY提示词，也不是原作者提示词**：

```text
Reconstruct the information hierarchy as a flat 1464 × 600 landscape infographic on white. Place a centered orange headline at the top. Below it, show an orange side-profile dog outline with dark horizontal and vertical measurement guides and circular endpoints. In the lower central region, arrange a six-column comparison table with alternating pale gray and pale cream column fills. Place a small orange dog outline above each column, progressing in illustrated size across the row. Put compact row labels to the left of the table. Use dark, restrained sans-serif typography and broad exterior whitespace. Keep the measurement diagram distinct from the selection table. This is a structural study only: do not reproduce the source brand, numbers, breed recommendations or commercial claims. Resolve all final copy and supported product data before producing a customer-facing asset.
```

应用到单尺寸狗笼：保留“测量→判断”的结构逻辑，改成一张经确认的内部空间卡；需本SKU净空/门洞数据和正确动物测量方式。只有外尺寸时只做外尺寸，不把它换名为内部空间。应用到相框：可借此分离照片尺寸与外框尺寸，但犬只轮廓和多尺寸系列均不沿用。以上是D提案，不是源图观察。

## AMZ-SEED-02：同系列官方说明书文字

[Amazon托管说明书](https://m.media-amazon.com/images/I/B1noytHSzXL.pdf)：实际读到包含B09G4KS7FY等型号的英文文字部分，未成功截图检查所有装配图。材料提示“门锁”“折叠”“托盘”和犬只空间是需要分开核对的任务；它们不意味着每种狗笼都具备相同结构。该资料只为所列型号提供说明，不能替我们的SKU补证。

## TT-SEED-01：TikTok Shop钉式挂钩

[商品页](https://shop.tiktok.com/us/pdp/non-trace-picture-frame-hooks-30pcs-abs-wall-hangers/1732605678712361916)：搜索索引中读到卖家商品文字，直链返回cache miss，浏览器尝试超时；实际未查看完整图集或短视频。coverage=`search-only`，contentType=`shop-text`。

文字提到小钉与锤击安装，同时使用“non-trace”营销表述，并列适用/不适用表面。可形成“安装机制必须先分流、限制条件不可丢”的研究问题，不能据此证明无损墙面，更不能为我们的粘贴挂钩照抄锤击动作。页面AI生成Q&A不算用户评论。

可提议一张安装接触近景，但由于未看见来源画面，必须标为原创D方案，不反推其机位/颜色/镜头。后续需实际原图或视频才能升级到visual-observed。

## YT-SEED-01：Command安装教程

[How to Apply Command Hooks (Short Version)](https://www.youtube.com/watch?v=29EhadAx88s)，检索显示作者3M Malaysia、发布2020-03-30。实际读到标题和描述中的清洁、贴条、按压与滑动步骤；直链读取失败，浏览器环境此前连续超时，本轮未继续同类重试。coverage=`text-only`，videoViewed=false；没有可用真实时间戳，不声称看过视频。

可推导需要把准备、贴合、固定分开核实的工作流；不能将此品牌的胶条/滑动机制、等待时间、承重或无痕声明转为本SKU事实。非同机制产品不用该操作路线。创建静态步骤图前还需本品说明书和对应状态图。

## 三个文本配方（原创，不是已看过的竞品画面）

|配方|信息结构|放行条件|必须避免|
|---|---|---|---|
|FRAME-FIT|主视图标外框，第二个明确标为同款的视图显示照片/卡纸适配，底部精简说明|外框、照片/窗口和背部支持状态有依据；实物重复仅表示不同视角|把照片尺寸写成外尺寸、虚构桌摆/墙挂兼容|
|HOOK-CONTACT|一张真实安装面近景加一处接触细节窗，必要时附依据充分的步骤|机制、表面、连接件、等待和载荷条件均按该图需要已确认|用装饰遮安装点、重物暗示高承重、混用钉式/胶式|
|CARD-INSERT|同一平面可读卡片插入口，副区显示已核外部/内部尺寸，生活背景低显著|卡套细分类、入口/内腔、卡片厚度及随货附件确认|以透明窗口大小代替入口兼容、凭空加伸缩绳或RFID功能|

使用文本配方前仍需完整逐图决定与独立提示词，不能将表格本身作为11图交付。以后新增真正看过的参考时，保存来源/视图/准入理由，不把未审图自动写入可复用图库。
