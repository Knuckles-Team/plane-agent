---
name: plane-api-planning-objects
skill_type: skill
description: >-
  Plane planning objects API. Cycles, modules, milestones, epics and initiatives with their work-item membership. Do NOT use for the task skills that already cover a workflow (plane-work-item-tracking, plane-cycle-planning, plane-create-work-item-guided, plane-my-priority-queue, plane-kg-ingestion).
license: MIT
tags: [plane, api-reference]
metadata:
  author: Knuckles-Team
  version: '1.0.0'
---
# Plane planning objects API

Cycles, modules, milestones, epics and initiatives with their work-item membership.

Every operation is its own typed tool; arguments follow the upstream API (path parameters are required,
filters are optional arguments). Read first (get, list, search), change second, and obtain approval before
any delete, disable, revoke or reset.

| Tool | Summary |
|---|---|
| `plane_add_work_items_to_cycle` | Add work items to a cycle. |
| `plane_add_work_items_to_milestone` | Add work items to a milestone. |
| `plane_add_work_items_to_module` | Add work items to a module. |
| `plane_archive_module` | Archive a module. |
| `plane_create_cycle` | Create a new cycle. |
| `plane_create_epic` | Create a new epic (technically a work item with epic type). |
| `plane_create_initiative` | Create a new initiative in the workspace. |
| `plane_create_milestone` | Create a new milestone. |
| `plane_create_module` | Create a new module. |
| `plane_delete_cycle` | Delete a cycle by ID. |
| `plane_delete_epic` | Delete an epic by ID. |
| `plane_delete_initiative` | Delete an initiative by ID. |
| `plane_delete_milestone` | Delete a milestone by ID. |
| `plane_delete_module` | Delete a module by ID. |
| `plane_ingest_cycles` | Ingest a project's cycles as :Cycle nodes (+ :belongsToProject). |
| `plane_list_archived_cycles` | List archived cycles in a project. |
| `plane_list_archived_modules` | List archived modules in a project. |
| `plane_list_cycle_work_items` | List work items in a cycle. |
| `plane_list_cycles` | List all cycles in a project. |
| `plane_list_epics` | List all epics in a project. |
| `plane_list_initiatives` | List all initiatives in the workspace. |
| `plane_list_milestone_work_items` | List work items in a milestone. |
| `plane_list_milestones` | List all milestones in a project. |
| `plane_list_module_work_items` | List work items in a module. |
| `plane_list_modules` | List all modules in a project. |
| `plane_remove_work_item_from_cycle` | Remove a work item from a cycle. |
| `plane_remove_work_item_from_module` | Remove a work item from a module. |
| `plane_remove_work_items_from_milestone` | Remove work items from a milestone. |
| `plane_retrieve_cycle` | Retrieve a cycle by ID. |
| `plane_retrieve_epic` | Retrieve an epic by ID. |
| `plane_retrieve_initiative` | Retrieve an initiative by ID. |
| `plane_retrieve_milestone` | Retrieve a milestone by ID. |
| `plane_retrieve_module` | Retrieve a module by ID. |
| `plane_transfer_cycle_work_items` | Transfer work items from one cycle to another. |
| `plane_unarchive_module` | Unarchive a module. |
| `plane_update_cycle` | Update a cycle by ID. |
| `plane_update_epic` | Update an epic by ID. |
| `plane_update_initiative` | Update an initiative by ID. |
| `plane_update_milestone` | Update a milestone by ID. |
| `plane_update_module` | Update a module by ID. |
