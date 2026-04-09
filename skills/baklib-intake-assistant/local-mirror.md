# 本地镜像与词表：便于检索、统一说法

录入助手在建议「放哪、叫什么标签」时，应优先依赖**工作区内已有的 Baklib 镜像**与 **SQLite 台账**（含 DAM 标签/合集），再辅以 MCP 查询。这样便于全文检索、减少「同一概念多种写法」导致的重复标签/合集。

## 一、为什么要先做本地镜像

| 目的 | 说明 |
|------|------|
| **检索** | 用编辑器/终端/`rg` 在 **Markdown 正文与 frontmatter** 中搜标题、路径、已有栏目，比反复 `list` 全文更轻、上下文更完整。 |
| **父级与目录感** | 知识库树在 `.md` 目录结构或 frontmatter 中往往更直观，便于选 `parent_id` 或建议新建父级的命名。 |
| **DAM 术语一致** | **合集目录名**与**标签**以磁盘目录 + **SQLite 中与线上一致的记录**为准，同步脚本负责对齐，避免多种说法并存。 |

实现方式：由团队自研/自管的同步程序通过 **Baklib Open API**（或等价能力）拉取；本技能**不绑定**具体可执行文件名，但**统一约定**镜像根目录结构、**仅用 SQLite** 存同步状态与 DAM 标签/合集元数据。记忆文件里配置路径即可（见 [reference.md](reference.md)）。

## 二、统一规范：SQLite 台账 + 先清单后同步

### 2.1 同步流程（必须：先统计，再执行）

1. **生成同步清单**：程序对比远端与 SQLite 台账中的版本指纹（如 `updated_at` / `revision` / ETag，以 API 实际字段为准），产出**待拉取条目数量**（可按知识库 / 资源库 / 站点分页统计）。  
2. **向用户展示摘要**：明确告知本次将新增、更新、（若有）删除或跳过的**大致数量与范围**，必要时列出风险（磁盘占用、耗时）。  
3. **用户统一确认**后，再执行实际拉取与写盘。  
4. **写盘完成后**：更新 SQLite 中对应行的状态与指纹，保证下次增量可对比。

录入助手若参与「要不要现在同步」：应提醒用户遵循上述**先清单、后执行**，避免长任务误跑。

### 2.2 台账存储：统一使用 SQLite 3

- **唯一**推荐的同步状态载体：**SQLite 单文件**（路径由 `defaults.sync_index_path` 指定）。  
- 存放内容至少包括：各实体远端 **ID**、**版本指纹**、**本地相对路径**、**上次成功同步时间**；以及 **DAM 标签、合集**与资源的关联（见 2.4），与线上一致、可增量对比。  
- 若需在对话里快速浏览「待同步数量」，可由同步程序额外写出一份**人类可读摘要**（如 `sync-manifest.json` 或 `.md`），路径可用 `defaults.sync_manifest_path`；**仍以 SQLite 为权威台账**。

### 2.2.1 随技能提供的脚本（`scripts/`）

本技能目录下 [`scripts/`](scripts/) 提供一组**可复用 CLI**（Python 3.10+，默认仅标准库），与上表路径约定对齐：

- 打开数据库时由 [`scripts/lib/db.py`](scripts/lib/db.py) **`ensure_schema`** 自动建表/迁移（`PRAGMA user_version`，当前版本 `1`），无需单独 `init_db` / `schema.sql`。  
- **推荐顺序**：任意脚本首次连接建库 → 日常 `health_check.py` / `status.py` → `plan_sync.py --from-fixture …`（或接入你们自己的远端拉取）生成清单 → 用户确认后再执行实际拉取与写 `.md` → 可用 `record_sync_run.py` 记入 `sync_runs`。

环境变量与命令说明见 [`scripts/README.md`](scripts/README.md)；Fixture 示例见 [`scripts/fixtures/example-remote-index.json`](scripts/fixtures/example-remote-index.json)。

### 2.3 镜像根目录与落盘格式（Markdown）

在 **`baklib_mirror_root`** 下使用**固定三级顶层目录**（名称建议与下表一致，便于协作）：

