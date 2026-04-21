# Fizzy 功能域地图

以下路径均相对于 Fizzy 仓库根目录（如 `app/models/...`）。**标签**：`通用` = 多数 Rails 产品可对照；`专有` = Fizzy 业务或强绑定；`借鉴` = 专有域里仍可学的实现技巧。

---

## 多租户与请求上下文

- **用户可见能力**：按账户隔离数据；URL 带账户作用域；后台任务恢复账户上下文。
- **关键路径**：`app/models/current.rb`、`app/models/account/multi_tenantable.rb`、`config/initializers/tenanting/account_slug.rb`（`AccountSlug::Extractor` 中间件）。
- **代码重心**：`Current` 上 session → identity → user 的派生关系；`with_account` / `without_account`；模型 `default: -> { ... Current.account }` 模式。
- **标签**：专有为主；**借鉴**「CurrentAttributes + Job 里恢复租户」的套路。

---

## 身份、会话与注册

- **用户可见能力**：Magic link 登录、Passkey、会话菜单、跨账户 session transfer、注册 / signup completion、邮箱验证与多邮箱。
- **关键路径**：`app/controllers/sessions/*`、`app/controllers/signups/*`、`app/models/identity.rb`、`app/models/magic_link*.rb`、`app/controllers/concerns/authentication*.rb`。
- **代码重心**：`Authentication` concern 如何与 `Current` 结合；`Sessions::MagicLinksController` 与 `Identity` 的交互。
- **标签**：**通用** 参考价值高（无密码 / WebAuthn 组合）。

---

## Kanban 核心（Board / Column / Card）

