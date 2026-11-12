# Plane Kg Ingestion

Natively mirror Plane data into the medulla knowledge graph as typed OWL nodes via the plane-agent MCP server — push projects (:SoftwareProject), work items (:Issue) and cycles (:Cycle) with their containment/assignment links. Use when the agent must ingest or refresh a project's tracking data in the KG for cross-source reasoning or semantic search. Do NOT use for operational CRUD/triage (use plane-work-item-tracking) or sprint planning (use plane-cycle-planning).

# Plane Knowledge-Graph Ingestion

Push Plane records into the ONE medulla knowledge graph as **typed OWL
nodes** — `:SoftwareProject`, `:Issue`, `:Cycle`, `:Workspace`, `:ProjectState`,
`:Person` — with their `:belongsToProject` / `:inWorkspace` / `:assignedTo` /
`:hasState` / `:inCycle` links. Backs cross-source reasoning and semantic search.

## When to use
- Seed or refresh a project's work items / cycles / projects in the KG.
- Make Plane tracking data reachable to graph queries and other connectors.

## When NOT to use
- Operational reads/writes on Plane itself → `plane-work-item-tracking` /
  `plane-cycle-planning`.
- Generic document-sync of many sources → the `scion-sdk-source-integration`
  skill drives the `plane-projects` mcp_tool preset instead.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`plane-agent`** MCP server. A
reachable medulla engine is required for a real write; with no engine the
tools **no-op** and return `{"ingested": null}` (safe to call anywhere).

| Variable | Required | Notes |
|----------|----------|-------|
| `PLANE_API_KEY` | ✅ | Plane API key |
| `PLANE_WORKSPACE_SLUG` | ✅ | Target workspace slug |

## Tools
One typed tool per record kind lists via the real Plane client, then pushes typed nodes best-effort.

| Tool | Parameters | What it ingests |
|------|------------|-----------------|
| `plane_ingest_projects` | `per_page`, `cursor` | projects → `:SoftwareProject` (+ `:Workspace` / `:inWorkspace`) |
| `plane_ingest_work_items` | `project_id` (required), `per_page`, `cursor` | work items → `:Issue` (+ `:belongsToProject` / `:assignedTo` / `:hasState` / `:inCycle`) |
| `plane_ingest_cycles` | `project_id` (required), `per_page`, `cursor` | cycles → `:Cycle` (+ `:belongsToProject`) |

Node ids follow `plane:<class>:<externalId>` (e.g. `plane:issue:<uuid>`), and each
`type` matches a class the package's `plane.ttl` ontology federates into the hub.

## Recipes
Ingest every project: call `plane_ingest_projects` with no arguments.
Ingest a project's work items: `plane_ingest_work_items` with `project_id` and optional `per_page`.
Ingest a project's cycles: `plane_ingest_cycles` with `project_id`.

## Gotchas
- Ingestion is **best-effort and idempotent**: no engine → `{"ingested": null}`,
  no exception; re-running MERGEs the same node ids.
- Listing tools do not ingest on their own; call the explicit ingest tools for a backfill or a refresh.
- `plane_ingest_work_items` needs a `project_id`; without it the Plane list
  call fails before anything is pushed.
- The shared `native_ingest` primitive is used when present; otherwise a
  self-contained txn fallback writes the same nodes.

## Related
- **plane-work-item-tracking** / **plane-cycle-planning** — produce the records this
  skill mirrors into the graph.
- **scion-sdk-source-integration** — the fleet-wide `source_sync` path that
  consumes the `plane-projects` document preset.
