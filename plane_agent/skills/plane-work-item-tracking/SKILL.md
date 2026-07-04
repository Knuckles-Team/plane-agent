---
name: plane-work-item-tracking
description: >-
  Track and manage Plane work items (issues) via the plane-agent MCP server —
  list, search, read, create, update and delete work items, and manage their
  comments, links, relations and work logs with the domain-typed tool. Use when
  the agent must triage a project's backlog, open or update an issue, comment on
  or link work items, or log time. Do NOT use for sprint/cycle or module planning
  (use plane-cycle-planning) or for pushing Plane data into the knowledge graph
  (use plane-kg-ingestion).
license: MIT
tags: [plane, issues, work-items, project-tracking, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Plane Work Item Tracking

Domain-typed access to Plane **work items** (issues) for backlog triage and
day-to-day tracking. Prefer these tools over ad-hoc HTTP — they carry Plane's
work-item field conventions and return work-item-shaped records.

## When to use
- List / search / triage a project's work items.
- Read a single work item by id or by project identifier + sequence number.
- Create, update, or delete a work item.
- Add comments, links, or relations; read activity; create work logs.

## When NOT to use
- Cycle (sprint) or module planning → `plane-cycle-planning`.
- Ingesting Plane records into the knowledge graph → `plane-kg-ingestion`.
- Workspace/member administration, states, labels, pages → the corresponding
  `plane_workspaces` / `plane_states` / `plane_labels` / `plane_pages` tools.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`plane-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `PLANE_BASE_URL` | optional | API base (default `https://api.plane.so`) |
| `PLANE_API_KEY` | ✅ | Plane API key (`x-api-key`) |
| `PLANE_WORKSPACE_SLUG` | ✅ | Target workspace slug |
| `PLANE_SSL_VERIFY` | optional | TLS verification toggle |
| `MCP_TOOL_MODE` | optional | `condensed` \| `verbose` \| `both` — selects the condensed surface below vs. the 1:1 verbose tools |

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the client method.

| Condensed tool | Key actions |
|----------------|-------------|
| `plane_work_items` | `list_work_items`, `search_work_items`, `retrieve_work_item`, `retrieve_work_item_by_identifier`, `create_work_item`, `update_work_item`, `delete_work_item`, `list_work_item_comments`, `create_work_item_comment`, `list_work_item_links`, `create_work_item_link`, `list_work_item_relations`, `list_work_item_activities`, `list_work_logs`, `create_work_log` |

### Key parameters
- `project_id` — required for every list/create call.
- `work_item_id` — required for retrieve/update/delete and sub-resource calls.
- `project_identifier` + `issue_identifier` — for `retrieve_work_item_by_identifier`
  (e.g. project key `PROJ` + sequence `42`).
- `data` — object of field→value for create/update (`name`, `description`,
  `priority`, `state`, `assignees`, …).

## Recipes (`params_json`)
List a project's work items (cursor pagination survives in the raw envelope):
```json
{"project_id":"<project_uuid>","per_page":50}
```
Retrieve one by human identifier (project key + sequence):
```json
{"project_identifier":"PROJ","issue_identifier":42}
```
Create a work item:
```json
{"project_id":"<project_uuid>","data":{"name":"VPN gateway unreachable","priority":"high","description":"Reported by HQ"}}
```
Comment on a work item:
```json
{"project_id":"<project_uuid>","work_item_id":"<id>","data":{"comment_html":"<p>Investigating.</p>"}}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `priority` is a choice value: `urgent`, `high`, `medium`, `low`, or `none`.
- `state` and `assignees` expect Plane **ids** (state uuid, member ids), not names —
  resolve them via `plane_states` / `plane_workspaces` first.
- `list_work_items` returns the raw Plane envelope (`results`, `next_cursor`,
  `count`, …); page with the cursor fields rather than assuming a flat list.
- Every call is workspace-scoped by `PLANE_WORKSPACE_SLUG`; a `project_id` from a
  different workspace 404s.

## Related
- **plane-cycle-planning** — schedule these work items into cycles and modules.
- **plane-kg-ingestion** — mirror work items into the knowledge graph as typed
  `:Issue` nodes (the `plane_ingest` tool, `ingest_work_items` action; also fires
  automatically on `list_work_items`).
