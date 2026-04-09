#!/usr/bin/env python3
"""Pretty-print last sync manifest JSON (see plan_sync.py output)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from lib.cli_common import BaklibPathsError, manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__
        + " 路径固定为：自 cwd 向上找到的首个 `.baklib/last-sync-manifest.json`。"
    )
    args = parser.parse_args()

    try:
        path = manifest_path()
    except BaklibPathsError as e:
        print(str(e), file=sys.stderr)
        return 4

    if not path.is_file():
        print(f"manifest not found: {path}", file=sys.stderr)
        return 2

    data = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