```text
{baklib_mirror_root}/
├── 知识库/
│   └── <space 目录名或 space_id>/
│       └── <文章目录树>/
│           └── ...                    # 每篇文章对应目录或 .md，由同步工具定义
├── 资源库/
│   └── <合集目录名>/                  # 与线上一致；无合集可用约定占位名如「未分类」
│       └── ...                        # 每条资源建议对应 .md（元数据 + 正文说明）及按需 sidecar
└── 站点/
    └── <site 目录名或 site_id>/
        └── <页面目录树>/
            └── ...                    # 页面内容以 .md 为主
```

- **正文与可编辑说明**：统一落为 **`.md`**，并建议用 **YAML frontmatter** 保存 `article_id` / `page_id` / `entity_id`、`parent_id`、`space_id` / `site_id` 等（字段以你们 API 为准）。  
- **二进制原件**（图片、PDF 等）：是否一并下载到 `资源库/合集/...` 由团队策略决定；若仅同步元数据，也应在对应 `.md` 或 SQLite 中记录远端引用信息，便于核对。

### 2.4 资源库：合集目录 + 标签写入 SQLite

- **合集**：与线上合集一致的**文件夹名**挂在 `资源库/<合集>/` 下；台账表中记录 `entity_id` ↔ 合集名 ↔ 相对路径，便于增量对比与移动检测。  
- **标签**：**不以散落 Markdown 为权威列表**；在 SQLite 中维护**标签表**及**资源—标签关联表**（或与 API 结构同构的字段），每次同步后与线上一致。录入助手查标签、合集时：**优先查 SQLite**（或由脚本从 SQLite **导出**只读 `dam-taxonomy.yaml` 供 `rg` 使用）。  
- 若仍配置 `dam_taxonomy_path`：可作为导出快照；**与 SQLite 冲突时以 SQLite 为准**，并应重新导出 YAML。

### 2.5 建议的 SQLite 表划分（实现时可调整表名）

以下仅为**逻辑模型**，具体列类型与索引由同步程序实现：

| 逻辑表 | 用途 |
|--------|------|
| `kb_articles` | 知识库文章：`article_id`、`space_id`、版本指纹、`relative_path` |
| `dam_entities` | 资源：`entity_id`、合集目录名、`relative_path`、版本指纹 |
| `dam_tags` | 标签名（及若有的远端 tag id） |
| `dam_entity_tags` | 资源与标签多对多 |
| `dam_collections` | 合集元数据（若需与文件夹外的 id 对齐） |
| `site_pages` | 站点页面：`page_id`、`site_id`、版本指纹、`relative_path` |
| `sync_runs` | 可选：每次任务起止时间、清单统计、操作人/触发源 |

## 三、知识库：在镜像中的使用方式

- 检索入口：`{baklib_mirror_root}/知识库/`。  
- 录入前：先在该树下 **搜索** 是否已有同类文章或合适父级；再用 MCP **`kb_list_articles` / `kb_get_article`** 核对线上 ID。  
- 若无镜像：建议用户按第二节建立同步；此前仅依赖 MCP，并提示重复与结构漂移风险。

## 四、站点：在镜像中的使用方式

- 检索入口：`{baklib_mirror_root}/站点/<site>/`。  
- 与知识库相同：先本地 `.md` 与 frontmatter，再 MCP 校验。

## 五、与 MCP 的分工

| 场景 | 优先 | 补充 |
|------|------|------|
| 搜已有 KB / 站点内容 | `知识库/`、`站点/` 下 Markdown | MCP 校验 ID |
| DAM 标签、合集用词 | SQLite（及 `资源库/` 目录名） | MCP 上传文件；后台补全若 API 未覆盖 |
| 待同步数量、是否过期 | SQLite 台账 + 同步清单摘要文件 | — |

## 六、仓库卫生

- 镜像目录与 `.sqlite` 可能含内部信息：按需 **`.gitignore`** 或专用私有仓。  
- 勿把 API 密钥写入镜像、台账或清单文件。

## 附录：为何不再推荐用 JSON 存台账

JSON 适合极小样本或调试；在**大量 KB/DAM/站点实体**与**高频增量**下，整文件读写与合并成本高。**本技能约定以 SQLite 为唯一台账**，JSON 仅可作为同步程序生成的**只读摘要**（见 2.2）。
