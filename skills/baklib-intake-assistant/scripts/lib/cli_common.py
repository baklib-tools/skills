"""Shared CLI helpers: paths from env/flags (aligned with skill reference.md)."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


def default_db_path() -> Path:
    raw = os.environ.get("BAKLIB_SYNC_INDEX_PATH") or os.environ.get("SYNC_INDEX_PATH")
    if raw:
        return Path(raw).expanduser()
    return Path(".baklib/sync-state.sqlite")


def default_mirror_root() -> Path:
    raw = os.environ.get("BAKLIB_MIRROR_ROOT")
    if raw:
        return Path(raw).expanduser()
    return Path("baklib-mirror")


def default_manifest_path() -> Path:
    raw = os.environ.get("BAKLIB_SYNC_MANIFEST_PATH")
    if raw:
        return Path(raw).expanduser()
    return Path(".baklib/last-sync-manifest.json")


def add_db_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--db",
        type=Path,
        default=None,
        help="SQLite ledger path (default: env BAKLIB_SYNC_INDEX_PATH or .baklib/sync-state.sqlite)",
    )


def add_mirror_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--mirror-root",
        type=Path,
        default=None,
        help="Mirror root with 知识库/, 资源库/, 站点/ (env BAKLIB_MIRROR_ROOT or ./baklib-mirror)",
    )


def resolve_db_path(args: argparse.Namespace) -> Path:
    return (args.db or default_db_path()).resolve()


def resolve_mirror_root(args: argparse.Namespace) -> Path:
    return (args.mirror_root or default_mirror_root()).resolve()
