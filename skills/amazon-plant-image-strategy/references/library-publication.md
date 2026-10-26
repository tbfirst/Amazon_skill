# 完整库构建与发布范围（1.11.0）

维护者需要扩库、导出或准备独立资源发布时读取。普通用户直接用reference-library流程。

本版本保留阶段A构建契约，并实现阶段B的通用HTTPS同步、按需取图和缓存状态，操作见[远程图库](library-remote.md)。没有自动上传或切正式stable；本轮使用双私有HTTPS测试源，候选构建成功不等于已开通云服务。

## 发布规则

使用`assets/reference-library/publication-policy.json`，schemaVersion=1。defaults目前为`status=published, scopes=[text]`；images/cards/recipes可按已有ID覆盖。未知ID、未知scope或非法状态报错。状态为published/draft/withdrawn；scope为text/preview/original。

- image必须已通过视觉复用审核；拒绝、hold、未观察或历史禁止展示不能由发布规则强行放行。
- 明确进入A+产品模板的图必须有唯一已审核principalProduct。身份冲突不自动合并。
- 默认text发布原创观察和结构提示词；不自动分发源图片。preview/original分别由维护者按可分发范围配置。
- selection只控制离线精选，不限制完整发布集合。构建读取全部主库图像和全部series。
- withdrawn图从正常索引和配方分支排除，系列保留原图位和原因，另列入revocations。客户端同步后，已知撤回ID即使有旧缓存也不能再成为正常候选或重新获取；自动物理清理与完整跨项目撤回传播仍待后续。

示例为结构说明，其中IMG-ID应替换为真实已审核ID：

```json
{
  "schemaVersion": 1,
  "defaults": {"status": "published", "scopes": ["text"]},
  "images": {
    "IMG-ID": {"scopes": ["text", "preview", "original"], "reason": "此图已确认可按该范围分发"}
  },
  "cards": {},
  "recipes": {}
}
```

## 维护者命令

先完成采集、看图审核、approved-only同步和主库导出，再构建到与主库分离的目录。使用实际安装路径和本次不可变版本号：

```powershell
$skillRoot = 'E:/Amazon_skill/skills/amazon-plant-image-strategy'
python -B -X utf8 "$skillRoot/scripts/library_build.py" build --source-root 'E:/Amazon_generate/plant/library' --output 'E:/Amazon_skill/outputs/library-publication' --version '2026.10.22.1' --policy "$skillRoot/assets/reference-library/publication-policy.json"
python -B -X utf8 "$skillRoot/scripts/library_build.py" verify 'E:/Amazon_skill/outputs/library-publication/versions/2026.10.22.1/manifest.json'
python -B -X utf8 "$skillRoot/scripts/library_catalog.py" search --manifest 'E:/Amazon_skill/outputs/library-publication/versions/2026.10.22.1/manifest.json' --kind image --image-type '细节图' --limit 5
```

构建和完整校验需要Pillow；普通文字检索不需要。仅给已实际规划的不可变版本目录填写`--base-url https://实际域名/versions/版本/`；该参数只写资源定位，不证明URL已上传或能访问。没有真实托管地址时省略，不生成虚构URL。候选manifest始终包含`status=candidate, hostingVerified=false`。

同名版本禁止覆盖；修正后使用新版本。构建先在独立staging目录生成并校验，成功后改名提交；失败不修改旧版本、源主库或stable。结束前重新检查源JSON哈希；采集/导出期间源库改变会停止本次构建。大批收录建议先冻结主库副本。

## 输出契约

| 文件 | 内容 |
| --- | --- |
| versions/版本/manifest.json | kind、schemaVersion=1、libraryVersion、minSkillVersion、各JSON哈希/字节数、覆盖数、源快照哈希 |
| search-index.json | 全部正常发布记录的轻量摘要、逐图record描述符与各类media描述符 |
| records/前缀/记录哈希.json | 完整观察/recipe、来源、审核、独立记录与提示词修订号 |
| cards.json / recipes.json | 模板与配方，配方只保留可发布来源与实际存在的逐图分支 |
| series.json | 全部源系列、原始members顺序、变体、明确缺口与published状态 |
| coverage.json / revocations.json | 放行/排除理由、使用的规则与撤回记录 |
| previews/ / originals/ | 仅所配置范围内的文件；各自SHA-256、实际格式/尺寸/字节数 |
| candidate-版本.json | 本地候选manifest位置与哈希；不是stable发布指针 |

预览保留整幅构图，最长边至多1000像素、WebP编码；透明度保留，不承诺固定KB。原图复制原始字节，扩展名按解码格式保存。预览哈希不能拿原图哈希替代；原图内容改变需新图像身份，文字修订改变详细记录哈希但保留IMG-ID。

## 消费与验收

`library_catalog.py search/show --manifest 实际路径`与旧`--catalog`、`--source-root`分开解析；未知schema或不兼容minSkillVersion报错。搜索读取轻量索引，不展开全部逐图recipe；show按ID验证所选详细记录。available/localAvailable仅代表本地已验证文件；缺图仍可读文字，不假装已看图或可远程下载。

`prepare-hosting --manifest 路径 --output 新目录`把同一版本分成metadata和media两棵目录树，前者不含图片；`private-channel --manifest 路径 --manifest-url 实际HTTPS地址 --output 新文件`生成带清单哈希的私有频道候选。两者不上传、不切正式stable。上传时先放资源和详细记录，再放manifest；普通消费者验证通过后才切频道。本轮尚未连接真实云源。客户端已能通过可信配置同步完整索引并按需取图；agent保存实际libraryVersion/manifestHash，自动项目锁文件和迁移工具仍待后续阶段。

回归包含：独立目录无作者源盘、完整集合不受selection限制、拒绝/撤回排除且图序保留、预览/原图独立哈希、源文件变更失败、不可变版本不覆盖、坏索引和未知schema拒绝、缺图分支可读但错误ID拒绝。真实完整库另运行build/verify并保存覆盖报告。
