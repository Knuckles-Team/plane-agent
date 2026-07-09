---
name: plane-cycle-planning
skill_type: skill
description: >-
  Plan and run Plane cycles (sprints) and modules via the plane-agent MCP server —
  create/read/update cycles and modules, assign or transfer work items between
  them, and read a cycle's or module's work-item roster. Use when the agent must
  set up a sprint, group work into a feature module, move issues across cycles, or
  review what is scheduled in a cycle. Do NOT use for work-item CRUD/triage (use
  plane-work-item-tracking) or knowledge-graph ingestion (use plane-kg-ingestion).
license: MIT
tags: [plane, cycles, sprints, modules, planning, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Plane Cycle & Module Planning

Domain-typed access to Plane **cycles** (time-boxed sprints) and **modules**
(feature groupings) for iteration planning. Prefer these tools over ad-hoc HTTP —
they carry Plane's cycle/module conventions and return cycle/module-shaped records.

## When to use
- Create / read / update / delete a cycle (sprint) or module.
- Add work items to, or remove them from, a cycle or module.
- Transfer work items from one cycle to another.
- Read the work-item roster of a cycle or module.

## When NOT to use
- Creating or editing the work items themselves → `plane-work-item-tracking`.
- Pushing cycles/work items into the knowledge graph → `plane-kg-ingestion`.
- Epics, milestones, or initiatives → the `plane_epics` / `plane_milestones` /
  `plane_initiatives` tools.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`plane-agent`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `PLANE_BASE_URL` | optional | API base (default `https://api.plane.so`) |
| `PLANE_API_KEY` | ✅ | Plane API key (`x-api-key`) |
| `PLANE_WORKSPACE_SLUG` | ✅ | Target workspace slug |
| `PLANE_SSL_VERIFY` | optional | TLS verification toggle |
| `MCP_TOOL_MODE` | optional | `condensed` \| `verbose` \| `both` |

## Tools & actions
Prefer the **condensed** tools; each takes `action` + a `params_json` **JSON string**.

| Condensed tool | Key actions |
|----------------|-------------|
| `plane_cycles` | `list_cycles`, `create_cycle`, `retrieve_cycle`, `update_cycle`, `delete_cycle`, `list_cycle_work_items`, `add_work_items_to_cycle` |
| `plane_modules` | `list_modules`, `create_module`, `retrieve_module`, `update_module`, `delete_module`, `list_module_work_items`, `add_work_items_to_module` |

### Key parameters
- `project_id` — required for every call.
- `cycle_id` / `module_id` — required for retrieve/update/delete and roster calls.
- `issue_ids` — a **list** of work-item ids for `add_work_items_to_*`.
- `data` — object for create/update (`name`, `start_date`, `end_date`, …).

## Recipes (`params_json`)
Create a two-week cycle:
```json
{"project_id":"<project_uuid>","data":{"name":"Sprint 12","start_date":"2026-07-07","end_date":"2026-07-20"}}
```
List a project's cycles:
```json
{"project_id":"<project_uuid>"}
```
Add work items to a cycle:
```json
{"project_id":"<project_uuid>","cycle_id":"<cycle_uuid>","issue_ids":["<id1>","<id2>"]}
```
Read a cycle's work-item roster:
```json
{"project_id":"<project_uuid>","cycle_id":"<cycle_uuid>"}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- `add_work_items_to_cycle` / `add_work_items_to_module` take `issue_ids` as a JSON
  **array**, not a comma string; the client maps it to Plane's `issues` field.
- `start_date` / `end_date` are ISO-8601 dates (`YYYY-MM-DD`); an end before start is
  rejected by Plane.
- A work item can sit in at most one cycle at a time — use `transfer_cycle_work_items`
  (verbose surface) to move it, or remove-then-add.
- All ids are workspace-scoped by `PLANE_WORKSPACE_SLUG`.

## Related
- **plane-work-item-tracking** — create and triage the work items you schedule here.
- **plane-kg-ingestion** — mirror cycles into the knowledge graph as typed `:Cycle`
  nodes linked to their `:SoftwareProject`.
