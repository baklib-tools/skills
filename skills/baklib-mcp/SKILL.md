---
name: baklib-mcp
description: 说明如何配置并使用 Baklib MCP：涵盖鉴权与 MCP 客户端配置、优先经 MCP 读写知识库/站点/DAM；站点页 template_variables 所需 DAM signed_id 经 MCP 按 purpose 获取（表单为 dynamic_form）或与 dam_upload_entity 返回值组合。写入 DAM 内容片段、知识库正文、站点 BKE 富文本时统一使用 BKE Markdown；解析或撰写 BKE Markdown 前须确认已安装并加载配套技能 baklib-bke-markdown，否则先提示用户按仓库说明安装。在用户配置 Baklib MCP、操作线上 Baklib 或写入站点资源字段时使用；任何写入前须经用户确认。
---

# Baklib MCP（组合使用指南）

本技能说明如何在**已接入 MCP 的 AI 代理环境**中启用 **Baklib MCP**，并规定对 Baklib（知识库 / 站点 / 资源库 / 应用库）的读写**一律优先走 MCP**；同时给出与 **[baklib-mcp-server](https://github.com/xiaohui-zhangxh/baklib-mcp-server)** 配套的**组合能力**（多步串联、站点页 DAM 字段）。

## ✅ 强制规范（重要）

当用户询问或要求执行与 **Baklib 知识库（KB）/站点（Site）/资源库（DAM）/应用库（Apps）** 相关的「查询清单/读取内容/写入或批量更新/同步数据/生成话术并回填」等操作时：

- **必须优先使用 Baklib MCP 工具获取真实数据**：先 list/get，再基于返回结果进行摘要/话术/下一步建议；写操作遵循 get → create/update/delete →（必要时）get 校验。
- **除非用户明确要求**（例如「用 curl/脚本直接调用 HTTP API」），否则**不要**主动使用 `curl`、自写脚本、或其它方式**绕过 MCP** 去读写 Baklib 线上数据。
- **避免臆测**：在未查询前，不编造知识库/站点的名称、ID、数量、URL、栏目结构等。

## 📝 写入内容格式：统一使用 BKE Markdown

### 配套技能 `baklib-bke-markdown`（强制）

在通过 MCP **读取**需按 BKE 语义解析的正文（例如准备对照、改写或回填），或 **撰写/改写/回填** 下文表中任一 **BKE Markdown** 内容之前，代理须**先确认**当前会话已加载 **[baklib-bke-markdown](https://github.com/baklib-tools/skills/blob/main/skills/baklib-bke-markdown/SKILL.md)** 技能（例如：宿主已安装该技能且可在技能列表中打开其 `SKILL.md`，或用户已明确引用该技能）。

- **若无法确认**已安装/已加载：**不得**仅凭本文件与通用 Markdown 臆写 BKE 扩展语法；须**暂停**正文层面的解析与撰写，**先提示用户**安装并（按所用工具说明）重新加载技能后再继续。
- **安装方式**（与仓库 [README](https://github.com/baklib-tools/skills/blob/main/README.md) 一致）：
  - **推荐（skills CLI）**：`npx skills add baklib-tools/skills --skill baklib-bke-markdown`；若与本技能一并安装，可用：`npx skills add baklib-tools/skills --skill baklib-mcp --skill baklib-bke-markdown`
  - **查看列表**：`npx skills add baklib-tools/skills --list`
  - **手动**：从仓库目录 [`skills/baklib-bke-markdown/`](https://github.com/baklib-tools/skills/tree/main/skills/baklib-bke-markdown) 复制到**你自己项目**中由工具指定的技能安装路径，保持内含 `SKILL.md`。

### 格式约定

通过 MCP 向 Baklib **写入**或**回填**下列内容时，**正文一律采用 BKE Markdown**：即在 **标准 Markdown / GFM** 之上，使用 Baklib BKE 编辑器约定的**扩展写法**（圆括号第三段属性、`dam-id`、文件卡片冒号语法、L2 HTML 注释块如 `link-card` / `fragment` / 嵌入等）。**完整语法、示例与避坑清单**见技能 **[baklib-bke-markdown](https://github.com/baklib-tools/skills/blob/main/skills/baklib-bke-markdown/SKILL.md)**；撰写或改写正文时应**打开并对照该技能**，不要仅凭「通用 Markdown」臆测扩展格式。各 MCP 工具的字段名仍以工具 schema 为准。

| 场景 | 说明 |
|------|------|
| **DAM 内容片段** | 片段类文本字段以 **BKE Markdown** 编写，便于在资源侧与下游引用中保持一致结构（含 DAM 引用等扩展）。 |
| **知识库文档内容** | 文章/文档正文、摘要等文本型内容以 **BKE Markdown** 写入；避免把纯 HTML 或未文档化的专有格式当作主载体。 |
| **站点页面 BKE 富文本** | 模板中 BKE 富文本类字段的值以 **BKE Markdown** 提供；图片等资源仍通过 DAM `signed_id` 等机制按模板要求填入 **`template_variables`**，与上文 DAM 规范一致。 |

**代理注意**：从 MCP **读取**到的内容可能是 HTML 或内部序列化形式；**写入**时仍按上表约定输出 **BKE Markdown**（并遵循 **baklib-bke-markdown** 技能中的扩展规则），除非用户明确要求使用其它格式或工具文档另有说明。

## 🔍 MCP 配置检查规则

**重要**：当你需要调用 MCP 操作 Baklib 知识库/资源库/应用库的时候，必须先确认 Token 已配置。

Token 配置优先级（从高到低）：

1. **command ENV**（启动 MCP server 的命令环境变量）
2. **用户目录配置文件**：`~/.config/BAKLIB_MCP_TOKEN`

### 检查步骤

1. **检查 Token 配置文件是否存在**
   - 优先检查 MCP server 启动时的环境变量是否已注入 Token
   - 若未注入，再检查 `~/.config/BAKLIB_MCP_TOKEN` 是否存在
   - 如果仍不存在，需要提醒用户创建该文件并写入 Token
2. **验证配置内容**
   - 如果文件存在，检查是否包含必要的认证信息（API 密钥 Token）
   - 确认配置项已正确填写（不是占位符或空值）

## 🧩 安装与启用（用户未配置时要提醒）

如果用户希望借助 **MCP 已连接的 AI 代理**执行 Baklib 相关操作，但 MCP 尚未就绪，需要引导用户完成以下步骤（这是标准流程，不要跳过）：

1. **配置 Token**（二选一，推荐优先用 command ENV）：
   - **方式 A（推荐）**：将 Token 通过 MCP server 的 command 环境变量注入
   - **方式 B**：在 `~/.config/BAKLIB_MCP_TOKEN` 写入一行 `<key>:<secret>`（不要带引号、不要带 `KEY=` 前缀）
2. **确保 MCP 服务器已在客户端声明**：按**所用 MCP 宿主**的文档编辑其 MCP 配置（配置文件路径因产品而异），确保已注册 Baklib MCP server；包版本建议 **`@baklib/baklib-mcp-server@0.4.0`** 或以上，以获得「按 purpose 获取 `signed_id`」等能力。
3. **重载 MCP**：保存配置后按客户端要求**重启应用或刷新 MCP 连接**，使新配置生效。
4. **验证工具可用**：在已连接 MCP 的**工具/函数列表**中应能看到 Baklib MCP 的相关工具（命名与参数字段以**当前版本工具描述**为准）。

## ⚠️ 未配置时的处理流程

如果 Token 未配置或配置不完整，需要执行以下步骤：

### 步骤 1：提醒用户创建 Token 文件

提醒用户在用户目录创建 `~/.config/BAKLIB_MCP_TOKEN`：

```bash
mkdir -p ~/.config
printf '%s' '<key>:<secret>' > ~/.config/BAKLIB_MCP_TOKEN
```

### 步骤 2：指导用户配置认证信息

提醒用户将 Token 写入 `~/.config/BAKLIB_MCP_TOKEN` 文件：

1. **API 密钥（Token）**
   - 获取方式：登录 Baklib 后台，进入 **个人中心** → **API 密钥对**，创建并复制 API 密钥
   - 写入格式：`<key>:<secret>`（一行即可）

**重要提示**：

- `~/.config/BAKLIB_MCP_TOKEN` 属于敏感信息文件，不要提交到版本控制
- API 密钥是敏感信息，不要泄露给他人

### 步骤 3：验证配置

配置完成后，提醒用户：

- 保存 `~/.config/BAKLIB_MCP_TOKEN` 文件（或确保 command ENV 已正确注入）
- 按客户端说明**重载 MCP**（如重启应用或刷新连接）以使配置生效
- 重新尝试 MCP 操作

## ❌ 身份认证错误处理

**重要**：当调用 Baklib MCP 工具时，如果遇到身份认证错误（如 401 Unauthorized、认证失败、Token 无效等），需要执行以下步骤：

### 错误识别

常见的身份认证错误包括：

- `401 Unauthorized`
- `认证失败`
- `Token 无效`
- `身份验证错误`
- `API 密钥错误`
- 其他与认证相关的错误信息

### 处理步骤

1. **检查 Token 是否已配置（按优先级）**
   - 优先检查 command ENV 是否已注入
   - 若未注入，再检查 `~/.config/BAKLIB_MCP_TOKEN` 是否存在
2. **检查配置是否正确**
   - 如果存在配置，检查是否包含正确的认证信息
   - 确认 Token（`<key>:<secret>`）已正确填写
   - 确认不是占位符或空值
3. **提示用户配置或更新认证信息**

   如果 Token 未配置或配置不正确，提示用户：

   ```
   ⚠️ 身份认证错误：请检查并配置 Token（优先 command ENV，其次 ~/.config/BAKLIB_MCP_TOKEN）

   请执行以下步骤：
   1. 在用户目录创建配置文件：
      mkdir -p ~/.config
      printf '%s' '<key>:<secret>' > ~/.config/BAKLIB_MCP_TOKEN

   2. 将 Token 写入该文件（一行）：
      <key>:<secret>

   3. 获取 API 密钥：
      - 登录 Baklib 后台
      - 进入「个人中心」→「API 密钥对」
      - 创建并复制 API 密钥

   4. 保存文件并按客户端说明重载 MCP（如重启应用或刷新连接）
   ```

4. **验证修复**
   - 配置完成后，提醒用户重载 MCP
   - 重新尝试 MCP 操作，确认认证错误已解决

## 🖼 站点页面与 DAM `signed_id`（MCP ≥0.4.0）

**`@baklib/baklib-mcp-server@0.4.0` 起**，MCP 已支持按**用途（purpose）**获取适用于场景的 **`signed_id`**。代理应**只通过 MCP 工具**完成，**不再**使用手写 HTTP 调用 Open 平台接口作为补缺。

操作建议（具体**工具名、必填参数**以当前 MCP 连接中加载的**工具 schema** 为准）：

1. **`dam_upload_entity`**：若工具说明中返回 **`signed_id`**，且站点模板可直接使用该值，写入 **`site_create_page` / `site_update_page`** 的 **`template_variables`** 即可。
2. **仅有数字 `entity_id`、需要站点表单用 `signed_id`**：使用 MCP 中提供的 **「按 purpose 获取 signed_id」** 能力（例如传入 `entity_id` 与 **`purpose=dynamic_form`**）。**站点页面表单里，凡 DAM `signed_id` 相关字段，purpose 一律使用 `dynamic_form`**，与 baklib-mcp-server / 官方文档一致。
3. **仍须遵守**：**写入/更新站点页前**向用户**确认**；勿在仓库或公开对话中粘贴密钥。

## 🔗 典型组合：上传图片并写入站点页「图片」类字段

1. **上传**：MCP **`dam_upload_entity`**（`file_path`、`type` 设为 `image` 等），从返回中取 **`signed_id`**（若有且模板可直接用，可跳过下一步）。
2. **若需按站点表单 purpose 再解析**：用 MCP 提供的 **purpose 参数**（**`dynamic_form`**）获取最终写入 `template_variables` 的 **`signed_id`**。
3. **定位页面与字段名**：MCP **`site_list_pages`** / **`site_get_page`** 确认 **`site_id`**、**`page_id`** 及模板中图片字段在 **`template_variables`** 的键名（**勿臆测**）。
4. **更新页面**：用户确认后，MCP **`site_update_page`** 写入对应键（结构对齐 **`site_get_page`**）。
5. **校验**：必要时再次 **`site_get_page`**。

## 🧭 清单类/参数缺失时的标准做法（避免来回问）

- **清单类需求**（「我有哪些知识库/站点/页面/资源？」）：先用 MCP 的 list 工具列出实体，再输出整理后的结果。
- **参数缺失/不确定**（例如缺 `site_id` / `kb_space_id`）：先列出可选实体（先列站点/知识库），再让用户在列表里选择或继续下一步工具调用。
- **接口返回空**：如确认为空，直接告知为空，并给出 MCP 能力范围内的下一步（创建/导入/同步）。

## 🧾 输出建议（面向用户）

- **先给可操作结果**：例如分组列出知识库列表、站点列表，并附关键标识（如 `id`）。
- **再给 1-2 条下一步**：例如「要列页面需要哪个 `site_id`」「要生成并回填话术需要哪类文章范围」等。

## 📝 配置说明

### MCP 客户端配置（常见为 `mcp.json` 形态）

配置文件**路径与文件名因 MCP 宿主而异**，请查阅所用客户端文档。以下为 **JSON 结构示例**（字段与命名以你使用的 MCP server 实现为准）：

```json
{
    "mcpServers": {
        "baklib-workspace": {
            "command": "npx",
            "args": [
                "-y",
                "@baklib/baklib-mcp-server@0.4.0"
            ],
            "env": {
                "BAKLIB_MCP_TOKEN": "<key>:<secret>"
            }
        }
    }
}
```

### Token 配置

Token 配置优先级（从高到低）：

1. **command ENV**（推荐）：将 Token 通过 MCP server 的 command 环境变量注入
2. **用户目录配置文件**：`~/.config/BAKLIB_MCP_TOKEN`（文件内容为 Token：`<key>:<secret>`，一行即可）

## 🔐 安全注意事项

1. **不要提交敏感信息**：不要将 `~/.config/BAKLIB_MCP_TOKEN` 提交到版本控制系统
2. **避免硬编码**：不要把 Token 写进仓库里的脚本/文档/配置文件
3. **定期更新密钥**：如果 API 密钥泄露或过期，及时更新 Token（ENV 或 `~/.config/BAKLIB_MCP_TOKEN`）
4. **MCP 配置文件**：凡存放 server 声明与密钥占位符的 MCP 配置，均不建议提交到版本控制；务必确保其中不包含任何敏感信息

## 📚 相关文件

- **BKE Markdown 撰写（扩展语法）**：[baklib-bke-markdown/SKILL.md](https://github.com/baklib-tools/skills/blob/main/skills/baklib-bke-markdown/SKILL.md)（单独安装技能时以宿主文档为准；仓库协作约定见 [AGENTS.md](https://github.com/baklib-tools/skills/blob/main/AGENTS.md)）
- **Token 配置文件**：`~/.config/BAKLIB_MCP_TOKEN`（用户目录）
- **MCP 服务器配置**：由 MCP 宿主决定（参阅该客户端的 MCP 设置文档）
- **Git 忽略规则**：避免将任何 Token 文件提交到 Git

## 🎯 使用场景

此规则适用于以下场景：

- 使用 MCP 工具创建、更新或查询 Baklib 知识库文章（正文格式见 **baklib-bke-markdown**）
- 使用 MCP 工具操作 Baklib 资源库（含按 **purpose** 获取 **`signed_id`**）
- 使用 MCP 工具操作 Baklib 应用库
- **组合流程**：DAM 上传或按 entity 取 **`signed_id`**（**`dynamic_form`**）→ 写入站点页 **`template_variables`**
- 执行需要调用 Baklib MCP 服务的指令（如「同步需求到 MCP 知识库」）
