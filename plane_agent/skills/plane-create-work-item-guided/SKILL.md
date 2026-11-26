---
name: plane-create-work-item-guided
skill_type: skill
description: >-
  Create a Plane work item after discovering, from the live instance, which work-item type to use and which custom properties that type defines — plus the valid state, label, and assignee ids — then populate and submit it. Use when the agent must open a Plane work item and needs the correct type + custom-property schema and resolved ids instead of guessing.
license: MIT
tags: [plane, create-work-item, work-item-types, properties, custom-fields, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# Plane Create Work Item Guided

Scope: Create a Plane work item after discovering, from the live instance, which work-item type to use and which custom properties that type defines — plus the valid state, label, and assignee ids — then populate and submit it. Use when the agent must open a Plane work item and needs the correct type + custom-property schema and resolved ids instead of guessing. Do NOT use for listing the user's own work (use plane-my-priority-queue), cycle/module planning (use plane-cycle-planning), or Jira issues (use atlassian-create-issue-guided).

Every step below is one typed tool call; there is no `action` or JSON-string argument. Resolve ids by name first, read before you change, and ask for approval before anything destructive.

## Steps

1. Resolve the project with `plane_list_projects` and verify exactly one project matches the requested name.
2. Read the valid ids with `plane_list_states`, `plane_list_labels` and `plane_list_work_item_types` and verify the state, label and type names the requester wants appear in the output.
3. Read the type's custom fields with `plane_list_work_item_properties` and verify every required property has a value from the requester.
4. Create the item with `plane_create_work_item` and verify the response returns a work item id and sequence number.
5. Read it back with `plane_retrieve_work_item` and verify the title, state, type and properties match the request.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| 401 or 403 response | `PLANE_API_KEY` is missing or revoked, or `PLANE_BASE_URL` or `PLANE_WORKSPACE_SLUG` is wrong | Set `PLANE_BASE_URL`, `PLANE_API_KEY` and `PLANE_WORKSPACE_SLUG` in the environment, restart the server, and repeat `plane_get_me` |
| 404 or empty result for a project, work item or cycle | The id was guessed instead of resolved by name | Resolve the id with `plane_list_projects` or the matching list tool and use the id returned |
| Create rejected with a validation error | A required property is missing or an id belongs to another project | Reread `plane_list_work_item_properties` and `plane_list_states` for this project, fix the data, and call `plane_create_work_item` again with the corrected data |

## Create work item guided

Discover the project's states, labels, types and custom properties, then create the work item.

1. `plane_list_projects` (per_page, cursor, order_by)
2. `plane_list_states` (project_id, params_json)
3. `plane_list_labels` (project_id, params_json)
4. `plane_list_work_item_types` (project_id)
5. `plane_list_work_item_properties` (project_id, type_id, params_json)
6. `plane_create_work_item` (project_id, data)

## Guardrails

- Never print tokens, passwords or webhook secrets.
- Public or destructive actions need the requester's confirmation of the target and text.
- Report ids (and refusal codes) for every call.
