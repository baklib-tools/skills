#!/usr/bin/env python3
"""
Validate mirror layout (知识库/, 资源库/, 站点/) and optional path consistency
between SQLite relative_path rows and files on disk.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from lib.cli_common import BaklibPathsError, ledger_db_path, mirror_root_path
from lib.db import connect

TOP_DIRS = ("知识库", "资源库", "站点")


def _check_paths(conn, mirror: Path, scope: str) -> tuple[list[str], list[str]]:
    """Return (missing, extra_warnings)."""
    missing: list[str] = []
    warnings: list[str] = []

    queries: list[tuple[str, str]] = []
    if scope in ("all", "kb"):
        queries.append(("kb_articles", "SELECT relative_path FROM kb_articles"))
    if scope in ("all", "dam"):
        queries.append(("dam_entities", "SELECT relative_path FROM dam_entities"))
    if scope in ("all", "site"):
        queries.append(("site_pages", "SELECT relative_path FROM site_pages"))

    seen_on_disk: set[Path] = set()
    for label, sql in queries:
        for row in conn.execute(sql):
            rel = (row["relative_path"] or "").strip()
            if not rel:
                warnings.append(f"{label}: empty relative_path row")
                continue
            full = (mirror / rel).resolve()
            try:
                full.relative_to(mirror.resolve())
            except ValueError:
                warnings.append(f"{label}: path escapes mirror root: {rel}")
                continue
            seen_on_disk.add(full)
            if not full.exists():
                missing.append(f"{label}: missing file {rel}")

    return missing, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scope",
        choices=("all", "kb", "dam", "site", "none"),
        default="all",
        help="Which tables to check against disk (default: all)",
    )
    parser.add_argument(
        "--skip-path-check",
        action="store_true",
        help="Only verify top-level 知识库/资源库/站点 directories exist",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    try:
        db_path = ledger_db_path()
        mirror = mirror_root_path()
    except BaklibPathsError as e:
        print(str(e), file=sys.stderr)
        return 4

    top_ok = {name: (mirror / name).is_dir() for name in TOP_DIRS}
    all_top_exist = all(top_ok.values())

    missing_files: list[str] = []
    path_warnings: list[str] = []

    if not args.skip_path_check and args.scope != "none":
        conn = connect(db_path)
        try:
            missing_files, path_warnings = _check_paths(conn, mirror, args.scope)
        finally:
            conn.close()

    payload = {
        "mirror_root": str(mirror),
        "top_level_dirs": top_ok,
        "top_level_ok": all_top_exist,
        "missing_files": missing_files,
        "path_warnings": path_warnings,
    }

    ok = all_top_exist and not missing_files

    if args.json:
        payload["ok"] = ok
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"mirror_root: {mirror}")
        for name in TOP_DIRS:
            status = "ok" if top_ok[name] else "MISSING"
            print(f"  {name}/ : {status}")
        if not args.skip_path_check and args.scope != "none":
            print("path_check:")
            if missing_files:
                for m in missing_files:
                    print(f"  MISSING {m}")
            else:
                print("  (no missing files)")
            for w in path_warnings:
                print(f"  WARN {w}")
        print(f"overall: {'OK' if ok else 'FAIL'}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
