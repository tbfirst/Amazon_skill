# 研究检查点与离线检查

脚本只整理输入和检查已记录的数据；不访问 Amazon、不下载图片、不模拟浏览器、不证明来源真实。浏览仍使用当前宿主提供的工具。Python 3.10+ 标准库即可，无需安装包。无法运行脚本时按同一字段人工核对，不因脚本缺失停止研究。

## 输入标准化

在 skill 目录运行（实际执行时使用脚本的绝对路径）：

```sh
python -X utf8 scripts/research_audit.py normalize B0FB3F3TLM "https://www.amazon.com/dp/B0FB3F3TLM?th=1" B0H2LZNL5H
```

输出按“站点+ASIN”去重并保留原始输入；裸 ASIN 默认 US，可用 `--marketplace` 选择脚本支持的站点。未知站点人工处理，不猜成美国站。短链接必须先由正常浏览器解析，再交给脚本；不使用非 Amazon 页面或 URL 查询串中偶然出现的 ASIN。脚本不改输入文件。脚本中的例子是工具示例，不是实际项目的默认竞品。

## 每竞品一个 JSON 文件

将 `competitors/<ASIN>.json` 作为续跑检查点，与同名 `.md` 的详细观察保持一致。一个研究项目只放一个站点；多站点按子项目分开，避免相同 ASIN 覆盖。首次可复制以下结构，再用实际观察填充；未知项保留 null/pending。

```json
{
  "schema_version": 1,
  "asin": "B0FB3F3TLM",
  "marketplace": "US",
  "identity": {
    "verified": false,
    "title": null,
    "variant": null,
    "final_asin": null,
    "source": null,
    "observed_at": null,
    "resolution": null
  },
  "sections": {
    "gallery": {"status": "pending", "inventory_total": null},
    "aplus": {"status": "pending", "inventory_total": null},
    "review_photos": {"status": "pending", "inventory_total": null},
    "reviews": {"status": "pending", "sampling": null}
  },
  "visuals": [],
  "reviews": [],
  "attempts": []
}
```

字段约定：

- `identity.verified` 仅在实际核对商品和变体后设置 true，填标题、变体（无可选变体也要说明）、落地 ASIN、页面来源和 ISO 日期时间；历史观察只知日期时保留日期精度，不编造时间。请求/落地 ASIN 不一致需 `resolution` 说明核对结果；无法确定时仍为 false。
- `sections` 状态：pending、observed、partial、text-only、access-blocked、not-observed、absent。除 pending/observed 外需 `reason`；观察过或访问过的区段需 `source`（URL及区域定位）。`absent` 表示实际检查后未发现，不是没有检查。
- `inventory_total` 仅填写实际盘点的视觉单元数。图库单位为独立静态图；A+ 可选图片或模块作为单元，先在 `reason`/`scope` 写清，整项目保持一致。尚未展开/加载完成时用 null。observed 要求盘点单元全部有观察记录；partial 报告实际观察数，不凑齐。
- `visuals` 每项：`id`、`section`（gallery/aplus/review_photos）、`observed: true`、`source`、`locator`、`observed_at`、`layout`、`lighting`、`shadow`、`transfer_to`（适用的11张图ID数组，可为空）。没有看过的图只放区段待办，不创建视觉证据。光向无法确定时写“无法从该图可靠判断”，不编值。
- `reviews` 每项：`id`（平台ID或人工稳定定位ID）、`kind: original`、`source`、`variant_scope`、`summary`、`themes` 字符串数组；可补日期、星级、筛选条件。只存实际读过的原文的忠实摘要，平台 AI 摘要另写 `.md`，不进入此数组。找不到平台ID时相同可定位正文复用同一人工ID，不能每页重新编号。
- 原文区 observed/partial 需要 `sampling` 说明排序、筛选、日期与抽样范围。这里 observed 表示计划采样步骤完成，绝不表示读过所有历史评论。脚本从独立记录导出 N 和主题 n，一条评论对同一主题只计一次。
- 评论来源路径在同名 `.md` 分列“详情页内嵌顶评”和“完整列表”的状态、来源与理由；JSON复用 `sections.reviews.sampling` 和 `attempts` 记录，不新增必填字段。`attempts.route` 可写 `dp-top-reviews` / `review-list`，附实际URL/区域与结果。已读内嵌原文而完整列表受限时，`sections.reviews.status` 用 `partial`，在 `reason` 写列表缺口并保留 `reviews` 数组；不把总体写为 `access-blocked`。公开采样范围完成且无待补范围时可用 `observed`，不足30条不是缺口本身。
- `attempts` 每项至少 `section`、`route`、`result`，建议附时间和页面定位。access-blocked 必须有一次真实访问记录；不能把尚未尝试写成受阻。

仅用用户公开产品信息研究，检查点不保存账号、Cookie、个人地址或无关用户资料。

## 检查与汇总

```sh
python -X utf8 scripts/research_audit.py audit /absolute/project/competitors
```

脚本把 Markdown 报告写到标准输出，不改已有研究文件。通过宿主文件工具将结果保存为项目的 `research-audit.md`，避免 Windows 重定向改变编码。

退出码：0=记录内部一致（仍可能有缺口）；1=发现结构/证据对应错误、无法读取记录或目录中无记录；2=命令或未能进入审计的错误。不要把0解释为研究完成、政策通过或证据真实。检查报告会区分 errors 和 gaps/warnings；缺少评论但如实记录登录限制是可接受的草案状态。

脚本检查的主要问题：重复竞品、混站点、身份未核实却归属视觉、未目视却写视觉证据、observed 与盘点数不一致、重复评论、AI摘要混入原文样本、主题重复计数、无恢复记录就称受阻、映射到11张图之外。跨 ASIN 重复评论ID会告警；跨竞品汇总时还需人工去重同一原文并核对父子变体。

通过检查后，主代理仍需人工核对来源是否真的支持结论、截图是否读清，以及 prompt 是否把竞争陈述偷换为我方事实。脚本不解析或运行网页内容，也不能验证自然流量。
