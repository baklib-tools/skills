"""Resolve fixed paths: walk upward from cwd to find `.baklib/` under the skill project."""

from __future__ import annotations

from pathlib import Path

# Fixed filenames inside the discovered `.baklib` directory
LEDGER_DB_NAME = "sync-state.sqlite"
MANIFEST_NAME = "last-sync-manifest.json"
# Mirror tree lives next to `.baklib` (same project root)
MIRROR_DIR_NAME = "baklib-mirror"


class BaklibPathsError(FileNotFoundError):
    """Raised when no `.baklib` directory is found walking up from the start path."""


def find_baklib_dir(start: Path | None = None) -> Path:
    """
    Walk upward from `start` (default: cwd) including start and all parents.
    Return the first path `.../.baklib` that exists as a directory.
    """
    cur = (start or Path.cwd()).resolve()
    for d in [cur, *cur.parents]:
        candidate = d / ".baklib"
        if candidate.is_dir():
            return candidate
    raise BaklibPathsError(
        "未找到 `.baklib/` 目录：请从技能项目内运行脚本，并在项目根（或上级包含该根的目录）"
        "创建 `.baklib` 文件夹后再执行。例如：mkdir -p .baklib"
    )


def ledger_db_path(start: Path | None = None) -> Path:
    """`<project>/.baklib/sync-state.sqlite`"""
    return find_baklib_dir(start) / LEDGER_DB_NAME


def manifest_path(start: Path | None = None) -> Path:
    """`<project>/.baklib/last-sync-manifest.json`"""
    return find_baklib_dir(start) / MANIFEST_NAME


def mirror_root_path(start: Path | None = None) -> Path:
    """`<project>/baklib-mirror` — 与 `.baklib` 同级，内含 知识库/、资源库/、站点/`"""
    return find_baklib_dir(start).parent / MIRROR_DIR_NAME
