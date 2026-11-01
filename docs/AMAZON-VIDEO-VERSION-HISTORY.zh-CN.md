# 视频技能：中文版本历史与本地回滚索引

整理日期：2026-11-01。当前源码及安装副本为 **v5.4.0**。所有提交和标签仅保存在本地，未推送。

这些提交是根据现存备份、Git原始树和本次修改记录补存，提交日期为实际补存日期，不冒充历史发布。只归档视频技能子树；不是当时整个仓库的快照。v5.0.0至v5.4.0依次进入main，更早版本以独立恢复提交和附注标签保留。

## v5主线

|版本|本地提交|本地标签|中文变更说明|
|---|---|---|---|
|v5.0.0|`7ddbcb8606`|`amazon-video-v5.0.0`|最终套图转整片方案、分析说明书及两类分镜图|
|v5.1.0|`1d744c2b76`|`amazon-video-v5.1.0`|真实相机绕行、环境视差与可辨认插花动作|
|v5.2.0|`71d1590830`|`amazon-video-v5.2.0`|展示台背景库、配色适配与成束插入方案|
|v5.3.0|`30c1354b10`|`amazon-video-v5.3.0`|双参考六维逆推和可替换SKU的提示词模板库|
|v5.4.0|`bfa14d0230`|`amazon-video-v5.4.0`|详细表与宫格同源生成、镜号对应及格下中文说明|

## 更早的可见快照

|版本|本地提交|本地标签|中文说明|
|---|---|---|---|
|v1.0.0|`0045a56f02`|`amazon-video-v1.0.0`|初始视频前期策划与素材承接|
|v1.1.0|`28412e6bed`|`amazon-video-v1.1.0`|补充商品视频制作规范|
|v1.2.0|`3458829102`|`amazon-video-v1.2.0`|统一整片中文提示词|
|v1.3.0|`faf4cfe0bd`|`amazon-video-v1.3.0`|完善单次提交与视频执行词|
|v1.4.0|`e82c9ea80a`|`amazon-video-v1.4.0`|整理交付目录和编号素材包|
|v1.4.1|`8f5ed8d67a`|`amazon-video-v1.4.1`|补充ASIN素材承接|
|v1.5.0|`e89fb4d9dd`|`amazon-video-v1.5.0`|竞品视频风格分析|
|v1.6.0|`57166ff87a`|`amazon-video-v1.6.0`|内置拍摄模板与商品连续性|
|v2.0.0|`a75095fb29`|`amazon-video-v2.0.0-snapshot-70e3965f`|三段15秒、故事板与跨段连续性|
|v2.0.0|`92adc7f2c8`|`amazon-video-v2.0.0-snapshot-d2bcb05e`|三段15秒、故事板与跨段连续性|
|v3.0.0|`0bbca4ca9f`|`amazon-video-v3.0.0`|四段10秒与21比9文字分镜流程|
|v3.2.0|`bfd83843f7`|`amazon-video-v3.2.0`|运镜库、执行卡与多角度覆盖|
|v3.5.0|`5fdd4e34fa`|`amazon-video-v3.5.0`|16比9分段执行与镜头表内提示词|
|v3.6.0|`7914d06914`|`amazon-video-v3.6.0`|优化分段视频导演流程|
|v4.0.0|`b5ea10ca04`|`amazon-video-v4.0.0`|分离花卉与草木路线并约束新片时长|
|v4.0.1|`0e09d3e87e`|`amazon-video-v4.0.1`|修订花卉与草木执行规则|
|v4.1.0|`defd4293a7`|`amazon-video-v4.1.0-partial`|花卉环绕与插花规则的残存文件归档|
|v4.2.0|`7ecf79d0b0`|`amazon-video-v4.2.0-snapshot-81f2b254`|六种花卉展示格式与参考研究|
|v4.2.0|`7fde4d4e15`|`amazon-video-v4.2.0-snapshot-847c0c6f`|六种花卉展示格式与参考研究|
|v4.4.0|`176969886e`|`amazon-video-v4.4.0`|综合展示、多场景与15秒生成预算|

