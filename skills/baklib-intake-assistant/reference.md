# baklib-intake-assistant — 记忆文件参考

「该放 KB 还是 DAM、站点何时用、知识库树内父级、DAM 标签/合集在 MCP 下的处理方式」见 [routing-guide.md](routing-guide.md)；「镜像目录、SQLite 台账、同步清单流程」见 [local-mirror.md](local-mirror.md)。

## 文件格式

使用 **YAML**，UTF-8。勿写入 Token、Cookie、内网 URL 或客户敏感数据。

## 顶层字段

| 字段 | 说明 |
|------|------|
| `version` | 可选，整数，便于日后迁移 |
| `defaults` | 可选，缺省目标（如常用 `kb_space_id`） |
| `rules` | 可选，按顺序匹配的规则列表 |
| `notes` | 可选，给人看的说明，代理可忽略 |

## `defaults` 示例

```yaml
defaults:
  kb_space_id: "<知识库 space_id 占位符>"
  site_id: "<站点 id 占位符>"
  # 镜像根：与项目根下 `.baklib` 同级，固定为 baklib-mirror/（内含 知识库/、资源库/、站点/）
  baklib_mirror_root: "baklib-mirror"
  # 台账与清单：固定为项目根 `.baklib/sync-state.sqlite`、`.baklib/last-sync-manifest.json`（与 scripts 向上搜索规则一致）
  sync_index_path: ".baklib/sync-state.sqlite"
  sync_manifest_path: ".baklib/last-sync-manifest.json"
  # 可选：从 SQLite 导出的 DAM 词表快照；与库内数据冲突时以 SQLite 为准
  dam_taxonomy_path: "docs/baklib/dam-taxonomy.yaml"
  # 兼容旧配置：若仍使用 kb_mirror_root，视为等同于 {baklib_mirror_root}/知识库
  # kb_mirror_root: "baklib-mirror/知识库"
```

路径与同步流程见 [local-mirror.md](local-mirror.md)。**配套脚本**从 cwd **向上查找** `.baklib/`，使用其中固定文件名；记忆文件中的路径应与该约定一致，见 [scripts/README.md](scripts/README.md)。

## `rules` 项

每项建议包含：

| 字段 | 说明 |
|------|------|
| `match` | 字符串；对用户请求或内容做**简单关键词**匹配（不实现复杂正则引擎时可按「包含子串」理解） |
| `destination` | 目标描述（见下表） |
| `priority` | 可选，数字越大越优先；无则按列表顺序 |

### `destination.type` 取值

| type | 含义 | 常用参数 |
|------|------|----------|
| `kb_article` | 知识库文章 | `space_id`，可选 `parent_id` |
| `dam` | 资源库上传 | 可选 `entity_type`：`image` / `file` / `video` / `audio` |
| `site_page` | 站点页面 | `site_id`，`template_name`（如 `page`），可选 `parent_id`、`published` |
| `local_markdown` | 写入工作区文件 | `relative_path`（相对项目根） |

具体参数名与 MCP 工具字段对齐；创建前仍应用 MCP `list_*` / `get_*` 校验 ID 仍有效。

## 完整示例（虚构 ID）

```yaml
version: 1
defaults:
  kb_space_id: "kb-space-001"
rules:
  - match: "会议纪要"
    priority: 10
    destination:
      type: kb_article
      space_id: "kb-space-001"
      parent_id: "article-parent-meetings"
  - match: "截图|png|jpg"
    destination:
      type: dam
      entity_type: image
  - match: "官网帮助页"
    destination:
      type: site_page
      site_id: "site-001"
      template_name: page
      published: true
notes:
  - 示例仅供结构参考，请替换为真实 ID 或先用 MCP 列出后填入
```

## 匹配歧义时

若同一内容命中多条规则，代理应：

1. 列出命中规则及 `destination` 摘要  
2. 若存在 `priority`，优先推荐高优先级  
3. **等待用户确认一条**后再执行 MCP
