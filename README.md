# Baklib AI Skills

本仓库收集与 **Baklib** 相关的 Cursor Agent Skills，供在对话中自动匹配或手动引用。

## 使用方式

将本仓库克隆或加入工作区后，Cursor 会读取 `.cursor/skills/` 下各技能目录中的 `SKILL.md`。技能元数据中的 `description` 用于判断是否与当前任务相关。

## 技能列表

| 技能 | 说明 |
|------|------|
| [baklib-data-import](.cursor/skills/baklib-data-import/SKILL.md) | 使用 [baklib-tools/importer](https://github.com/baklib-tools/importer) 将本地磁盘文件批量导入 Baklib（DAM / 可选站点页） |

## 贡献

新增技能时：在 `.cursor/skills/<skill-name>/` 下放置 `SKILL.md`，并在上表中登记；`name` 与目录名建议一致，描述需写清能力与触发场景（见 Cursor 官方「创建 Skill」约定）。
