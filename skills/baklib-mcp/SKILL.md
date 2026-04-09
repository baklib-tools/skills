---
name: baklib-mcp
description: 指导在 Cursor 中使用 Baklib MCP（baklib-mcp-server ≥0.3.0）：鉴权与 mcp.json、优先 MCP 读写 KB/站点/DAM；站点页 template_variables 所需 DAM signed_id 通过 MCP 按 purpose 获取（表单场景为 dynamic_form），或与 dam_upload_entity 返回值组合使用。在用户配置 Baklib MCP、操作线上数据、或写入站点页资源字段时使用。任何写入前须向用户确认。
---

# Baklib MCP（Cursor 组合使用指南）

本技能说明如何在 Cursor 中启用 **Baklib MCP**，并规定对 Baklib（知识库 / 站点 / 资源库 / 应用库）的读写**一律优先走 MCP**；同时给出与 **[baklib-mcp-server](https://github.com/xiaohui-zhangxh/baklib-mcp-server)**（建议 **≥0.3.0**）配套的**组合能力**（多步串联、站点页 DAM 字段）。

## ✅ 强制规范（重要）

当用户询问或要求执行与 **Baklib 知识库（KB）/站点（Site）/资源库（DAM）/应用库（Apps）** 相关的「查询清单/读取内容/写入或批量更新/同步数据/生成话术并回填」等操作时：

- **必须优先使用 Baklib MCP 工具获取真实数据**：先 list/get，再基于返回结果进行摘要/话术/下一步建议；写操作遵循 get → create/update/delete →（必要时）get 校验。
- **除非用户明确要求**（例如「用 curl/脚本直接调用 HTTP API」），否则**不要**主动使用 `curl`、自写脚本、或其它方式**绕过 MCP** 去读写 Baklib 线上数据。
- **避免臆测**：在未查询前，不编造知识库/站点的名称、ID、数量、URL、栏目结构等。

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

如果用户希望在 Cursor 中执行 Baklib 相关操作，但 MCP 尚未就绪，需要引导用户完成以下步骤（这是标准流程，不要跳过）：

1. **配置 Token**（二选一，推荐优先用 command ENV）：
   - **方式 A（推荐）**：将 Token 通过 MCP server 的 command 环境变量注入
   - **方式 B**：在 `~/.config/BAKLIB_MCP_TOKEN` 写入一行 `<key>:<secret>`（不要带引号、不要带 `KEY=` 前缀）
2. **确保 MCP 服务器配置存在**：检查 `~/.cursor/mcp.json`，确保已声明 Baklib MCP server；包版本建议 **`@baklib/baklib-mcp-server@0.3.0`** 或以上，以获得「按 purpose 获取 `signed_id`」等能力。
3. **重启 Cursor**：让 MCP 服务加载最新配置。
4. **验证工具可用**：在 Cursor 工具列表中应能看到 Baklib MCP 的相关工具（命名与参数字段以**当前版本工具描述**为准）。

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
- 重启 Cursor 以使配置生效
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

   4. 保存文件并重启 Cursor
   ```

4. **验证修复**
   - 配置完成后，提醒用户重启 Cursor
   - 重新尝试 MCP 操作，确认认证错误已解决

## 🖼 站点页面与 DAM `signed_id`（MCP ≥0.3.0）

**`@baklib/baklib-mcp-server@0.3.0` 起**，MCP 已支持按**用途（purpose）**获取适用于场景的 **`signed_id`**。代理应**只通过 MCP 工具**完成，**不再**使用手写 HTTP 调用 Open 平台接口作为补缺。

操作建议（具体**工具名、必填参数**以你 Cursor 里加载的 MCP 工具 schema 为准）：

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

### mcp.json 文件

检查 `~/.cursor/mcp.json`。以下为示例配置（字段与命名以你使用的 MCP server 实现为准）：

```json
{
    "mcpServers": {
        "baklib-workspace": {
            "command": "npx",
            "args": [
                "-y",
                "@baklib/baklib-mcp-server@0.3.0"
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
4. **mcp.json 文件**：如果你把 MCP 配置放在 `~/.cursor/mcp.json`（用户目录），同样不建议提交到版本控制；务必确保其中不包含任何敏感信息

## 📚 相关文件

- **Token 配置文件**：`~/.config/BAKLIB_MCP_TOKEN`（用户目录）
- **MCP 服务器配置**：`~/.cursor/mcp.json`（用户目录）
- **Git 忽略规则**：避免将任何 Token 文件提交到 Git

## 🎯 使用场景

此规则适用于以下场景：

- 使用 MCP 工具创建、更新或查询 Baklib 知识库文章
- 使用 MCP 工具操作 Baklib 资源库（含按 **purpose** 获取 **`signed_id`**）
- 使用 MCP 工具操作 Baklib 应用库
- **组合流程**：DAM 上传或按 entity 取 **`signed_id`**（**`dynamic_form`**）→ 写入站点页 **`template_variables`**
- 执行需要调用 Baklib MCP 服务的指令（如「同步需求到 MCP 知识库」）

---

**规则版本**：v4.0  
**最后更新**：2026-04-09  
**变更说明**：

- v2.0：更新为使用 npm 包方式（`@baklib/baklib-mcp-server@0.2.0`），不再使用 HTTP POST 方式。认证信息通过环境变量配置。
- v3.0：简化配置流程，`mcp.json` 文件固定，用户只需配置 Token（按 Skills 配置规范放置）。
- v3.1：新增身份认证错误处理规则，当遇到认证错误时提示用户检查 Token 配置。
- v3.2：更新 Token 配置优先级为 command ENV > `~/.config/BAKLIB_MCP_TOKEN`；移除工作目录 `.config/` 与 `.env.mcp` 配置方式；补充 MCP 使用文档链接。
- v3.3–v3.5：曾文档化通过 Open API 在仅有 `entity_id` 时换取 `signed_id`；已由 MCP 能力替代。
- v4.0：**依赖 `baklib-mcp-server` ≥0.3.0**，站点页 DAM **`signed_id`** 一律经 **MCP** 按 **purpose**（表单为 **`dynamic_form`**）获取；**删除** Open API 手写补缺说明；示例包版本更新为 **0.3.0**。
