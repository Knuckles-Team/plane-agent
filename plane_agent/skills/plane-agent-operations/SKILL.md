---
name: plane-agent-operations
skill_type: skill
description: >-
  Operate plane-agent through its governed MCP and Arbora capabilities, including plane create work item guided, plane cycle planning, plane kg ingestion, plane my priority queue, plane work item tracking. Use when a request requires this provider's read, change, automation, ingestion, troubleshooting, or evidence workflows.
---

# Plane Agent Operations

Every step below is one typed tool call; there is no `action` or JSON-string argument. Resolve ids by name first, read before you change, and ask for approval before anything destructive.

## Steps

1. Call `plane_get_me` and verify the response returns your user id and display name.
2. Call `plane_get_workspace` and verify the workspace slug matches the one the requester named.
3. Call `plane_list_states` for the target project and verify the state names you will use appear in the listing.
4. Describe the planned `plane_update_state` or `plane_create_state` call to the requester and verify explicit approval before running it.
5. Run the change and read it back with `plane_retrieve_state` and verify the stored name and group match the request.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| 401 or 403 response | `PLANE_API_KEY` is missing or revoked, or `PLANE_BASE_URL` or `PLANE_WORKSPACE_SLUG` is wrong | Set `PLANE_BASE_URL`, `PLANE_API_KEY` and `PLANE_WORKSPACE_SLUG` in the environment, restart the server, and repeat `plane_get_me` |
| 404 or empty result for a project, work item or cycle | The id was guessed instead of resolved by name | Resolve the id with `plane_list_projects` or the matching list tool and use the id returned |
| Feature change has no effect | The feature is disabled at workspace level | Read `plane_get_workspace_features`, ask the requester to enable it with `plane_update_workspace_features`, and repeat `plane_update_project_features` |

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
