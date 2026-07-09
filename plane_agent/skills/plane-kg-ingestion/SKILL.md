---
name: plane-kg-ingestion
skill_type: skill
description: >-
  Natively mirror Plane data into the epistemic-graph knowledge graph as typed
  OWL nodes via the plane-agent MCP server — push projects (:SoftwareProject),
  work items (:Issue) and cycles (:Cycle) with their containment/assignment links.
  Use when the agent must ingest or refresh a project's tracking data in the KG for
  cross-source reasoning or semantic search. Do NOT use for operational CRUD/triage
  (use plane-work-item-tracking) or sprint planning (use plane-cycle-planning).
license: MIT
tags: [plane, knowledge-graph, ingestion, ontology, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Plane Knowledge-Graph Ingestion

Push Plane records into the ONE epistemic-graph knowledge graph as **typed OWL
nodes** — `:SoftwareProject`, `:Issue`, `:Cycle`, `:Workspace`, `:ProjectState`,
`:Person` — with their `:belongsToProject` / `:inWorkspace` / `:assignedTo` /
`:hasState` / `:inCycle` links. Backs cross-source reasoning and semantic search.

## When to use
- Seed or refresh a project's work items / cycles / projects in the KG.
- Make Plane tracking data reachable to graph queries and other connectors.

## When NOT to use
- Operational reads/writes on Plane itself → `plane-work-item-tracking` /
  `plane-cycle-planning`.
- Generic document-sync of many sources → the `agent-utilities-source-integration`
  skill drives the `plane-projects` mcp_tool preset instead.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`plane-agent`** MCP server. A
reachable epistemic-graph engine is required for a real write; with no engine the
tools **no-op** and return `{"ingested": null}` (safe to call anywhere).

| Variable | Required | Notes |
|----------|----------|-------|
| `PLANE_API_KEY` | ✅ | Plane API key |
| `PLANE_WORKSPACE_SLUG` | ✅ | Target workspace slug |
| `PLANE_KG_INGEST` | optional | `true` (default) auto-ingests on the `list_*` fetch flow; set `false` to disable |
| `MCP_TOOL_MODE` | optional | `condensed` \| `verbose` \| `both` |

## Tools & actions
One action-routed tool lists via the real Plane client, then pushes typed nodes
best-effort. Takes `action` + a `params_json` **JSON string**.

| Condensed tool | Action | What it ingests |
|----------------|--------|-----------------|
| `plane_ingest` | `ingest_projects` | projects → `:SoftwareProject` (+ `:Workspace` / `:inWorkspace`) |
| `plane_ingest` | `ingest_work_items` | work items → `:Issue` (+ `:belongsToProject` / `:assignedTo` / `:hasState` / `:inCycle`) |
| `plane_ingest` | `ingest_cycles` | cycles → `:Cycle` (+ `:belongsToProject`) |

Node ids follow `plane:<class>:<externalId>` (e.g. `plane:issue:<uuid>`), and each
`type` matches a class the package's `plane.ttl` ontology federates into the hub.

### Key parameters
- `action` — one of `ingest_projects`, `ingest_work_items`, `ingest_cycles`.
- `params_json` — a JSON **string** of the underlying `list_*` params.
  `ingest_work_items` and `ingest_cycles` require `project_id`.

## Recipes (`action` + `params_json`)
Ingest every project in the workspace — `action="ingest_projects"`:
```json
{}
```
Ingest a project's work items — `action="ingest_work_items"`:
```json
{"project_id":"<project_uuid>","per_page":100}
```
Ingest a project's cycles — `action="ingest_cycles"`:
```json
{"project_id":"<project_uuid>"}
```

## Gotchas
- Ingestion is **best-effort and idempotent**: no engine → `{"ingested": null}`,
  no exception; re-running MERGEs the same node ids.
- Auto-ingest already fires on `plane_work_items list_work_items`,
  `plane_projects list_projects`, and `plane_cycles list_cycles` when
  `PLANE_KG_INGEST` is not `false` — call these explicit tools for an on-demand
  backfill or when auto-ingest is disabled.
- `plane_ingest ingest_work_items` needs a `project_id`; without it the Plane list
  call fails before anything is pushed.
- The shared `native_ingest` primitive is used when present; otherwise a
  self-contained txn fallback writes the same nodes.

## Related
- **plane-work-item-tracking** / **plane-cycle-planning** — produce the records this
  skill mirrors into the graph.
- **agent-utilities-source-integration** — the fleet-wide `source_sync` path that
  consumes the `plane-projects` document preset.
