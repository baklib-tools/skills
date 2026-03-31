<p align="center">
  <img src="assets/logo.svg" alt="Baklib AI Skills" width="420" height="80" />
</p>

# Baklib AI Skills

面向 **Baklib** 使用场景整理的 **Cursor Agent Skills**：在对话中由模型按 `description` 自动选用，也可手动打开对应 `SKILL.md` 作参考。

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

从本仓库的 `.cursor/skills/` 中复制需要的技能目录到本地项目的 `.cursor/skills/`（或你使用的技能加载路径），保持每个技能为独立子目录且内含 `SKILL.md`。

## 技能列表

| 技能 | 安装命令 | 说明 |
|------|----------|------|
| [baklib-data-import](.cursor/skills/baklib-data-import/SKILL.md) | `npx ctx7 skills install /baklib-tools/skills baklib-data-import` | 基于 [baklib-tools/importer](https://github.com/baklib-tools/importer) 将本地磁盘文件批量导入 Baklib（DAM，可选站点页） |

## 贡献

新增技能时：

1. 在 `.cursor/skills/<skill-name>/` 下添加 `SKILL.md`（`name` 与目录名建议一致）。
2. 在 frontmatter 的 `description` 中写清**能力**与**触发场景**，便于模型匹配。
3. 更新本 README 中的技能表。

编写约定可参考 Cursor 的 Skill 文档（如官方「创建 Skill」指南）。

---

## 相关链接

- [Baklib 官网](https://www.baklib.com)
- [Baklib 模板库（GitHub）](https://github.com/baklib-templates) — CMS / Wiki / 社区主题与示例站点
