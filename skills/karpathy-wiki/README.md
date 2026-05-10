# karpathy-wiki（Karpathy 式个人知识库）

## 作用

通过 LLM 构建**持续进化**的个人知识库：**raw / wiki / schema** 三层架构，以及 **Ingest**、**Query**、**Lint** 等核心操作思路（Karpathy 方法）。用于将 AI 从一次性检索器升级为「知识编译器」。

目录布局、操作契约与约束以 **[SKILL.md](SKILL.md)** 为准。

## 安装

```bash
npx skills add baklib-tools/skills --skill karpathy-wiki
```

手动安装：复制 [`skills/karpathy-wiki/`](https://github.com/baklib-tools/skills/tree/main/skills/karpathy-wiki)。

## 使用

在对话中说明「按 Karpathy / 卡帕西方法维护知识库」或加载本技能后，按 **[SKILL.md](SKILL.md)** 在本地工作区初始化三层目录并逐步 ingest；查询与校验流程遵循同文件。

## 示例

无固定 HTML 示例；可在自有笔记仓库中按 `SKILL.md` 搭建最小 wiki。

## 更新日志

- 在此补充面向使用者的变更摘要；细则见 Git 历史与本目录 **[SKILL.md](SKILL.md)**。
