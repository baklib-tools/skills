---
name: baklib-intake-assistant
description: 将工作区内的零散信息识别、整理后录入 Baklib；优先查 baklib_mirror_root 下 知识库/资源库/站点 的 Markdown 镜像与 SQLite 台账中的 DAM 标签/合集，并按路由指南判断 KB/DAM/站点。在用户要求录入、归档、同步、选存放位置或避免重复标签时使用；须已启用 Baklib MCP。任何写入前须列出拟执行操作并征得用户确认。
---

# Baklib 信息录入助手（工作区 + MCP）

面向**当前工作区**：把识别到的信息结构化，优先通过 **Baklib MCP** 写入云端；用项目内的**偏好/规则文件**实现可复用的「记忆」，减少重复追问。

## 与全局规则的关系

- **MCP 与鉴权**：先阅读并遵循同仓库技能 [baklib-mcp-config](../baklib-mcp-config/SKILL.md)（Token、`list/get` 再写入、禁止臆测清单数据等）。
- **写入确认**：执行 **任意** MCP 创建/更新/删除前，必须用自然语言列出：**将调用的工具名、关键参数（如 `space_id` / `site_id` / 标题 / 是否发布）**，并得到用户**明确同意**后再调用。若用户仅说「录入」但未确认方案，先展示方案再执行。
- **本地文件写入**：若用户要求写入仓库内 Markdown 等路径，同样先说明路径与内容摘要，确认后再写入。

## 记忆文件（偏好与规则）

**作用**：保存「这类内容默认放哪里」「常用知识库/站点 ID」等，使助手在多轮对话中行为一致。

**推荐路径（择一，由使用者在自有项目中创建）**：

1. 项目根目录 `.config/baklib-intake-assistant.yaml`（若含个人习惯，请加入 `.gitignore`）
2. 或项目根目录 `baklib-intake-assistant.preferences.yaml`

**启动时**：若上述文件存在，**先读取**再处理本次请求；若无文件，依赖对话与 MCP `list_*` 结果，并在首次约定规则后**建议用户写入记忆文件**以便下次复用。

字段与示例见 [reference.md](reference.md)。

## 本地镜像与 SQLite 台账（强烈建议）

团队约定：**同步状态与 DAM 标签/合集关系统一走 SQLite**；镜像内容落在 **`baklib_mirror_root`** 下 **`知识库/`、`资源库/`、`站点/`**，正文以 **Markdown** 为主；同步前程序先生成**清单与数量**，**用户确认后再执行**。

1. 记忆文件中配置 `baklib_mirror_root`、`sync_index_path`（必填于该约定下）；可选 `sync_manifest_path`、`dam_taxonomy_path`（导出快照）。  
2. 录入检索：`知识库/`、`站点/` 下搜 `.md`；DAM **标签与合集名**以 **SQLite**（及 `资源库/<合集>/` 目录名）为准。  

完整目录结构、表划分与流程见 **[local-mirror.md](local-mirror.md)**。无镜像时仍可用 MCP，但应提醒重复标签风险并建议按该规范建同步。

## 三类载体怎么选（知识库 / 资源库 / 站点）

录入前先按内容形态做**路由判断**（表格、边界 case、KB 树内位置、DAM 与标签/合集在 MCP 下的处理方式）：

- 完整说明见 **[routing-guide.md](routing-guide.md)**（录入助手应阅读后再给「放哪里」的建议）。

要点速记：

- **KB**：可检索的叙述性知识；**位置** = `space_id` + 可选 **`parent_id`（父文章）** + 可选 **`position`（排序）**。  
- **DAM**：原文件与附件；当前 MCP 侧重上传与 **`name` / `description`**；**标签、合集**若未在工具参数中出现，则把意图写进 `description` 并提示用户在 **Baklib 后台**补全，勿伪造 MCP 参数。  
- **Site**：对外发布、依赖站点模板/导航的页面；**站点标签**用 `site_*_tag` 系列工具，勿与 DAM 标签混为一谈。

## 标准工作流

1. **理解输入 + 查本地镜像**  
   区分：纯文本、Markdown/HTML、本地文件路径、多段混合。必要时用只读方式打开工作区文件核对内容（不要臆测未打开的文件内容）。  
   - 若配置了 `baklib_mirror_root`：在 **`知识库/`**、**`站点/`** 下 **检索** `.md`；若仅配置了旧的 `kb_mirror_root`，则等价于在其目录检索。  
   - DAM 标签/合集：**以 `sync_index_path` 所指向的 SQLite 为准**（代理可通过用户提供的只读查询/导出文件读取）；若有 `dam_taxonomy_path` 快照则作辅助，冲突以 SQLite 为准。  
   - 若用户要**触发同步**：提醒先跑「清单 → 确认数量 → 再同步」，见 [local-mirror.md](local-mirror.md) 第二节。

2. **整理产出物**  
   - 拟定**标题**、**正文**（清理明显噪声、统一 Markdown/HTML 与换行）  
   - 附件：二进制/大文件优先考虑 **DAM**（`dam_upload_entity`），再在文章/页面中引用返回的标识（以 MCP 实际返回为准）  
   - 若需归入某父级：先 `get`/`list` 确认 `parent_id` 存在

3. **解析存放位置（决策树）**  
   - 结合 [routing-guide.md](routing-guide.md) 判断 KB / DAM / Site 的**推荐载体**与理由；涉及「哪个知识库、父级哪一篇、DAM 标签/合集」时按该文档第四节、第七节向用户说清楚。  
   - **记忆文件中有唯一匹配规则** → 采用该目标；仍须在执行前向用户**复述**本次将写入的位置与标题，请其确认（除非用户在同一句已明确「按记忆执行」且规则无歧义，也建议简要列出一行摘要）。  
   - **多条规则可能命中** → 列出候选（类型 + 名称/ID + 匹配理由），给出**推荐项**，**等待用户选定**后再执行。  
   - **无匹配或记忆文件不存在** → **询问**用户：希望进入 KB 文章 / DAM / 站点页面 / 仅本地路径；缺 `space_id`/`site_id` 时先用 MCP **列出可选实体**再请用户选。

4. **执行与校验**  
   用户确认后：按 [baklib-mcp-config](../baklib-mcp-config/SKILL.md) 要求 **get → create/update →（必要时）get** 校验；失败时回报错误原文与建议下一步（鉴权、参数、重名等）。

5. **更新记忆（可选）**  
   当用户说「以后 XXX 都放到 Y」时，将对应规则**追加或合并**进记忆文件（保持 YAML 有效）；不要写入任何 Token 或密钥。

## 能力边界（不做什么）

- 不代替用户保管或生成 Baklib API 密钥；不绕过 MCP 擅自调用私有 HTTP API（除非用户明确要求且与 baklib-mcp-config 例外条款一致）。  
- 不假设模型「记得」上一轮以外的内容：**持久记忆仅来自记忆文件 + 用户本次明确陈述**。  
- 单次对话内若未落盘记忆文件，下轮可能丢失「口头约定」；应在合适时机提示落盘。

## 附加资源

- 镜像目录、SQLite 台账与同步清单：[local-mirror.md](local-mirror.md)  
- 同步辅助 CLI（状态检查、清单对比、导出词表等）：[scripts/README.md](scripts/README.md)  
- 知识库 / 资源库 / 站点选型与位置说明：[routing-guide.md](routing-guide.md)  
- 记忆文件字段说明与示例：[reference.md](reference.md)  
- MCP 与 Token：[baklib-mcp-config](../baklib-mcp-config/SKILL.md)
