---
name: mineru-office-to-markdown
description: >-
  使用开源 MinerU 在本地将 PDF、DOCX、PPTX、XLSX 及常见图片转为 Markdown（及配套资源），
  便于知识库、RAG、Baklib 录入前处理。在用户提到 MinerU、办公文档转 Markdown、
  PDF 转 MD、PPT/Word 抽取正文、本地批量解析、pipeline 后端时使用。
---

# MinerU：办公文档 → Markdown（本地）

[MinerU](https://github.com/opendatalab/mineru) 可将 **PDF、DOCX、PPTX、XLSX、图片** 等转为 **Markdown / JSON** 等结构化结果，表格多为 HTML 表格嵌入 MD，复杂版式还原能力较强。本技能说明**在你本机**的安装方式、推荐 CLI 参数，以及**目录批量**时的必备注意事项。

**官方文档**：[Usage](https://opendatalab.github.io/MinerU/usage/) · [CLI 参数](https://opendatalab.github.io/MinerU/usage/cli_tools/) · [常见问题](https://opendatalab.github.io/MinerU/faq/)

## 本技能不做什么

- **不在此仓库内执行** MinerU：解析依赖本机 Python 环境与较大模型下载，须由使用者在**自己的工作区终端**运行命令。
- **不替代** MinerU 官方对许可证、商用范围与模型来源的说明；生产或对外分发前请阅读仓库 [LICENSE](https://github.com/opendatalab/mineru/blob/master/LICENSE.md)。
- **不保证** 对 `.doc`（老版 Word）直接支持：MinerU 以 **`DOCX`** 等现代格式为主；老文档请先另存为 DOCX 或 PDF 再转换。

## 前置条件

- **Python**：3.10–3.13（Windows 上若依赖限制，请以官方文档为准，常见为 3.10–3.12）。
- **磁盘与内存**：全量安装与模型缓存通常需要**数十 GB** 磁盘与**足够内存**；大 PDF 首次运行会下载模型，耗时较长。
- **网络**：首次使用需能从模型源拉取权重（见官方「模型源配置」）。

## 安装（推荐）

在**独立虚拟环境**中安装，避免污染系统 Python：

```bash
pip install --upgrade pip
pip install uv
uv venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
uv pip install -U "mineru[all]"
```

源码安装与精简依赖见官方 [Quick Start](https://github.com/opendatalab/mineru) 与 [Extension Modules](https://opendatalab.github.io/MinerU/quick_start/extension_modules/)。

## 单文件转换

将 `<输入文件>` 换为你的 PDF / DOCX / PPTX / XLSX / 图片路径，`<输出目录>` 为**已存在或可由工具创建的父目录**：

```bash
mineru -p "<输入文件>" -o "<输出目录>" -b pipeline -l ch
```

说明：

- **`-b pipeline`**：兼容面广，可在纯 CPU 环境运行（具体以本机实测为准）；需要更高精度时可查阅官方后端对比表改用 `hybrid-*` / `vlm-*`（硬件要求更高）。
- **`-l ch`**：中文 OCR/版面语言提示；多语言文档请查阅 CLI 的 `-l` 可选值。

仅处理 PDF **部分页**（0-based）示例：

```bash
mineru -p "<输入.pdf>" -o "<输出目录>" -b pipeline -l ch -s 0 -e 9
```

更多参数（公式/表格开关、环境变量等）见官方 [CLI 工具说明](https://opendatalab.github.io/MinerU/usage/cli_tools/)。

## 目录批量（重要）

当前 CLI 对「输入目录」的扫描**通常只处理该目录下的直接文件**，**不会递归子文件夹**。若根目录下只有子目录、没有散落文件，会报 *No supported documents found*。

**推荐做法**（二选一）：

1. **分批**：对每个**仅含素材文件的子文件夹**分别执行一次 `mineru -p "<子目录>" -o "<输出根>" ...`。
2. **扁平化**：将支持的文件复制到**单层临时目录**（注意重名可加前缀），再对该临时目录执行一次 `mineru`。

支持的扩展名以官方为准，一般包括：`pdf`、`docx`、`pptx`、`xlsx`、常见图片格式等。**CSV** 等表格文件通常不在同一套「版式解析」路径内，需改用表格工具或专用导入流程。

## 输出结果怎么找

成功后在输出目录下会按文档名生成子文件夹；常见情况：

- 版式解析结果可能在 **`auto/`** 下生成 `*.md` 与 `images/` 等。
- **Office 原生解析**结果可能在 **`office/`** 下生成 `*.md`（以你本机 MinerU 版本实际目录为准）。

若日志中出现与 **`*_origin.pdf` 可视化**相关的 *Skipping visualization*，多为可选中间件缺失，**不一定表示**正文 Markdown 未生成，请以对应 `*.md` 是否存在为准。

## 与 Baklib 工作流衔接

转换得到的 Markdown 与图片可在本地校对后，再使用本仓库 **[baklib-data-import](../baklib-data-import/SKILL.md)** 将文件批量迁入 Baklib DAM（或按你们镜像规范放入 `baklib-intake-assistant` 约定目录）。路径、元数据与脱敏规则以各技能说明为准。

## 故障排查提示

- **首次大文档失败、第二次成功**：多为首次仍在下载模型；可先对**少量页**试跑，再全量。
- **超时或内存**：查阅官方 FAQ；可尝试调整官方文档中的窗口/并发相关环境变量（如 `MINERU_PROCESSING_WINDOW_SIZE` 等）。
- **命令帮助**：`mineru --help`。
