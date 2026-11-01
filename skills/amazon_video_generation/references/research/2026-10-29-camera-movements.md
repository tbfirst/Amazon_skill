# 2026-10-29 运镜研究与适配边界

本次用于完善技能，未生成商品故事板、未提交即梦、未取得商品成片。原视频观察、文字资料与本技能导演建议分开记录。

## 用户参考的访问结果

| ID | 来源 | 实际取得 | 可以支持 / 尚不能支持 |
| --- | --- | --- | --- |
| V-CAM01 | [用户短链](https://v.douyin.com/6YZoVI3Y48Q/) → [抖音7623429768080765106](https://www.douyin.com/video/7623429768080765106) | HTTP重定向已确认；GET返回页面但无可读标题、视频数据或媒体链接 | 用户提供标题“电影感运镜的终极指南，镜头运动全解析”；未看连续画面/未听音轨，不报告原片切点、轨迹与配乐核验 |
| V-CAM02 | [用户短链](https://v.douyin.com/umJYXpGbkG0/) → [抖音7657907648347700389](https://www.douyin.com/video/7657907648347700389) | HTTP重定向已确认；页面未提取到标题/视频数据 | 用户提供“十九秒教会8种实用手机运镜”；19秒/8种只是分享文案，未核媒体时长、完整八招和“两倍”的原意 |
| V-CAM03 | [B站同标题页面](https://www.bilibili.com/list/ml3158673540?bvid=BV14iXCBAE48&oid=116324240070666) | 网页可读标题、简介、作者显示“吸一口风rocky”；直接视频页返回412 | 简介列推拉摇移等基础类别；只能作为同标题候选，未证明与V-CAM01逐帧相同。尚有光为收藏列表创建者，不混作视频作者 |

web工具未能打开两条抖音短链；curl解析后读取落地页仍未取得画面。没有绕过登录/验证码或反复下载受限内容。需要精确复刻原教程时补可播放原片或对应片段；当前技能方法库无需等待，可依可靠术语与用户表达完成。

## 补充一手资料

- [Adobe：Tracking shot examples](https://www.adobe.com/creativecloud/video/production/cinematography/camera-shots-and-angles/tracking-shot.html)：已读网页，帮助区分跟随主体的镜头描述与dolly器材/运动组织。未观看页内视频。
- [Adorama：Basic Camera Movements for Video](https://www.adorama.com/alc/basic-camera-movements-for-video/)：已读作者教程，核对水平摇/俯仰摇、推拉/横移/升降、变焦及转焦的区别。未播放嵌入示范。
- [Runway：Camera Terms, Prompts, & Examples](https://help.runwayml.com/hc/en-us/articles/47313504791059-Camera-Terms-Prompts-Examples)：已读官方术语说明，参考arc与orbit区分，以及写出运动各阶段可见内容的表达方法。未查看动态示例；其Gen-4.5能力与复杂组合建议不推作即梦支持承诺，也不承接示例中的形变、超现实环境或主体动作。

上述基础术语转写用于 [运镜库](../camera-movement-library.md)。具体植物场景、短弧幅度、5秒揭示节奏、段落分配与降级方案均为本次适配建议，未通过对照生成实验或转化数据验证。“两倍环绕”保留歧义，不编造出处或定义；“遮挡上升”采用可解释的固定前景+相机升高方案，不声称等同原片。

## 研究如何进入工作流

| 来源/输入 | 可迁移内容 | 技能落点 |
| --- | --- | --- |
| 用户期望多角度、环绕、遮挡上升 | 商品静止下的立体展示与空间揭示意图 | M04/M08及条件式2×解释；主要用于C02 |
| 摄影术语资料 | 分开相机平移、转向、焦距与焦点 | 运镜词典、分镜路径/视线/终点字段 |
| 模型厂商提示词资料 | 用可见阶段和终点写动作 | 即梦正文自然语言展开；不只给术语标签 |
| 历史4×10秒约定 | 该首尾约定已取消，不用于新项目 | 保留当时研究背景，当前按方向/项目选择 |

## 第二轮补充（组合、手持与多角度）

同一天为补齐“组合运镜、手持、机位覆盖”再次检索。以下均为网页文字阅读，**未播放**页面内嵌视频，也未取得用户两条抖音的连续画面；因此只采用术语区分、操作惯例与可解释的量化经验，不引用任何“转化率/完播率”数字作为依据。

| 来源 | 可迁移内容 | 采信程度 |
| --- | --- | --- |
| [Runway：AI Camera Prompts](https://runway.com/en/resources/ai-camera-prompts) | 静态镜最难落地，需描述画面内允许的运动并再次锁定相机；每个运动词都要带速度/时长；orbit（绕满）与 arc（不绕满的弧线）分开 | 官方文档，术语与表达可用；不当作即梦能力承诺 |
| [Versely：AI Video Motion Design Prompting 2026](https://versely.studio/blog/ai-video-motion-design-prompting-2026) | 提示词结构 `运动类型 + 速度 + 主体关系`，并写明起始与结束景别 | 行业博客，作写法参考 |
| [航拍网：拍摄短视频的运镜方法](https://www.chinahpsy.com/detail-208299.html) | 小环绕适合产品、大环绕适合人物；前景遮挡分入镜/出镜；旋转需配推拉且不可久转；组合搭配清单；起落幅各停1–2秒、全程匀速 | 创作者教程，作惯例参考 |
| [8种万能运镜手法](http://mp.weixin.qq.com/s?__biz=MzkyOTcxMjQwMA==&mid=2247484453&idx=1&sn=98c3bd6cedc98cd190745de5ff167f60) | 推拉全程3–5秒；甩镜约0.5秒；环绕保持高度与方向一致；15秒片2–3种手法足够 | 创作者教程，作节奏起稿 |
| [ProcessOn：短视频拍摄运镜手法](https://www.processon.com/view/6983ff93a555e7047cf4cf70) | 推→停→拉；环绕+推进的螺旋路径；低角度移跟约10–20cm | 图示资料，作组合与低角度起稿 |
| [今晚报：视频里的运镜](https://jinwanbaoepaper.enorth.com.cn/zlnsb/html/2026-10/28/content_87946_3960290.htm) | 摇镜约每分钟90°；一个推镜至少5–8秒到位；推+摇两动作连用即够 | 大众科普，作慢速基准 |
| [K3：Product Videography Checklist](https://www.k3videoproduction.com/blog/top-video-production-in-chicago-product-videography-checklist/) | 电商角度清单：45°高位最通用、正面 hero、俯视 flat lay、细节近景；切点2–4秒；简单硬切优于花哨转场 | 商业制作方，作角度覆盖参考 |
| [ZHIYUN](https://store.zhiyun-tech.com/fr/blogs/news/camera-gimbal-vs-handheld-shooting-which-setup-works-better-for-video-creators)、[Nitro](https://www.nitromediagroup.com/camera-movement-in-filmmaking-handheld-vs-stabilized-shots/) | 手持=亲近/纪录感，稳定器=被引导的抛光感；客户常把无动机的晃动读成廉价；稳定器不替代运动设计 | 厂商与制作方观点，支撑“手持仅条件使用” |
| [Freshpack：产品摄像入门](https://www.freshpackphoto.co.uk/?p=921) | 180°快门法则（快门≈2×帧率）得到自然运动模糊；24/30fps 为常见交付 | 摄影教程，仅用于实拍设置 |

未采信的部分：各站点的“最佳时长/转化提升”类数字、AI 平台对复杂组合的“完全可控”说法、以及任何把“两倍环绕”定义为固定参数的表述。原片含义仍未核实。

## 本轮落点

- 单运动扩到 M00–M19（新增甩镜、滚转、变焦、推拉变焦、手持、贴面掠移、完整环绕、主体自转），每条带段位、边界与降级：见 [运镜库](../camera-movement-library.md)。
- 组合独立成 K01–K06（推→停→拉、螺旋推进、横移+微升、推进+前景遮挡、环绕+后拉、升降+俯仰补偿），并写明“一个主路径 + 最多一个辅助”。
- 新增 [运镜执行卡](../camera-shot-cards.md)：11 张卡含秒数、起终点、实拍设置、即梦句式、常见失败与降级；两倍环绕给出三种解释的判定与改写。
- 新增 [机位覆盖](../multi-angle-coverage.md)：P1–P8 机位、30°变化规则、180°轴线、景别阶梯、品类矩阵与拍摄日清单。
- 速度基准、起落幅 1–2 秒、180°快门法则进入分镜与执行卡；不写进 AI 提示词的部分明确标注。
- `scripts/check_camera_plan.py` 把“一镜一主运动/C01、C04 约束/未知ID/含糊词”变成可跑的检查。
