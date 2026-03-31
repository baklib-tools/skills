<p align="center">
  <img src="assets/logo.svg" alt="Baklib AI Skills" width="420" height="80" />
</p>

# Baklib AI Skills

面向 **Baklib** 使用场景整理的 **Cursor Agent Skills**：在对话中由模型按 `description` 自动选用，也可手动打开对应 `SKILL.md` 作参考。

本仓库内技能**源码**统一放在根目录 [`skills/`](skills/)（供发布与协作）；使用者在各自项目中再安装到 `.cursor/skills/` 等路径。存放约定见 [AGENTS.md](AGENTS.md)。

## 使用方式

支持两种方式，可任选其一或组合使用。

### 1. 命令行安装（推荐）

在已安装 Node.js 的环境中执行（将 `<skill-name>` 换成下表中的技能目录名）：

```bash
npx ctx7 skills install /baklib-tools/skills <skill-name>
```

示例：安装数据导入技能：

```bash
npx ctx7 skills install /baklib-tools/skills baklib-data-import
```

具体行为与参数以 [Context7](https://github.com/upstash/context7#installation) 当前 CLI 文档为准。

### 2. 手动拷贝

从本仓库根目录的 `skills/<skill-name>/` 复制到**你自己项目**中的 Cursor 技能目录（常见为 `.cursor/skills/<skill-name>/`，以你使用的加载方式为准），保持每个技能为独立子目录且内含 `SKILL.md`。

## 技能列表

| 技能 | 安装命令 | 说明 |
|------|----------|------|
| [baklib-data-import](skills/baklib-data-import/SKILL.md) | `npx ctx7 skills install /baklib-tools/skills baklib-data-import` | 基于 [baklib-tools/importer](https://github.com/baklib-tools/importer) 将本地磁盘文件批量导入 Baklib（DAM，可选站点页） |
| [baklib-mcp-config](skills/baklib-mcp-config/SKILL.md) | `npx ctx7 skills install /baklib-tools/skills baklib-mcp-config` | 使用 Baklib MCP 操作线上数据 |
| [nano-banana-pro-prompting](skills/nano-banana-pro-prompting/SKILL.md) | `npx ctx7 skills install /baklib-tools/skills nano-banana-pro-prompting` | Gemini 3 Pro Image（Nano Banana Pro）**提示词撰写**与复查（不含脚本/API） |
| [image-generation](skills/image-generation/SKILL.md) | `npx ctx7 skills install /baklib-tools/skills image-generation` | 图像生成**工作流总览**；须配合 `image-generation-ucloud` / `image-generation-openrouter` 等**服务商子技能**才能实际出图 |
| [image-generation-ucloud](skills/image-generation-ucloud/SKILL.md) | `npx ctx7 skills install /baklib-tools/skills image-generation-ucloud` | **UCloud ModelVerse** 图像 API（鉴权、端点、模型要点） |
| [image-generation-openrouter](skills/image-generation-openrouter/SKILL.md) | `npx ctx7 skills install /baklib-tools/skills image-generation-openrouter` | **OpenRouter** 出图（chat/completions、modalities 等） |

## 贡献

新增技能前请先阅读 [AGENTS.md](AGENTS.md)（脱敏、技能边界、可移植性）。然后：

1. 在仓库根目录 `skills/<skill-name>/` 下添加 `SKILL.md`（`name` 与目录名建议一致）。
2. 在 frontmatter 的 `description` 中写清**能力**与**触发场景**，便于模型匹配。
3. 更新本 README 中的技能表。

编写约定可参考 Cursor 的 Skill 文档（如官方「创建 Skill」指南）。

---

## 相关链接

- [Baklib 官网](https://www.baklib.com)
- [Baklib 模板库（GitHub）](https://github.com/baklib-templates) — CMS / Wiki / 社区主题与示例站点
