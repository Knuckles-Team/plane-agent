---
name: plane-my-priority-queue
description: >-
  Surface the Plane work items assigned to the current user across the workspace,
  rank them by a combined priority + staleness score (highest priority at the top,
  items untouched for more than 7 days flagged and boosted), and suggest updates to
  those work items from the current session's context. Use when the agent must answer
  "what should I work on", "what's assigned to me", or "what's gone stale" in Plane,
  or wants to push conversation findings back onto the user's open work items. Do NOT
  use for creating new work items (use plane-create-work-item-guided), cycle/sprint
  planning (use plane-cycle-planning), or Jira issues (use atlassian-my-priority-queue).
license: MIT
tags: [plane, my-work, work-items, triage, staleness, priority, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# My Plane Priority Queue

Find every work item assigned to the current user across the workspace, present it as
**one list ordered by a combined priority + staleness score**, and turn what was learned
in this session into concrete, confirm-before-write updates.

## When to use
- "What's assigned to me / what should I work on next?" in Plane.
- "What of mine has gone stale?" (untouched > 7 days).
- After a working session, to push findings back onto the relevant open work items.

## When NOT to use
- Creating a new work item with type/property discovery → `plane-create-work-item-guided`.
- Scheduling work into cycles/modules → `plane-cycle-planning`.
- The same capability on Jira → `atlassian-my-priority-queue`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`plane-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `PLANE_BASE_URL` | optional | API base (default `https://api.plane.so`) |
| `PLANE_API_KEY` | ✅ | Plane API key (`x-api-key`) |
| `PLANE_WORKSPACE_SLUG` | ✅ | Target workspace slug — every call is scoped to it |
| `MCP_TOOL_MODE` | optional | `condensed` (default) exposes the action-routed tools below |

The condensed tools take `action` + a `params_json` **JSON string**.

## Tools & actions
| Condensed tool | Key actions used here |
|----------------|-----------------------|
| `plane_users` | `get_me` (resolve the current member id) |
| `plane_projects` | `list_projects` (enumerate the workspace's projects) |
| `plane_states` | `list_states` (resolve state → group to drop finished work) |
| `plane_work_items` | `list_work_items`, `create_work_item_comment`, `update_work_item` |

## Key parameters & the Jira difference
Plane has **no query language and no cross-project search** for "assigned to me", and
`list_work_items` is **project-scoped**. So the queue is assembled client-side:
1. one member id, 2. iterate projects, 3. one filtered list call per project,
4. rank the concatenation locally. The staleness/priority math lives in
`scripts/rank_items.py` — pipe the collected items through it, do not eyeball the order.

## Recipes

### 1. Assemble and rank my queue
Resolve identity, then projects:
```json
{}
```
`plane_users get_me` → your member `id`. `plane_projects list_projects` → project ids.

For **each** project, list your open items (the response is a raw cursor envelope —
page with `next_cursor`):
```json
{"project_id":"<project_uuid>","assignees":"<member_id>","per_page":100}
```
`plane_work_items list_work_items`. To drop finished work, call `plane_states list_states`
for that project and exclude items whose `state` id belongs to a state with
`group` ∈ {`completed`, `cancelled`} (see `references/filter-recipes.md`).

Concatenate every project's `results` into one JSON array and rank it:
```bash
python scripts/rank_items.py all_items.json          # human table with ⚠STALE flags
python scripts/rank_items.py --json all_items.json   # ranked JSON
```
`score = priority_rank*100 + min(days_stale,30) + (25 if days_stale>7)`, where
Plane priorities map `urgent=5, high=4, medium=3, low=2, none=1`, and staleness is
computed from `updated_at`.

### 2. Suggest updates from this session's context
For each ranked item, scan the **current conversation** for facts that concern it. For
every match, **draft** and **confirm before writing**:
- A progress comment → `plane_work_items` `action="create_work_item_comment"`,
  `params_json={"project_id":"…","work_item_id":"…","data":{"comment_html":"<p>…</p>"}}`.
- A field edit (priority, state, assignees) → `plane_work_items` `action="update_work_item"`,
  `params_json={"project_id":"…","work_item_id":"…","data":{...}}`.

Never apply a write without explicit user confirmation of the drafted change.

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- Every call is scoped to `PLANE_WORKSPACE_SLUG`; a `project_id` from another workspace 404s.
- `list_work_items` returns the raw envelope (`results`, `next_cursor`, `count`); page the
  cursor rather than assuming a flat list, then feed the merged `results` to the script.
- `state` on a work item is a **uuid**, not a name — resolve the completed/cancelled groups
  from `list_states` before filtering.
- `updated_at` bumps on any edit (including a comment), so a freshly-commented item is not
  "stale" even if untouched functionally — this matches Jira's `updated` semantics.
- `rank_items.py` treats a missing priority as `none` and clamps the staleness term at 30 days.

## Related
- **plane-create-work-item-guided** — open a new work item with type/property discovery.
- **plane-cycle-planning** — schedule these items into cycles and modules.
- **atlassian-my-priority-queue** — the same capability for Jira issues.
