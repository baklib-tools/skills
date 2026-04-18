---
name: requirements-to-published-content
description: 从干系人需求采集、分析整理、方案撰写到对外可发布内容的协作流水线；可组合配图、公众号 HTML、站点/MCP 发布等技能分阶段执行。在用户要落地「需求→定稿→多渠道发布」最佳实践、或扩展团队内容发布 playbook 时使用；不代替项目管理工具与平台合规责任。
---

# 需求到可发布内容（工作流技能）

本技能描述一条**可复用的协作链**：把零散需求变成**可对外传播**的文稿与页面。渠道可逐步扩展（例如首期微信公众号 + 企业站点；后续可增加知乎、小红书、站群等），**不因单一渠道命名或写死实现**。

## 适用场景

- 市场 / 产品 / 售前团队要把「客户/内部需求」变成**对外文案**与**可访问页面**。
- 希望代理按**阶段**选用不同技能（需求整理 → 方案 → 配图 → HTML → 站点发布），而非混在一个提示词里。

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

**执行顺序**：通常 **A→B→C→D**，再并行或串行 **E/F/G**；配图可在 D 之后或与 E 穿插。任何**写入线上系统**的操作须先征得用户确认（见 `baklib-mcp` 等技能约定）。

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
