# baklib-mcp（Baklib MCP 使用指南）

## 作用

说明如何在已接入 **MCP** 的 AI 环境中配置并使用 **Baklib MCP**：鉴权、客户端配置，以及对知识库 / 站点 / 资源库（DAM）等操作的**优先走 MCP** 规范；站点页 DAM `signed_id`、**BKE Markdown** 与配套技能 **baklib-bke-markdown** 的组合要求均在技能正文中约定。

完整强制规则与工具组合以 **[SKILL.md](SKILL.md)** 为准。

## 安装

```bash
npx skills add baklib-tools/skills --skill baklib-mcp
```

常与 **baklib-bke-markdown** 一并安装：

```bash
npx skills add baklib-tools/skills --skill baklib-mcp --skill baklib-bke-markdown
```

手动安装：复制 [`skills/baklib-mcp/`](https://github.com/baklib-tools/skills/tree/main/skills/baklib-mcp)。MCP Server 见上游 **[baklib-mcp-server](https://github.com/xiaohui-zhangxh/baklib-mcp-server)** 文档。

## 使用

1. 按 **[SKILL.md](SKILL.md)** 配置 MCP 与凭据（遵守 `.config/` 约定）。
2. 任意**写入**线上 Baklib 前须征得用户确认；读取与摘要优先使用 MCP 工具返回的真实数据。

## 示例

无单独 HTML 示例；可与仓库内 **baklib-intake-assistant**、**requirements-to-published-content** 等工作流技能组合使用。

## 更新日志

- 在此补充面向使用者的变更摘要；细则见 Git 历史与本目录 **[SKILL.md](SKILL.md)**。
