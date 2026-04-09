#!/usr/bin/env python3
"""Insert one row into sync_runs (for sync jobs or wrappers)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from lib.cli_common import BaklibPathsError, ledger_db_path
from lib.db import connect


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--started-at", help="ISO8601 (default: now UTC)")
    parser.add_argument("--finished-at", help="ISO8601 (optional)")
    parser.add_argument("--stats-json", help='JSON object string, e.g. \'{"kb_update":3}\'')
    parser.add_argument("--stats-file", type=Path, help="JSON file for stats object")
    parser.add_argument("--exit-code", type=int, default=0)
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    stats = None
    if args.stats_file:
        stats = json.loads(args.stats_file.read_text(encoding="utf-8"))
    elif args.stats_json:
        stats = json.loads(args.stats_json)

    started = args.started_at or _utc_now_iso()
    stats_s = json.dumps(stats, ensure_ascii=False) if stats is not None else None

    try:
        db_path = ledger_db_path()
    except BaklibPathsError as e:
        print(str(e), file=sys.stderr)
        return 4

    conn = connect(db_path)
    try:
        cur = conn.execute(
            "INSERT INTO sync_runs (started_at, finished_at, stats_json, exit_code, notes) "
            "VALUES (?, ?, ?, ?, ?)",
            (started, args.finished_at, stats_s, args.exit_code, args.notes),
        )
        conn.commit()
        rid = cur.lastrowid
    finally:
        conn.close()

    print(rid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
