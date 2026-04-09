"""
Placeholder for Baklib Open API remote index fetch.

Implement fetch_remote_index() in your deployment to return the same shape as
fixtures/example-remote-index.json (kb_articles, dam_entities, site_pages arrays).
"""

from __future__ import annotations

from typing import Any


def fetch_remote_index() -> dict[str, Any]:
    raise NotImplementedError(
        "Wire Baklib Open API here, or use plan_sync.py --from-fixture for dry runs."
    )
