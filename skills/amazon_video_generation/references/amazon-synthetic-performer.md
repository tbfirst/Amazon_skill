# Amazon写实AI人物披露与元数据

本页在规划人物素材或交接Amazon最终发布文件时读取。核查日期2026-11-01；适用依据是Amazon官方公告，不把社媒转述当作“所有AI图片都须标记”的规则。

## 已核范围

Amazon的[官方公告](https://sellercentral.amazon.com/seller-forums/discussions/t/4963c253-80c3-41a7-9e68-5c262bd06582?mons_sel_locale=de_DE&pageName=US%3ASC%3ATrim-seller-forums%2Fdiscussions%2Ft%2F4963c253-80c3-41a7-9e68-5c262bd06582)明确：全球站点的listing和A+中，含写实AI生成人物的图片或视频，在上传前用支持IPTC/XMP的工具将`contains-synthetic-performer`写入文件的XMP `dc:subject`。Amazon在适用情况下显示披露；该标签不是画面水印或商品关键词。

|最终媒体内容|本技能处理|
|---|---|
|完全由AI生成、看似真人的人物，包括画面中可见配角|按要求标记；是否主角不改变人物的生成来源|
|仅真实人物，即使经过AI编辑|公告列为不需要此标签；保留人物来源事实，不能把凭空生成演员算作真人编辑|
|仅商品、动物、植物或无人布景|不因使用AI就添加人物标签|
|仅非写实人物，或公告列举的电影／游戏等表现作品角色|公告列为豁免；不等于获得角色使用权|
|只露AI生成的写实手／局部身体，或来源无法区分|所读公告未细化身体裁切边界，不能自行宣称“没露脸免标”；记录待核，针对实际成片查当前官方说明。确认是写实合成人体时建议保守标记，明确这是执行建议，不冒充官方新增条款|

真人参考图不自动证明输出人物仍是真人；按实际生成方式和最终文件判断。未知来源不靠肉眼“像真人”猜测。其他广告版位使用该版位当前规则，不拿商品详情页流程替代广告审核。

## 前期包与发布文件分开

本技能默认只交即梦参考图和提示词，不产出最终视频。把预计人物来源、标签是否适用、待核点及成片导出后检查写入现有分析说明书/README；没有最终文件时标“发布元数据待处理”，不能称已完成标记。

分镜表和宫格是即梦输入，**给输入图加标签不能保证生成的视频继承标签**。不把标签词放入TXT、格下说明或成片字幕，不批量给所有内部参考图打人物标签。若某张图另被用户选为Amazon买家可见素材，再单独按该图实际内容处理。标签也不能补救虚构商品功能或错误结构。

## 最终文件的写入与复核

按[官方操作说明](https://sellercentral.amazon.com/help/hub/reference/external/GFXHCHYZRGJRBZA5)和实际文件格式选择支持工具。应写入嵌入式XMP `dc:subject`关键词列表，保留原有关键词；文件名、普通备注、Windows“主题”、仅侧车`.xmp`或MP4普通comment不等于这个字段。

若使用ExifTool，先在交付目录外的最终文件副本中操作。以下以已确认适用的`final.mp4`为例；先读取，缺少该值时才追加，已有则跳过，避免重复关键词：

```bash
exiftool -G1 -s -XMP-dc:Subject final.mp4
exiftool '-XMP-dc:Subject+=contains-synthetic-performer' final.mp4
exiftool -G1 -s -XMP-dc:Subject final.mp4
```

第一、三行是检查，第二行仅在确认缺少时运行。ExifTool默认保留原文件备份；备份留在工作区，不能塞入既定精简交付包。图片换为实际文件名。此处是操作说明，不默认安装软件或批量修改用户库；实际运行前核工具版本对该容器/格式的写入支持，失败时不能仅因命令已运行就标完成。

在**最终拼接、转码、压缩和导出完成后**读取真正准备上传的文件，确认`XMP-dc:Subject`列表含完整关键词，其他关键词仍在，文件正常解码播放。再次导出可能丢失元数据，需重新检查；原参考图、前一版MP4或侧车通过不代表最终文件通过。不承诺Amazon所有位置都会显示提示。

Amazon[工作人员的补充说明](https://sellercentral-europe.amazon.com/seller-forums/discussions/t/cdb33a1c-a36c-4fcb-8dde-b180fe503e92)说明A+上传可使用“AI-generated people”选项由平台加标。仅在实际A+入口可见且适用时采用并记录，不推定其他上传入口也有此选项；普通listing文件仍按要求嵌入元数据。不同资料对生效日期/旧素材追溯有差异，本技能不写未经确认的统一历史截止日。

技术字段参考：[ExifTool XMP-dc](https://exiftool.org/TagNames/XMP.html#dc)说明Subject为可写多值字段；[ExifTool命令说明](https://exiftool.org/exiftool_pod.html)用于追加与备份行为。只有实际处理并回读的文件才可在README记录“已验证”。
