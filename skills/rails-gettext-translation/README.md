# rails-gettext-translation（Rails + gettext 翻译工作流）

## 作用

面向 **Rails** 与 **gettext（PO/POT）** 工作流：`msgmerge` / `msgfmt`、Rails 提取任务、配合 **gpt-po-translator** 等工具批量翻译或修复 fuzzy；密钥从项目 `.config/` 或环境变量读取（与具体商业产品解耦）。

任务路由、命令示例与安全边界以 **[SKILL.md](SKILL.md)** 为准。

## 安装

```bash
npx skills add baklib-tools/skills --skill rails-gettext-translation
```

手动安装：复制 [`skills/rails-gettext-translation/`](https://github.com/baklib-tools/skills/tree/main/skills/rails-gettext-translation) 到本地技能目录。

## 使用

1. 确认 Rails 应用已配置 gettext 相关 gem 与提取任务。
2. 按 **[SKILL.md](SKILL.md)** 执行提取、合并与翻译辅助步骤。

## 示例

无独立 examples 子目录；可按 `SKILL.md` 中的命令在自有 Rails 项目中复现。

## 更新日志

- 在此补充面向使用者的变更摘要；细则见 Git 历史与本目录 **[SKILL.md](SKILL.md)**。
