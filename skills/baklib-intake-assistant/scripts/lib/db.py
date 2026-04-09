"""
SQLite schema for Baklib mirror sync ledger (see ../local-mirror.md §2.5).

Migrations are driven by PRAGMA user_version. Call ensure_schema(conn) after connect.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Union

SCHEMA_VERSION = 1

PathLike = Union[str, Path]


def connect(db_path: PathLike) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    ensure_schema(conn)
    return conn


def ensure_schema(conn: sqlite3.Connection) -> None:
    cur = conn.execute("PRAGMA user_version")
    version = int(cur.fetchone()[0])
    while version < SCHEMA_VERSION:
        version += 1
        _MIGRATIONS[version](conn)
        conn.execute(f"PRAGMA user_version = {version}")
    conn.commit()


def _migrate_1(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS kb_articles (
            space_id TEXT NOT NULL,
            article_id TEXT NOT NULL,
            fingerprint TEXT,
            relative_path TEXT NOT NULL,
            last_synced_at TEXT,
            PRIMARY KEY (space_id, article_id)
        );

        CREATE INDEX IF NOT EXISTS idx_kb_articles_path ON kb_articles(relative_path);

        CREATE TABLE IF NOT EXISTS dam_entities (
            entity_id TEXT PRIMARY KEY,
            collection_name TEXT,
            relative_path TEXT NOT NULL,
            fingerprint TEXT,
            last_synced_at TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_dam_entities_path ON dam_entities(relative_path);

        CREATE TABLE IF NOT EXISTS dam_collections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            remote_id TEXT,
            name TEXT NOT NULL UNIQUE,
            folder_path TEXT
        );

        CREATE TABLE IF NOT EXISTS dam_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            remote_id TEXT,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS dam_entity_tags (
            entity_id TEXT NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (entity_id, tag_id),
            FOREIGN KEY (tag_id) REFERENCES dam_tags(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_dam_entity_tags_entity ON dam_entity_tags(entity_id);

        CREATE TABLE IF NOT EXISTS site_pages (
            site_id TEXT NOT NULL,
            page_id TEXT NOT NULL,
            fingerprint TEXT,
            relative_path TEXT NOT NULL,
            last_synced_at TEXT,
            PRIMARY KEY (site_id, page_id)
        );

        CREATE INDEX IF NOT EXISTS idx_site_pages_path ON site_pages(relative_path);

        CREATE TABLE IF NOT EXISTS sync_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TEXT NOT NULL,
            finished_at TEXT,
            stats_json TEXT,
            exit_code INTEGER,
            notes TEXT
        );
        """
    )


_MIGRATIONS: dict[int, callable] = {
    1: _migrate_1,
}
