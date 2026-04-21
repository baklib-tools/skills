# Fizzy：通用模式、专有实现与可借鉴点

本文档与 [feature-map.md](feature-map.md) 配合使用：先按域定位文件，再用下表判断**哪些能搬到别的项目**、**哪些只能学思路**。

---

## 1. 横切架构模式（多为「通用 / 借鉴」）

| 模式 | Fizzy 中的体现 | 可迁移性 | 不要照搬 |
|------|----------------|----------|----------|
| Vanilla Rails，薄控制器 | 控制器调 ` @card.gild`、`@comment = @card.comments.create!` | **高**：富模型 API + REST 子资源 | 具体路由命名 |
| 浅 Active Job | `perform` 一行调模型，如 `delivery.deliver` | **高** | 队列名、`discard_on` 策略 |
| `_later` 入队方法 | `deliver_later`、`materialize_storage_later` | **高** | 与同步方法命名是否叫 `_now` 可随项目 |
| CurrentAttributes | `app/models/current.rb` 管 session / identity / user / account | **高** | 租户维度（Fizzy 是 account 路径前缀） |
| Turbo / Flash / View transitions | `TurboFlash`、`ViewTransitions` concern | **中**：依赖 Hotwire 栈 | UI 细节 |
| 组合式 ApplicationController | 多个小 concern 而非上帝类 | **高** | 具体 include 列表 |
| 多态活动 + JSON particulars | `Event` + `event/particulars` | **中–高** | particulars 字段形状 |
| 出站 Webhook 管线 | `Event` → Job → `Webhook::Delivery` | **高** | 投递重试与 product 字段 |
| 搜索去范式 | `Search::Record` + model `searchable` | **中**：思路通用 | MySQL 分片与 FTS 细节 |
| 存储台账 | `Storage::Entry` + `Total` + materialize job | **中–高** | 是否按 account/board 分 owner |
| 大 ZIP 流式 | `ZipFile::Reader`、`RemoteIo` | **高**（思路） | 与 S3/本地配置耦合部分 |

---

## 2. 强产品绑定（「专有」为主）

| 领域 | 说明 | 仍能借鉴什么 |
|------|------|----------------|
| 路径多租户 | URL 中 account 段、`SCRIPT_NAME` 技巧 | 测试里如何隔离 `Current.account` |
| Kanban 名词 | Column / Card / triage / not_now / closure | **动词拆资源** 的 REST 设计 |
| Entropy 自动推迟 | 业务规则 + 周期任务 | 定时任务与领域对象协作方式 |
| UUID 主键 + fixture 顺序 | 测试稳定性 | 若你也用 UUID，可参考 fixture 策略 |
| 16 分片 MySQL 全文检索 | 性能方案 | 多数项目用 pg + tsvector 或 Elasticsearch 替代 |
| fizzy-saas / 计费 | 私有 gem（README 说明） | 忽略或仅看接口边界 |
| Prompts 命名空间 | 实验或 AI 相关入口 | **独立路由命名空间** 隔离新能力 |

---

## 3. 安全与合规（优先「借鉴」）

| 主题 | 代码线索 | 要点 |
|------|----------|------|
| SSRF | `app/models/ssrf_protection.rb`、webhook 请求前校验 | 出站 HTTP 白名单/限制 |
| Webhook 响应大小 | `Webhook::Delivery::MAX_RESPONSE_SIZE` 等 | 防内存与日志爆炸 |
| 会话与 Passkey | `sessions/passkeys`、`my/passkeys` | WebAuthn 与 magic link 并存时的边界 |

---

## 4. 与其他 Rails 项目对话时的用法

- **「像 Fizzy 那样做通知」**：指向 `Notification::Bundle` + `DeliverJob` + `push_later` 链，说明是**批量+异步**，而非具体文案。
- **「像 Fizzy 那样拆 Card 操作」**：指向 `routes` 里 `resource :closure` 等，强调 **新资源代替 member action**。
- **「像 Fizzy 那样做活动流」**：指向 `Event` 多态 + `particulars`，强调 **扩展字段** 而不是几十张 event 子表。

---

## 5. STYLE.md 的定位

Fizzy 仓库的 `STYLE.md` 是贡献指南性质的 Ruby/Rails 习惯说明，**不是**架构文档。实现级问题以 **本技能 feature-map + Fizzy 源码** 为准；风格问题可打开 Fizzy 仓库内 `STYLE.md` 原文扫一眼即可。
