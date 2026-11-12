---
name: plane-kg-ingestion
skill_type: skill
description: >-
  Natively mirror Plane data into the medulla knowledge graph as typed
  OWL nodes via the plane-agent MCP server — push projects (:SoftwareProject),
  work items (:Issue) and cycles (:Cycle) with their containment/assignment links.
  Use when the agent must ingest or refresh a project's tracking data in the KG for
  cross-source reasoning or semantic search. Do NOT use for operational CRUD/triage
  (use plane-work-item-tracking) or sprint planning (use plane-cycle-planning).
license: MIT
tags: [plane, knowledge-graph, ingestion, ontology, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# Plane Kg Ingestion

Every step below is one typed tool call; there is no `action` or JSON-string argument. Resolve ids by name first, read before you change, and ask for approval before anything destructive.

## Mirror plane to graph

Land projects, work items and cycles in the knowledge graph.

1. `plane_ingest_projects` (per_page, cursor)
2. `plane_ingest_work_items` (project_id, per_page, cursor)
3. `plane_ingest_cycles` (project_id, per_page, cursor)

## Guardrails

- Never print tokens, passwords or webhook secrets.
- Public or destructive actions need the requester's confirmation of the target and text.
- Report ids (and refusal codes) for every call.
