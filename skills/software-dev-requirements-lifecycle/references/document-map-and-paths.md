# 文档地图、目录结构与命名

本文是 [../SKILL.md](../SKILL.md) 的配套参考：新项目可按需裁剪，但应在项目根 **`AGENTS.md`（或等价文件）** 中写死路径与真源优先级，避免混用多套叫法。

## 仓库根（常见）

| 文件 | 作用 |
|------|------|
| `AGENTS.md` | 文档真源优先级、更新节奏（面向人类与 AI 代理） |
| `CHANGELOG.md` | 对外发版变更（建议遵循 [Keep a Changelog](https://keepachangelog.com/)） |

## `docs/` 建议布局

```text
docs/
├── README.md                      # 文档导航：链接到各类「当前版」入口
├── product-requirements.md        # 当前有效 PRD（或 prd.md，二选一并在 AGENTS 声明）
├── product-design.md              # 可选；小团队可合并进 PRD，用二级标题分区
├── development-plan.md            # 开发计划：里程碑、阶段、勾选状态
├── glossary.md                    # 可选：术语表 / 领域对象（面向团队 + 可摘要给用户）
├── backlog/                       # 可选：用户故事独立维护时
│   ├── README.md                  # 故事索引（US-xxx 与状态）
│   └── US-042-short-slug.md      # 可选：按故事拆文件
├── changes/                       # 需求变更台账（追加式，少删改旧文）
│   └── 2026-04-19-CR-003-us-042.md
├── decisions/                     # ADR / 重大决策
│   └── 004-short-decision-title.md
├── help/                          # 用户帮助中心（终端用户）；站外托管则在 README 写 URL
│   └── ...                        # 详见 help-center-information-architecture.md
└── journal/                       # 可选：对内开发日志
    └── 2026-04.md
```

若帮助文档托管在 GitBook、Notion、产品内嵌帮助等，`docs/README.md` 中给出**显式 URL**，并在 `AGENTS.md` 标明「用户文档真源」。

## 命名规则摘要

| 类型 | 建议 | 示例 |
|------|------|------|
| 普通 Markdown | kebab-case，语义清晰 | `product-requirements.md` |
| ADR | 三位序号 + kebab 短标题 | `docs/decisions/004-webhook-idempotency.md` |
| 变更单 | 日期 + 可选编号/故事引用 | `docs/changes/2026-04-19-CR-003.md` |
| 用户故事文件（若拆文件） | `US-编号-short-slug` | `US-042-export-orders.md` |
| 对内月记 | `YYYY-MM` | `docs/journal/2026-04.md` |

正文与变更单中统一使用 **`US-042`** 这类故事 ID，与 `backlog/` 文件名或 PRD 内表格对应。

## 真源优先级（示例，项目需自洽）

若未另立 ADR，可在 `AGENTS.md` 中采用类似顺序（按需改写）：

1. 已采纳的 ADR / 决策记录  
2. 当前 PRD（产品范围与验收）  
3. 技术规格（实现细节；与产品冲突时以产品 + ADR 为准）  
4. 开发计划勾选（是否交付以计划 + 测试为准）  

## 与 CHANGELOG 的分工

| 文档 | 读者 | 内容侧重 |
|------|------|----------|
| CHANGELOG / 发布说明 | 对接人、关注版本的人 | 版本号、新增/修复/破坏性变更 |
| 用户帮助 | 终端业务用户 | 如何完成任务、截图、FAQ；见 `help-center-information-architecture.md` |
