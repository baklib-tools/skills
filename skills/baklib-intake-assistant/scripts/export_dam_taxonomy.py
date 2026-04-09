#!/usr/bin/env python3
"""Export dam_collections + dam_tags from SQLite to YAML (collections / tags lists)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from lib.cli_common import add_db_argument, resolve_db_path
from lib.db import connect


def _yaml_escape(s: str) -> str:
    if any(c in s for c in ('"', "'", ":", "\n", "\\")) or s.strip() != s:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_db_argument(parser)
    parser.add_argument("-o", "--out", type=Path, help="Output file (default: stdout)")
    args = parser.parse_args()
    db_path = resolve_db_path(args)

    conn = connect(db_path)
    try:
        collections = [
            r["name"]
            for r in conn.execute("SELECT name FROM dam_collections ORDER BY name COLLATE NOCASE")
        ]
        tags = [r["name"] for r in conn.execute("SELECT name FROM dam_tags ORDER BY name COLLATE NOCASE")]
    finally:
        conn.close()

    lines = ["# Exported from Baklib sync ledger (dam_collections / dam_tags)", "collections:"]
    for c in collections:
        lines.append(f"  - {_yaml_escape(c)}")
    lines.append("tags:")
    for t in tags:
        lines.append(f"  - {_yaml_escape(t)}")
    text = "\n".join(lines) + "\n"

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
