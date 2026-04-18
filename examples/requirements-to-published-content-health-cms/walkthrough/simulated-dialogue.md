# 模拟对话：从需求到公众号稿（阶段 A–G）

> 以下为**摘要式**演示，非真实会话全文。用户指令可原样复制改编；**AI 应答**只列要点，便于对照技能阶段。

**环境假设**：Cursor 已添加本机 **`baklib-workspace`** 产品知识库根目录（路径自定，参见 [上级 README](../README.md)）与本 `skills` 仓库；已安装 `requirements-to-published-content`、`wechat-mp-html`（及按需的配图类技能）。

---

## 第 1 轮 — 加载上下文（阶段 A）

**用户**：

> 请遵循技能 `requirements-to-published-content`。先阅读我工作区里的 **`baklib-workspace`**，重点检索 **`baklib-mirror/知识库/`** 里与 Baklib **知识库、资源库、站点、API、审核与权限**相关的说明，建立对我们产品能力的印象。  
> 然后阅读本示例中的客户需求：[../fixtures/requirement-input-desensitized.md](../fixtures/requirement-input-desensitized.md)（若多根工作区，请用资源管理器定位到 `skills` 仓库下的该路径）。  
> **不要**编造未在文档中出现的功能名。

**AI 应答要点**：

- 确认已用只读方式浏览 `baklib-workspace` 中若干与产品能力相关的 Markdown（具体文件随镜像而异）。  
- 概括：Baklib 侧可交付的能力边界（知识内容、DAM、站点发布、API、审计等）与需谨慎表述的「工作流 / 全渠道矩阵」等。  
- 说明下一步将输出结构化需求分析，并引用客户 fixtures 中的条款编号。

**本步产出**：对话内摘要；正式落盘见 [artifacts/01-requirement-analysis.md](../artifacts/01-requirement-analysis.md)。

---

## 第 2 轮 — 需求分析（阶段 B）

**用户**：

> 基于 fixtures 与你的产品理解，写一份《需求分析》：优先级、约束、风险。保存为仓库内 `artifacts/01-requirement-analysis.md`（若本会话不能写文件，则把全文输出在对话里）。

**AI 应答要点**：

- 输出结构化分析：P0/P1、干系人、分期与风险（与 01 文件结构一致）。  

**本步产出**：[artifacts/01-requirement-analysis.md](../artifacts/01-requirement-analysis.md)。

---

## 第 3 轮 — 正式方案书（阶段 C）

**用户**：

> 写《正式方案书》：哪些需求可响应、哪些部分响应或暂不响应，并给分期路线。语气可给客户内部汇报。对应 `artifacts/02-formal-proposal-baklib.md`。

**AI 应答要点**：

- 用表格或章节区分 **可 / 部分 / 需集成或分期 / 不纳入本期**。  
- 明确「医学部单节点审核」「直播不在本期」等与 fixtures 答疑一致。  
- 免责声明：以官方版本与签约为准。

**本步产出**：[artifacts/02-formal-proposal-baklib.md](../artifacts/02-formal-proposal-baklib.md)。

---

## 第 4 轮 — 推广案例叙事（阶段 D）

**用户**：

> 虚构一家「康维医疗科技」，写一篇推广向案例故事，不出现真实客户名，对应 `artifacts/03-promotional-case-study.md`。

**AI 应答要点**：

- 叙事弧线：分散 → 选型 Baklib → 分期落地 → 业务结果（虚构但合理）。  

**本步产出**：[artifacts/03-promotional-case-study.md](../artifacts/03-promotional-case-study.md)。

---

## 第 5 轮 — 对外长文（阶段 D）

**用户**：

> 把案例压缩改写成可对外发布的科普/观点稿，不要太「销售腔」，对应 `artifacts/04-public-article.md`。

**本步产出**：[artifacts/04-public-article.md](../artifacts/04-public-article.md)。

---

## 第 6 轮 — 公众号 Markdown 定稿（阶段 D → E）

**用户**：

> 改成公众号适合的篇幅与标题，保留「三要点」结构；在文内用注释说明配图意向，但不要代替我指定每张图的提示词。输出 `artifacts/05-wechat-article.md`。

**AI 应答要点**：

- 标题、导语、分节、CTA；配图仅写**位置与意图**，不越俎代庖生成最终绘图指令（留给下一轮）。

**本步产出**：[artifacts/05-wechat-article.md](../artifacts/05-wechat-article.md)。

---

## 第 7 轮 — 配图推导（阶段 F）

**用户**：

> 加载 `nano-banana-pro-prompting`（若已安装）。根据 05 的正文，**你自己推导**三镜头配图主题与提示词约束，写入 `artifacts/image-plan-from-content.md`。不要假设我会上传参考图。

**AI 应答要点**：

- 从段落抽取情绪与隐喻 → 映射 Shot1/2/3。  
- 写明与 nano-banana 分步模板、单次请求自包含等约束一致。

**本步产出**：[artifacts/image-plan-from-content.md](../artifacts/image-plan-from-content.md)。

---

## 第 8 轮 — 公众号 HTML（阶段 E）

**用户**：

> 按技能 `wechat-mp-html`，把 05 的正文排成可粘贴公众号的 HTML，使用 `#js_content` 与标准复制按钮；图片先用占位 URL。写入 `artifacts/06-wechat-article.html`。

**AI 应答要点**：

- 正文块级以 `section` + inline style；复制脚本使用 `ClipboardItem`。  

**本步产出**：[artifacts/06-wechat-article.html](../artifacts/06-wechat-article.html)。

---

## 第 9 轮 — 站点发布（阶段 G，可选）

**用户**：

> 若已配置 Baklib MCP，是否可以把 04 同步到知识库？请先列出将调用的工具与参数，我确认后再执行。

**AI 应答要点**：

- **不**自动写入；仅列出 `list/get` → 用户选定 → `create/update` 草案。  
- 本示例仓库**默认不执行** MCP 写入；对话在此结束即可。

---

## 阶段对照速查

| 轮次 | 阶段 | 关键技能/资源 |
|------|------|----------------|
| 1 | A | `baklib-workspace` + fixtures |
| 2 | B | — |
| 3 | C | — |
| 4–5 | D | — |
| 6 | D→E | `wechat-mp-html`（定稿） |
| 7 | F | `image-generation` 族、`nano-banana-pro-prompting` |
| 8 | E | `wechat-mp-html` |
| 9 | G | `baklib-mcp`（可选，须确认） |
