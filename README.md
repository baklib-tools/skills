<p align="center">
  <img src="assets/logo.svg" alt="Baklib AI Skills" width="420" height="80" />
</p>

# Baklib AI Skills

面向 **Baklib** 使用场景整理的 **Agent Skills**（适用于支持技能加载的 AI 代理与编辑环境）：在对话中由模型按 `description` 自动选用，也可手动打开对应 `SKILL.md` 作参考。

本仓库内技能**源码**统一放在根目录 `[skills/](skills/)`（供发布与协作）；使用者在各自项目中再安装到**所用工具指定的技能目录**。存放约定见 [AGENTS.md](AGENTS.md)。

与 Baklib / 本仓库工作流相关的工具与项目外链（如 PDF 处理、本地 LLM 客户端等）见 **[docs/curated-links.md](docs/curated-links.md)**。

## 使用方式

支持两种方式，可任选其一或组合使用。

### 1. 命令行安装（推荐）

在已安装 Node.js 的环境中执行。

查看本仓库已发布技能列表：

```bash
npx skills add baklib-tools/skills --list
```

安装单个技能（将 `<skill-name>` 换成下表中的技能目录名）：

```bash
npx skills add baklib-tools/skills --skill <skill-name>
```

示例：同时安装 **baklib-mcp** 与 **baklib-bke-markdown**（常用组合）：

```bash
npx skills add baklib-tools/skills --skill baklib-mcp --skill baklib-bke-markdown
```

示例：仅安装数据导入技能：

```bash
npx skills add baklib-tools/skills --skill baklib-data-import
```

具体行为与参数以 `skills` 包 CLI 为准（可执行 `npx skills --help` 查看）。

技能用法与效果示例见目录 **[examples/](examples/README.md)**（含截图与可运行 HTML）。

### 2. 手动拷贝

从本仓库根目录的 `skills/<skill-name>/` 复制到**你自己项目**中的技能安装目录（**具体路径以所用 Agent 或编辑器的技能安装说明为准**），保持每个技能为独立子目录且内含 `SKILL.md`。

## 外部技能（Git Submodule）

除根目录 [`skills/`](skills/) 下由本仓库**直接维护**的发布技能外，仓库在 **`external-skills/`** 中通过 **Git Submodule** 引入外部社区的优质技能、设计规范索引等资源，便于本地查阅或对照参考（**不等同**于 `skills/` 下的安装目标；安装到个人项目时仍以本仓库 `skills/<name>/` 为源、并按工具文档落位）。

克隆本仓库后若需拉取子模块内容，请执行：

```bash
git submodule update --init --recursive
```

