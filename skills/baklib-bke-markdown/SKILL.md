---
name: baklib-bke-markdown
description: Self-contained guide for writing Baklib BKE Markdown (L1/L2, DAM dam-id, file colon-syntax, link cards, fragments, embeds, tables). Use when authoring or importing BKE Markdown, inserting DAM assets, or resolving DAM ids via MCP; not for editor implementation or maintaining product docs repos.
---

# BKE Markdown 撰写指南（独立副本）

本文件**单独发布即可使用**，不依赖其它仓库路径。BKE 是 Baklib 基于 Tiptap 的编辑器；交换格式在 **标准 Markdown / GFM** 之上增加 **圆括号第三段引号** 与 **成对 HTML 注释块（L2）**。

## 何时阅读详规

- 撰写或改写 **DAM 图 / 文件卡片 / 站内链接 / L2 块** 前，按需打开下表中的 `references/` 文件。
- **完整分节语法、表格与示例**放在 `references/`，便于主文件保持较短篇幅并支持渐进加载（与 [AGENTS.md](https://github.com/baklib-tools/skills/blob/main/AGENTS.md) 约定一致）。

## 速查（加载本技能时必读）

1. **圆括号第三段**：通常为 `键=值` 空格分隔；**文件卡片**第三段为 `dam-id:` / `dam-type:`（**冒号**），`sync-master:false` 亦为冒号。
2. **L2 块**：`<!-- bke:<类型>#<配对id> 键=值 -->` … `<!-- /bke:<类型>#<配对id> -->`；配对 id 仅用于锚定，**不是** `dam-id`。
3. **DAM 资源**：手写 Markdown 以 **`dam-id`**（工作台打开资源时地址栏编号）为主；与产品内部其它 id 字段区分。
4. **`bke:link-card`**：注释内**不写** `display=`、`signed-id=`。

## 详细文档（`references/`）

| 章节 | 文件 |
|------|------|
| 第 1–4 节：总则、链接、图片、文件卡片 | [references/syntax-core.md](references/syntax-core.md) |
| 第 5–11 节：链接卡片、片段、分栏、标注框、嵌入等 | [references/syntax-blocks.md](references/syntax-blocks.md) |
| 第 12–19 节：表格、任务列表、标题区、段落对齐、markdownBlock 等 | [references/syntax-gfm-and-advanced.md](references/syntax-gfm-and-advanced.md) |
| 第 20 节：DAM 与 MCP | [references/dam-mcp.md](references/dam-mcp.md) |
| 第 21–22 节：自检清单、版本说明 | [references/checklist-and-versioning.md](references/checklist-and-versioning.md) |

## 版本与复制说明

- 语法以 Baklib BKE **面向用户的交换格式**为准；自检与版本说明见 [references/checklist-and-versioning.md](references/checklist-and-versioning.md)。
- 分发本技能时：须包含 **`SKILL.md` 与整个 `references/` 目录**（若另有 `scripts/`、`assets/` 等亦一并保留）。
