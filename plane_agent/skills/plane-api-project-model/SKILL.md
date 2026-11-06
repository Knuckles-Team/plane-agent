---
name: plane-api-project-model
skill_type: skill
description: >-
  Plane project model API. Projects, states, labels, work-item types and properties, and project or workspace features. Do NOT use for the task skills that already cover a workflow (plane-work-item-tracking, plane-cycle-planning, plane-create-work-item-guided, plane-my-priority-queue, plane-kg-ingestion).
license: MIT
tags: [plane, api-reference]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Plane project model API

Projects, states, labels, work-item types and properties, and project or workspace features.

Every operation is its own typed tool; arguments follow the upstream API (path parameters are required,
filters are optional arguments). Read first (get, list, search), change second, and obtain approval before
any delete, disable, revoke or reset.

| Tool | Summary |
|---|---|
| `plane_create_label` | Create a new label. |
| `plane_create_project_page` | Create a new project page. |
| `plane_create_state` | Create a new state. |
| `plane_create_work_item_property` | Create a new work item property. |
| `plane_create_work_item_type` | Create a new work item type. |
| `plane_delete_project` | Delete a project by ID. |
| `plane_delete_state` | Delete a state by ID. |
| `plane_delete_work_item_property` | Delete a work item property by ID. |
| `plane_delete_work_item_type` | Delete a work item type by ID. |
| `plane_get_me` | Get current user information. |
| `plane_get_project_features` | Get features of a project. |
| `plane_get_project_members` | Get all members of a project. |
| `plane_get_project_worklog_summary` | Get work log summary for a project. |
| `plane_get_workspace` | Get current workspace details. |
| `plane_get_workspace_features` | Get features of the current workspace. |
| `plane_get_workspace_members` | Get all members of the current workspace. |
| `plane_ingest_projects` | Ingest Plane projects as :SoftwareProject nodes (+ :Workspace / :inWorkspace). |
| `plane_list_labels` | List all labels in a project. |
| `plane_list_projects` | List all projects in the workspace. |
| `plane_list_states` | List all states in a project. |
| `plane_list_users` | List all users in the workspace. |
| `plane_list_work_item_properties` | List work item properties for a work item type. |
| `plane_list_work_item_types` | List work item types in a project. |
| `plane_retrieve_project` | Retrieve a project by ID. |
| `plane_retrieve_project_page` | Retrieve a project page by ID. |
| `plane_retrieve_state` | Retrieve a state by ID. |
| `plane_retrieve_work_item_property` | Retrieve a work item property by ID. |
| `plane_update_project_features` | Update features of a project. |
| `plane_update_state` | Update a state by ID. |
| `plane_update_work_item_property` | Update a work item property by ID. |
| `plane_update_work_item_type` | Update a work item type by ID. |
| `plane_update_workspace_features` | Update features of the current workspace. |
