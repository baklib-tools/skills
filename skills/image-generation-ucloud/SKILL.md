---
name: image-generation-ucloud
description: >-
  通过 UCloud ModelVerse 图像 API 出图：鉴权、端点、模型与尺寸约定。
  在用户指定 UCloud、ModelVerse、api.modelverse.cn 或需 doubao-seedream / gemini-3-pro-image-preview / gemini-3.1-flash-image-preview 时使用。
---

# 图像生成 · UCloud（ModelVerse）

## 技能范围

- **本技能只解决**：如何按 UCloud 公开文档调用 **ModelVerse** 图像相关接口（鉴权位置、端点形态、模型与参数要点）。
- **不包含**：替代用户执行扣费请求、保证 SLA；亦不重复 **提示词写法**（见 [nano-banana-pro-prompting](../nano-banana-pro-prompting/SKILL.md)）。

## 执行前检查 API 密钥

在运行 `generate_ucloud_image.py` 或代用户发起请求前，**先确认**已具备 UCloud 密钥；若缺失，提示用户**优先**在**项目根**创建 **`.config/UCLOUD_API_KEY`**（单行文本，UTF-8），其次再考虑环境变量 **`UCLOUD_API_KEY`**。本仓库示例脚本在读取提示词前会校验密钥，缺失时按上述顺序提示。

## 官方文档与模型列表 API

- 产品与接口说明以 UCloud 文档为准，例如文档中心内 **ModelVerse** 各模型「图像 API」章节（路径可能随版本调整，请站内搜索模型名）。
- **Gemini 3.1 Flash Image**：[gemini-3.1-flash-image](https://docs.ucloud.cn/modelverse/api_doc/image_api/gemini-3.1-flash-image)（文档路径名可能与 **API 返回的 `baseModelId`** 不完全一致，以接口为准。）
- **Gemini 3 Pro Image（示例）**：[gemini-3-pro-image](https://docs.ucloud.cn/modelverse/api_doc/image_api/gemini-3-pro-image)
- **核对模型 ID（无需密钥）**：
  - `GET https://api.modelverse.cn/v1beta/models` — Gemini 协议，`models[].baseModelId`（如 `gemini-3.1-flash-image-preview`）。
  - `GET https://api.modelverse.cn/v1/models` — OpenAI 兼容列表，`data[].id`。
- 本仓库脚本支持 **`--list-models`**，会请求上述接口并节选名称中含 `image` 的条目，便于与脚本内置 ID 对照。

## 鉴权与配置

- **密钥**：使用你在 UCloud 控制台获得的 **ModelVerse API Key**。**推荐**：项目根 **`.config/UCLOUD_API_KEY`**（单行文本，UTF-8）；**备选**：环境变量 **`UCLOUD_API_KEY`**。本仓库示例脚本的读取顺序为 **`.config` 文件优先于环境变量**。
- **勿**在技能或仓库中写入真实密钥。

## 两种 HTTP 形态（需按模型选用）

### 1）通用图像生成（`images/generations`）

- **典型用途**：`doubao-seedream-4.5` 等文档中约定走该路径的模型（豆包文生图；**模型 ID 以文档/控制台为准**，不一定出现在 `v1beta/models` 列表中）。
- **端点（示例）**：`POST https://api.modelverse.cn/v1/images/generations`
- **请求头**：`Authorization` 为 API Key；`Content-Type: application/json`。
- **响应**：常见为 JSON，`data[0]` 中含 `url` 或 `b64_json`；下载或解码后写入文件即可。
- **水印**：若文档支持 `watermark` 字段，按文档与合规要求设置。

### 2）Gemini 系列图像 · `generateContent`（v1beta）

- **典型模型 ID（示例）**：`gemini-3-pro-image-preview`、`gemini-3.1-flash-image-preview`（与 `GET v1beta/models` 的 `baseModelId` 对齐；亦可能出现 `publishers/google/models/gemini-3-pro-image-preview` 等长名，以接口为准）。
- **端点形态（示例）**：`POST https://api.modelverse.cn/v1beta/models/<model-id>:generateContent`
- **请求头**：文档若要求使用 **`x-goog-api-key`** 传递密钥，则与上一种 `Authorization` 方式区分，**不得混用**；以官方示例为准。
- **请求体要点**：`contents` 承载用户文本；`generationConfig` 内配置 **`responseModalities`**（如含 `IMAGE`）、**`imageConfig`**（如 **`aspectRatio`**、**`imageSize`** 等）。常见 **1K** 配图可在 `imageSize` 中使用 **`1K`**，具体以文档为准。
- **响应**：从 `candidates[].content.parts[]` 中解析 **`inlineData`**（base64）与 `mimeType`，再写入二进制文件。

## 模型与尺寸（摘要）

| 类型 | 说明 |
|------|------|
| `gemini-3-pro-image-preview` | 宽高比多由 `imageConfig.aspectRatio` 表达；分辨率档见 `imageSize`（如 1K）。 |
| `gemini-3.1-flash-image-preview` | 同上（`generateContent`）；名称以 `v1beta/models` 为准。 |
| `doubao-seedream-4.5` | 尺寸常为具体像素串或文档给定别名；总像素区间以文档为准。 |

**尺寸与别名** 以 UCloud 当前文档为准；本技能内示例脚本若含别名表，仅为方便使用，**上线前请对照文档校验**。

## 本技能内参考脚本

- **路径**：[`scripts/generate_ucloud_image.py`](scripts/generate_ucloud_image.py)（仅 UCloud ModelVerse：`images/generations` 与 `v1beta` `generateContent`）。
- **依赖**：Python 3、`requests`。
- **密钥**：`UCLOUD_API_KEY` 或项目根 `.config/UCLOUD_API_KEY`。

```bash
python path/to/image-generation-ucloud/scripts/generate_ucloud_image.py --list-models
python path/to/image-generation-ucloud/scripts/generate_ucloud_image.py \
  --prompt prompt.txt --output out.png --size 4:3
python path/to/image-generation-ucloud/scripts/generate_ucloud_image.py \
  --prompt prompt.txt --output out.png --model gemini-3.1-flash-image-preview --size 16:9 --image-size 1K
```

OpenRouter 出图请使用 **`image-generation-openrouter`** 目录下脚本，勿与本脚本混用。

## 与总技能、OpenRouter 的关系

- 总览与工作流：**[image-generation](../image-generation/SKILL.md)**。
- 若 UCloud 不可用或需使用 OpenRouter 路由的 Gemini 图像能力：**[image-generation-openrouter](../image-generation-openrouter/SKILL.md)**。

## 不做什么

- 不绑定某一私有仓库目录或内部文件名（如「某营销目录下的唯一规范」）；公开读者应能在自己的项目中复现「密钥 + 端点 + 请求体」。
