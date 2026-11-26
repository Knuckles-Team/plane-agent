---
name: plane-kg-ingestion
skill_type: skill
description: >-
  Natively mirror Plane data into the medulla knowledge graph as typed OWL nodes via the plane-agent MCP server — push projects (:SoftwareProject), work items (:Issue) and cycles (:Cycle) with their containment/assignment links. Use when the agent must ingest or refresh a project's tracking data in the KG for cross-source reasoning or semantic search.
license: MIT
tags: [plane, knowledge-graph, ingestion, ontology, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# Plane Kg Ingestion

Scope: Natively mirror Plane data into the medulla knowledge graph as typed OWL nodes via the plane-agent MCP server — push projects (:SoftwareProject), work items (:Issue) and cycles (:Cycle) with their containment/assignment links. Use when the agent must ingest or refresh a project's tracking data in the KG for cross-source reasoning or semantic search. Do NOT use for operational CRUD/triage (use plane-work-item-tracking) or sprint planning (use plane-cycle-planning).

Every step below is one typed tool call; there is no `action` or JSON-string argument. Resolve ids by name first, read before you change, and ask for approval before anything destructive.

## Steps

1. Call `plane_get_me` to confirm the credential and verify it returns your user id.
2. Run `plane_ingest_projects` and verify the response reports a project count above zero.
3. Run `plane_ingest_work_items` for one project id from that result and verify the response reports a work item count.
4. Run `plane_ingest_cycles` for the same project id and verify the response reports a cycle count.
5. Page through any large project by passing `cursor` from the previous result and verify the count grows until no cursor is returned.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| 401 or 403 response | `PLANE_API_KEY` is missing or revoked, or `PLANE_BASE_URL` or `PLANE_WORKSPACE_SLUG` is wrong | Set `PLANE_BASE_URL`, `PLANE_API_KEY` and `PLANE_WORKSPACE_SLUG` in the environment, restart the server, and repeat `plane_get_me` |
| Ingest returns zero nodes | No reachable knowledge graph engine, so the best-effort ingest no-ops | Configure the engine endpoint through the Arbora settings and rerun `plane_ingest_projects` |
| 404 or empty result for a project, work item or cycle | The id was guessed instead of resolved by name | Resolve the id with `plane_list_projects` or the matching list tool and use the id returned |

## Mirror plane to graph

Land projects, work items and cycles in the knowledge graph.

1. `plane_ingest_projects` (per_page, cursor)
2. `plane_ingest_work_items` (project_id, per_page, cursor)
3. `plane_ingest_cycles` (project_id, per_page, cursor)

## Guardrails

- Never print tokens, passwords or webhook secrets.
- Public or destructive actions need the requester's confirmation of the target and text.
- Report ids (and refusal codes) for every call.
