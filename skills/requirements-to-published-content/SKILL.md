---
name: requirements-to-published-content
description: 从干系人需求采集、分析整理、方案撰写到对外可发布内容的协作流水线；收到需求后须先汇报拟执行步骤并征得用户对可选产出（软文/公众号/配图/MCP 等）的确认，未确认前不调用计费出图或写入线上。可组合 wechat-mp-html、配图类技能与 baklib-mcp 分阶段执行；不代替项目管理与平台合规责任。
---

# 需求到可发布内容（工作流技能）

本技能描述一条**可复用的协作链**：把零散需求变成**可对外传播**的文稿与页面。渠道可逐步扩展（例如首期微信公众号 + 企业站点；后续可增加知乎、小红书、站群等），**不因单一渠道命名或写死实现**。

## 适用场景

- 市场 / 产品 / 售前团队要把「客户/内部需求」变成**对外文案**与**可访问页面**。
- 希望代理按**阶段**选用不同技能（需求整理 → 方案 → 配图 → HTML → 站点发布），而非混在一个提示词里。

## 用户怎么使用（与仓库示例的关系）

1. **安装**：在使用者**自己的项目**里通过 `npx skills add … --skill requirements-to-published-content` 安装本技能（并视需要安装 `wechat-mp-html`、配图子技能、`baklib-mcp` 等），使 Agent 能加载本 `SKILL.md`。  
2. **挂载产品知识**：在 Cursor（或其它宿主）中把团队本地的 **Baklib 产品知识库根目录**（可命名为 `baklib-workspace` 等）**加入工作区**，便于模型检索能力与写方案。  
3. **发起任务**：用户在新对话中说明「按 requirements-to-published-content 处理」，并**粘贴或 @ 引用**客户需求正文（可来自邮件、CRM、Markdown 文件）。  
4. **产出位置**：代理在**当前工作区**中生成或更新文件；**具体路径与文件名由用户指定或协商**，不必与公开仓库里 [examples/requirements-to-published-content-health-cms](https://github.com/baklib-tools/skills/blob/main/examples/requirements-to-published-content-health-cms/README.md) 的目录结构一致——该目录仅为**演示范本**（含模拟对话与示例 artifacts）。  
5. **配图与费用**：**默认不得**在用户未明确同意的情况下调用计费图像 API、或批量生成 PNG；即使用户已安装 `image-generation-ucloud` 等技能，也须在**执行前确认**（见下节）。

## 执行前确认（强制）

收到用户需求后，代理**必须先**完成下列交互，**再**执行对应步骤（分析与基础方案可视为默认进行，但若用户只想「只要分析」也须尊重）：

1. **汇报计划**：用简短编号列出**本轮拟执行的步骤**（例如：① 需求分析 ② 正式方案 ③ 对外软文 ④ 公众号 Markdown ⑤ 公众号 HTML ⑥ 配图推导 ⑦ 调用出图 API ⑧ MCP 写入等——按实际勾选）。  
2. **逐项确认**（应用自然语言一次性提问亦可），至少覆盖：  
   - 是否需要**推广/案例向软文**（阶段 D 的一种）？  
   - 是否需要**公众号**相关产出（Markdown 定稿 / **wechat-mp-html** 排版 HTML）？  
   - 是否需要**生成配图**（仅文字推导提示词，还是**调用 API 出图**——二者不同；后者涉及密钥与费用，**必须单独确认**）？  
   - 是否需要 **Baklib MCP 写入**（须遵守 [baklib-mcp](https://github.com/baklib-tools/skills/blob/main/skills/baklib-mcp/SKILL.md) 的写入前确认）？  
3. **等待用户明确答复**后再执行；若用户选择「只做 ①②」，则**不得**擅自撰写软文、生成配图或写入 MCP。  
4. 用户可在执行过程中**追加或收紧**范围（例如「方案可以，不要公众号」），代理应**立即调整**后续步骤。

## 推荐阶段（可按组织裁剪）

| 阶段 | 目标 | 常见产出 | 可组合技能（示例） |
|------|------|----------|-------------------|
| A. 采集与澄清 | 统一术语、边界、干系人 | 需求摘要、问题清单、验收口径 | 团队自有模板或通用对话整理 |
| B. 分析与结构化 | 优先级、风险、依赖 | 结构化需求说明、用户故事 | 同上 |
| C. 方案与设计 | 可对外讲述的叙事 | 方案大纲、对比表、架构说明 | 同上 |
| D. 对外文稿 | 脱敏、可读、可传播 | 长文 Markdown/Doc、FAQ | 依团队风格 |
| E. 渠道排版 | 符合各平台版式 | 公众号 HTML、其它渠道稿 | [wechat-mp-html](https://github.com/baklib-tools/skills/blob/main/skills/wechat-mp-html/SKILL.md) |
| F. 配图（可选） | 统一视觉语言 | 提示词、成图文件 | [image-generation](https://github.com/baklib-tools/skills/blob/main/skills/image-generation/SKILL.md) 及子技能、[nano-banana-pro-prompting](https://github.com/baklib-tools/skills/blob/main/skills/nano-banana-pro-prompting/SKILL.md) 等 |
| G. 站点 / 知识库发布（可选） | 可分享链接、可复制 HTML | BKE 正文、站点页 | [baklib-mcp](https://github.com/baklib-tools/skills/blob/main/skills/baklib-mcp/SKILL.md)、[baklib-bke-markdown](https://github.com/baklib-tools/skills/blob/main/skills/baklib-bke-markdown/SKILL.md) |

**执行顺序**：在用户对**执行前确认**作答后，通常 **A→B→C→D**，再并行或串行 **E/F/G**；配图可在 D 之后或与 E 穿插。任何**写入线上系统**的操作须先征得用户确认（见 `baklib-mcp` 等技能约定）。**F（出图 API）与 E（公众号 HTML）均属于「可选」，以用户确认项为准，不得默认全开。**

## 渠道扩展位（占位）

以下可在本技能后续版本中补充独立小节或链接到专用技能，**名称保持与本技能一致**：

- **知乎 / 小红书 / 站群**：各自标题长度、卡片、外链与图片规则不同；建议为每渠道单独维护「排版技能」或在 `references/` 中增加 `channels/*.md`（若你在 fork 中扩展）。

首期若只做 **微信公众号**：在阶段 E 加载 **wechat-mp-html**，按该技能生成 `#js_content` 与复制按钮；阶段 G 若需 Baklib 站点一键复制 HTML，按 **baklib-mcp** 与 BKE 正文规范操作。

## 能力边界（不做什么）

- 不代替需求管理工具（Jira、飞书项目等）中的正式签收与变更流程。
- 不保证任一渠道的推荐算法或审核结果。
- 不将内部机密写入公开技能正文；脱敏责任在使用者与团队流程。

## 安装相关技能

```bash
npx skills add baklib-tools/skills --list
npx skills add baklib-tools/skills --skill requirements-to-published-content --skill wechat-mp-html
# 若使用 Baklib 发布：
npx skills add baklib-tools/skills --skill baklib-mcp --skill baklib-bke-markdown
```

具体参数以 `npx skills --help` 为准。

## 示例（仓库内）

端到端演示见 **[examples/requirements-to-published-content-health-cms/README.md](https://github.com/baklib-tools/skills/blob/main/examples/requirements-to-published-content-health-cms/README.md)**：在 Cursor 中挂载本地 **Baklib 产品知识库**（目录名示例 **`baklib-workspace`**，绝对路径由使用者本机自定）、结合脱敏客户需求，产出分析、正式方案、推广叙事、对外长文、公众号稿与配图推导说明；**模拟对话**见 [walkthrough/simulated-dialogue.md](https://github.com/baklib-tools/skills/blob/main/examples/requirements-to-published-content-health-cms/walkthrough/simulated-dialogue.md)。
