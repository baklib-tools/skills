# BKE Markdown · DAM 与 MCP（第 20 节）

## 20. DAM 与 MCP（可选）

- **编号来源**：界面地址栏、用户告知、或 **Baklib 工作区 MCP**（工具名因发行版可能为 `dam_upload_entity`、`dam_get_entity`、`dam_list_entities` 等）。
- **`dam_upload_entity`**：本地 `file_path` 上传；`type` 常见 `image` / `file` / `video` / `audio`；响应中的**数字 `id`** 即手写 Markdown 的 **`dam-id`**。
- **`dam_get_entity`**：按 `id` 查元数据（名称、类型等）写 `alt` 或链接文字；若工具支持 `include_signed_id`，用于**编辑器 HTML** 等场景——**BKE Markdown 用户向仍以 `dam-id` 为主**。
- **`dam_list_entities`**：分页筛选，从条目取 `id`。
- 调用前以**当前环境 MCP 工具描述**为准（参数必填项、枚举）。
- 通常**无需**单独「下载文件」工具即可写 Markdown；落地文件用实体详情中的 URL 或产品下载能力。

