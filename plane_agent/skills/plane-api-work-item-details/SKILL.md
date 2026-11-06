---
name: plane-api-work-item-details
skill_type: skill
description: >-
  Plane work-item details API. Comments, links, relations, activities, work logs, intake and pages around a work item. Do NOT use for the task skills that already cover a workflow (plane-work-item-tracking, plane-cycle-planning, plane-create-work-item-guided, plane-my-priority-queue, plane-kg-ingestion).
license: MIT
tags: [plane, api-reference]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Plane work-item details API

Comments, links, relations, activities, work logs, intake and pages around a work item.

Every operation is its own typed tool; arguments follow the upstream API (path parameters are required,
filters are optional arguments). Read first (get, list, search), change second, and obtain approval before
any delete, disable, revoke or reset.

| Tool | Summary |
|---|---|
| `plane_advanced_search_work_items` | Advanced search for work items. |
| `plane_create_intake_work_item` | Create a new intake work item in a project. |
| `plane_create_work_item` | Create a new work item. |
| `plane_create_work_item_comment` | Create a comment for a work item. |
| `plane_create_work_item_link` | Create a link for a work item. |
| `plane_create_work_item_relation` | Create relations for a work item. |
| `plane_create_work_log` | Create a work log for a work item. |
| `plane_delete_intake_work_item` | Delete an intake work item by work item ID. |
| `plane_delete_work_item` | Delete a work item by ID. |
| `plane_delete_work_item_comment` | Delete a comment for a work item. |
| `plane_delete_work_item_link` | Delete a link for a work item. |
| `plane_delete_work_log` | Delete a work log for a work item. |
| `plane_ingest_work_items` | Ingest a project's work items as :Issue nodes (+ :belongsToProject / :assignedTo / :hasState / :inCycle). |
| `plane_list_intake_work_items` | List all intake work items in a project. |
| `plane_list_work_item_activities` | List activities for a work item. |
| `plane_list_work_item_comments` | List comments for a work item. |
| `plane_list_work_item_links` | List links for a work item. |
| `plane_list_work_item_relations` | List relations for a work item. |
| `plane_list_work_items` | List work items in a project. |
| `plane_list_work_logs` | List work logs for a work item. |
| `plane_remove_work_item_relation` | Remove a relation from a work item. |
| `plane_retrieve_intake_work_item` | Retrieve an intake work item by work item ID. |
| `plane_retrieve_work_item` | Retrieve a work item by ID. |
| `plane_retrieve_work_item_activity` | Retrieve a specific activity for a work item. |
| `plane_retrieve_work_item_by_identifier` | Retrieve a work item by project identifier and issue sequence number. |
| `plane_retrieve_work_item_comment` | Retrieve a specific comment for a work item. |
| `plane_retrieve_work_item_link` | Retrieve a specific link for a work item. |
| `plane_search_work_items` | Search work items across a workspace. |
| `plane_update_intake_work_item` | Update an intake work item by work item ID. |
| `plane_update_work_item` | Update a work item by ID. |
| `plane_update_work_item_comment` | Update a comment for a work item. |
| `plane_update_work_item_link` | Update a link for a work item. |
| `plane_update_work_log` | Update a work log for a work item. |
