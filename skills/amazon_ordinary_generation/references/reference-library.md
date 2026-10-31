# 内置套图、逐图文字模板与候选选择

与植株版使用相同的策划入口：竞品反推、内置套图提示词、具名混合；路线、具体套图和逐图来源分别确定。普通商品库独立保存在`assets/reference-library/catalog.json`，不依赖植株技能安装目录或作者磁盘。

## 实际资源与来源性质

当前包含200条逐任务改写的普通商品文字模板：52条操作、110条布局、38条光影；以及8套有序11资产策划配方。它们是内置策划材料，不是200条未知SKU的READY提示词，也不是8套已看过的普通商品竞品照片。此次未移植植株原图库、植物外观事实或历史“已目视”结论。每条保留原模板ID/版本作编写来源，不把旧ASIN当成本项目竞品。

文字模板覆盖保真、取景、融合、细节、参数、包装/状态、光影、场景、组件与修复；形态专用任务仅在本SKU适用时采用。MAIN模板仅适用于明确范围内的主图，不给默认11图新增MAIN；操作与光影是单图组成方法，不增加图片预算。

每条模板包含`taskEn`任务边界和`artDirectionEn`具体画面提案：机位、全貌与局部关系、支撑遮挡、景深、光源与受影面或文字区域。后者是可讨论的美术方向，不是已确认选择或实际观察；已选竞品构图及用户决定优先。避免把200条限制句拼成冗长提示词，按本图一个主任务选布局，按需要加入一个光影或修复方法，再去重转译。

另有8种商品形态分支（刚性、柔性、平面、包装、组件、手持、安装、细长）和6种表面分支（哑光、亮面、金属、透明、织物、印刷）。它们按本图实际展示任务选取，不按类目名称强套；不选就不注入。材质分支须绑定有依据的具体部位，多材质商品分别说明，不能把金属反射应用到塑料外壳。分支不证明材质、耐用性或功能，也不取代问答。

8套配方分别以用途选择、结构适配、柔性工艺、平面印刷、包装内容、连接状态、组件操作、空间支撑为叙事主线。它们是可组合方向，不是支持类目的封闭名单。原配方有不适用的步骤/比较/视角时，说明缺口并讨论替代任务，保留目标ID与范围；不能删掉未回答问题后声称全套已经解决。

读取套图时先用`planningFocusEn`明确该套的买家问题、资产分工和适用边界，再讨论slots中的候选结构；槽位不是固定摄影清单。比如柔性商品重在测量状态、缝线与垂落，连接商品重在接口、配套对象和真实状态，包装商品重在购买单位、包装外观与已证内容物。

## 按资产检索与读取

命令从项目目录运行，`<skill-root>`替换为本技能安装绝对路径：

```sh
python3 "<skill-root>/scripts/library_catalog.py" search --kind series --limit 3
python3 "<skill-root>/scripts/library_catalog.py" show ORD-SET-STRUCTURE
python3 "<skill-root>/scripts/library_catalog.py" search --kind template --design-group dimensions-details --limit 5
python3 "<skill-root>/scripts/library_catalog.py" show ORD-DETAIL-07 --asset-role DIM01
python3 "<skill-root>/scripts/library_catalog.py" show ORD-DETAIL-07 --asset-role DETAIL01
python3 "<skill-root>/scripts/library_catalog.py" profiles
python3 "<skill-root>/scripts/library_catalog.py" show ORD-DETAIL-02 --asset-role DETAIL01 --product-form soft --material textile
python3 "<skill-root>/scripts/library_catalog.py" show ORD-AMZ-93 --asset-role APLUS01 --product-form packaged --material printed
python3 "<skill-root>/scripts/library_catalog.py" search --kind template --design-group scenes --query "侧光" --limit 3
python3 "<skill-root>/scripts/library_catalog.py" search --kind template --design-group aplus --asset-role APLUS01 --limit 5
```

检索返回文字而非图片；DIM与DETAIL共用结构池但有独立角色分支，A+与SCENE也按角色重新构图，不能只换标题或照搬源画幅。`show`返回的planningTemplate是给策划阶段使用的模板，最终须填入实际附件、身份、画布、唯一布局与准确文字，并移除代理工作流和内部ID。

编写时先说清可见结果，再给附件角色、商品锁、唯一构图、物理关系、光影和准确文字。背景、手部、安装面、开盒内容仅在本图需要且有依据时写入；新图任务不凭空要求编辑底图或“修复旧缺陷”。形态/材质分支与模板冲突时先改选适配条目，不能同时要求哑光和镜面、无字和加标签、固定背景和重建背景。只有一件商品、一个状态或一个用途时，替换配方中不适用的多件、双状态或多场景任务；用不同买家问题区分资产，不为凑图重复桌面摆拍。

先由技能检索2–3个适配候选，在聊天展示套图卡、逐图骨架和取舍，清楚标`text-only / 文字蓝图`，再实际弹窗让用户选择。不要求卖家自行翻200条模板，不伪造样图缩略图，不因文字方案没有图片就静默改成原创或跳过讨论。已选/明确委托的内容直接沿用。

## 竞品与内置路线分别使用

- 选竞品：以本次实际看过的具体源图为主，保留整套顺序与逐图分支，不让内置默认覆盖已选来源；必要辅助条目要说明负责哪些属性。
- 选内置：先定具体ORD-SET及逐图模板，再结合本品事实进行多轮布局、文案与字体讨论。竞品研究继续回答买家问题；内置模板不补齐竞品/评论/关键词覆盖。
- 选混合：逐ID列主来源与辅助模板各负责什么，锁定统一的设计语言；不随意拼接冲突的字系、色板和物理条件。

用户明确选择自主设计时记original；它不是无回答时的默认路线。竞品访问受限时，完成有限恢复后可展示内置文字方案继续讨论，同时保留真实研究缺口。

## 项目新增视觉参考与恢复

内置模板的可复用任务保持普通商品语义，检索输出同样要落实usagePlan/propsPlan/graphicPlan及本图机位；按商品实际用途选择，不将所有模板实例化为无使用对象的同角度静物。跨图采用[差异检查](scene-expansion.md#整套差异检查)，对比/步骤允许保留同机位。模板中的画面提案是起点，不是统一房间、柔光或无图形禁令；可见图形与copyMode分别决定。200条模板与8套配方不需要每个商品强行使用全部分支。

当前库不携带图片。项目采集仍按[媒体存储](media-storage.md)保存源图、来源/变体/图序与哈希；下载、实际看图、反推、用户选定分别记录。要复用某张图时先打开检查，不把文字索引或文件存在当作本轮目视。

新增图先逐图记录accept/reject/hold、可迁移结构与质量理由，低清/混乱构图不自动进入可复用候选。A+另核principalProduct及实际区段；相同ASIN/品牌或布局不能合并不同商品身份。买家图片供研究，不默认作为构图库。没有用户要求维护图库时，增量保存在项目输出，不自动修改技能包或上传外部服务。

用户提供兼容文字目录时，可用`--catalog <实际JSON>`显式检索并记录版本；不能冒称该参数会同步远程服务。外部图片必须实际取得并看过再用。续聊沿用已记录库版本/条目，只有用户选择更换来源或新证据影响方向时更新，不重置全部问卷。
