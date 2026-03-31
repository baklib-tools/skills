---
name: image-generation
description: >-
  图像生成工作流总览：何时出图、如何选用后端子技能、与提示词技能配合。
  在用户需要配图/示意图、选择 UCloud 或 OpenRouter 等 API 出图、或询问本仓库「出图技能怎么组合」时使用。
---

# 图像生成（总技能）

## 执行前提：须配合服务商子技能

本总技能**不能**单独完成「调 API、运行脚本、产出图像」；只说明工作流、组合方式与密钥检查原则，**不包含**任一服务商的完整端点、请求体与可执行命令。

- **必须**与至少一个 **`image-generation-<服务商>`** 子技能同时使用（当前为 **`image-generation-ucloud`**、**`image-generation-openrouter`**；以后仓库若增加其它供应商，命名约定见下表）。实际出图时以**对应子技能**的 `SKILL.md` 与目录内脚本为准。
- 若环境中**仅有**本总技能、**没有**任一端子技能，代理应**先**请用户选定或说明打算使用的后端（或根据已有密钥推断），再打开该子技能；**不要**仅凭本文件自行拼凑 HTTP 调用。
- **提示词类技能**（如 `nano-banana-pro-prompting`）可与总技能、服务商子技能组合，但**不能**替代服务商子技能完成鉴权与请求。

## 命名与组合规则（开源场景）

本仓库将「出图」拆成 **1 个总技能 + 若干后端子技能**，避免把某一云厂商或某一账号流程写死为唯一路径。

| 类型 | 目录名（`name`） | 何时阅读 |
|------|------------------|----------|
| 总览 | `image-generation` | 工作流、授权、与提示词技能配合、选哪个后端 |
| UCloud ModelVerse | `image-generation-ucloud` | 使用 UCloud 文档中的 ModelVerse 图像 API |
| OpenRouter | `image-generation-openrouter` | 使用 OpenRouter 调用 Gemini 等图像能力 |

**约定**：以后若增加其他供应商，使用同一前缀 `image-generation-` + 短后缀（如 `image-generation-xxx`），并在本文件表格中补充一行。

## 本技能做什么

- 说明 **何时** 适合调用出图能力（含与正文/营销文案的配合方式）。
- 指引 **下一步** 应打开哪个子技能（按用户实际使用的接口）。
- 指向本仓库已有的 **提示词专项技能**（见下文），与「如何调 HTTP」解耦。

## 本技能不做什么

- **不**作为可独立执行的出图技能：端点、模型 ID、脚本路径与参数以各 **`image-generation-*` 服务商子技能**为准，本文件不重复罗列以免与子技能脱节。
- **不**代替用户保管或填写密钥、**不**承诺计费与配额；密钥与费用以各平台控制台为准。
- **不**把某一项目的私有目录、内部规范文件名写死为唯一路径；你应在**自己的项目**里维护风格说明与占位约定。
- 提示词撰写原则见 `nano-banana-pro-prompting`；**单次 API 请求的提示词须自包含**，勿假设模型能「记住上一张图」（见该技能与 [AGENTS.md](../../AGENTS.md)）。

## 与提示词技能的关系

- **撰写/优化** Nano Banana（Gemini 3 Pro Image）类提示词：使用 **[nano-banana-pro-prompting](../nano-banana-pro-prompting/SKILL.md)**。
- **调用哪个 HTTP 接口**：按后端阅读 **`image-generation-ucloud`** 或 **`image-generation-openrouter`**；二者与提示词技能正交，可任意组合。

## 执行前检查 API 密钥（代理必读）

在运行各服务商脚本或替用户发起出图请求之前，**先确认**对应密钥是否已配置；若未配置，**不要静默失败**，应提示用户**优先**在**项目根目录**下创建 **`.config/`** 内密钥文件（再备选环境变量）：

| 后端 | 优先（项目根） | 备选（环境变量） |
|------|----------------|------------------|
| UCloud | `.config/UCLOUD_API_KEY` | `UCLOUD_API_KEY` |
| OpenRouter | `.config/OPENROUTER_API_KEY` | `OPENROUTER_API_KEY` |

文件内容为**单行**密钥文本，UTF-8 编码；**勿**将密钥写入仓库或技能正文。脚本会从项目根向上查找含 `.config` 的目录（详见各子技能说明）。

## 工作流建议（通用）

1. **先定模型与风格**（是否用 Gemini 3 Pro Image、是否需图内文字等），再写提示词文件（UTF-8）。
2. **再选后端**：有 UCloud ModelVerse 密钥则读 `image-generation-ucloud`；若使用 OpenRouter 则读 `image-generation-openrouter`。
3. **再执行**：由用户或 CI 在本地运行其脚本/工具发起请求；代理可协助检查命令行参数与错误信息含义，但**不**默认代跑生产密钥请求（除非你明确授权且环境已配置）。

### 与「文章成稿」类任务的配合

- 若正文中仅有配图占位，**不要默认自动出图**；在用户**明确**要求生成配图或等价指令后再执行出图与替换占位。
- 若任务本身已包含「生成配图」「成片」等授权，可按该任务技能执行，仍建议 **Nano Banana + 选定后端** 与项目规范一致。

## 参考脚本（按服务商拆分）

各云厂商的 **模型 ID、参数、请求体** 差异大，本仓库将 **Python 示例脚本放在对应子技能目录**，避免一个脚本里堆满互斥逻辑：

| 服务商 | 脚本路径 | 依赖 |
|--------|----------|------|
| UCloud ModelVerse | [`image-generation-ucloud/scripts/generate_ucloud_image.py`](../image-generation-ucloud/scripts/generate_ucloud_image.py) | `requests` |
| OpenRouter | [`image-generation-openrouter/scripts/generate_openrouter_image.py`](../image-generation-openrouter/scripts/generate_openrouter_image.py) | `requests` |

将对应技能目录复制到你项目中的 Cursor 技能路径后，在项目根执行；脚本通过向上查找含 **`.config`** 的目录定位密钥文件，详见各脚本 `--help`。本仓库**不提供**本地离线出图示例脚本（能力因环境差异大，由用户自行选用工具链）。

**总技能目录不再提供**「三合一」聚合脚本；换后端时换目录与脚本即可。

## 失败时

- 优先根据 **stderr 与各平台返回** 判断是鉴权、模型名、尺寸还是限流。
- 可在 **不泄露密钥** 的前提下，切换到另一后端子技能中的流程（例如 UCloud 不可用时改用 OpenRouter），并相应调整模型与尺寸参数。
