# Agent 参考知识库

套图项目先按[参考路线](set-layout-dialogue.md#先弹窗选择提示词参考路线)落实用户选择：本轮竞品、内置参考或明确混合。选竞品路线时不自动换成内置模板。图库不提供本SKU事实或本轮竞品、评论、关键词研究覆盖。

## 本地精简库

当前有138张内置图片（A+64、尺寸/细节14、场景60），另保留5张已回查原图的A+文字分支。234个卡片入口包括34个逐图导航和200个重写的独立模板；其中193个是上轮误删后恢复，另外2个光影导航改回具体效果任务，并恢复5个有独立用途的布局家族。10个A+产品组索引65个逐图分支。配图存在与否不决定模板质量。

依据[三类版式池](classified-reference-layouts.md)筛选少量图片，展示候选，打开所选全图，再读取提示词。脚本返回路径不等于看图；总览只能支持粗略结构，不能证明细字、精确光位、材质或真实SKU数量。`reviewed-layouts.json`维护129张场景/A+的可见结构（含5个外部回查文字分支）；`classified-layouts.json`维护14张尺寸/细节的双角色适配。

```powershell
python -X utf8 scripts/library_catalog.py search --kind image --design-group scenes --available-only --limit 6
python -X utf8 scripts/library_catalog.py show IMG-6bc344ab57d2809d
python -X utf8 scripts/library_catalog.py show IMG-880f4592b15af043 --asset-role DIM01
python -X utf8 scripts/library_catalog.py show IMG-880f4592b15af043 --asset-role DETAIL01
python -X utf8 scripts/library_catalog.py search --kind recipe --design-group aplus --available-only --limit 3
python -X utf8 scripts/library_catalog.py show APLUS-PRODUCT-B0FNBSD73T --image-id IMG-a92b1f33d2ceb429
```

`show IMG-ID`对单角色图返回`planningTemplate`；尺寸/细节须指定角色。`show 卡片ID`对逐图导航定位同一图，对独立模板返回`card.prompt`。独立任务的维护源是`curated-templates.json`；明确记录taskEn、必要输入、sourceEvidence与质量决定，刷新时生成正文。`show A+配方ID`只列分支，必须选具体图片才返回执行方向，不能用一张默认主视觉覆盖整组。A+仍按已审核主要产品身份分组，文件夹/品牌/ASIN不授权合并不同产品。

`search --kind series`及`show SET-ID`保留原图序和缺失位置；有部分参考不等于整套已随包。可用历史套图见[来源套图](curated-source-sets.md)。缺图只改变`localAvailable/resolvedFile`和可上传附件，不自动撤销已审核的文字模板。缺图分支明确标为文字适配，不能展示不存在的预览或声称本轮看过原图。改变过哈希的文件也不作为有效附件；重新纳入图片仍须审核。

无Python时读取[Markdown索引](../assets/reference-library/index.md)，按链接打开图片，再按图像ID读取JSON对应字段。不要全文加载大目录；检索无结果时拆分关键词或按角色搜索，不从文件名猜布局。

## 观察、提案与交付

只把图片中可辨的分区、主体、窗口形状、文字底板和明暗关系记为观察。精确坐标、相机参数、光位和新场景为设计建议，需在brief中区分。原图的数量、材质、功能、耐候主张及满盆效果不能迁移为本品事实。

选择后按[参考迁移](reference-fidelity.md)记录来源图/哈希、真实目视范围、保留项与调整项。需要新背景或原创方案时标为设计提案；无图不等于禁止创作，但不能伪装成观察反推。最终按[Lovart交接](lovart-prompts.md)把模板落实成独立英文prompt：准确附件、SKU、区块、文案、尺度和画布，移除内部ID、待填项与策划前言。

无字图不附带冗余字体指令；有字图按用户选择落实字族、层级及底板。保留窗口数/标题条/文字位置等已选结构；不凭旧“统一风格”强制改白底、左大右小或去底板。缺少已选细节窗所需实拍时解决素材缺口或讨论替代，不生成隐藏纹理填空。

## 模板质量筛选与参考范围

恢复的文字模板涵盖商品保真、光照/阴影、取景、容器融合、场景、真实细节、尺寸信息、素材准备及局部修复。它们供11图策划按需调用；MAIN和修复知识不自动增加主图、资产数量或授权生图。

本轮查阅外部library的规范、旧卡片、任务定义及196张相关参考总览，并打开尺寸/细节、花环、套盆等8张大图及4张原始图库图复查；另外回查5个A+来源。只为实际检查的可见内容记录来源；sourceEvidence的磁盘路径用于追溯，不是跨设备依赖或自动上传的附件。

`curated-templates.json`中的decisions逐项记录原343卡的恢复/合并/删除，recipeDecisions记录原50配方。OUT明确删除；已有拒绝结论、非植物灯饰、主题重复和含糊冲突任务不机械恢复。没有配图但输入明确、结果可执行的任务可以保留。没有生图实测的条目不标为效果通过。

## 可选外部库与研究回退

用户提供外部库时可用`--source-root`读取，版本目录可用`--manifest`，远程配置按[同步和按需取图](library-remote.md)使用。外部文字索引可能含未缓存图片；`textSearchable`并不代表图片存在或已看。先取所选图片并查看，外部来源须逐项核对后决定恢复、重写、合并或删除，不能整库覆盖本地维护结果。续跑记录实际`libraryVersion/manifestHash`。

本轮竞品经过合理恢复仍受限时，展示2–3个兼容的本地真实参考，继续必要的布局对话；只对缺口使用LIB来源，保留已成功的V研究。无参考图可支持的方向只能作为明确的原创提案，不补造竞品观察、评论或关键词结论。

移图/删图后运行`python -B scripts/refresh_local_library.py`及`--check`，只刷新可用性和索引，保留质量合格的文字。新增图先目视收录并写逐图布局；刷新不代替审核。由旧外部库重建时先输出到独立目录并对照本地维护源，避免覆盖新布局和删除选择。

## 增量收录与识别

用户已要求持续丰富库；今后每次本技能进行获授权的竞品研究时，收录该任务实际收集的新公开参考。这不是后台无限抓取，也不自动创建定时任务。抓图接入见[competitor collection](competitor-collection.md)。

以下为有可写外部图库时的维护流程，示例路径属于维护者环境。普通使用者无需运行这些命令或搭建展示页；未配置外部库时将新图及观察保存在当前项目增量包，内置库照常用于检索与版式选择。

```powershell
python -X utf8 scripts/reference_ingest.py scan --library "E:/Amazon_generate/plant/library" --source "本次抓图根目录" --report "项目目录/ingestion-audit.json"
python -X utf8 scripts/reference_ingest.py contact-sheets --library "E:/Amazon_generate/plant/library" --source "本次抓图根目录" --output "项目目录/review-sheets" --report "项目目录/image-inventory.json"
```

逐张识别新图；编号总览可做第一轮分类，复杂信息图、细小层级及最终入选图再开大图。写visual-observations.json，其images以完整SHA-256为键，每项至少有status、reviewMethod、imageTypes、overview、layout、copyIntegration、lighting、shadows、transferable、limitations、recipe，并明确reuseDecision（accept/reject/hold）和qualityReasons。A+另写principalProduct（id、label、reviewStatus=reviewed或confirmed、reviewMethod及范围）；身份未知或冲突不能因已accept就自动进入产品模板。只有商业构图清晰、主体突出、可迁移结构有意义的图才accept；低清、构图混乱、杂乱实景、已确认买家秀不进入可复用配方。不能凭随拍风格断言其买家来源；来源不明就如实标注。裁切细节图可作为细节参考，不冒充完整商品主图。只记真正看到的内容；observed-overview与observed-full区分范围。扫描/下载只是pending，脚本不能代替视觉模型。

```powershell
python -X utf8 scripts/reference_ingest.py sync --approved-only --library "E:/Amazon_generate/plant/library" --source "本次抓图根目录" --observations "项目目录/visual-observations.json" --report "项目目录/ingestion-result.json"
python -X utf8 scripts/library_catalog.py import --source-root "E:/Amazon_generate/plant/library" --destination "assets/reference-library" --selection "assets/reference-library/selection.json"
```

图库同步后还须刷新展示页：在本机库目录运行 `python -B -X utf8 export_catalog.py`，再运行 `node verify_gallery_logic.cjs` 和 `python -B -X utf8 verify_library.py`。`index.html` 合并原模板、布局家族和可复用图像索引，以相册展示同配方多张样例；同ASIN/变体的已收录图按原图序提供系列入口。只更新JSON或便携快照不会自动重建HTML。受限/拒绝图继续排除，系列是已放行部分图序，不声称完整竞品套图。离线JSON仍是agent检索入口。

sync只复制缺失原图，按文件SHA与含透明度的解码像素去重；相似图只标候选，不自动合并颜色或布光差异。同图新增来源合入aliases，其occurrences保留源ASIN、product_description/brand_story、模块序号和模块内图序；重复运行不创建第二份配置。A+的aplusTemplateEligible只说明图像审核及唯一已审核身份同时成立，不证明已看全模块或有平台上传资格。aplusNativeText独立保留，不自动烘焙为图片文字。只提交新增/修订图片的完整观察即可，旧观察按哈希合并保留；空images不表示清空。语义校验通过后才导入，JSON逐文件原子替换；这不是跨文件数据库事务，运行中断后重跑校验。原图不改写，历史审核限制保留；未通过示例可作为有限制观察档案，不能升格为合格成图。临时断开的抓图来源不影响已入库原图；库内已索引原图丢失/被换则停止同步，先恢复或明确处理记录，不能静默保留“已观察”状态。坏manifest记录来源警告并继续读取有效图片，无法解码的图片保持pending，总览显示占位。库不可写时先存项目增量包，明确尚未写回并继续可完成研究。

approved-only仅复制明确通过视觉审核的新图；拒绝/待定图只保留 `screening-report.json` 的来源与理由，不复制图像字节。已在库内的历史档案保留，但 `reuseEligible=false`，默认检索隐藏；只在诊断时用 `--include-restricted` 查看。原图库删除前须逐图核验独立副本的哈希，并排除运行及重建脚本对旧目录的依赖，不能仅凭aliases存在就宣称可删。

图像检索依据实际观察的主题、布局和光影，不把统一禁用词、历史文件名或路径当作已看见的内容。pending只按元数据检索；结果同时返回审核限制和目视范围。入选前检查原图，不能把排序靠前当成质量认证。

刷新便携快照只读取原库、更新指定目标并记录哈希，不等于逐图检查。没有可靠URL就保留本地来源和缺口，不猜ASIN。用户认可的实际成图另记验收范围，不能把竞品参考当自己的实测成品。

本地发布维护使用`selection.json`选定随包图片；运行`refresh_local_library.py`后，活动图像和提示词也限定为现存图片，保留套图中的缺失图位。外部完整库与本地精简库分别维护。独立资源构建另用`publication-policy.json`选择文字/预览/原图发布范围；默认仅文字，原图需维护者明确放行相应范围。不能按下载数自动放行原始amazon_scrape全部图片。退役的DSTYLE-01–08与`assets/layouts/`线框不再进入发布快照或默认模板检索；重建不能把它们带回。`bundledAssets`记录实际随包文件与哈希，`series`保留源顺序，`images`保留图像观察与唯一的逐图角色提示词。原始采集与维护者图库保持不变；安装目录不可写时项目增量留在输出目录，不要求普通使用者拥有作者的本机维护环境。
