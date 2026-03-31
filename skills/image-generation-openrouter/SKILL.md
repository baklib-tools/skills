---
name: image-generation-openrouter
description: >-
  通过 OpenRouter 调用图像模型（如 google/gemini-3-pro-image-preview）：鉴权、chat/completions、modalities 与尺寸思路。
  在用户指定 OpenRouter、需要与 UCloud 互备、或提到 openrouter.ai 出图时使用。
---

# 图像生成 · OpenRouter

## 技能范围

- **本技能只解决**：如何按 OpenRouter 公开方式发起 **带图像输出** 的请求（鉴权、端点、常用 JSON 字段）。
- **不包含**：替代用户付费、保证模型可用性；亦不重复 **提示词工程**（见 [nano-banana-pro-prompting](../nano-banana-pro-prompting/SKILL.md)）。

## 执行前检查 API 密钥

在运行 `generate_openrouter_image.py` 或代用户发起请求前，**先确认**已具备 OpenRouter 密钥；若缺失，提示用户**优先**在**项目根**创建 **`.config/OPENROUTER_API_KEY`**（单行文本，UTF-8），其次再考虑环境变量 **`OPENROUTER_API_KEY`**。本仓库示例脚本在读取提示词前会校验密钥，缺失时按上述顺序提示。

## 官方资源

- 控制台与密钥：<https://openrouter.ai/keys>
- 模型页（名称以站点为准）：例如 `google/gemini-3-pro-image-preview` 的说明与限制。

## 鉴权与配置

- **密钥**：**推荐**项目根 **`.config/OPENROUTER_API_KEY`**（单行，UTF-8）；**备选**环境变量 **`OPENROUTER_API_KEY`**。本仓库示例脚本的读取顺序为 **`.config` 文件优先于环境变量**。
- **请求头**：`Authorization: Bearer <API_KEY>`，`Content-Type: application/json`。
- 文档中可能建议附加 **`HTTP-Referer`**、**`X-Title`** 等用于统计或展示名；填你的站点或应用名即可，**勿**写入机密。

## 端点与协议要点

- **端点（常见）**：`POST https://openrouter.ai/api/v1/chat/completions`
- **模型**：例如 **`google/gemini-3-pro-image-preview`**（以 OpenRouter 模型列表为准）。
- **消息体**：使用 `messages` 数组；用户内容可用多模态列表，其中包含 **`type: text`** 的提示词。
- **图像输出**：请求级可能需要声明 **`modalities`**（如同时包含 `image` 与 `text`），以便返回内嵌图像；**具体字段名与取值以 OpenRouter 当前文档与模型页为准**。
- **解析响应**：常见为 `choices[0].message` 下 **`images`** 数组或内嵌 base64 / URL；不同返回形态需分支处理（下载 URL 或解析 `data:image/...;base64,...`）。

## 尺寸与宽高比

OpenRouter 上各模型对分辨率的表达可能不同于 UCloud 直连：有的依赖 **提示词内明确比例/像素**，有的依赖厂商在网关侧支持的参数。**以对应模型在 OpenRouter 的说明为准**；本技能内示例脚本中若有 `2k`/`4k` 等别名，仅为示例映射。

## 本技能内参考脚本

- **路径**：[`scripts/generate_openrouter_image.py`](scripts/generate_openrouter_image.py)（仅 OpenRouter `chat/completions` 与响应解析）。
- **依赖**：Python 3、`requests`。
- **密钥**：`OPENROUTER_API_KEY` 或项目根 `.config/OPENROUTER_API_KEY`。
- **可选环境变量**：`OPENROUTER_HTTP_REFERER`、`OPENROUTER_HTTP_TITLE`（请求头展示用）。

```bash
python path/to/image-generation-openrouter/scripts/generate_openrouter_image.py \
  --prompt prompt.txt --output out.png --size 4:3
python path/to/image-generation-openrouter/scripts/generate_openrouter_image.py \
  --prompt prompt.txt --output out.png --model google/gemini-3-pro-image-preview --size 16:9
```

UCloud ModelVerse 直连请使用 **`image-generation-ucloud`** 目录下脚本。

## 与总技能、UCloud 的关系

- 总览：**[image-generation](../image-generation/SKILL.md)**。
- UCloud ModelVerse 直连：**[image-generation-ucloud](../image-generation-ucloud/SKILL.md)**。

同一套提示词可先在文档中定稿，再分别对接两条 HTTP 路径；**每条请求提示词仍须自包含**。

## 不做什么

- 不保证「与 UCloud 完全同像素/同计费」；两路为不同供应商形态，仅可作为互备或能力补充。
