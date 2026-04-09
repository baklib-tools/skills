#!/usr/bin/env python3
"""
Compare remote index (fixture or future API) with SQLite fingerprints; write manifest JSON only.

Without --from-fixture, exits with code 3 (remote fetch not implemented in this bundle).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from lib.cli_common import BaklibPathsError, ledger_db_path, manifest_path
from lib.db import connect


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sample(items: list[Any], n: int = 20) -> list[Any]:
    return items[:n]


def plan_kb(conn, remote_list: list[dict[str, Any]]) -> tuple[dict[str, int], dict[str, list]]:
    local = {
        (r["space_id"], r["article_id"]): (r["fingerprint"] or "")
        for r in conn.execute("SELECT space_id, article_id, fingerprint FROM kb_articles")
    }
    remote_map = {}
    for item in remote_list:
        sid = item.get("space_id") or ""
        aid = item.get("article_id") or ""
        fp = item.get("fingerprint") or ""
        if not sid or not aid:
            continue
        remote_map[(sid, aid)] = fp

    create_keys = [k for k in remote_map if k not in local]
    update_keys = [k for k in remote_map if k in local and local[k] != remote_map[k]]
    delete_keys = [k for k in local if k not in remote_map]

    summary = {
        "kb_create": len(create_keys),
        "kb_update": len(update_keys),
        "kb_delete": len(delete_keys),
    }
    samples = {
        "kb_create": [{"space_id": k[0], "article_id": k[1]} for k in _sample(create_keys)],
        "kb_update": [{"space_id": k[0], "article_id": k[1]} for k in _sample(update_keys)],
        "kb_delete": [{"space_id": k[0], "article_id": k[1]} for k in _sample(delete_keys)],
    }
    return summary, samples


def plan_dam(conn, remote_list: list[dict[str, Any]]) -> tuple[dict[str, int], dict[str, list]]:
    local = {
        r["entity_id"]: (r["fingerprint"] or "")
        for r in conn.execute("SELECT entity_id, fingerprint FROM dam_entities")
    }
    remote_map = {}
    for item in remote_list:
        eid = item.get("entity_id") or ""
        if not eid:
            continue
        remote_map[eid] = item.get("fingerprint") or ""

    create_ids = [k for k in remote_map if k not in local]
    update_ids = [k for k in remote_map if k in local and local[k] != remote_map[k]]
    delete_ids = [k for k in local if k not in remote_map]

    summary = {
        "dam_create": len(create_ids),
        "dam_update": len(update_ids),
        "dam_delete": len(delete_ids),
    }
    samples = {
        "dam_create": [{"entity_id": k} for k in _sample(create_ids)],
        "dam_update": [{"entity_id": k} for k in _sample(update_ids)],
        "dam_delete": [{"entity_id": k} for k in _sample(delete_ids)],
    }
    return summary, samples


def plan_site(conn, remote_list: list[dict[str, Any]]) -> tuple[dict[str, int], dict[str, list]]:
    local = {
        (r["site_id"], r["page_id"]): (r["fingerprint"] or "")
        for r in conn.execute("SELECT site_id, page_id, fingerprint FROM site_pages")
    }
    remote_map = {}
    for item in remote_list:
        sid = item.get("site_id") or ""
        pid = item.get("page_id") or ""
        if not sid or not pid:
            continue
        remote_map[(sid, pid)] = item.get("fingerprint") or ""

    create_keys = [k for k in remote_map if k not in local]
    update_keys = [k for k in remote_map if k in local and local[k] != remote_map[k]]
    delete_keys = [k for k in local if k not in remote_map]

    summary = {
        "site_create": len(create_keys),
        "site_update": len(update_keys),
        "site_delete": len(delete_keys),
    }
    samples = {
        "site_create": [{"site_id": k[0], "page_id": k[1]} for k in _sample(create_keys)],
        "site_update": [{"site_id": k[0], "page_id": k[1]} for k in _sample(update_keys)],
        "site_delete": [{"site_id": k[0], "page_id": k[1]} for k in _sample(delete_keys)],
    }
    return summary, samples


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from-fixture",
        type=Path,
        help="JSON file with kb_articles, dam_entities, site_pages arrays",
    )
    args = parser.parse_args()

    if not args.from_fixture:
        print(
            "Remote fetch is not implemented in this bundle. Pass --from-fixture path.json "
            "or implement fetch_remote_* in your project.",
            file=sys.stderr,
        )
        return 3

    raw = json.loads(args.from_fixture.read_text(encoding="utf-8"))
    kb_remote = raw.get("kb_articles") or []
    dam_remote = raw.get("dam_entities") or []
    site_remote = raw.get("site_pages") or []

    try:
        db_path = ledger_db_path()
        out = manifest_path()
    except BaklibPathsError as e:
        print(str(e), file=sys.stderr)
        return 4

    conn = connect(db_path)
    try:
        s1, z1 = plan_kb(conn, kb_remote)
        s2, z2 = plan_dam(conn, dam_remote)
        s3, z3 = plan_site(conn, site_remote)
    finally:
        conn.close()

    summary = {**s1, **s2, **s3}
    samples = {**z1, **z2, **z3}
    manifest = {
        "generated_at": _utc_now_iso(),
        "source": "fixture",
        "fixture_path": str(args.from_fixture.resolve()),
        "db_path": str(db_path.resolve()),
        "dry_run": True,
        "summary": summary,
        "samples": samples,
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote manifest: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
