# 速查与模板索引（`reference.md`）

本文件为 **software-dev-requirements-lifecycle** 技能的单文件入口：与 **[`references/`](references/)** 分册配合使用——**长模板、帮助 IA、仓库目录**见分册；此处提供 **PRD 目录建议**、**术语表示例**，并索引其余文件。

| 分册 | 内容 |
|------|------|
| [`mineru-office-to-markdown`](https://github.com/baklib-tools/skills/blob/main/skills/mineru-office-to-markdown/SKILL.md) | 同仓库技能：PDF / Office → 本地 Markdown；需求材料为附件时与本技能衔接 |
| [references/document-map-and-paths.md](references/document-map-and-paths.md) | `docs/` 布局、文件命名、真源优先级示例 |
| [references/templates.md](references/templates.md) | 用户故事、GWT、变更单、Definition of Done |
| [references/help-center-information-architecture.md](references/help-center-information-architecture.md) | 帮助中心分层、首页导航、单篇 how-to 结构（对应计划 §D） |
| [references/agents-document-map-template.md](references/agents-document-map-template.md) | 新项目可粘贴的 `AGENTS.md` 最小文档地图片段 |

---

## PRD 建议目录（当前有效基线）

可按项目改名为 `product-requirements.md` 等；小团队可删节合并章节。

```markdown
# <产品名> 产品需求（PRD）

## 1. 背景与目标
- 业务背景、要解决什么问题
- 成功指标（可量化或可对账）

## 2. 用户与场景
- 角色列表、典型场景（谁、何时、为何）

## 3. 范围
- **In scope**（本期必做）
- **Out of scope**（明确不做，避免蔓延）

## 4. 用户故事与验收
- 按史诗/模块列出故事（建议 ID：`US-001` …）
- 每条附验收标准（Given/When/Then 或检查清单）

## 5. 优先级与依赖
- P0/P1… 或 MoSCoW
- 跨团队/第三方依赖与假设

## 6. 风险与开放问题
- 未决事项、需客户确认的点

## 7. 修订记录（可选；或单独走 changes/ 台账）
- 版本、日期、摘要
```

---

## 术语表示例（团队与用户对齐）

| 术语 | 定义 | 备注 |
|------|------|------|
| 订单 | 用户一次下单产生的业务单据，含行项目与金额 | 与「支付单」区分 |
| 核销 | 订单达到业务认定「完成」条件的状态迁移 | 以客户确认的口径为准 |
| 连接器 | 与外部销售系统同步数据/事件的适配层 | 非泛指任意 API |

新成员入职或对外沟通前，补充本表可减少「同名不同义」返工；可单独建 `docs/glossary.md`。

---

## 帮助中心 how-to 骨架（摘要）

完整结构见 [references/help-center-information-architecture.md](references/help-center-information-architecture.md)。

**单篇顺序**：一句话目的 → 前置条件 → 编号步骤 → 预期结果 → 常见问题 → 相关链接（2～3 个）。

**首页**：`help/README.md` 用分组（按角色或按任务），避免平铺几十篇文件。

---

## 变更请求 / 用户故事 / GWT 全文模板

见 [references/templates.md](references/templates.md)。