同版本v2.0.0、v4.2.0各有两份不同的原始树，使用树哈希后缀区分，不推定其先后次序。v4.1.0只有入口与references残存备份，标签明确带`partial`，用于查阅，不作为完整可运行版本。

## 来源与验证边界

- Git原始树按树哈希原样保留；目录备份按逐文件SHA-256核对后入库，不用新版本内容补齐旧版。历史文件混有LF/CRLF；当前仓库仅对视频技能子树关闭自动换行转换，以保留快照字节及避免纯换行误报，不改变其他技能的规则。
- v5.3.0：以本次v5.4.0修改前的会话读取内容恢复分镜交付规范，对其余改动执行精确反向转换，删除v5.4.0新文件；重新应用原修改脚本后，所有受影响文档与当前源码一致。来源会话为`rollout-2026-11-01T08-50-26-01a19496-1559-7492-82f0-d26401281f36.jsonl`，原文件读取调用为`call_76c054bf2cca46f6b6df10de5bc598ef`。它是有据恢复，不声称找到独立原始v5.3.0树。
- v5.3.0保留当时源码缺少`assets/storyboard-editor.html`的状态；v5.4.0从安装副本补齐，78项测试通过。其他历史版本未重新运行测试，历史缺件、旧模型能力假设和已弃用工作流不因归档而变成当前推荐。
- v1.7.0、v3.1.0、v4.3.1等仅见文字记录而本次未找到独立完整快照的版本，不伪造版本提交；相关累计内容可在后继快照查阅。
- `.agents/skills/amazon-video-generation`是被Git忽略的本地安装副本。回滚源码不会自动回滚安装副本；正式启用旧版时须按目标源码同步安装目录，并清理仅属于新版的文件。

### 快照来源与技能树

