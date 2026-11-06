---
name: plane-my-priority-queue
skill_type: skill
description: >-
  Surface the Plane work items assigned to the current user across the workspace,
  rank them by a combined priority + staleness score (highest priority at the top,
  items untouched for more than 7 days flagged and boosted), and suggest updates to
  those work items from the current session's context. Use when the agent must answer
  "what should I work on", "what's assigned to me", or "what's gone stale" in Plane,
  or wants to push conversation findings back onto the user's open work items. Do NOT
  use for creating new work items (use plane-create-work-item-guided), cycle/sprint
  planning (use plane-cycle-planning), or Jira issues (use atlassian-my-priority-queue).
license: MIT
tags: [plane, my-work, work-items, triage, staleness, priority, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---

# Plane My Priority Queue

Every step below is one typed tool call; there is no `action` or JSON-string argument. Resolve ids by name first, read before you change, and ask for approval before anything destructive.

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
