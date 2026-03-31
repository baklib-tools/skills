#!/usr/bin/env python3
"""
OpenRouter 图像生成（参考实现）

仅处理 OpenRouter 的 chat/completions + modalities 等协议；模型 ID、字段以 OpenRouter 文档为准。
依赖：requests。

密钥（读取顺序）：优先项目根 .config/OPENROUTER_API_KEY，其次环境变量 OPENROUTER_API_KEY。
可选环境变量：OPENROUTER_HTTP_REFERER、OPENROUTER_HTTP_TITLE（请求头展示用）
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path

import requests


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


def get_openrouter_api_key() -> str | None:
    return get_api_key("OPENROUTER_API_KEY", "OPENROUTER_API_KEY")


SIZE_ALIASES = {
    "4:3": "1024x768",
    "3:4": "768x1024",
    "16:9": "1024x576",
    "9:16": "576x1024",
    "1:1": "1024x1024",
    "2k": "2048x2048",
    "4k": "4096x4096",
}

DEFAULT_MODEL = "google/gemini-3-pro-image-preview"


def print_openrouter_key_help() -> None:
    print("", file=sys.stderr)
    print("📌 未检测到 OpenRouter API 密钥，请任选其一：", file=sys.stderr)
    print(
        "   • 优先：在项目根目录创建 .config/OPENROUTER_API_KEY（单行密钥，UTF-8）",
        file=sys.stderr,
    )
    print(
        "   • 备选：环境变量 OPENROUTER_API_KEY",
        file=sys.stderr,
    )
    print("   • 密钥获取：https://openrouter.ai/keys", file=sys.stderr)
    print("   技能说明：image-generation-openrouter（本仓库 skills/ 下）", file=sys.stderr)


def generate_image(
    prompt: str,
    output_file: str,
    model: str,
    size: str | None = None,
) -> bool:
    api_key = get_openrouter_api_key()
    if not api_key:
        print("❌ 错误: 未找到 OpenRouter API 密钥", file=sys.stderr)
        print_openrouter_key_help()
        return False

    api_size = SIZE_ALIASES.get(size, size) if size else "1024x1024"
    if size and size in SIZE_ALIASES:
        print(f"   尺寸别名 {size!r} → {api_size}", file=sys.stderr)

    size_prompt = f"Generate an image with aspect ratio {api_size}. {prompt}"

    referer = os.getenv("OPENROUTER_HTTP_REFERER", "https://example.com")
    title = os.getenv("OPENROUTER_HTTP_TITLE", "Image Generation")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": referer,
        "X-Title": title,
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": size_prompt}]}
        ],
        "modalities": ["image", "text"],
    }

    print("🎨 正在使用 OpenRouter 生成图像...", file=sys.stderr)
    print(f"   模型: {model}", file=sys.stderr)
    print(f"   提示词: {prompt}", file=sys.stderr)
    print(f"   尺寸: {api_size}", file=sys.stderr)

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=120)
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
        return False

    result = response.json()

    if "choices" not in result or not result["choices"]:
        print("❌ 错误: API 响应格式不正确，未找到 choices", file=sys.stderr)
        print(
            f"   响应: {json.dumps(result, indent=2, ensure_ascii=False)}",
            file=sys.stderr,
        )
        return False

    message = result["choices"][0].get("message", {})

    image_data = None
    mime_type = None

    images = message.get("images", [])
    if images and isinstance(images, list):
        for img in images:
            if isinstance(img, dict):
                image_url = img.get("image_url", {})
                if isinstance(image_url, dict):
                    fetched = image_url.get("url", "")
                    if fetched:
                        if fetched.startswith("data:"):
                            image_data = fetched
                            mime_type = "image/png"
                        else:
                            try:
                                img_response = requests.get(fetched, timeout=30)
                                if img_response.status_code == 200:
                                    output_path = Path(output_file)
                                    output_path.parent.mkdir(
                                        parents=True, exist_ok=True
                                    )
                                    output_path.write_bytes(img_response.content)
                                    print(
                                        f"✅ 图像已下载保存: {output_path}",
                                        file=sys.stderr,
                                    )
                                    return True
                            except OSError as e:
                                print(f"❌ 下载图像失败: {e}", file=sys.stderr)
                                return False
                        break

    if not image_data:
        content = message.get("content", [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "image":
                    image_data = item.get("data") or item.get("image_url", {}).get(
                        "url"
                    )
                    mime_type = item.get("mime_type", "image/png")
                    break
        elif isinstance(content, dict) and content.get("type") == "image":
            image_data = content.get("data") or content.get("image_url", {}).get("url")
            mime_type = content.get("mime_type", "image/png")

    if not image_data:
        print("❌ 错误: 响应中未找到图像数据", file=sys.stderr)
        print(
            f"   响应内容: {json.dumps(message, indent=2, ensure_ascii=False)}",
            file=sys.stderr,
        )
        return False

    try:
        if "," in str(image_data):
            image_data = str(image_data).split(",", 1)[1]

        image_bytes = base64.b64decode(image_data)
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(image_bytes)
        print(f"✅ 图像已保存: {output_path}", file=sys.stderr)
        print(f"   格式: {mime_type}", file=sys.stderr)
        return True
    except (OSError, ValueError) as e:
        print(f"❌ 保存图像失败: {e}", file=sys.stderr)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="OpenRouter 图像生成（chat/completions）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --prompt prompt.txt --output out.png --size 4:3
  %(prog)s --prompt prompt.txt --output out.png --model google/gemini-3-pro-image-preview --size 16:9
        """,
    )
    parser.add_argument("--prompt", required=True, help="提示词文件路径（UTF-8）")
    parser.add_argument("--output", required=True, help="输出图像路径")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"OpenRouter 模型 ID（默认 {DEFAULT_MODEL}）",
    )
    parser.add_argument(
        "--size",
        default=None,
        metavar="比例或别名",
        help="宽高比或 2k/4k 等（见脚本内别名表；以 OpenRouter/模型说明为准）",
    )

    args = parser.parse_args()

    if not get_openrouter_api_key():
        print("❌ 错误: 未找到 OpenRouter API 密钥", file=sys.stderr)
        print_openrouter_key_help()
        sys.exit(1)

    try:
        prompt = Path(args.prompt).read_text(encoding="utf-8")
    except OSError as e:
        print(f"❌ 无法读取提示词文件 {args.prompt}: {e}", file=sys.stderr)
        sys.exit(1)

    ok = generate_image(prompt, args.output, model=args.model, size=args.size)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
