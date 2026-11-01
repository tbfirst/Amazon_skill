# 双参考视频：六维英文逆推与SKU适配模板

本库是供策划agent使用的研究与适配资料，分为**原片分析**和**项目适配**两层。英文段落是根据可见画面逆向设计的复现建议，不是恢复原作者提示词，也不证明作者用了某种模型、镜头或3D工作流。技能默认最终交付仍是中文整片即梦词；只有用户明确要求英文执行版时才另交。

## 原片完整报告

- [A：儿童折叠沙发床广告](reverse-prompts/bilibili-shot-prompts.md)：逐镜时间码、画面依据、总体风格、音景边界及英文段落。
- [B：花材布置与成品展示](reverse-prompts/download-shot-prompts.md)：逐镜时间码、画面依据、总体风格、音景边界及英文段落。

两片分别含19个和16个关键镜头/操作段的完整英文段落；A片另外记录12.280–12.320秒单帧闪切，不作为可生成叙事镜头。两片均重新查看全帧连续缩略联系表（949＋945帧），并复核关键原分辨率帧；原音未听审，已提取可解码音轨不等于已听辨。

这两份随技能保存的完整报告可独立阅读；媒体来源、帧审阅范围、音轨核实程度见各报告前言。源片时间区间只是研究索引，不能当成当前入口可生成长度；小格连续帧检查不能冒称每帧全分辨率质检，音轨存在或能量非零也不能证明已听辨音乐、旁白或音效。

## 六维写法与移植规则

|维度|适配时必须落实|避免|
|---|---|---|
|电影化镜头设计|景别、起终机位、主路径、构图、焦点与前后景关系|把主体自转称为环绕；只写“电影感”|
|主角与叙事动作|商品/手部是谁，起态→接触/变化→终态，回答哪个买家问题|背景演员抢商品；动作不能支持所宣称功能|
|世界与材质|所选场景、主台/花器、已核花材表面、比例和承重|从玩具复制绒面/海绵，从花艺片复制未售花材|
|风格锚点与物理光照|全片一组克制的色彩/质感规则；光源方向、软硬、接触阴影及反射|每镜随机换滤镜、商品漂色、光随相机旋转|
|沉浸式音景|本项目轻音乐/环境音/接触音/无旁白策略；逐项标来源或设计|未试听就断言原片音乐类型、节拍或无音乐|
|整合与规格|每镜一段连贯高密度正文，随后给目标时长、画幅、入口适用规格|假定焦距、ISO、帧率是模型可控参数；一镜等于一次生成|

原片A提供用途→状态/结构→接触反馈→用途结果的叙事；原片B提供成品→过程→累积→细节→成品的叙事。一般商品按[通用流程](product-video-workflow.md)挑选信息任务，不强制环绕/插花；flowers才沿用[花卉时间线](flower-showcase-workflow.md)与[动态规则](dynamic-flower-direction.md)。T04/T05是花卉特例，T01/T02/T03/T06的具体物件/声音措辞也要重写，不能逐字拼成终稿。

**编译边界**：原片功能/道具的“不继承”规则、观察与推断、音轨是否听审、源片时间码和模板ID只留分析说明书；不把它们转成TXT、分镜表或宫格的禁用清单。执行内容仅描述当前SKU需要的结果和实际附件。只迁移有用拍法，不禁用恰好也是本SKU真实功能的词。跨C-ID的声音按[执行词声音规则](full-film-prompt.md)处理，内部模板的“继续”只可指同一次任务内已选音景，不指向模型没有收到的前段。

## 模板到源片的溯源

时间码是源片索引，不是模板建议时长。A/B镜号分别对应上面的完整报告，技术规格沿用各报告的源文件记录；本项目规格另外确定。

|模板|原片镜号与时间码|借用与改写边界|
|---|---|---|
|T01 用途先行|A分镜1，0.000–2.880；B分镜1，0.000–2.400|借成品/用途先行；BG展示台与明确相机环绕是用户扩展，不能称为原片同轨迹|
|T02 尺度与空间状态|A分镜2，2.880–6.480|借读数起态、过渡、读数终态；原片主体展开并变朝向，花卉默认改相机绕固定主体，不继承折叠机构与尺寸|
|T03 动态细节|A分镜8，16.120–17.760；A分镜9，17.760–18.720；B分镜14，23.367–25.400|A是按压与近静态面料插镜，B是手托/轻触花头；只借接触/纹理叙事，风动是新增选项，不把按压或静图默认套给花卉|
|T04 逐次插花|B分镜4–8，5.500–13.800；B分镜9–12，13.800–21.833|材料组→单枝→累积；分镜5只见已弯茎，分镜12只见填充后调整，不能补称完整弯折/全部填充枝插入均已拍到。默认3次来自用户要求|
|T05 成束插入|用户新增动作模式，无原片对应完整序列|可借B片材料介绍与接触连续性，但不将任一源时间码当成已观察成束整理后入瓶的证据|
|T06 用途扩展/回环|A分镜12–19，21.880–37.960；B分镜15–16，25.400–31.533|A多用途，B同厨房成品首尾呼应；不把B说成多房间，不把原片近静态用途镜复刻成静图轮播；户外画面不证明耐候|

