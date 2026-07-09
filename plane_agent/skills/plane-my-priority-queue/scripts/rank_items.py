#!/usr/bin/env python3
"""Rank Plane work items by a combined priority + staleness score.

Reads the JSON produced by the ``plane_work_items`` ``list_work_items`` action —
a raw cursor envelope ``{"results": [...]}``, a bare list, or a list you have
concatenated across several projects — from a file argument or stdin, and prints a
single list sorted highest-first by::

    score = priority_rank * 100 + min(days_stale, 30) + (25 if days_stale > 7 else 0)

Priority dominates; staleness breaks ties and boosts anything untouched for more
than 7 days (flagged ``STALE``). Stdlib only — no third-party dependencies.

Usage::

    plane_work_items list_work_items ... > items.json
    python rank_items.py items.json            # human table
    python rank_items.py --json items.json     # ranked JSON list
    cat items.json | python rank_items.py      # stdin
    python rank_items.py --now 2026-07-09T00:00:00Z items.json   # deterministic
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

# Plane has a FIXED priority choice set; higher rank floats to the top.
PRIORITY_RANK = {
    "urgent": 5,
    "high": 4,
    "medium": 3,
    "low": 2,
    "none": 1,
}
DEFAULT_PRIORITY_RANK = 1  # missing/unknown priority -> treated as "none"
STALE_DAYS = 7
STALE_BONUS = 25
STALE_CAP = 30


def parse_dt(value: str) -> datetime:
    """Parse a Plane ISO-8601 timestamp into an aware UTC datetime.

    Handles trailing ``Z``, microseconds, and ``+00:00`` offsets. Falls back to
    epoch when it cannot be parsed.
    """
    if not value:
        return datetime.fromtimestamp(0, tz=timezone.utc)
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    if len(text) >= 5 and text[-5] in "+-" and text[-3] != ":":
        text = text[:-2] + ":" + text[-2:]
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z"):
            try:
                dt = datetime.strptime(value.strip(), fmt)
                break
            except ValueError:
                continue
        else:
            return datetime.fromtimestamp(0, tz=timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def extract_items(payload) -> list:
    """Accept a list, or an envelope keyed by 'results'/'work_items'/'issues'."""
    if isinstance(payload, list):
        # Could be a list of items, or a list of per-project envelopes.
        items = []
        for entry in payload:
            if isinstance(entry, dict) and isinstance(entry.get("results"), list):
                items.extend(entry["results"])
            else:
                items.append(entry)
        return items
    if isinstance(payload, dict):
        for key in ("results", "work_items", "issues"):
            if isinstance(payload.get(key), list):
                return payload[key]
    return []


def rank(items: list, now: datetime) -> list:
    ranked = []
    for item in items:
        priority = (item.get("priority") or "").lower()
        rank_val = PRIORITY_RANK.get(priority, DEFAULT_PRIORITY_RANK)
        updated = item.get("updated_at") or ""
        days_stale = max(0, (now - parse_dt(updated)).days) if updated else 0
        score = rank_val * 100 + min(days_stale, STALE_CAP)
        if days_stale > STALE_DAYS:
            score += STALE_BONUS
        seq = item.get("sequence_id")
        ranked.append(
            {
                "id": item.get("id", "?"),
                "sequence_id": seq,
                "name": item.get("name") or "",
                "priority": item.get("priority") or "none",
                "days_stale": days_stale,
                "stale": days_stale > STALE_DAYS,
                "score": score,
            }
        )
    ranked.sort(key=lambda r: (r["score"], r["days_stale"]), reverse=True)
    return ranked


def render_table(rows: list) -> str:
    if not rows:
        return "(no work items assigned)"
    header = f"{'ITEM':<10} {'PRIORITY':<8} {'STALE':<7} {'SCORE':<6} NAME"
    lines = [header, "-" * len(header)]
    for r in rows:
        flag = "⚠STALE" if r["stale"] else ""
        ident = (
            f"#{r['sequence_id']}" if r["sequence_id"] is not None else str(r["id"])[:8]
        )
        lines.append(
            f"{ident:<10} {r['priority']:<8} {str(r['days_stale']) + 'd':<7} "
            f"{r['score']:<6} {flag + ' ' if flag else ''}{r['name'][:70]}"
        )
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="JSON file (default: stdin)")
    parser.add_argument("--json", action="store_true", help="emit ranked JSON list")
    parser.add_argument("--now", help="override 'now' as ISO-8601 (for tests)")
    args = parser.parse_args(argv)

    raw = open(args.path, encoding="utf-8").read() if args.path else sys.stdin.read()
    now = parse_dt(args.now) if args.now else datetime.now(timezone.utc)
    rows = rank(extract_items(json.loads(raw)), now)

    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        print(render_table(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