|标签|来源|技能子树|
|---|---|---|
|`amazon-video-v1.0.0`|/tmp/amazon-video-upgrade-before/source|`08c35ea1111b58dd753923ecc66bdb5f93480cc5`|
|`amazon-video-v1.1.0`|/tmp/amazon-video-jvlang-before/source|`934323218007b8cfbf5e364c7b1c2151cc970a54`|
|`amazon-video-v1.2.0`|/tmp/amazon-video-single-prompt-before/source|`35f944666199ccbf4bcbbe88cbe614911dba20ec`|
|`amazon-video-v1.3.0`|/tmp/amazon-video-package-before/source|`b7f6a81b7f5f2e32273dfb04b03b2a0813af748c`|
|`amazon-video-v1.4.0`|/tmp/amazon-video-asin-before/active|`032719f77c3707ae6f3c0f1ba2bff4bf45cb38b2`|
|`amazon-video-v1.4.1`|/tmp/amazon-video-style-before/source|`4986be761a8ac7e6edd56b122aadc8d41895acd3`|
|`amazon-video-v1.5.0`|/tmp/amazon-video-template-before/source|`efa0471f54c8770e85db31e7e97365ecce9a1ba7`|
|`amazon-video-v1.6.0`|Git原始未引用树 df6fca939f4d28f3e83e30006ea2a2311b940209|`df6fca939f4d28f3e83e30006ea2a2311b940209`|
|`amazon-video-v2.0.0-snapshot-70e3965f`|Git原始未引用树 70e3965fa031b59420713dcf108b54d206f170c0|`70e3965fa031b59420713dcf108b54d206f170c0`|
|`amazon-video-v2.0.0-snapshot-d2bcb05e`|Git原始未引用树 d2bcb05ec2d30af1e1a94df1feb84cddbcaf9cb9|`d2bcb05ec2d30af1e1a94df1feb84cddbcaf9cb9`|
|`amazon-video-v3.0.0`|Git原始未引用树 42a50bfa515553c5d6add3d574ecef16dcd3320c|`42a50bfa515553c5d6add3d574ecef16dcd3320c`|
|`amazon-video-v3.2.0`|Git原始未引用树 c7d49b4865af5dcba4495e9ec705c7571c4c3f02|`c7d49b4865af5dcba4495e9ec705c7571c4c3f02`|
|`amazon-video-v3.5.0`|Git原始未引用树 11054c6c08a1611a12e9b391597f2f1a566c9ff9|`11054c6c08a1611a12e9b391597f2f1a566c9ff9`|
|`amazon-video-v3.6.0`|Git原始未引用树 406a2fccff27384a915c5bb0795855833852d502|`406a2fccff27384a915c5bb0795855833852d502`|
|`amazon-video-v4.0.0`|Git原始未引用树 8e585be7810f7fcad993c4c7371019ca03238069|`8e585be7810f7fcad993c4c7371019ca03238069`|
|`amazon-video-v4.0.1`|Git原始未引用树 1407f6cf31315fece95188c8458b53df8b7b356d|`1407f6cf31315fece95188c8458b53df8b7b356d`|
|`amazon-video-v4.1.0-partial`|/tmp/amazon-video-v4.1-backup|`c234d0a15738d009d604423a31bb17c5305ee346`|
|`amazon-video-v4.2.0-snapshot-81f2b254`|Git原始未引用树 81f2b254e5d4e15613b4aa54442cc94bc90d86e5|`81f2b254e5d4e15613b4aa54442cc94bc90d86e5`|
|`amazon-video-v4.2.0-snapshot-847c0c6f`|Git原始未引用树 847c0c6f8f591661865c43b47ddba46fd02a04b7|`847c0c6f8f591661865c43b47ddba46fd02a04b7`|
|`amazon-video-v4.4.0`|Git原始未引用树 88e890127ea1c75eff1dd46ad1a572ddcbf5eea3|`88e890127ea1c75eff1dd46ad1a572ddcbf5eea3`|
|`amazon-video-v5.0.0`|Git原始未引用树 7eba1844f170df8a8928022330266c47dfd5d000|`7eba1844f170df8a8928022330266c47dfd5d000`|
|`amazon-video-v5.1.0`|Git原始未引用树 472aef297dd093c0ae20ffe5873c35605a98c8d0|`472aef297dd093c0ae20ffe5873c35605a98c8d0`|
|`amazon-video-v5.2.0`|Git原始未引用树 ff4a319d6a3086993c85c8d5ea888deeba88cc49|`ff4a319d6a3086993c85c8d5ea888deeba88cc49`|
|`amazon-video-v5.3.0`|/tmp/amazon-video-recovered-v5.3.0|`9531115f1ef6326157f6d20257bd1560979a14b0`|
|`amazon-video-v5.4.0`|/mnt/e/Amazon_skill/skills/amazon_video_generation|`849dc6c715573d5169860093ffd3868b5db42e43`|

## 查看和回滚

先查看版本及差异：

```sh
git tag --list "amazon-video-*"
git show --stat amazon-video-v5.2.0
git show amazon-video-v5.3.0:skills/amazon_video_generation/SKILL.md
git diff amazon-video-v5.2.0 amazon-video-v5.4.0 -- skills/amazon_video_generation
```

只想查看或测试旧版，使用独立工作目录，当前v5.4.0不变：

```sh
git worktree add --detach ../Amazon_video_v5.2.0 amazon-video-v5.2.0
```

旧标签所在的独立工作目录沿用当时的换行规则，可能出现仅换行差异；这不代表快照缺损。若需要逐字节取出旧版，可用`git archive --format=tar --output=../amazon-video-v5.2.0.tar amazon-video-v5.2.0 skills/amazon_video_generation`后解包。

确认要启用旧版时，先提交或备份视频技能的未提交修改，再仅恢复该技能并记录新的回滚提交：

```sh
git restore --source=amazon-video-v5.2.0 --staged --worktree -- skills/amazon_video_generation
git commit -m "回滚视频技能至v5.2.0：恢复展示台背景库版本"
```

随后将此源码目录完整同步到`.agents/skills/amazon-video-generation`，核对入口版本和文件清单，再运行该版本适用的检查。恢复v5.4.0同理，替换标签即可；不需要重置整个仓库。

## 后续迭代约定

每个明确对外可见的版本完成后：更新版本号，验证并同步源码/安装副本，单独做本地提交，使用中文标题和正文记录变更、验证及限制，添加`amazon-video-v<版本>`附注标签，并补充本索引。只提交本次视频技能相关文件；未经要求不推送远程。
