---
name: karpathy-wiki
description: >-
  通过 LLM 构建持续进化的个人知识库（卡帕西知识库）：将 AI 从一次性检索器升级为知识编译器。
  当用户提到 karpathy-wiki、Karpathy Wiki、LLM Wiki、个人知识库编译、RAG 替代方案、raw/wiki/schema 三层架构时使用。
---

# Karpathy Wiki（卡帕西知识库）

通过 LLM 构建持续进化的个人知识库，将 AI 从一次性检索器升级为知识编译器。

## 核心思想

传统 RAG 每次提问都要重新读原始文档，知识无法积累。Karpathy 的方法：让 AI 把原始资料编译成一个**持续进化的 Wiki**，AI 不再是检索秘书，而是知识库工程师。

## 三层架构

```
raw/（原始素材层）  ← 你存放，AI 只读
    ↑↓
wiki/（知识库层）   ← AI 生成的结构化 Markdown，互相链接
    ↑↓
AGENTS.md（Schema） ← 定义 AI 如何组织 Wiki
```

## 目录结构

```
.
├── raw/
│   ├── articles/  books/  papers/  courses/
│   ├── resources/  quotes/  tools/  work/
├── wiki/
│   ├── index.md  log.md
│   ├── entities/  concepts/  threads/  sources/  agents/
├── output/
└── AGENTS.md
```

## 页面类型

### 实体页 `wiki/entities/`

- 命名：小写 kebab-case，如 `andrej-karpathy.md`
- Frontmatter：`type: entity` + `tags: [...]`

### 概念页 `wiki/concepts/`

- 命名：小写 kebab-case，如 `rag.md`

### 线索页 `wiki/threads/`

- 命名：小写 kebab-case，如 `ai-engineering-trilogy.md`

### 来源摘要页 `wiki/sources/`

- 命名：与 raw 文件名呼应
- Frontmatter：`type: source` + `date: YYYY-MM-DD` + `raw: raw/.../xxx.md`

## 链接规范

- 使用 Obsidian Wikilink：`[[page-name]]`
- 链接目标文件名不带 `.md` 后缀
- 页面标题使用一级标题 `# Title`

## 三种核心操作

### Ingest（摄入）

1. 读取素材
2. 创建/更新来源摘要页
3. 提取实体（无则新建，有则追加）
4. 提取概念（无则新建，有则整合）
5. 更新线索页
6. 更新 `wiki/index.md`
7. 追加 `wiki/log.md`

### Query（查询）

1. 先读 `wiki/index.md`
2. 定位相关页
3. 读取并综合
4. 引用来源
5. 回写好答案：若用户认可，提议保存为 wiki 新页面

### Lint（检查）

1. 扫描矛盾
2. 发现孤立页
3. 检查缺失页
4. 评估数据缺口
5. 输出 Markdown 报告

## 特殊文件规范

### `wiki/index.md`

内容导向的目录，每页一行摘要 + 链接。按分类组织。每次 Ingest 后更新。

### `wiki/log.md`

时间导向的追加日志。条目格式：`## [YYYY-MM-DD] 操作类型 | 标题/简述`
操作类型：`ingest`、`query`、`lint`、`update`、`create`
保持 append-only。