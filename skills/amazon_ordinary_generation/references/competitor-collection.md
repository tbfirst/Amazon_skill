# 完整图库与 A+ 采集

访问失败时先按[公开Amazon访问诊断与恢复](public-amazon-access.md)识别宿主网络权限与网站门槛，再继续本节；有效缓存优先，登录/验证码不绕过。

迁移绿植版的逐区段采集与核查方法，遵循 [项目媒体存储](media-storage.md)。允许下载图片、保存manifest与恢复点，但不写入技能包。优先使用已安装的外部采集器；不可用时使用本技能的浏览器采集入口，依赖缺失要明确报告。

1. 用户给出的ASIN优先核查；先核站点、请求ASIN、当前子ASIN、颜色和规格。历史ASIN记录只辅助去重；先检查当前项目媒体是否存在及区段覆盖，缺图补采。仅用户明确要求不再访问的ASIN才禁止重采。
2. 发现实际可用的 `amazon-variant-gallery-scraper` 时读其SKILL及入口，核实gallery/A+支持及安全启动参数。按其实际入口执行 `scripts/scrape.sh ASIN --out <项目研究目录>`，允许落盘；支持时可用 `--aplus-only` 补采。遵循实际锁与变体规则，不强制解锁。未安装时读下方内置采集入口。
3. 在正常商品页逐项打开全部静态缩略图及放大图，保留页面顺序，核对当前变体。若正常页面数据提供 `colorImages`、`hiRes`、`large` 或 `data-a-dynamic-image`，仅取当前变体的实际候选，逐图查看。缩略图、URL列表、标题文本不能替代看完整图；视频另列。
4. 正常滚动至商品描述/A+，等待懒加载，在实际A+容器内依模块顺序查看图片、切片与原生文字。品牌故事、比较模块、广告推荐分开；检查横向轮播的可达页。不能抓完整页媒体池后全算A+。
5. `aplus`为空必须继续检查`aplusOther`及标准模块；970宽、方图、竖图不因比例而排除。宽度≥1200且比例2.30–2.50只是宽幅参考筛选，绝不是A+存在判断。模块来源不明记unknown；混合商品逐图核主体，不因同ASIN就合并身份。
6. 正常显示URL与明确提供的原图可下载到项目目录后解码；核真实尺寸、格式、可读性，失败退回显示图，不猜隐藏接口。相同媒体可去重，但在manifest保留每个模块的provenance、URL和实际文件；下载成功与目视确认分开。
7. 对gallery、A+、品牌故事分别记录发现数、实际查看数、反推数、变体范围、加载状态、失败原因及下一步。只有完整遍历已加载的对应区段、所有可见静态项都看过才标该区段完整；页面总量未知就标partial。成功检查且确无区段才记not-present；空抓取不是无A+。
8. 每个失败区段按research.md有限恢复：一次直链、一次可用正常浏览器、一次精准公开搜索/官方关联页。真实登录/验证码门槛停止该路线。保留已读区段，必要补图在聊天请求；未看到的布局只能标原创提案，不能假称竞品反推。

为本SKU策划图片时，首批可用画面完成实际看图、足以比较方向后，立即转入 [采集后的参考选择弹窗](discovery-layout.md#采集后的参考选择弹窗)：先展示真实候选与覆盖，再实际调用提问工具确认尚未决定的参考路线、来源与程度。不要等全部ASIN或三平台研究结束，也不要从“图片已下载”直接跳到11条prompt。明确回答/委托的范围沿用；待答期间继续独立采集与源图分析。

逐图反推背景、机位、主体比例、分区、文字精确位置与层级、色彩、装饰和光影，选定参考后再形成DIM/DETAIL/SCENE/A+的确定映射。研究套图保留源顺序，生产套图仍默认六张附图加五张A+，不得以抓取图片数改变交付数量。

## 批量输入与逐竞品完成条件

先保留输入，再抓取。将本轮**所有**用户链接按站点+ASIN规范化去重，原始追踪链接留在inputs数组；同父不同子ASIN不能悄悄删掉，标关联变体。短链先正常展开，尚未解析的链接写入discovery待办，不丢弃。3–6只限制默认自主扩搜预算，不限制用户指定范围。

```powershell
python "<skill-root>/scripts/research_audit.py" normalize <全部ASIN或完整链接> --out "<project>/research/competitor-inputs.json"
python "<skill-root>/scripts/collect_competitors.py" --inputs "<project>/research/competitor-inputs.json" --out "<project>/research/competitor-media"
python "<skill-root>/scripts/research_audit.py" audit "<project>/research/amazon" --inputs "<project>/research/competitor-inputs.json"
```

输入登记已存在时保留旧版，用新revision记录新增范围，不以成功结果倒推/缩减输入。批量入口按输入表逐个调用正常浏览器采集器，独立输出，单个失败/超时仍继续后续来源；每完成一项保存batch-manifest，未执行项保持queued/running。它不抓原评、不做目视，也不把captured-partial标成整套已读。可用外部采集器时同样按输入表遍历，遵循其真实并发/锁约定；不要两个采集器同时重复抓同一来源。

研究检查点与媒体采集清单分开：对输入表的每个唯一来源创建`research/amazon/<ASIN>.json`（多站点分目录），gallery/aplus/review_photos/reviews分别登记盘点、实际查看和恢复路线。只有文本读取不算画廊采集；一个成功不能代表全部。输出逐竞品覆盖表时列明请求/落地ASIN、变体、图序、下载/实际查看数量、A+模块、原评N及失败项。

首批画面可讨论后允许进入选参考，但其余输入仍推进至实际完成、已有可复用证据已检查，或有限恢复耗尽；不能因为主参考已选就跳过其他指定来源。用户明确移除某来源时才修订范围，保留决定。审计中的“存在检查点”不等于“采集完成”，仍如实展示partial/access-blocked。

## 内置正常浏览器入口

以下命令从项目工作区执行，不从技能安装目录执行；将 `<skill-root>` 替换为实际安装绝对路径。外部采集器不可用时，使用 `python3 "<skill-root>/scripts/collect_competitor.py" --check` 检查依赖。此脚本需 Python Playwright 与 Chromium；在允许安装依赖的环境执行 `python3 -m pip install playwright` 和 `python3 -m playwright install chromium`，不得将依赖或浏览器打包进skill。缺依赖或浏览器启动受限时明确报告，不声称已采集。

执行：`python3 "<skill-root>/scripts/collect_competitor.py" ASIN --out "<project-root>/outputs/<product-slug>/research/competitor-media"`。有图形环境时可加 `--headed`。脚本使用正常浏览器、新上下文、启用沙箱；逐缩略图切换、有限滚动、从A+容器收集媒体，不绕过登录或验证码。

输出按ASIN及运行时间隔离，manifest保留来源和下载结果，不覆盖旧结果。该轻量入口仅捕获当前DOM可见候选，不保证所有变体、横向轮播和懒加载模块齐全；状态最多partial。需人工/视觉工具解码检查图片、核变体、打开轮播并逐模块补查，再按实际覆盖更新研究记录。它不会把下载标成已看，也不按宽高过滤标准A+。没有DOM模块边界时moduleIndex为-1，表示unknown。

浏览器因验证码停止后，可用公开检索已提供的页面缓存补充研究：记录缓存时间，从明确的colorImages当前变体数组和A+容器定位媒体，逐图检查；不是绕过验证码重试同一浏览器路线。缓存不是实时完整页面，不能写当前完整覆盖。若工具仅返回HTML文本，不能把图片URL当成已看图片。已有Chromium可显式传 `--browser-executable <实际路径>`；不得通过关闭浏览器沙箱解决启动失败。
