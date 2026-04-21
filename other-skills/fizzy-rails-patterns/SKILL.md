---
name: fizzy-rails-patterns
description: Maps 37signals open-source Fizzy app by feature domain (multi-tenancy, Kanban, events, notifications, webhooks, search, import/export, storage ledger, entropy, public boards) with code focal points in app/models and app/controllers. Classifies patterns as portable vs product-specific vs borrowable implementation ideas. Use when exploring Fizzy source, comparing architecture to another Rails app, asking what to read first, implementation focus, or migrating ideas without copying Kanban semantics. Triggers: Fizzy, feature map, domain, AGENTS, thin jobs, Current.account, webhook pipeline, search shards, large ZIP.
---

# Fizzy 源码技能（架构与功能参考）

本技能以 **Fizzy 仓库内的路由、模型与任务** 为主线索，回答：有哪些功能域、**读代码时盯哪些文件**、**哪些模式可搬到其他项目**、哪些是产品专有但仍可学实现技巧。  
**不**把 `STYLE.md` 当作架构权威；贡献风格请直接打开 Fizzy 仓库里的 `STYLE.md` 原文（见文末）。

## 使用方式（agent）

1. 在本地克隆 [Fizzy](https://github.com/basecamp/fizzy)（或用户提供的同一路径工作副本）。
2. 用户问题若涉及具体能力，先在 [`config/routes.rb`](https://github.com/basecamp/fizzy/blob/main/config/routes.rb) 定命名空间，再下钻控制器 → 模型 concern → Job。
3. 判断可迁移性时，先查 [patterns.md](patterns.md)，再对照 [feature-map.md](feature-map.md) 里该域的「代码重心」。

## 核心文档（渐进式披露）

| 文件 | 内容 |
|------|------|
| [feature-map.md](feature-map.md) | 按功能域列出能力、关键路径、2–5 个代码重心、通用/专有/借鉴标签 |
| [patterns.md](patterns.md) | 横切模式对照表；专有域仍可借鉴的点；安全类线索；与其他项目对话时的「指代用语」 |

## 仓库内补充阅读

- **`AGENTS.md`**：开发命令、多租户梗概、Solid Queue、搜索与导入导出等高层说明（与 feature-map 互补）。
- **`STYLE.md`**：Ruby/Rails 书写习惯（条件、方法顺序、REST、薄 Job 等），**仅作风格附录**，不替代领域设计。

## STYLE.md（附录级）

若需对齐 Fizzy 贡献风格：在 Fizzy 根目录阅读 `STYLE.md`（README 的 Contributing 节亦有链接）。实现与架构问题以 `feature-map.md` / 源码为准。
