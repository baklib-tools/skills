# baklib-data-import（本地文件批量导入 Baklib）

## 作用

基于 **[baklib-tools/importer](https://github.com/baklib-tools/importer)**，将本地磁盘上的文件批量导入 **Baklib**（资源库 DAM，可选同步到站点页）。适用于迁移素材、目录批量入库等。

导入字段、CLI 参数与错误处理以 **[SKILL.md](SKILL.md)** 为准。

## 安装

```bash
npx skills add baklib-tools/skills --skill baklib-data-import
```

手动安装：复制仓库 [`skills/baklib-data-import/`](https://github.com/baklib-tools/skills/tree/main/skills/baklib-data-import) 到本地技能目录；Importer 本体按技能正文或上游仓库说明安装。

## 使用

1. 配置 Baklib 访问方式（URL、凭据等），详见 **[SKILL.md](SKILL.md)** 与 `.config/` 约定（见仓库 [AGENTS.md](https://github.com/baklib-tools/skills/blob/main/AGENTS.md)）。
2. 按技能中的步骤调用 importer，完成映射与导入。

## 示例

- 仓库示例：[import-files.md](../../examples/import-files.md)（与本技能配套的导入说明）。

## 更新日志

- 在此补充面向使用者的变更摘要；细则见 Git 历史与本目录 **[SKILL.md](SKILL.md)**。
