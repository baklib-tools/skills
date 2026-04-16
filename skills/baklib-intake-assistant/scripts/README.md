# Baklib 镜像同步辅助脚本

与技能 [`local-mirror.md`](https://github.com/baklib-tools/skills/blob/main/skills/baklib-intake-assistant/local-mirror.md) 约定一致：SQLite 台账、镜像根下 **`知识库/`**、**`资源库/`**、**`站点/`**。  
**首次运行任意会打开数据库的脚本时，会自动建表/迁移**（`lib/db.py` 中 `PRAGMA user_version`），无需单独执行 `init_db` 或 `schema.sql`。

当前 **schema 版本**：`1`（见 `lib/db.py` 中 `SCHEMA_VERSION`）。

## 路径约定（固定，不可通过环境变量或 CLI 覆盖）

所有脚本从 **当前工作目录（cwd）** 出发，**逐级向父目录查找**名为 **`.baklib`** 的目录（须已存在且为文件夹）。找到后使用：

| 用途 | 绝对路径规则 |
|------|----------------|
| SQLite 台账 | `{找到的项目根}/.baklib/sync-state.sqlite` |
| 同步清单 JSON | `{找到的项目根}/.baklib/last-sync-manifest.json` |
| Markdown 镜像根 | `{找到的项目根}/baklib-mirror/`（与 `.baklib` 同级，内含 `知识库/`、`资源库/`、`站点/`） |

因此：请在**技能项目根**创建 `.baklib`（可先 `mkdir -p .baklib`），并在该根下维护 `baklib-mirror/`。在子目录中运行脚本时，只要 cwd 仍位于该根之下，向上搜索即可命中同一套路径。

若未找到 `.baklib/`，脚本以退出码 **4** 报错并提示创建目录。

## 脚本说明

| 脚本 | 作用 | 退出码 |
|------|------|--------|
| `status.py` | 各表行数、最近一次 `sync_runs`、`--json` | 0；找不到 `.baklib` 为 4 |
| `health_check.py` | 检查 `baklib-mirror` 下顶层三目录；可选核对台账 `relative_path` | 0 正常，1 失败，4 找不到 `.baklib` |
| `export_dam_taxonomy.py` | 从 `dam_collections` / `dam_tags` 导出 YAML（`-o` 或 stdout） | 0；4 找不到 `.baklib` |
| `show_manifest.py` | 打印 `.baklib/last-sync-manifest.json` | 0；2 清单不存在；4 找不到 `.baklib` |
| `plan_sync.py` | `--from-fixture` 对比指纹并**只写**上述清单路径 | 0；3 未提供 fixture；4 找不到 `.baklib` |
| `record_sync_run.py` | 向 `sync_runs` 插入一条记录，打印新行 id | 0；4 找不到 `.baklib` |

## 推荐顺序

1. 在技能项目根执行 `mkdir -p .baklib`，并创建 `baklib-mirror/知识库` `资源库` `站点`（可用 `mkdir -p`）。  
2. 在**项目内任意子目录**或根目录运行：`python3 health_check.py`（可先 `--skip-path-check`）。  
3. `python3 plan_sync.py --from-fixture fixtures/example-remote-index.json`。  
4. 向用户展示清单后执行实际拉取与写 `.md`；结束时 `record_sync_run.py` 记一笔。

## Fixture 格式（`plan_sync.py --from-fixture`）

与 [`fixtures/example-remote-index.json`](fixtures/example-remote-index.json) 相同顶层键：

- `kb_articles`: `{ "space_id", "article_id", "fingerprint" }`  
- `dam_entities`: `{ "entity_id", "fingerprint" }`  
- `site_pages`: `{ "site_id", "page_id", "fingerprint" }`  

对比规则：远端有而库无 → `*_create`；库有且指纹不同 → `*_update`；库有而远端无 → `*_delete`（仅统计，不自动删文件）。

## 运行示例

```bash
# 在技能项目根（已存在 .baklib/）
cd /path/to/your-skill-project
mkdir -p .baklib baklib-mirror/{知识库,资源库,站点}
python3 path/to/scripts/status.py --json
python3 path/to/scripts/plan_sync.py --from-fixture path/to/scripts/fixtures/example-remote-index.json
```

勿将含 **API 密钥** 的配置提交到 Git；可用本地 `config.local.*` 并加入 `.gitignore`。

## 远端拉取

在 [`lib/remote_client.py`](lib/remote_client.py) 中实现 `fetch_remote_index()`，或在业务仓库包装 `plan_sync.py` 的逻辑。本仓库脚本**不绑定**具体 Baklib HTTP 端点。
