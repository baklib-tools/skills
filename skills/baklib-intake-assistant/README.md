# baklib-intake-assistant（Baklib 录入与本地镜像台账）

## 作用

结合 **Baklib MCP** 做内容录入；约定本地镜像根下 **`知识库/`**、**`资源库/`**、**`站点/`** 存放 Markdown，并用 **SQLite** 台账跟踪同步状态。同目录提供 **[scripts/](scripts/README.md)**（如 `status`、`health_check`、`plan_sync`），以及 **[local-mirror.md](local-mirror.md)** 等补充说明。

操作流程、目录约定与脚本用法以 **[SKILL.md](SKILL.md)** 为准。

## 安装

```bash
npx skills add baklib-tools/skills --skill baklib-intake-assistant
```

手动安装：复制 [`skills/baklib-intake-assistant/`](https://github.com/baklib-tools/skills/tree/main/skills/baklib-intake-assistant) 到本地技能目录（含 `scripts/`、`references/` 等）。

## 使用

1. 配置 Baklib MCP 与本地镜像路径。
2. 按 **[SKILL.md](SKILL.md)** 与 **scripts/README.md** 维护台账与同步计划。

## 示例

脚本参数与典型会话见 **[scripts/README.md](scripts/README.md)**；镜像结构见 **[local-mirror.md](local-mirror.md)**。

## 更新日志

- 在此补充面向使用者的变更摘要；细则见 Git 历史与本目录 **[SKILL.md](SKILL.md)**。