| 子模块 | 说明 |
| ------ | ---- |
| [awesome-design-md](external-skills/awesome-design-md/README.md) | 来自 [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 的设计相关 Markdown / 品牌设计参考索引 |
| [buffett-skills](external-skills/buffett-skills/README.md) | 来自 [agi-now/buffett-skills](https://github.com/agi-now/buffett-skills) 的巴菲特投资思维框架相关技能与参考文档（[README 中文版](external-skills/buffett-skills/README.zh.md)） |

新增或更新子模块时请在变更说明中写清来源与用途；引用或摘录内容仍须遵守 [AGENTS.md](AGENTS.md) 中的脱敏与可移植性约定。

## 技能列表


| 技能                                                                         | 安装命令                                                                       | 说明                                                                                                                                                                                                                                          |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [baklib-data-import](skills/baklib-data-import/SKILL.md)                   | `npx skills add baklib-tools/skills --skill baklib-data-import`          | 基于 [baklib-tools/importer](https://github.com/baklib-tools/importer) 将本地磁盘文件批量导入 Baklib（DAM，可选站点页） [使用例子](examples/import-files.md)                                                                                                         |
| [mineru-office-to-markdown](skills/mineru-office-to-markdown/SKILL.md)     | `npx skills add baklib-tools/skills --skill mineru-office-to-markdown`  | 使用 [MinerU](https://github.com/opendatalab/mineru) 在本地将 PDF / DOCX / PPTX / XLSX / 图片转为 Markdown，供知识库与录入前处理（含目录批量注意事项）                                                                                                                                 |
| [git-commit](skills/git-commit/SKILL.md)                                   | `npx skills add baklib-tools/skills --skill git-commit`                  | 分析 git 变更、建议拆分提交并生成规范提交信息（Conventional Commits）                                                                                                                                                                                             |
| [rails-gettext-translation](skills/rails-gettext-translation/SKILL.md)     | `npx skills add baklib-tools/skills --skill rails-gettext-translation` | **Rails + gettext**：`msgmerge` / `msgfmt`、Rails 提取任务、**gpt-po-translator** 批量译 PO / 修 fuzzy；密钥从 `.config/` 或环境变量加载（与具体产品无关）                                                                                                                    |
| [baklib-mcp](skills/baklib-mcp/SKILL.md)                                   | `npx skills add baklib-tools/skills --skill baklib-mcp`                  | Baklib MCP：鉴权、优先 MCP 操作 KB/站点/DAM；站点页 `signed_id` 经 MCP 按 purpose（表单 `dynamic_form`）获取                                                                                                                                 |
| [baklib-intake-assistant](skills/baklib-intake-assistant/SKILL.md)         | `npx skills add baklib-tools/skills --skill baklib-intake-assistant`     | 结合 Baklib MCP 做录入；约定镜像根下 `知识库/`、`资源库/`、`站点/` 存 Markdown，**SQLite** 台账；含 [scripts](skills/baklib-intake-assistant/scripts/README.md)（`status`/`health_check`/`plan_sync` 等），见 [local-mirror](skills/baklib-intake-assistant/local-mirror.md) |
| [baklib-bke-markdown](skills/baklib-bke-markdown/SKILL.md)                 | `npx skills add baklib-tools/skills --skill baklib-bke-markdown`        | Baklib **BKE Markdown** 撰写与导入（L1/L2、`dam-id`、文件卡片冒号语法、链接卡片、片段/分栏/嵌入等；详规见同目录 **`references/`**）；可配合 MCP 解析 DAM 编号                                                                                                                                 |
| [nano-banana-pro-prompting](skills/nano-banana-pro-prompting/SKILL.md)     | `npx skills add baklib-tools/skills --skill nano-banana-pro-prompting`   | Gemini 3 Pro Image（Nano Banana Pro）**提示词撰写**与复查（不含脚本/API）                                                                                                                                                                                   |
| [image-generation](skills/image-generation/SKILL.md)                       | `npx skills add baklib-tools/skills --skill image-generation`            | 图像生成**工作流总览**；须配合 `image-generation-ucloud` / `image-generation-openrouter` 等**服务商子技能**才能实际出图                                                                                                                                               |
| [image-generation-ucloud](skills/image-generation-ucloud/SKILL.md)         | `npx skills add baklib-tools/skills --skill image-generation-ucloud`     | **UCloud ModelVerse** 图像 API（鉴权、端点、模型要点）                                                                                                                                                                                                    |
| [image-generation-openrouter](skills/image-generation-openrouter/SKILL.md) | `npx skills add baklib-tools/skills --skill image-generation-openrouter` | **OpenRouter** 出图（chat/completions、modalities 等）                                                                                                                                                                                            |
| [requirements-to-published-content](skills/requirements-to-published-content/SKILL.md) | `npx skills add baklib-tools/skills --skill requirements-to-published-content` | **工作流**：需求采集→分析→方案→对外文稿→（可选）配图 / 公众号 HTML / Baklib 站点发布；可扩展更多渠道                                                                                                                                 |
| [wechat-mp-html](skills/wechat-mp-html/SKILL.md)                           | `npx skills add baklib-tools/skills --skill wechat-mp-html`              | **微信公众号图文** HTML：`#js_content`、inline 样式、标准「复制正文到公众号」脚本；详规见 **`references/`**                                                                                                                                   |


## 贡献

新增技能前请先阅读 [AGENTS.md](AGENTS.md)（脱敏、技能边界、可移植性）。然后：

1. 在仓库根目录 `skills/<skill-name>/` 下添加 `SKILL.md`（`name` 与目录名建议一致）。
2. 在 frontmatter 的 `description` 中写清**能力**与**触发场景**，便于模型匹配。
3. 更新本 README 中的技能表。
4. 若从外部仓库以子模块形式纳入参考资源，放在 `external-skills/` 并同步更新上文「外部技能」表格。

编写约定可参考**具备 Skill 能力的平台**的公开文档（例如各编辑器或 Agent 产品附带的「创建 Skill」说明）。

---

## 相关链接

- [Baklib 官网](https://www.baklib.com)
- [Baklib 模板库（GitHub）](https://github.com/baklib-templates) — CMS / Wiki / 社区主题与示例站点