- **用户可见能力**：看板、列、卡片 CRUD；卡片在列间移动（drop 子资源：`closure`、`not_now`、`stream`、`column`）；金标、置顶、草稿、关闭、分配、步骤、标签、图片。
- **关键路径**：`app/models/board.rb`、`column.rb`、`card.rb` 及 `app/models/card/*`、`app/controllers/boards/*`、`cards/*`、`columns/cards/drops/*`。
- **代码重心**：把动词拆成 **独立 singular resource**（`resource :closure`、`resource :goldness`）对应 [`config/routes.rb`](https://github.com/basecamp/fizzy/blob/main/config/routes.rb)；concern 拆分（`closeable`、`postponable`、`assignable` 等）。
- **标签**：业务 **专有**；**借鉴** REST 子资源划分与 concern 边界。

---

## 评论、反应、@提及

- **用户可见能力**：卡片评论、emoji 反应、正文提及用户。
- **关键路径**：`app/models/comment.rb`、`concerns/mentions.rb`、`app/models/mention.rb`、`cards/comments_controller.rb`。
- **代码重心**：`after_save_commit` 触发异步 `Mention::CreateJob`；搜索与富文本结合处。
- **标签**：**通用**（提及、反应模式）。

---

## 活动流与时间线（Event）

- **用户可见能力**：全局/看板活动列表；按日聚合；Day timeline 列视图。
- **关键路径**：`app/models/event.rb`、`event/particulars.rb`、`event/description.rb`、`events_controller.rb`、`events/days_controller.rb`、`events/day_timeline/*`。
- **代码重心**：多态 `eventable`；`particulars` JSON；创建后 `dispatch_webhooks`；`Event::Description` 面向用户的文案组装。
- **标签**：**借鉴**「活动实体 + particulars + 多态」比照搬 Kanban 更通用。

---

## 通知（站内 / 批量 / Web Push）

- **用户可见能力**：通知列表、已读、托盘、退订、批量已读；可选 Push。
- **关键路径**：`app/models/notification.rb`、`notification/bundle.rb`、`notification/pushable.rb`、`app/jobs/notification/*`。
- **代码重心**：`Notification::Bundle` 聚合投递；`deliver_later` / `DeliverJob`；`push_later` 与 `Notification::PushJob`。
- **标签**：**通用**（批量通知、异步投递）；Push 渠道实现可 **借鉴**。

---

## 搜索

- **用户可见能力**：全文搜索、搜索历史 query、高亮。
- **关键路径**：`app/models/search.rb`、`search/query.rb`、`search/record*.rb`、`concerns/searchable.rb`（Card、Comment 等）。
- **代码重心**：MySQL / SQLite 不同适配；账户维度分片（若使用 MySQL）；索引与 `Search::ReindexJob`。
- **标签**：**专有**（分片与 FTS 细节）；**借鉴**「可搜索内容与 Search 表去范式 + 异步重建」。

---

## Webhook

- **用户可见能力**：看板配置出站 webhook、激活、投递记录、失败追踪。
- **关键路径**：`app/models/webhook.rb`、`webhook/delivery.rb`、`webhook/triggerable.rb`、`app/jobs/webhook/delivery_job.rb`、`app/models/ssrf_protection.rb`。
- **代码重心**：`Webhook::Delivery` 状态机与超时；`Event` 后异步 `WebhookDispatchJob`；SSRF 校验与响应大小限制。
- **标签**：**通用**（出站 webhook 管线 + 安全边界）。

---

## 导入 / 导出与超大 ZIP

- **用户可见能力**：账户级导出/导入；用户级 data export；大 ZIP 支持本地或远程存储。
- **关键路径**：`app/models/account/data_transfer/*`、`account/import.rb`、`account/export.rb`、`app/models/zip_file*.rb`、`account/data_import_job` 等 jobs。
- **代码重心**：`ZipFile::Reader` / `Writer`、`RemoteIo` 流式；manifest 与 record set 分批迁移。
- **标签**：**借鉴**（大文件流式、分批迁移模式）；产品格式 **专有**。

---

## 存储计量（Storage ledger）

- **用户可见能力**：账户/看板存储用量展示。
- **关键路径**：`app/models/concerns/storage/totaled.rb`、`storage/entry.rb`、`storage/total.rb`、`app/jobs/storage/materialize_job.rb`、`storage/reconcile_job.rb`。
- **代码重心**：`materialize_storage_later` → 薄 Job → `materialize_storage`；reconcile 双游标防并发写。
- **标签**：**借鉴**（台账 + 异步快照 + 对账）。

---

## Entropy（自动推迟）

- **用户可见能力**：闲置卡片自动进入「not now」；账户/看板级周期配置。
- **关键路径**：`app/models/entropy.rb`、`board/entropic.rb`、`card/postponable.rb`、`account/entropies_controller.rb`、`config/recurring.yml`（若有定时任务）。
- **代码重心**：周期任务与模型上的 `auto_postpone` 类逻辑。
- **标签**：业务 **专有**；**借鉴**「定时 + 领域规则」组织方式。

---

## 公开看板与只读访问

- **用户可见能力**：通过 publication key 公开看板/列/卡片只读视图。
- **关键路径**：`app/controllers/public/*`、`board/publishable.rb`、`board/publication.rb`、`public/base_controller.rb`。
- **代码重心**：独立 `Public::` 命名空间与路由；与主站 `Authorization` 分离。
- **标签**：**借鉴**（公开链接与主会话隔离）。

---

## 筛选器与 Saved views

- **用户可见能力**：保存的过滤器、刷新设置。
- **关键路径**：`app/models/filter.rb`、`filter/*`、`filters_controller.rb`。
- **代码重心**：`Filter::Params` / `Fields` 与查询组合。
- **标签**：**借鉴**（查询对象与持久化筛选）。

---

## 移动端 / PWA / 客户端配置

- **用户可见能力**：PWA manifest、service worker、iOS/Android 客户端拉配置。
- **关键路径**：`pwa_controller.rb`、`client_configurations_controller.rb`、`routes` 中 `manifest`、`service-worker`。
- **代码重心**：与 Hotwire Native / 客户端版本协商。
- **标签**：**通用**（薄配置端点）。

---

## 账户生命周期与 SaaS 周边

- **用户可见能力**：加入码、取消账户、账户设置、entropy 账户默认。
- **关键路径**：`account/*_controller.rb`、`account/cancellation.rb`、`account/join_code.rb`。
- **代码重心**：与 `saas` gem 边界（若开源目录含 stub）；`incinerate` 相关 job。
- **标签**：多为 **专有**；取消/清理流程可 **借鉴** 思路。

---

## AI / Prompts（若启用）

- **用户可见能力**：`prompts` 命名空间下列出 cards/users/boards 供提示或集成场景。
- **关键路径**：`app/controllers/prompts/*`、`event/promptable.rb`、`card/promptable.rb`。
- **代码重心**：与 `Event` / Card 的 promptable 挂钩点。
- **标签**：**专有**（产品方向）；**借鉴**「独立 prompts 路由命名空间」隔离实验性功能。

---

## 杂项与横切

- **QR 码**：`qr_codes_controller.rb`、`qr_code_link.rb` — **专有** 小功能。
- **Tags**：全局 tag 索引 — 与 Card `taggable` 配合。
- **Activities**：`activities#index` — 与 Event 列表可能分工，读控制器确认。
- **Admin**：`MissionControl::Jobs` 挂载 — **通用** Solid Queue 运维面。
- **Board 协作**：`Access`、`Assignment`、`Watch` — 模型 `access.rb`、`watch.rb`、`boards/accesses_controller.rb`。
- **横切 concerns**：`app/controllers/concerns/turbo_flash.rb`、`view_transitions.rb`、`board_scoped.rb`、`card_scoped.rb` — **借鉴** Turbo 与作用域 concern 组合。

---

## 阅读顺序建议（agent）

1. `config/routes.rb` → 定域。  
2. 该域 `app/controllers/**` → HTTP 与授权边界。  
3. `app/models/**` 对应模型与 concern → 业务规则。  
4. `app/jobs/**` → 异步与重试。  
5. `test/models/**` 或 `test/controllers/**` → 行为契约。
