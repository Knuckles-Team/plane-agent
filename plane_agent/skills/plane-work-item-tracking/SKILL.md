---
name: plane-work-item-tracking
skill_type: skill
description: >-
  Track and manage Plane work items (issues) via the plane-agent MCP server —
  list, search, read, create, update and delete work items, and manage their
  comments, links, relations and work logs with the typed tools. Use when
  the agent must triage a project's backlog, open or update an issue, comment on
  or link work items, or log time. Do NOT use for sprint/cycle or module planning
  (use plane-cycle-planning) or for pushing Plane data into the knowledge graph
  (use plane-kg-ingestion).
license: MIT
tags: [plane, issues, work-items, project-tracking, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# Plane Work Item Tracking

Every step below is one typed tool call; there is no `action` or JSON-string argument. Resolve ids by name first, read before you change, and ask for approval before anything destructive.

## Browse projects

Find a project and read its members, features, states and labels.

1. `plane_list_projects` (per_page, cursor, order_by)
2. `plane_retrieve_project` (project_id)
3. `plane_get_project_members` (project_id, params_json)
4. `plane_get_project_features` (project_id)
5. `plane_list_states` (project_id, params_json)
6. `plane_list_labels` (project_id, params_json)

## Find work items

Find work items by filter, text or identifier and read one.

1. `plane_list_work_items` (project_id, params_json)
2. `plane_search_work_items` (query, params_json)
3. `plane_advanced_search_work_items` (data)
4. `plane_retrieve_work_item` (project_id, work_item_id)
5. `plane_retrieve_work_item_by_identifier` (project_identifier, issue_identifier)

## Update work item

Change a work item and leave a comment with the reason.

1. `plane_retrieve_work_item_by_identifier` (project_identifier, issue_identifier)
2. `plane_update_work_item` (project_id, work_item_id, data)
3. `plane_create_work_item_comment` (project_id, work_item_id, data)
4. `plane_list_work_item_comments` (project_id, work_item_id, params_json)
5. `plane_list_work_item_activities` (project_id, work_item_id, params_json)

## Link and relate work items

Attach links and relate work items to each other.

1. `plane_create_work_item_link` (project_id, work_item_id, data)
2. `plane_list_work_item_links` (project_id, work_item_id, params_json)
3. `plane_create_work_item_relation` (project_id, work_item_id, data)
4. `plane_list_work_item_relations` (project_id, work_item_id)
5. `plane_remove_work_item_relation` (project_id, work_item_id, related_issue, confirm)

## Triage intake

Review incoming intake requests and accept, edit or reject them.

1. `plane_list_intake_work_items` (project_id, params_json)
2. `plane_retrieve_intake_work_item` (project_id, work_item_id)
3. `plane_create_intake_work_item` (project_id, data)
4. `plane_update_intake_work_item` (project_id, work_item_id, data)

## Track time

Log time on work items and summarise it for a project.

1. `plane_create_work_log` (project_id, work_item_id, data)
2. `plane_list_work_logs` (project_id, work_item_id, params_json)
3. `plane_update_work_log` (project_id, work_item_id, work_log_id, data)
4. `plane_get_project_worklog_summary` (project_id)

## Document in pages

Write and read project pages.

1. `plane_create_project_page` (project_id, data)
2. `plane_retrieve_project_page` (project_id, page_id)

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