## 可替换项

下列模板方括号是编写槽位，不是用户要上传的最终执行词。选择相关模块，填写并整合为一份完整脚本；不必每个模块都使用，也不能交带占位符的终稿。

|槽位|来源与用途|
|---|---|
|PRODUCT / COLORS / VESSEL|已查看的最终SKU图、真实售卖内容与容器关系；不能从源片继承|
|SURFACE / FLEXIBLE_PART|有依据的表面纹理与可动部位；未知材质只描述可见外观|
|SCENE / DISPLAY / NEAR_ANCHOR / FAR_ANCHOR|项目场景或BG01–BG11/OUT背景适配，明确三维相对位置|
|START / PATH / END|参考覆盖内的机位和动作；世界固定与屏幕投影变化分别描述|
|FEATURE / DIMENSION / ENDPOINTS|已核卖点、数值单位与测量端点；缺失则相关模块待定|
|INITIAL_CONTENTS / GROUPS / FINAL_LAYOUT|起态已有花材、手中花材、真实售卖分组及累积终态|
|STYLE / LIGHT / AUDIO|本项目选定的统一色彩材质与光照；音景为设计时明确标注|
|SECONDS / ASPECT / OUTPUT_SETTINGS|项目目标时长/画幅和实际入口可用设置；源文件规格只作记录|

以下每段把六维放进一段英文；声音均为**适配建议**，不因出现在模板中便成为源片已核音景。默认轻音乐、无旁白可按用户项目更改。真正提交前，按实际C-ID展开所有镜头与附件身份，不要求用户自行拼段。

## T01 用途先行与展示台开场

借用原片的“结果先行”叙事；空间环绕与按配色选展示台来自当前用户要求，并非声称原片有同样环绕。

> Open on [PRODUCT] in its finished arrangement, a calm sculptural presence on [DISPLAY] within [SCENE], preserving the exact [COLORS] and the approved [VESSEL]. Begin at [START] and move the camera along [PATH] to [END], maintaining a readable full silhouette while [NEAR_ANCHOR] shifts more strongly than [FAR_ANCHOR]; the vessel's position and orientation remain fixed in the room. Let the documented [SURFACE] retain its individual texture against the quieter materials of the display, with coherent [LIGHT], a grounded contact shadow and material-appropriate reflections. Hold the unified [STYLE] palette without tinting the merchandise, so the movement reveals volume and belonging rather than turning the arrangement into a rotating object. For the proposed sound design, carry a restrained [AUDIO] bed beneath subtle room ambience, without narration, and settle into a clear final view that invites the next explanatory shot. Technical target: [SECONDS] seconds, [ASPECT], [OUTPUT_SETTINGS]; one shot inside the planned generation task.

## T02 可读尺度与空间状态

借用原片A的“可读起态→过渡→可读终态”节奏；固定花卉改为相机绕行，真实结构变化仅在有证据时另设D3。

> Present [PRODUCT] and its approved [VESSEL] as a fixed, physically grounded object on [DISPLAY], beginning in a legible three-quarter view that reveals height and depth without exaggerating scale. Move the camera through [PATH] between the supported [START] and [END] viewpoints while the product remains stationary; let the display edge and distant [FAR_ANCHOR] reveal the changing perspective. Fine measurement guides extend from the verified [ENDPOINTS], their projected positions following the view, and display only [DIMENSION] in steady, front-readable lettering before the camera settles for a clean reading. Preserve [SURFACE] and [COLORS] under soft directional [LIGHT], with the same [STYLE] restraint used in the opening, making the interval a precise explanation of space rather than an invented transformation. As proposed audio, continue [AUDIO] quietly and optionally place a restrained graphic accent under the guide reveal, without narration or claims beyond the measurements. Technical target: [SECONDS] seconds, [ASPECT], [OUTPUT_SETTINGS]; retain enough final stillness to read the labels.

## T03 接触反馈与动态细节

借用两片“近景接触→可见响应→结果”的方法；风动是当前可选创意，不证明源片存在风或商品具有额外性能。选择一种主事件，不同时堆风与手势。

> Enter a close view of [FEATURE] on [PRODUCT], framing enough of its attachment and neighboring forms to keep the detail recognizably part of the same item. Under [LIGHT], the visible [SURFACE] holds delicate tonal variation rather than artificial gloss, anchored to the film's [STYLE] palette and the softly separated [SCENE] behind it. Show [ACTION: a fingertip approaching a verified contact point, gently brushing and releasing it, or a light airflow moving only the verified flexible parts], with a small, material-appropriate response that settles naturally while the vessel and supporting stems remain grounded. Keep the camera [PATH] and the contact unobscured, allowing the action to reveal the visible feature without pretending to prove softness, durability or recovery performance. For proposed sound, use low [AUDIO] with a subtle, appropriate contact or air texture only where useful, no narration, and finish on the readable detail. Technical target: [SECONDS] seconds, [ASPECT], [OUTPUT_SETTINGS]; avoid microscopic structures absent from the product references.

