# baklib-bke-markdown（Baklib BKE Markdown）

## 作用

**Baklib BKE Markdown** 的撰写、解析与导入约定：L1/L2、`dam-id`、文件卡片冒号语法、链接卡片、片段 / 分栏 / 嵌入等。完整语法表与避坑清单在同目录 **`references/`** 分篇维护；可与 **MCP** 解析 DAM 编号配合使用。

语法细节与路由以 **[SKILL.md](SKILL.md)** 为准。

## 安装

```bash
npx skills add baklib-tools/skills --skill baklib-bke-markdown
```

手动安装：复制 [`skills/baklib-bke-markdown/`](https://github.com/baklib-tools/skills/tree/main/skills/baklib-bke-markdown)（务必包含 **`references/`**）。

## 使用

撰写或回填 BKE 正文前，在会话中加载本技能并对照 **`references/`**；与 **baklib-mcp** 联用时遵守 MCP 技能中的 BKE 强制约定。

## 示例

正文示例片段见 **`references/`** 内各篇；仓库级组合示例见根目录 [examples/](https://github.com/baklib-tools/skills/tree/main/examples)。

## 更新日志

- 在此补充面向使用者的变更摘要；细则见 Git 历史与本目录 **[SKILL.md](SKILL.md)** 与 **`references/`**。
