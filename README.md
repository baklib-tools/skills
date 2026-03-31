# Baklib AI Skills

本仓库收集与 **Baklib** 相关的 Cursor Agent Skills，供在对话中自动匹配或手动引用。

## 使用方式

有两种常见用法，任选其一（或组合使用）：

### 1. 命令行（Context7）

通过 [Context7 安装说明](https://github.com/upstash/context7#installation) 一键为编辑器配置「CLI + Skills」或 MCP。官方推荐入口为：

```bash
npx ctx7 setup
```

针对 Cursor 时可加 `--cursor`；亦可使用 `--claude`、`--opencode` 等目标。向导会完成 OAuth、API Key（可选，见 [context7.com/dashboard](https://context7.com/dashboard)）及技能安装。**具体子命令与参数以 Context7 仓库文档为准**；若上游提供类似 `ctx7 install …` 的安装方式，同样以该文档为准。

### 2. 仓库直连（本仓库 `.cursor/skills/`）

将本仓库克隆或加入工作区后，Cursor 会读取 `.cursor/skills/` 下各技能目录中的 `SKILL.md`。技能元数据中的 `description` 用于判断是否与当前任务相关。

## 技能列表

| 技能 | 说明 |
|------|------|
| [baklib-data-import](.cursor/skills/baklib-data-import/SKILL.md) | 使用 [baklib-tools/importer](https://github.com/baklib-tools/importer) 将本地磁盘文件批量导入 Baklib（DAM / 可选站点页） |

## 贡献

新增技能时：在 `.cursor/skills/<skill-name>/` 下放置 `SKILL.md`，并在上表中登记；`name` 与目录名建议一致，描述需写清能力与触发场景（见 Cursor 官方「创建 Skill」约定）。
