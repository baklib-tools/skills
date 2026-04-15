#!/usr/bin/env python3
"""
UCloud ModelVerse 图像生成（参考实现）

仅处理 UCloud 文档中的模型与参数；模型 ID、尺寸别名以 UCloud 当前文档为准。
依赖：requests。将本技能目录安装到项目的技能路径（以所用工具文档为准）后，在项目根执行。

密钥（读取顺序）：优先项目根 .config/UCLOUD_API_KEY，其次环境变量 UCLOUD_API_KEY。
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from typing import Literal, TypedDict

import requests

# 官方模型列表（无需密钥即可查询，用于核对 baseModelId）
UCLOUD_V1BETA_MODELS_URL = "https://api.modelverse.cn/v1beta/models"
UCLOUD_V1_MODELS_URL = "https://api.modelverse.cn/v1/models"


class _ModelImagesGenerations(TypedDict):
    kind: Literal["images_generations"]
    sizes: dict[str, str]


class _ModelGenerateContent(TypedDict):
    kind: Literal["generate_content"]
    sizes: None  # 无像素别名表；--size 直接作 aspectRatio


ModelConfig = _ModelImagesGenerations | _ModelGenerateContent

# 仅保留：豆包文生图（images/generations）+ Gemini 图像（generateContent）。
# Gemini 模型 ID 请与 GET v1beta/models 返回的 baseModelId 对齐（例如 Flash 图像为 gemini-3.1-flash-image-preview）。
UCLOUD_MODELS: dict[str, ModelConfig] = {
    "doubao-seedream-4.5": {
        "kind": "images_generations",
        "sizes": {
            "4:3": "2304x1728",
            "3:4": "1728x2304",
            "16:9": "2560x1440",
            "9:16": "1440x2560",
        },
    },
    "gemini-3-pro-image-preview": {
        "kind": "generate_content",
        "sizes": None,
    },
    "gemini-3.1-flash-image-preview": {
        "kind": "generate_content",
        "sizes": None,
    },
}

DEFAULT_MODEL = "gemini-3-pro-image-preview"


def find_project_root() -> Path:
    script = Path(__file__).resolve()
    home = Path.home()
    p = script.parent
    for _ in range(10):
        if (p / ".config").is_dir() and p != home:
            return p
        if p == p.parent:
            break
        p = p.parent
    for depth in (4, 3):
        if len(script.parents) > depth:
            return script.parents[depth]
    return script.parents[-1]


def get_api_key(env_name: str, config_filename: str) -> str | None:
    project_root = find_project_root()
    config_file = project_root / ".config" / config_filename
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                key = f.read().strip()
                if key:
                    return key
        except OSError as e:
            print(f"⚠️  读取配置文件失败: {e}", file=sys.stderr)
    api_key = os.getenv(env_name)
    if api_key:
        return api_key.strip()
    return None


def get_ucloud_api_key() -> str | None:
    return get_api_key("UCLOUD_API_KEY", "UCLOUD_API_KEY")


def print_ucloud_api_key_help() -> None:
    print("", file=sys.stderr)
    print("📌 未检测到 UCloud API 密钥，请任选其一：", file=sys.stderr)
    print(
        "   • 优先：在项目根目录创建 .config/UCLOUD_API_KEY（单行密钥，UTF-8）",
        file=sys.stderr,
    )
    print(
        "   • 备选：环境变量 UCLOUD_API_KEY",
        file=sys.stderr,
    )
    print(
        "   • 换后端：OpenRouter 技能目录下脚本（image-generation-openrouter）",
        file=sys.stderr,
    )
    print(
        "   技能说明：image-generation-ucloud（本仓库 skills/ 下）",
        file=sys.stderr,
    )


def resolve_canonical_model_id(user_arg: str) -> str | None:
    """将 CLI 传入的模型名解析为 UCLOUD_MODELS 的键（兼容旧名与 API 长 ID）。"""
    u = user_arg.strip()
    if u in UCLOUD_MODELS:
        return u
    if "doubao-seedream" in u:
        return "doubao-seedream-4.5"
    # API 长名 -> 本脚本使用的短名
    if u == "publishers/google/models/gemini-3-pro-image-preview":
        return "gemini-3-pro-image-preview"
    # 含 gemini-3.1-flash-image 即视为 Flash 图像（含 -preview 与旧名无后缀）
    if "gemini-3.1-flash-image" in u:
        return "gemini-3.1-flash-image-preview"
    if "gemini-3-pro-image" in u:
        return "gemini-3-pro-image-preview"
    return None


def fetch_v1beta_models() -> list[dict[str, object]]:
    r = requests.get(UCLOUD_V1BETA_MODELS_URL, timeout=30)
    r.raise_for_status()
    data = r.json()
    return list(data.get("models") or [])


def print_official_model_lists() -> None:
    """打印官方 API 返回的模型 ID（走 stdout，便于重定向）。"""
    print("—— GET v1beta/models（Gemini 协议，含 generateContent，节选 id 含 image）——")
    try:
        models = fetch_v1beta_models()
    except requests.RequestException as e:
        print(f"❌ 请求失败: {e}", file=sys.stderr)
        return
    for m in models:
        bid = str(m.get("baseModelId", ""))
        actions = m.get("supportedActions") or []
        if "generateContent" not in actions:
            continue
        if "image" not in bid.lower():
            continue
        print(f"  {bid}")

    print()
    print("—— GET v1/models（OpenAI 兼容列表，节选 id 含 image）——")
    try:
        r = requests.get(UCLOUD_V1_MODELS_URL, timeout=30)
        r.raise_for_status()
        data = r.json()
        for row in data.get("data") or []:
            mid = str(row.get("id", ""))
            if "image" in mid.lower():
                print(f"  {mid}")
    except requests.RequestException as e:
        print(f"❌ v1/models 请求失败: {e}", file=sys.stderr)

    print()
    print(
        "本脚本内置文生图模型（见 UCLOUD_MODELS）："
        f" {', '.join(UCLOUD_MODELS)}。"
        " 豆包走 v1/images/generations，通常不在 v1beta 列表中，以 UCloud 图像 API 文档为准。"
    )


def resolve_api_size(sizes: dict[str, str] | None, size: str | None) -> str | None:
    """根据该模型的别名表解析 --size；无表则原样返回（或 None）。"""
    if not size:
        return None
    if sizes is None:
        return size
    resolved = sizes.get(size, size)
    if size in sizes:
        print(f"   尺寸别名 {size!r} → {resolved}", file=sys.stderr)
    return resolved


def _save_image_from_response(image_data: dict, output_path: Path) -> bool:
    if "url" in image_data:
        img_response = requests.get(image_data["url"], timeout=30)
        if img_response.status_code != 200:
            print(f"❌ 下载图像失败: HTTP {img_response.status_code}", file=sys.stderr)
            return False
        output_path.write_bytes(img_response.content)
        print(f"✅ 图像已保存: {output_path}", file=sys.stderr)
        return True
    if "b64_json" in image_data:
        image_bytes = base64.b64decode(image_data["b64_json"])
        output_path.write_bytes(image_bytes)
        print(f"✅ 图像已保存: {output_path}", file=sys.stderr)
        return True
    print("❌ 错误: 响应中未找到图像数据", file=sys.stderr)
    return False


def _request_images_generations(
    api_key: str,
    payload: dict,
    output_file: str,
    model_id: str,
    prompt: str,
    size_hint: str | None = None,
) -> bool:
    url = "https://api.modelverse.cn/v1/images/generations"
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    print("🎨 正在生成图像...", file=sys.stderr)
    print(f"   模型: {model_id}", file=sys.stderr)
    print(f"   提示词: {prompt}", file=sys.stderr)
    if size_hint:
        print(f"   尺寸: {size_hint}", file=sys.stderr)
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}", file=sys.stderr)
        return False
    if response.status_code != 200:
        print(f"❌ API 请求失败: HTTP {response.status_code}", file=sys.stderr)
        print(f"   响应: {response.text}", file=sys.stderr)
        print_ucloud_api_key_help()
        return False
    result = response.json()
    if "data" not in result or not result["data"]:
        print("❌ 错误: API 响应格式不正确", file=sys.stderr)
        print(f"   响应: {result}", file=sys.stderr)
        return False
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return _save_image_from_response(result["data"][0], output_path)


def generate_via_images_generations(
    model_id: str,
    prompt: str,
    output_file: str,
    size: str | None = None,
    n: int = 1,
    image_url: str | None = None,
) -> bool:
    cfg = UCLOUD_MODELS.get(model_id)
    if not cfg or cfg["kind"] != "images_generations":
        return False
    sizes = cfg["sizes"]
    api_key = get_ucloud_api_key()
    if not api_key:
        print("❌ 错误: 未找到 UCloud API 密钥", file=sys.stderr)
        print_ucloud_api_key_help()
        return False
    api_size = resolve_api_size(sizes, size)
    payload = {
        "model": model_id,
        "prompt": prompt,
        "n": n,
        "watermark": False,
    }
    if api_size:
        payload["size"] = api_size
    if image_url:
        payload["image"] = image_url
    return _request_images_generations(
        api_key, payload, output_file, model_id, prompt, api_size
    )


def generate_gemini_generate_content(
    prompt: str,
    output_file: str,
    model_id: str,
    size: str | None = None,
    image_size: str = "1K",
) -> bool:
    """v1beta generateContent，适用于文档中的 Gemini 图像模型 ID。"""
    api_key = get_ucloud_api_key()
    if not api_key:
        print("❌ 错误: 未找到 UCloud API 密钥", file=sys.stderr)
        print_ucloud_api_key_help()
        return False

    aspect_ratio = "4:3"
    if size:
        aspect_ratio = size

    url = f"https://api.modelverse.cn/v1beta/models/{model_id}:generateContent"
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": image_size,
            },
        },
    }

    label = "Gemini 图像"
    if "flash" in model_id.lower():
        label = "Gemini 3.1 Flash Image"
    elif "pro-image" in model_id.lower():
        label = "Gemini 3 Pro Image"

    print(f"🎨 正在使用 UCloud {label} 生成图像...", file=sys.stderr)
    print(f"   模型: {model_id}", file=sys.stderr)
    print(f"   提示词: {prompt}", file=sys.stderr)
    print(f"   宽高比: {aspect_ratio}, 分辨率: {image_size}", file=sys.stderr)

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=300)
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}", file=sys.stderr)
        return False

    if response.status_code != 200:
        print(f"❌ API 请求失败: HTTP {response.status_code}", file=sys.stderr)
        try:
            error_data = response.json()
            print(
                f"   错误详情: {json.dumps(error_data, indent=2, ensure_ascii=False)}",
                file=sys.stderr,
            )
        except Exception:
            print(f"   响应: {response.text}", file=sys.stderr)
        print_ucloud_api_key_help()
        return False

    result = response.json()
    candidates = result.get("candidates") or []
    if not candidates:
        print("❌ 错误: 响应中未找到 candidates", file=sys.stderr)
        print(
            f"   响应: {json.dumps(result, indent=2, ensure_ascii=False)}",
            file=sys.stderr,
        )
        return False

    content = candidates[0].get("content") or {}
    parts = content.get("parts") or []

    inline_data = None
    mime_type = "image/png"
    for part in parts:
        if not isinstance(part, dict):
            continue
        data_block = part.get("inlineData")
        if isinstance(data_block, dict) and "data" in data_block:
            inline_data = data_block["data"]
            mime_type = data_block.get("mimeType", mime_type)
            break

    if not inline_data:
        print("❌ 错误: 响应中未找到 inlineData 图像数据", file=sys.stderr)
        print(
            f"   响应: {json.dumps(result, indent=2, ensure_ascii=False)}",
            file=sys.stderr,
        )
        return False

    try:
        image_bytes = base64.b64decode(inline_data)
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(image_bytes)
        print(f"✅ 图像已保存: {output_path}", file=sys.stderr)
        print(f"   格式: {mime_type}", file=sys.stderr)
        return True
    except OSError as e:
        print(f"❌ 保存图像失败: {e}", file=sys.stderr)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="UCloud ModelVerse 图像生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --list-models
  %(prog)s --prompt prompt.txt --output out.png --size 4:3
  %(prog)s --prompt prompt.txt --output out.png --model gemini-3.1-flash-image-preview --size 16:9
  %(prog)s --prompt prompt.txt --output out.jpg --model doubao-seedream-4.5 --size 4:3
        """,
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="调用 GET v1beta/models 与 GET v1/models，列出官方返回的图像相关模型 ID（无需密钥）",
    )
    parser.add_argument("--prompt", help="提示词文件路径（UTF-8）")
    parser.add_argument("--output", help="输出图像路径")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=(
            f"模型 ID。默认 {DEFAULT_MODEL}；"
            "可选 gemini-3.1-flash-image-preview、doubao-seedream-4.5；"
            "与官方不一致时请运行 --list-models 核对"
        ),
    )
    parser.add_argument(
        "--size",
        default=None,
        metavar="比例或像素",
        help="宽高比（如 4:3）或文档要求的像素串；Gemini 类为 aspectRatio",
    )
    parser.add_argument(
        "--image-size",
        default="1K",
        metavar="1K|2K|…",
        help="仅 Gemini generateContent：generationConfig.imageConfig.imageSize（默认 1K）",
    )

    args = parser.parse_args()

    if args.list_models:
        print_official_model_lists()
        sys.exit(0)

    if not args.prompt or not args.output:
        parser.error("请提供 --prompt 与 --output，或使用 --list-models")

    if not get_ucloud_api_key():
        print("❌ 错误: 未找到 UCloud API 密钥", file=sys.stderr)
        print_ucloud_api_key_help()
        sys.exit(1)

    try:
        prompt = Path(args.prompt).read_text(encoding="utf-8")
    except OSError as e:
        print(f"❌ 无法读取提示词文件 {args.prompt}: {e}", file=sys.stderr)
        sys.exit(1)

    mid = resolve_canonical_model_id(args.model)
    if not mid:
        print(
            f"❌ 不支持的模型: {args.model}。内置：{', '.join(UCLOUD_MODELS)}",
            file=sys.stderr,
        )
        sys.exit(1)

    cfg = UCLOUD_MODELS[mid]
    if cfg["kind"] == "images_generations":
        ok = generate_via_images_generations(
            mid, prompt, args.output, size=args.size, n=1
        )
    else:
        ok = generate_gemini_generate_content(
            prompt,
            args.output,
            mid,
            size=args.size,
            image_size=args.image_size,
        )

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
