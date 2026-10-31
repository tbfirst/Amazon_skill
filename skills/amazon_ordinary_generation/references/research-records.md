# 分区检查点与离线研究审计

采用与植株版一致的“先核全部身份→盘点各区段→实际看图/读原评→跨套比较→问答与迁移”顺序。使用独立浏览器上下文或标签页保护用户页面，逐区段保存进度；不用并发子代理作为前提。三平台、公开来源和访问恢复仍按[研究流程](research.md)执行。

## 检查点格式

每站点独立项目，在`research/amazon/<ASIN>.json`保存以下canonical结构，与同名MD的详细观察一致。示例只说明字段，实际值必须来自本项目：

```json
{
  "schema_version": 1,
  "campaign_mode": "new-set",
  "asin": "B000000001",
  "marketplace": "US",
  "identity": {"verified": false, "title": null, "variant": null, "final_asin": null, "source": null, "observed_at": null},
  "sections": {
    "gallery": {"status": "pending", "inventory_total": null},
    "aplus": {"status": "pending", "inventory_total": null},
    "review_photos": {"status": "pending", "inventory_total": null},
    "reviews": {"status": "pending", "sampling": null}
  },
  "visuals": [], "reviews": [], "attempts": []
}
```

new-set默认映射11ID。set-refresh必须写`campaign_mode: set-refresh`和实际`target_asset_ids`；新品明确改范围也写target_asset_ids及scope_override_reason。研究图可以没有目标映射，不把源图库图数变成生产预算。

- identity核实后才设verified=true，同时填标题、实际变体、落地ASIN、来源和实际读取日期；跳转不同ASIN时补resolution。没有核过身份不归属视觉/原评。
- 区段status用pending/observed/partial/text-only/access-blocked/not-observed/absent。除pending/observed外写reason；访问或观察过的区段写source/定位。absent需成功检查的依据，不能由空抓取推得。
- gallery/A+/买家图的inventory_total用实际盘点单元数或null；observed必须所有盘点项都有目视记录，未展开或页面总量未知就partial。A+注明按图片还是模块计数，项目内口径统一；品牌故事另列，不能当A+内容。
- 每条visual写id、section（gallery/aplus/review_photos）、observed=true、source、locator、observed_at、layout、lighting、shadow、transfer_to数组。实际没看图的候选只在待办/采集manifest中，不能造一条visual。未知光向明确写无法判断。
- 每条review写稳定id、kind=original、source、variant_scope、忠实summary和themes数组，可补日期/星级/筛选。平台AI摘要、Q&A和转述不计原评；同评论同主题只计一次。
- reviews observed/partial必须有sampling说明实际采样范围/排序/日期；页面总评论数与实际唯一原文N分开。详情页内嵌顶评和完整列表路线分别记录，列表受限但已有原评时总体记partial并保留原文。
- attempts写section/route/result及实际来源和时间；access-blocked必须有真实尝试。受阻不覆盖已成功区段，也不以搜索命中或读字幕当实际看图/播放。

旧项目camelCase简表继续留作历史，续跑时按实际已有观察迁入上述结构：not-attempted→pending，blocked→access-blocked（须保留尝试），not-present→absent（须有检查依据），customerPhotos→review_photos。只有计数而无逐图记录不能升级observed。采集器自己的媒体manifest不是研究检查点，不用同文件冒充两者。

## 执行与解释

```sh
python3 "<skill-root>/scripts/research_audit.py" normalize <全部ASIN或链接> --out "<project>/research/competitor-inputs.json"
python3 "<skill-root>/scripts/research_audit.py" audit "<project>/research/amazon" --inputs "<project>/research/competitor-inputs.json"
```

normalize仅按站点+ASIN规范化去重，不联网展开短链；所有用户指定来源均纳入，3–6是默认扩搜预算而非截断上限。--out保存原始输入登记且不覆盖已有文件。audit带--inputs时检查每个请求来源是否有研究检查点；遗漏直接报错，诚实的partial/access-blocked保留为缺口，不冒充完成。只传研究目录时显示“无法检查遗漏输入”的警告。报告可存research-audit.md；Python不可用时人工用同一输入登记逐项核对。

审计检查身份、实际观察标记、盘点/已看数、原评去重/主题计数、访问尝试和目标资产映射；0表示记录内部一致，不是来源真实、研究完整或用户已回答弹窗。1表示结构/对应错误，2表示命令错误。评论/词表缺失如实保留，不补造需求比例或销量结论。
