---
name: plane-create-work-item-guided
description: >-
  Create a Plane work item after discovering, from the live instance, which
  work-item type to use and which custom properties that type defines — plus the
  valid state, label, and assignee ids — then populate and submit it. Use when the
  agent must open a Plane work item and needs the correct type + custom-property
  schema and resolved ids instead of guessing. Do NOT use for listing the user's own
  work (use plane-my-priority-queue), cycle/module planning (use plane-cycle-planning),
  or Jira issues (use atlassian-create-issue-guided).
license: MIT
tags: [plane, create-work-item, work-item-types, properties, custom-fields, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Guided Plane Work Item Creation

Never guess the schema. This skill **queries the instance** for the work-item types a
project offers and the custom properties each type defines, resolves the state / label /
assignee ids Plane requires, then builds a valid `create_work_item` payload.

## When to use
- Open a new Plane work item where you must respect the type's custom properties.
- The user says "file this in <project>" and the project uses typed work items / properties.

## When NOT to use
- Listing / triaging the user's own items → `plane-my-priority-queue`.
- Scheduling into cycles/modules → `plane-cycle-planning`.
- Creating a Jira issue → `atlassian-create-issue-guided`.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`plane-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `PLANE_BASE_URL` | optional | API base (default `https://api.plane.so`) |
| `PLANE_API_KEY` | ✅ | Plane API key (`x-api-key`) |
| `PLANE_WORKSPACE_SLUG` | ✅ | Target workspace slug |
| `MCP_TOOL_MODE` | ⚠️ see gotcha | Must be `verbose` or `both` to reach `plane_list_work_item_properties` |

## Tools & actions
| Tool | Key actions |
|------|-------------|
| `plane_projects` | `list_projects` (resolve a project name → uuid) |
| `plane_work_items` | `list_work_item_types`, `create_work_item` |
| `plane_list_work_item_properties` | **verbose-only** tool — a type's custom properties (`project_id` + `type_id`) |
| `plane_states` | `list_states` (state name → uuid) |
| `plane_labels` | `list_labels` (label name → uuid) |
| `plane_workspaces` | `get_workspace_members` (assignee name → member id) |

## Recipes (discover → resolve ids → create)

### 1. Resolve the project and its work-item types
```json
{"project_id":"<project_uuid>"}
```
`plane_work_items` `action="list_work_item_types"` → the types the project defines (Plane
types are first-class). Pick one with the user and note its `id` (`type_id`).

### 2. Discover the type's custom properties
```json
{"project_id":"<project_uuid>","type_id":"<type_uuid>"}
```
`plane_list_work_item_properties` (verbose surface) → each property's `id`, `display_name`,
`property_type` (`TEXT`, `DECIMAL`, `OPTION`, `RELATION`, `BOOLEAN`, `DATETIME`, …),
`is_required`, and (for `OPTION`) its allowed options. Collect **required** properties plus
any the user asked for. See `references/property-discovery.md` for the value shapes and how
custom-property values are attached on create.

### 3. Resolve the ids Plane needs (names are not accepted)
- `plane_states list_states` → the `state` uuid.
- `plane_workspaces get_workspace_members` → the `assignees` member ids.
- `plane_labels list_labels` → the `labels` uuids.

### 4. Create
```json
{"project_id":"<project_uuid>","data":{
  "name":"VPN gateway unreachable from HQ",
  "description_html":"<p>Repro: connect from HQ subnet ...</p>",
  "priority":"high",
  "type":"<type_uuid>",
  "state":"<state_uuid>",
  "assignees":["<member_uuid>"],
  "labels":["<label_uuid>"]
}}
```
`plane_work_items` `action="create_work_item"`. Report the returned `id` + `sequence_id`.
Attach custom-property values per `references/property-discovery.md`.

## Gotchas
- **Verbose surface required:** `plane_list_work_item_properties` exists only on the
  verbose tool surface. If `MCP_TOOL_MODE=condensed` (the default), custom-property
  discovery is unavailable — set `MCP_TOOL_MODE=verbose` or `both` on the server, or
  proceed with only the built-in fields and tell the user custom properties were skipped.
- `priority` is a fixed choice: `urgent`, `high`, `medium`, `low`, `none` — not free text.
- `state`, `assignees`, `labels`, and `type` are **uuids**, never names — always resolve
  them first (step 3).
- Rich text uses `description_html`, not markdown; a plain `description` string is stored
  but not rendered as HTML.
- `create_work_item` POSTs to the legacy `/issues/` path under the hood, but the field
  contract is the work-item one above — pass fields inside `data`.
- Every call is workspace-scoped by `PLANE_WORKSPACE_SLUG`.

## Related
- **plane-my-priority-queue** — after creating, see it in the ranked queue.
- **plane-work-item-tracking** — general work-item CRUD, comments, links, relations.
- **atlassian-create-issue-guided** — the same discovery-driven creation on Jira.
