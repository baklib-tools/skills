#!/usr/bin/env python3
"""Print SQLite ledger overview (row counts, last sync_run, DB mtime)."""

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
from lib.db import SCHEMA_VERSION, connect

TABLES = (
    "kb_articles",
    "dam_entities",
    "dam_collections",
    "dam_tags",
    "dam_entity_tags",
    "site_pages",
    "sync_runs",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()
    try:
        db_path = ledger_db_path()
    except BaklibPathsError as e:
        print(str(e), file=sys.stderr)
        return 4

    conn = connect(db_path)
    try:
        counts = {}
        for t in TABLES:
            row = conn.execute(f"SELECT COUNT(*) AS c FROM {t}").fetchone()
            counts[t] = int(row["c"])

        last_run = conn.execute(
            "SELECT id, started_at, finished_at, exit_code, stats_json, notes "
            "FROM sync_runs ORDER BY id DESC LIMIT 1"
        ).fetchone()
    finally:
        conn.close()

    db_stat = db_path.stat() if db_path.exists() else None
    payload = {
        "schema_version": SCHEMA_VERSION,
        "db_path": str(db_path),
        "db_mtime_iso": (
            datetime.fromtimestamp(db_stat.st_mtime, tz=timezone.utc).isoformat()
            if db_stat
            else None
        ),
        "counts": counts,
        "last_sync_run": ({k: last_run[k] for k in last_run.keys()} if last_run else None),
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"db_path:        {db_path}")
        print(f"schema_version: {SCHEMA_VERSION} (user_version in DB)")
        if db_stat:
            print(
                "db_mtime:       "
                f"{datetime.fromtimestamp(db_stat.st_mtime, tz=timezone.utc).isoformat()}"
            )
        print("row_counts:")
        for t, c in counts.items():
            print(f"  {t}: {c}")
        print("last_sync_run:")
        if last_run:
            for k in last_run.keys():
                print(f"  {k}: {last_run[k]}")
        else:
            print("  (none)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
