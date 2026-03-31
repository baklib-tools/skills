---
name: git-commit
description: 分析当前仓库的 git 变更（staged/unstaged/untracked），判断是否需要拆分为多条提交，并按 Conventional Commits 生成清晰的提交信息与提交计划；每次执行 git commit 前必须等待用户明确确认
---

# Git 提交助手（git-commit）

帮助用户把当前工作区变更整理成高质量提交：**先看清变更 → 必要时拆分 → 给出规范提交信息 → 每次 commit 前都要用户确认**。

## ✅ 核心原则

- **全面分析**：必须覆盖 staged / unstaged / untracked。
- **智能分组**：按“功能/模块/变更类型”分组，优先保证每条提交语义单一。
- **建议拆分**：当一条提交无法被一句话清晰描述时，默认建议拆分。
- **人工确认**：任何 `git commit` 前，必须等待用户明确确认（可 edit/skip/cancel）。
- **规范提交**：默认使用 **Conventional Commits**。

## 🔍 工作流程

### 1) 检查 Git 状态与差异

依次执行并收集输出：

```bash
git status
git status --short
git diff
git diff --cached
git log --oneline -10
```

输出给用户：
- 当前分支与是否干净
- staged/unstaged/untracked 文件清单
- 最近提交信息风格（用于对齐本仓库习惯）

### 2) 分析变更内容（逐文件）

对每个文件判定：
- **变更类型**：feat / fix / docs / refactor / test / chore / ci / build / style / perf
- **关联性**：是否属于同一功能或同一目的
- **风险点**：是否包含敏感信息（Token、cookie、`.env`、个人路径等）——发现则提醒并建议不要提交

输出给用户：
- 变更摘要（每个文件 1-2 行）
- 变更之间的关联性结论

### 3) 判断是否需要拆分 commit

优先使用这些判断：
- **应该拆分**：不同功能 / 不同模块 / 不同变更类型（例如 feat + docs）混在一起
- **可以合并**：同一功能跨多个文件的配套改动（例如 controller + view + routes）

给出拆分建议格式：

```text
建议拆分为 N 条 commit：

1) <type>(<scope>): <subject>
   - files: ...
   - why: ...

2) ...
```

### 4) 生成提交信息（Conventional Commits）

格式：

```text
<type>(<scope>): <subject>

<body 可选：说明为什么这么改/影响范围/迁移提示>
```

生成规则：
- **subject**：祈使句、尽量不超过 50 字符、结尾不加句号
- **scope**：能明确模块就写（如 `readme`、`skills`、`auth`），不确定可省略
- **body**：只写“为什么/影响/注意事项”，避免复述 diff

### 5) 等待用户确认并执行提交

对每条计划提交，必须先展示：
- 提交信息（完整）
- 将包含的文件列表
- 一句话变更说明

然后询问用户：`yes / no / edit / skip`

仅在用户回答 **yes** 后才执行：

```bash
git add <files...>
git commit -m "<message>"
```

提交后再展示：
- commit hash（短）
- 提交信息
- `git status` 结果

## 🧩 输出模板（推荐对话格式）

```text
准备提交以下变更：

提交信息：
<type>(<scope>): <subject>

变更文件：
- ...

变更说明：
- ...

是否确认提交？(yes/no/edit/skip)
```

## ⚠️ 需要特别警惕的内容（默认不提交）

- `.env`、密钥/Token 文件、cookie、凭证
- 用户目录路径、内网地址、客户数据
- 大量无关格式化（建议单独 style/refactor 提交）

