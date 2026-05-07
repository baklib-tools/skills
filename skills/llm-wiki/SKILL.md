---
name: llm-wiki
description: >-
  通过 LLM 构建持续进化的个人知识库（Karpathy 方法）：将 AI 从一次性检索器升级为知识编译器。
  当用户提到 LLM Wiki、Karpathy Wiki、个人知识库编译、RAG 替代方案、raw/wiki/schema 三层架构时使用。
---

# LLM Wiki（卡帕西方法）

通过 LLM 构建持续进化的个人知识库，将 AI 从一次性检索器升级为知识编译器。

## 核心思想

传统 RAG 的问题：每次提问 AI 都要重新读原始文档，知识无法积累。

Karpathy 的方法：让 AI 把原始资料编译成一个**持续进化的 Wiki**，AI 不再是每次查资料的秘书，而是知识库工程师。

## 三层架构

### 1. Raw Sources（原始素材层）
- 存放所有原始文档：文章、论文、笔记、PDF、金句、工具文档等
- 原则：AI 只读不改，这是你的信息源
- 典型结构：
  ```
  raw/
  ├── articles/     # 文章笔记
  ├── books/        # 书籍笔记
  ├── papers/       # 论文
  ├── courses/      # 课程笔记
  ├── resources/    # 资源链接
  ├── quotes/       # 金句
  ├── tools/        # 工具文档
  └── work/         # 工作文档
  ```

### 2. Wiki（知识库层）
- AI 生成的结构化 Markdown 文件集合，互相链接
- 包含：概念页、实体页、线索页、来源摘要
- 典型结构：
  ```
  wiki/
  ├── index.md      # 内容目录（内容导向）
  ├── log.md        # 操作日志（时间导向）
  ├── entities/     # 实体页（人名、公司、工具、模型）
  ├── concepts/     # 概念页（反复出现的概念）
  ├── threads/      # 线索页（跨领域大主题）
  ├── sources/      # 来源记录
  └── agents/       # AI 行为规则
  ```

### 3. Schema（规则文件）
- 告诉 AI 如何组织 Wiki 的配置文件
- 例如：`CLAUDE.md`、`AGENTS.md`、`agents/` 下的规则文件
- 你和 AI 共同维护，随使用不断优化

## 三种核心操作

### Ingest（摄入）
1. 把新素材放入 raw/
2. AI 读取素材，提取关键信息
3. 写入 Wiki 摘要页
4. 更新 index、相关实体页和概念页
5. 追加 log 记录

### Query（查询）
1. 向 AI 提问
2. AI 搜索 Wiki 中的相关页面（先读 index.md）
3. 综合已有知识生成回答
4. 好的答案可以回写到 Wiki

### Lint（检查）
定期让 AI 做健康检查：
- 页面之间的矛盾
- 过时声明
- 孤立页面（无入链）
- 缺失的交叉引用
- 数据缺口

## 目录结构关系

```
output/（你的产出）          ← 你主动创作
    ↑↓
wiki/（AI 编译的知识库）     ← AI 自动维护，你浏览和提问
    ↑↓
raw/（原始素材）             ← 你存放，AI 只读
```

## 使用流程

1. **初始化**：把 Karpathy Gist（https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f）发给 AI 工具
2. **准备 raw/**：把现有资料按类型放入 raw/ 对应子目录
3. **让 AI 生成 Wiki**：AI 读取 raw/ 所有内容，生成结构化的 wiki/
4. **用 Obsidian 浏览**：打开 raw/ 和 wiki/，查看知识图谱
5. **持续更新**：新素材放 raw/，AI 自动增量更新 Wiki

## Wiki 页面类型

### 概念页（concepts/）
- 你原创的、反复出现的、有完整论证的概念
- 每个概念一个 Markdown 文件，包含详细完整表述
- 例：AI OS、Code is Intent、万物皆文件

### 实体页（entities/）
- 人名、公司、工具、模型、产品等
- 你过去经常提到的对象
- 例：Karpathy、Claude、Obsidian、Logto

### 线索页（threads/）
- 可以归纳到一起的大主题
- 把分散的内容用逻辑串起来
- 例：AI 工程三部曲、AI 营销方法论

### 纲领性文件
- **index.md**：内容导向的目录，每个页面一行摘要 + 链接
- **log.md**：时间导向的操作记录，格式 `## [日期] 操作 | 标题`

## 实用技巧

- **Obsidian 是 IDE**：浏览 Wiki 的最佳工具，图谱视图看清知识关联
- **AI 是程序员**：Wiki 由 AI 生成和维护，你负责方向把控和提问
- **知识会累积**：每次添加新资料，Wiki 都会更新，不是每次重新检索
- **可以定制**：Karpathy 的文档是理念，具体结构你和 AI 一起定
- **git 版本控制**：Wiki 就是 Markdown 文件，天然支持 git

## 注意事项

- 初期 AI 消化所有素材可能耗时较长，耐心等待
- 知识库的架构方向必须由你把握，否则会变成"AI 的知识库"而非"你的知识库"
- 多 Agent 场景下注意规则文件同步（CLAUDE.md / AGENTS.md 保持一致）
- 定期做 lint 检查，保持 Wiki 健康
