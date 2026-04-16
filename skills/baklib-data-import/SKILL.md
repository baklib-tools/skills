---
name: baklib-data-import
description: >-
  指导使用 Baklib 开源导入工具（路径清单 → Excel → Open API）将本机、NAS
  或挂载盘上的文件按目录层级迁入 Baklib 资源库（DAM），并可选择同步创建 CMS
  站点资源页。在用户提到批量导入、本地文件进 Baklib、DAM 迁移、importer、
  Excel 导入、路径清单预处理时使用。
---

# Baklib 数据导入（本地磁盘 → Baklib）

官方工具仓库：[https://github.com/baklib-tools/importer](https://github.com/baklib-tools/importer)

**核心流程**：生成 UTF-8 路径清单（每行一个绝对路径）→ **离线**预处理生成 Excel → 在表中可选填写「打标签」「新目录」→ 配置 Open API → 执行导入脚本。

## 前置条件

- Python **3.8+**（建议 3.10+）
- 克隆或下载 importer 仓库，在仓库根目录安装依赖：`pip install -r requirements.txt`
- Baklib **Open API** 的 `access_key`、`secret_key`、目标 `site_id` 及正确的 `api.base_url`（见控制台 / 文档）

## 四步操作（仓库根目录下执行）

### 1. 路径清单

在 macOS / Linux 上可用 `find` 导出文件列表（详见仓库 `docs/02-file-list-mac-linux.md`）：

```bash
find /你的根目录 -type f > file_list.txt
```

清单需为 **UTF-8**，每行一个**绝对路径**。

### 2. 预处理 → Excel

```bash
python3 preprocessing/extract-file-paths.py ./file_list.txt --split 10000 --format excel
```

预处理**不访问网络**。`--split` 可按行数拆成多个表；输出目录中的 `.xlsx` 供下一步编辑。

**长时间导入期间的增量文件**：若从开始清单到导入完成相隔很久，客户可能在原磁盘继续写入新文件。导入结束后可再扫一遍磁盘，用清单差集只挑出新增路径：

```bash
python3 preprocessing/compare_file_lists.py \
  --baseline ./file_list_at_import_start.txt \
  --current ./file_list_rescan.txt \
  -o ./new_files_only.txt
# 或 --scan /数据根目录（清单勿放在该目录内，避免被当成新文件）
```

得到 `new_files_only.txt` 后，可再执行本技能第 2 步 `extract-file-paths.py` 生成 Excel 并走导入。详见 importer 仓库 `preprocessing/README.md`。

### 3. 编辑 Excel（可选但常用）

按 `docs/03-excel-guide.md` 理解各列；可批量填写 **打标签**、**新目录**，覆盖或补充仅由路径推导的结果。

### 4. 配置并导入

将 `config.example.json` 复制为仓库根目录的 `config.json`，填写密钥与导入段参数（示例字段名以仓库内文件为准）：

- `site_id`、`api.base_url`、`api.access_key`、`api.secret_key`
- `import.path_prefix`：去掉盘符/共享根等前缀后，用于对齐 Baklib 中 DAM 目录层级；过深时受 `import.max_depth` 等限制
- `import.skip_directories`：可选，跳过指定相对路径子树
- NAS / 路径映射：Excel 中为服务器路径、本机从挂载点读文件时，使用仓库文档中的 `**excel_path_prefix` + `local_path_root`**（见官方 README 与 `docs/`）

**仅导入资源库（DAM）**：

```bash
python3 baklib_import/import_files_to_dam.py --excel ./your.xlsx --config config.json
```

**DAM + CMS 站点资源页**（Wiki 类站点请**仅**用 DAM 脚本）：

```bash
python3 baklib_import/import_files_to_site.py --excel ./your.xlsx --config config.json
```

首次运行强烈建议：`--dry-run` 和/或 `--max-rows 10` 试跑；更多参数见 `docs/05-import-runbook.md`。

## 安全与仓库卫生

- **不要**将真实 `config.json`、含内部路径的 Excel 或敏感日志提交到 Git。
- 官方仓库已 `.gitignore` 本地 `config.json`；用户自己的副本需自行保管。

## 文档索引（importer 仓库内）


| 路径                             | 用途         |
| ------------------------------ | ---------- |
| `docs/00-index.md`             | 总入口与阅读顺序   |
| `docs/01-workflow-sop.md`      | 端到端 SOP    |
| `docs/04-import-quickstart.md` | API 导入快速开始 |
| `docs/05-import-runbook.md`    | 命令行参数与行为   |


代理协助用户时：若涉及具体列名、Windows 排障或高级参数，应引导阅读上述文档或打开仓库中对应文件，避免臆造未在文档中出现的 API 字段。