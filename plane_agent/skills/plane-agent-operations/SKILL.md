---
name: plane-agent-operations
skill_type: skill
description: >-
  Operate plane-agent through its governed MCP and Arbora capabilities, including plane create work item guided, plane cycle planning, plane kg ingestion, plane my priority queue, plane work item tracking. Use when a request requires this provider's read, change, automation, ingestion, troubleshooting, or evidence workflows.
---

# Plane Agent Operations

Every step below is one typed tool call; there is no `action` or JSON-string argument. Resolve ids by name first, read before you change, and ask for approval before anything destructive.

## Verify workspace

Confirm the credential, the workspace and its features.

1. `plane_get_me`
2. `plane_get_workspace`
3. `plane_get_workspace_members`
4. `plane_get_workspace_features`

## Configure project model

Shape a project's states, labels, types and properties.

1. `plane_list_states` (project_id, params_json)
2. `plane_create_state` (project_id, data)
3. `plane_retrieve_state` (project_id, state_id)
4. `plane_update_state` (project_id, state_id, data)
5. `plane_create_label` (project_id, data)
6. `plane_list_work_item_types` (project_id)
7. `plane_create_work_item_type` (project_id, data)
8. `plane_update_work_item_type` (project_id, work_item_type_id, data)
9. `plane_list_work_item_properties` (project_id, type_id, params_json)
10. `plane_create_work_item_property` (project_id, type_id, data)
11. `plane_update_work_item_property` (project_id, type_id, work_item_property_id, data)
12. `plane_update_project_features` (project_id, data)

## Guardrails

- Never print tokens, passwords or webhook secrets.
- Public or destructive actions need the requester's confirmation of the target and text.
- Report ids (and refusal codes) for every call.