T03–T06用于新项目时追加[终态与运动规则](terminal-state-and-motion.md)：从本SKU选定完成态倒推操作，不从空瓶任意拼三枝；场景按[任务与空间](volumetric-scene-direction.md)，手持按[物理连续性](physical-continuity.md)设计。模板研究措辞不直接复制为执行正文。

## T04 花材逐次累积：默认3次

借用原片B“材料辨认→插入→调整→下一组”的连续性。具体3次是用户默认，不等于原片每个花材组的实拍次数。

> In a clear working view of [VESSEL] on [DISPLAY], begin with the documented [INITIAL_CONTENTS] already in place and the approved [GROUPS] visibly available to the hands. Let the first insertion establish [PLACEMENT_1], the second build [PLACEMENT_2], and the third complete [PLACEMENT_3]: each stem approaches the opening, enters along a plausible path, seats, and is released before the next action begins. Preserve every earlier stem and its accumulating silhouette, showing the actual [COLORS] and [SURFACE] without instant multiplication or unexplained substitution; cuts may omit the pause between completed actions, never their meaningful contact. A steady, readable camera and soft [LIGHT] hold the same [STYLE] world, with the vessel's contact shadow and the hands' occlusion grounding the craft in [SCENE]. As proposed audio, retain gentle [AUDIO] and low material-appropriate handling sounds without narration, then allow a brief final adjustment and an unobstructed view of [FINAL_LAYOUT]. Technical target: [SECONDS] seconds, [ASPECT], [OUTPUT_SETTINGS]; schedule enough time for three readable insertion-and-release actions.

## T05 手中整理后成束一次插入

这是用户新增的替代模式，不能记为原片B已证实动作。它承接相同的材料→动作→结果叙事。

> Frame the hands and [VESSEL] together within [SCENE], beginning with [INITIAL_CONTENTS] in the vessel and the approved [GROUPS] gathered loosely in one hand. The supporting hand holds the lower stems while the other deliberately adjusts height, facing direction and color balance, letting [SURFACE] and [COLORS] remain identifiable as the arrangement takes shape; then gather and align the stem ends, guide the bundle through the opening in one plausible insertion, seat it, release it, and make a small final adjustment toward [FINAL_LAYOUT]. Keep the bundle diameter compatible with the opening, every existing flower continuous, and the camera on [PATH] quiet enough to read grip, entry and release. Maintain [STYLE] through coherent [LIGHT], grounded shadows and the restrained materials of [DISPLAY]. For proposed audio, continue soft [AUDIO] beneath light handling sounds, without narration, so the tactile sequence feels complete rather than a sudden jump to a finished bouquet. Technical target: [SECONDS] seconds, [ASPECT], [OUTPUT_SETTINGS]; this is one insertion after visible preparation, not three repeated bundle insertions.

## T06 用途扩展与成品回环

借用原片A的多用途收束与原片B的首尾成品呼应；花卉跨场景运动连续性按当前要求重新设计。

> Reveal the same completed [PRODUCT] in [SCENE], its [COLORS], [VESSEL] and [FINAL_LAYOUT] immediately recognizable from the preceding shot. Begin on a matching position, scale or motion direction and let [SCENE_EVENT or CAMERA_PATH] unfold as a real interval: the near [NEAR_ANCHOR] and distant [FAR_ANCHOR] separate through parallax, or a visible placement-and-release action establishes the arrangement's use without changing what is sold. Preserve the documented [SURFACE] and a plausible contact with [DISPLAY], adapting [LIGHT] to the new room or sheltered outdoor setting while retaining the film's [STYLE] color discipline. Let the final composition echo the opening and settle on the product, leaving [APPROVED_COPY_OR_NONE] readable if requested. For this generation task, specify a restrained [AUDIO_STYLE] and suitable room ambience, without narration; any shared soundtrack across separate tasks is a separate production decision. Technical target: [SECONDS] seconds, [ASPECT], [OUTPUT_SETTINGS]; this is a dynamic scene, not a still photograph enlarged before the next cut.

## 从库到项目的最短路径

1. 选叙事方法与相关模块，记录完整报告中的来源镜号/时间码；新增用户创意标“项目扩展”，不硬找源片证据。
2. 写全片风格锚点与各镜真实任务，填写SKU事实和动作状态，按选定片长重新分配时间。未核事实只阻塞相应模块。
3. 将适配后的英文语义整合成中文主提示词；Mini单次15秒时按自然切点分C01/C02，每段独立自足，逐镜英文模块不意味着逐镜生成。
4. 将内部来源/研究说明留在分析说明书，检查最终TXT、上传表与格下说明仅含本SKU执行信息；同步实际分镜板、导演表和上传参考；动态动作只有实际生成后才能验收。不得把本库段落齐全当成已经完成该SKU的视频包。
