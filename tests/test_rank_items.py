"""Regression tests for the plane-my-priority-queue ranking helper.

Loads ``skills/plane-my-priority-queue/scripts/rank_items.py`` by path (it is a
standalone stdlib script, not an importable package module) and pins the combined
priority + staleness scoring, ordering, multi-project envelope flattening, and
STALE flags.
"""

import importlib.util
from datetime import datetime, timezone
from pathlib import Path

_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plane_agent"
    / "skills"
    / "plane-my-priority-queue"
    / "scripts"
    / "rank_items.py"
)

_spec = importlib.util.spec_from_file_location("plane_rank_items", _SCRIPT)
rank_items = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rank_items)

NOW = datetime(2026, 7, 9, tzinfo=timezone.utc)


def _item(seq, priority, updated):
    return {"id": f"id{seq}", "sequence_id": seq, "name": f"item {seq}",
            "priority": priority, "updated_at": updated}


def test_ordering_and_scores():
    items = [
        _item(3, "urgent", "2026-07-07T00:00:00Z"),        # 2d fresh
        _item(1, "none", "2026-05-30T00:00:00Z"),          # 40d stale
        _item(12, "urgent", "2026-06-25T00:00:00.000000Z"),  # 14d stale
        _item(9, "high", "2026-06-19T00:00:00Z"),          # 20d stale
    ]
    ranked = rank_items.rank(items, NOW)
    assert [r["sequence_id"] for r in ranked] == [12, 3, 9, 1]
    scores = {r["sequence_id"]: r["score"] for r in ranked}
    assert scores[12] == 5 * 100 + 14 + 25   # 539
    assert scores[3] == 5 * 100 + 2           # 502
    assert scores[9] == 4 * 100 + 20 + 25     # 445
    assert scores[1] == 1 * 100 + 30 + 25     # 155 (none=1, staleness capped at 30)


def test_missing_priority_defaults_to_none_rank():
    row = rank_items.rank([{"id": "x", "sequence_id": 5, "name": "x",
                            "updated_at": "2026-07-08T00:00:00Z"}], NOW)[0]
    assert row["priority"] == "none"
    assert row["score"] == 1 * 100 + 1  # rank 1, 1 day, not stale


def test_stale_flag_boundary():
    seven = rank_items.rank([_item(1, "high", "2026-07-02T00:00:00Z")], NOW)[0]
    eight = rank_items.rank([_item(2, "high", "2026-07-01T00:00:00Z")], NOW)[0]
    assert seven["days_stale"] == 7 and seven["stale"] is False
    assert eight["days_stale"] == 8 and eight["stale"] is True


def test_extract_flattens_multiproject_envelopes():
    payload = [
        {"results": [_item(1, "high", "2026-07-08T00:00:00Z")], "next_cursor": "x"},
        {"results": [_item(2, "low", "2026-07-08T00:00:00Z")]},
    ]
    assert len(rank_items.extract_items(payload)) == 2
    assert len(rank_items.extract_items({"results": [_item(1, "high", "2026-07-08T00:00:00Z")]})) == 1
