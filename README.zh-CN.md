# 植株商品图 Skill 集合

当前包含一个正式 skill：**lovart-plant-product-images**。英文规则负责执行，中文文档负责使用说明；仍支持中文大白话输入。优先解决商品走样、融合生硬和构图难控制。

本目录是独立的本地 Git 仓库，日期为 2026-10-14。第一版本纳入本地初始提交，后续由你配置远程仓库并推送；许可证按你的决定暂缓。生成的 dist/ 压缩包保留在本地，不重复纳入 Git。

## 文件入口

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](skills/lovart-plant-product-images/SKILL.md) | Agent 安装后发现和执行的英文入口 |
| [完整 Lovart 指令](skills/lovart-plant-product-images/LOVART_INSTRUCTIONS.md) | 在 Lovart 内创建自定义 skill 的完整文本，不依赖读取本地模块 |
| [references](skills/lovart-plant-product-images/references/) | 八个功能模块，以及 Lovart 执行适配说明 |
| [设计与后续计划](docs/DESIGN.zh-CN.md) | 已确认决策、集合结构、后期整套 Amazon 图片开发 |
| [验收案例](skills/lovart-plant-product-images/evaluation/CASES.md) | 中文/英文需求及预期行为 |
| [验证状态](docs/VALIDATION.md) | 本轮检查与仍待进行的实图验证 |

## 在 Lovart 中使用

1. 打开项目并启用 Thinking Mode。官方要求本会话至少已有一次 Agent 对话，才可创建自定义 skill。
2. 打开上面的完整指令文件，将正文作为对话中的工作规则提供给 Lovart。可先输入：“请按以下规则处理植株商品图片，之后我会提供商品图和具体要求。”随后粘贴完整英文规则。
3. 上传实拍与必要参考图，完成一个具体任务并检查结果。用户继续在 Lovart 界面选择图像模型；skill 不替你切换。
4. 打开 Skill Book → Create a Skill → 保存到 My Skills。可命名为“植株商品生图”。
5. 查看并编辑保存后的指令，核对商品保护、图源角色、真实尺寸、三轮修复等关键规则没有被自动总结丢失。若当前编辑器允许，可将完整指令作为保存的执行内容；平台长度与附件支持以实际界面为准，未做账户内验证。
6. 新对话中从 Skill Book 选择这个 skill，再上传商品图并输入大白话。

以上流程依据 [Lovart 官方文档](https://www.lovart.ai/docs/how-to-prompt/agent-skills)。本包不承诺 Lovart 能从 GitHub 直接导入通用 SKILL.md，也不承诺只输入名称就已加载 My Skills。

可直接试用的请求：

> 使用植株商品生图。将这束花放在欧式阳台上，花束是售卖商品，花盆只是道具，保持原花材数量、颜色和纹理。略微俯视，但看得清盆身。生成 1 张 2048×2048 的 PNG。

这里的张数、像素与格式只是示例。你实际使用时指定自己的规格，已有确认规格可沿用。

## 在其他 Agent 中安装和选择

集合采用 skills/技能名/SKILL.md 结构。安装工具将各 skill 注册到目标 Agent 后，支持自动发现的 Agent 可根据名称和描述判断使用哪一项，再按需读取模块。当前只有一个 skill，八个功能模块不需要分别安装；以后可以继续加入其他有明确职责的 skill。

**把仓库克隆下来不等于完成安装；安装指令也不等于获得 Lovart 生图能力。** Agent 必须实际有可用的 Lovart 工具或浏览器访问能力。没有连接时，会给出可粘贴到 Lovart 的提示词、参考图角色及缺失信息，并说明尚未执行出图。

本地可选用第三方 [skills CLI](https://github.com/vercel-labs/skills)，需要 Node.js/npm。在集合根目录执行：

```sh
npx skills add . --list
npx skills add . --skill lovart-plant-product-images
```

安装时按提示选择目标 Agent。也可以按目标 Agent 的官方安装方式复制完整 skill 文件夹。请保留 references、scripts 等随附资源。本轮只准备安装说明，没有运行安装或改动全局配置。

将来创建 GitHub 仓库后，把 OWNER/REPOSITORY 换成真实仓库标识：

```sh
npx skills add OWNER/REPOSITORY --list
npx skills add OWNER/REPOSITORY --skill lovart-plant-product-images
npx skills add OWNER/REPOSITORY --skill '*'
```

最后一条选择仓库当前所有 skill，由安装器提示选择目标 Agent；不表示今后新增 skill 会自动安装。当前仓库地址与许可证未确定，这些命令是发布后的使用模板。

## 日常工作规则

- 真实植物、仿真植物、花环、花束、盆栽、花箱均支持。
- 未指定场景/道具时，可自主选现实欧式住宅环境；用户明确指定的环境优先。
- 售卖主体和随货配件保留；装饰道具可调整。明确要求时可作实物允许的造型整理，不复制花材增加丰满度。
- 添加其他装饰花材需要明确要求。
- 场景可做视觉比例匹配；尺寸图必须提供真实数值、单位和测量部位。
- 细节图可自动拟写简短英文外观文案，默认模型直接绘字；不得编造性能、成分或随货清单。
- 比例、像素、张数、格式由用户指定；模型沿用用户在 Lovart 的选择。
- 首次生成后最多三轮自动修复，所有模块与候选共用预算；超限后文字说明问题。
- 仅要求提示词/讨论时不生图。整套 Amazon 图片规划与生产留给后续版本。

## 更新与验证

维护英文 SKILL.md 和 references 后，在集合根目录运行：

```sh
python skills/lovart-plant-product-images/scripts/build_lovart_instructions.py
python skills/lovart-plant-product-images/scripts/build_lovart_instructions.py --check
```

脚本只使用 Python 3.10+ 标准库，生成/核对完整指令，不连接 Lovart、不生成图片、不进行 Git 操作。不要直接修改生成版后忘记更新源文件。

当前可以进行本地试用。公开发布前再确定仓库地址和许可证；本包未附开源授权。
