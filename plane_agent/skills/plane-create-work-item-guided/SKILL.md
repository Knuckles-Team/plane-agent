---
name: plane-create-work-item-guided
skill_type: skill
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
  author: Knuckles-Team
  version: '0.1.0'
---

# Plane Create Work Item Guided

Every step below is one typed tool call; there is no `action` or JSON-string argument. Resolve ids by name first, read before you change, and ask for approval before anything destructive.

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
