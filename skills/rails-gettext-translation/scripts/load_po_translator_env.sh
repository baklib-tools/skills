#!/usr/bin/env bash
# 从工作区根目录 .config/ 读取密钥与端点，导出为 gpt-po-translator 常用环境变量。
# 约定：文件名与变量名一致、全大写（见本仓库 AGENTS.md「技能配置读取约定」）。
# 用法（在 Rails 项目根目录）：source /path/to/rails-gettext-translation/scripts/load_po_translator_env.sh
# 规则：若对应环境变量已存在且非空，则不覆盖（便于 CI/CD 注入）。

set -euo pipefail

if [[ -n "${BASH_SOURCE[0]:-}" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
elif [[ -n "${ZSH_VERSION:-}" ]]; then
  SCRIPT_DIR="$(cd "$(dirname "${(%):-%x}")" && pwd)"
else
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
fi

_find_repo_root() {
  local dir="$SCRIPT_DIR"
  while [[ "$dir" != "/" ]]; do
    if [[ -d "$dir/.git" ]]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  # 未找到 .git 时：假定脚本位于 <项目>/<若干层>/scripts/，向上三级作为兜底
  echo "$(cd "$SCRIPT_DIR/../../.." && pwd)"
}

REPO_ROOT="$(_find_repo_root)"
CFG="$REPO_ROOT/.config"

_export_if_empty() {
  local file="$1" env_name="$2"
  if eval "[[ -n \"\${$env_name:-}\" ]]"; then
    return 0
  fi
  if [[ ! -f "$file" ]]; then
    return 0
  fi
  local val
  val="$(tr -d '\r' < "$file" | head -n 1)"
  if [[ -z "$val" || "$val" =~ ^[[:space:]]*# ]]; then
    return 0
  fi
  export "$env_name=$val"
}

_export_if_empty "$CFG/OPENAI_API_KEY" OPENAI_API_KEY
_export_if_empty "$CFG/OPENAI_BASE_URL" OPENAI_BASE_URL
if [[ -z "${OPENAI_COMPATIBLE_BASE_URL:-}" && -n "${OPENAI_BASE_URL:-}" ]]; then
  export OPENAI_COMPATIBLE_BASE_URL="$OPENAI_BASE_URL"
fi
_export_if_empty "$CFG/OPENAI_COMPATIBLE_API_KEY" OPENAI_COMPATIBLE_API_KEY
_export_if_empty "$CFG/ANTHROPIC_API_KEY" ANTHROPIC_API_KEY
_export_if_empty "$CFG/AZURE_OPENAI_ENDPOINT" AZURE_OPENAI_ENDPOINT
_export_if_empty "$CFG/AZURE_OPENAI_API_KEY" AZURE_OPENAI_API_KEY
