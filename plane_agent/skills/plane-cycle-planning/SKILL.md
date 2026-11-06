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
  author: Knuckles-Team
  version: '0.1.0'
---

# Plane Cycle Planning

Every step below is one typed tool call; there is no `action` or JSON-string argument. Resolve ids by name first, read before you change, and ask for approval before anything destructive.

## Plan cycle

Create a cycle, fill it with work items, move leftovers and read what is in it.

1. `plane_create_cycle` (project_id, data)
2. `plane_list_cycles` (project_id, params_json)
3. `plane_retrieve_cycle` (project_id, cycle_id)
4. `plane_update_cycle` (project_id, cycle_id, data)
5. `plane_add_work_items_to_cycle` (project_id, cycle_id, issue_ids)
6. `plane_list_cycle_work_items` (project_id, cycle_id, params_json)
7. `plane_remove_work_item_from_cycle` (project_id, cycle_id, work_item_id, confirm)
8. `plane_transfer_cycle_work_items` (project_id, cycle_id, new_cycle_id)
9. `plane_list_archived_cycles` (project_id, params_json)

## Plan modules and milestones

Group work into modules and milestones.

1. `plane_create_module` (project_id, data)
2. `plane_list_modules` (project_id, params_json)
3. `plane_update_module` (project_id, module_id, data)
4. `plane_add_work_items_to_module` (project_id, module_id, issue_ids)
5. `plane_list_module_work_items` (project_id, module_id, params_json)
6. `plane_remove_work_item_from_module` (project_id, module_id, work_item_id, confirm)
7. `plane_archive_module` (project_id, module_id)
8. `plane_unarchive_module` (project_id, module_id)
9. `plane_list_archived_modules` (project_id, params_json)
10. `plane_create_milestone` (project_id, data)
11. `plane_list_milestones` (project_id, params_json)
12. `plane_update_milestone` (project_id, milestone_id, data)
13. `plane_add_work_items_to_milestone` (project_id, milestone_id, issue_ids)
14. `plane_list_milestone_work_items` (project_id, milestone_id, params_json)
15. `plane_remove_work_items_from_milestone` (project_id, milestone_id, issue_ids, confirm)

## Plan epics and initiatives

Plan epics and initiatives above individual work items.

1. `plane_create_epic` (project_id, data)
2. `plane_list_epics` (project_id, params_json)
3. `plane_retrieve_epic` (project_id, epic_id)
4. `plane_update_epic` (project_id, epic_id, data)
5. `plane_create_initiative` (data)
6. `plane_list_initiatives` (per_page, cursor, order_by)
7. `plane_retrieve_initiative` (initiative_id)
8. `plane_update_initiative` (initiative_id, data)

## Retire plane objects

Delete work items, comments, links, cycles, modules, epics, initiatives, milestones, states or a project after approval.

1. `plane_delete_work_item` (project_id, work_item_id, confirm)
2. `plane_delete_work_item_comment` (project_id, work_item_id, comment_id, confirm)
3. `plane_delete_work_item_link` (project_id, work_item_id, link_id, confirm)
4. `plane_delete_cycle` (project_id, cycle_id, confirm)
5. `plane_delete_module` (project_id, module_id, confirm)
6. `plane_delete_epic` (project_id, epic_id, confirm)
7. `plane_delete_initiative` (initiative_id, confirm)
8. `plane_delete_milestone` (project_id, milestone_id, confirm)
9. `plane_delete_state` (project_id, state_id, confirm)
10. `plane_delete_project` (project_id, confirm)
11. `plane_delete_intake_work_item` (project_id, work_item_id, confirm)
12. `plane_delete_work_log` (project_id, work_item_id, work_log_id, confirm)
13. `plane_delete_work_item_property` (project_id, type_id, work_item_property_id, confirm)
14. `plane_delete_work_item_type` (project_id, work_item_type_id, confirm)

## Guardrails

- Never print tokens, passwords or webhook secrets.
- Public or destructive actions need the requester's confirmation of the target and text.
- Report ids (and refusal codes) for every call.
