---
name: plane-my-priority-queue
skill_type: skill
description: >-
  Rank the Plane work items assigned to the current user by priority plus staleness, flagging items untouched for more than 7 days, and suggest updates from session context. Use when the agent must show my open work, build a priority queue, or find stale assigned items.
license: MIT
tags: [plane, my-work, work-items, triage, staleness, priority, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# Plane My Priority Queue

Scope: Surface the Plane work items assigned to the current user across the workspace, rank them by a combined priority + staleness score (highest priority at the top, items untouched for more than 7 days flagged and boosted), and suggest updates to those work items from the current session's context. Use when the agent must answer "what should I work on", "what's assigned to me", or "what's gone stale" in Plane, or wants to push conversation findings back onto the user's open work items. Do NOT use for creating new work items (use plane-create-work-item-guided), cycle/sprint planning (use plane-cycle-planning), or Jira issues (use atlassian-my-priority-queue).

Every step below is one typed tool call; there is no `action` or JSON-string argument. Resolve ids by name first, read before you change, and ask for approval before anything destructive.

## Steps

1. Call `plane_get_me` and verify the response returns the current user id.
2. List projects with `plane_list_projects` and verify at least one project is returned.
3. For each project call `plane_list_work_items` with the assignee filter set to your user id and verify every returned item names you as assignee.
4. Rank the `plane_list_work_items` results by priority and days since update, flag any untouched for more than 7 days, and verify the top item has the highest priority among them.
5. Suggest updates for stale items, apply one with `plane_update_work_item` only after approval, and verify the change with `plane_retrieve_work_item`.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| 401 or 403 response | `PLANE_API_KEY` is missing or revoked, or `PLANE_BASE_URL` or `PLANE_WORKSPACE_SLUG` is wrong | Set `PLANE_BASE_URL`, `PLANE_API_KEY` and `PLANE_WORKSPACE_SLUG` in the environment, restart the server, and repeat `plane_get_me` |
| Queue is empty | No items are assigned to the user or the filter used the wrong id | Reread `plane_get_me` and rerun `plane_list_work_items` with that user id |
| 404 or empty result for a project, work item or cycle | The id was guessed instead of resolved by name | Resolve the id with `plane_list_projects` or the matching list tool and use the id returned |

## My priority queue

List the work items assigned to the current user, ranked by priority and staleness.

1. `plane_get_me`
2. `plane_list_projects` (per_page, cursor, order_by)
3. `plane_list_states` (project_id, params_json)
4. `plane_list_work_items` (project_id, params_json)

## Guardrails

- Never print tokens, passwords or webhook secrets.
- Public or destructive actions need the requester's confirmation of the target and text.
- Report ids (and refusal codes) for every call.
