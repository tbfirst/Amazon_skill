# Amazon公开竞品页访问诊断与恢复

在商品页/图片读取失败、浏览器超时或本地采集依赖缺失时读取。先复用项目缓存；网络故障、工具故障和网站访问门槛分别处理，不由一个工具失败推断商品下架或无图无评。

## 识别失败层

- web工具的Cache miss只说明该读取通道未取得页面。正常浏览器若超时，可用本地HTTP客户端读取同一公开URL；缺Playwright/Chromium不影响已安装requests或标准库的公开HTML读取。不为此默认安装浏览器依赖或修改全局网络设置。
- 本地请求若报WinError 10013、socket permission denied等宿主网络权限错误，记录原错误。在宿主支持时，通过exec_command的sandbox_permissions=require_escalated申请对原公开URL的一次联网验证；遵循实际审批结果。这是宿主联网授权，不是绕过网站限制，也不假定所有环境都允许或都需要提权。
- HTTP 200仍须检查最终URL、标题和正文：/ap/signin或Sign in是登录页；Robot Check/validateCaptcha是验证门槛。403/429/503、超时分别记录，不当成成功，不通过换账号、代理、cookies或伪装反复重试。

## 最小公开验证

用已安装客户端读取本次用户指定ASIN；不取凭据、私有profile或登录态。以下示例只读详情，不自动提权：

```python
from pathlib import Path
import requests

asin = "USER_ASIN"  # 替换为实际已登记的ASIN
out = Path("PROJECT_RESEARCH_DIR") / asin / "run-YYYYMMDD-HHMMSS"
out.mkdir(parents=True, exist_ok=False)
r = requests.get(f"https://www.amazon.com/dp/{asin}", timeout=35)
(out / "detail.html").write_text(r.text, encoding="utf-8")
print(r.status_code, r.url, len(r.content))
```

先检查依赖存在；缺requests时可用标准库urllib完成同类公开读取，不要求安装新包。固定ASIN示例不进入真实采集清单。若需要宿主联网授权，只对公开读取命令走实际审批，不修改安全设置或把审批当作登录授权。

## HTML与图片的使用边界

1. 保存请求/最终URL、状态、标题、时间、原始HTML及失败记录；新运行用独立目录，不覆盖成功缓存。确认请求ASIN、落地ASIN、当前颜色/尺寸/组合。
2. 仅下载正常HTML/DOM明确引用的图片URL；用当前变体colorImages、hiRes/large、data-a-dynamic-image及实际A+容器定位。全页URL池只能标candidate，可能含其他变体、缩略/原图重复、广告、跨售、品牌故事；不得直接计作当前图库或A+模块。
3. A+需保留区段、模块/轮播顺序和原生文字；不只按URL含aplus或宽高比判断存在。静态HTML无法解析模块时标unknown/partial，必要时用正常浏览器补查。
4. 项目目录保存URL→文件映射、真实解码尺寸、格式、哈希及原始出现位置。下载并解码成功仅表示文件可读；实际看图、逐图分析、用户选中分别记录。静态HTML恢复不等于动态页面完整覆盖。

## 评论单独判断

先检查详情页公开内嵌原评，再尝试完整评论列表；两条路径分别记成功/失败。review-body/customer_review等标记可辅助发现，未命中不证明商品没有评论。完整列表跳登录时保存最终URL和页面性质，停止该路线；需要用户正常登录浏览器的可见内容或用户提供导出时，再取最小缺项，不索取密码或cookies。不以总评分、AI摘要、搜索摘要代替已读原文；样本N按实际取得并去重的原文数，未取得则N=0且不解释为零需求。

## 复用和停止

原路径失败后，每个明确不同层级做一次有依据验证；宿主网络错误可在审批允许后对原URL验证一次。遇登录/验证码或相同站点限制则停止，不用轮换headers/代理或无界重试。已有有效缓存优先，不为检查可用性重复下载全部素材。恢复任一区段后更新先前access-blocked记录，并保留失败历史；不让旧失败覆盖新成功，也不把图片通路成功宣称为评论已恢复。

验证案例：2026-11-02 Windows宿主中，默认requests报WinError 10013；获准联网后三个公开Amazon详情页及实际引用图片成功读取，完整评论列表仍跳Sign in。此为诊断示例，不保证其他ASIN/时段结果，也不携带项目商品图片或硬编码项目路径。
