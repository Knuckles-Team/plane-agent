# Discovering & attaching Plane custom properties

Plane's answer to Jira custom fields is **properties**, and they are attached to a
**work-item type**, not to the project globally. Discover them with the verbose tool
`plane_list_work_item_properties` (`params_json={"project_id":"…","type_id":"…"}`), which
returns descriptors shaped like:

```json
{
  "id": "b1f2...",
  "display_name": "Severity",
  "property_type": "OPTION",
  "is_required": true,
  "is_multi": false,
  "settings": {"options": [{"id":"o1","name":"S1"},{"id":"o2","name":"S2"}]}
}
```

> Requires `MCP_TOOL_MODE=verbose` or `both`. Under `condensed` (the default) this tool is
> not mounted — either flip the mode on the server or create the item with built-in fields
> only and tell the user custom properties were skipped.

## What to collect
1. Every descriptor with `is_required: true`.
2. Any property the user explicitly names (match on `display_name`, case-insensitive).

## `property_type` → value shape
| `property_type` | Value | Notes |
|-----------------|-------|-------|
| `TEXT` | `"free text"` | Single/multi-line text. |
| `DECIMAL` / `NUMBER` | `5` | Bare number. |
| `BOOLEAN` | `true` | |
| `DATETIME` | `"2026-07-15T00:00:00Z"` | ISO-8601. |
| `OPTION` (single) | the option `id` | Pick from `settings.options`. |
| `OPTION` (`is_multi:true`) | list of option `id`s | |
| `RELATION` (member/issue) | the related member/work-item `id` | |
| `URL` / `EMAIL` | `"https://…"` / `"a@b.com"` | Validated by Plane. |

Always use the option **`id`** from `settings.options`, not the display name.

## Attaching values on create
Built-in fields (`name`, `description_html`, `priority`, `state`, `assignees`, `labels`,
`type`) go directly in `data` on `create_work_item`. Custom-property **values** are set
against the property ids. Depending on the deployment, either:

- include a `properties` map in `data` keyed by property id —
  `"properties": {"<property_id>": "<value>"}` — when the create endpoint accepts it, or
- create the work item first, then set each value with the verbose
  `plane_create_work_item_property_value` (or `update_work_item`) call against
  `work_item_id` + `property_id`.

Prefer the first form when the instance supports it; fall back to the second (create → set
values) otherwise. Confirm which path works on the target instance with a single required
property before bulk-setting.

## Id resolution cheat-sheet
| Field | Resolve with |
|-------|--------------|
| `type` | `plane_work_items list_work_item_types` → type `id` |
| `state` | `plane_states list_states` → state `id` |
| `assignees` | `plane_workspaces get_workspace_members` → member `id` |
| `labels` | `plane_labels list_labels` → label `id` |
| custom `OPTION` values | `plane_list_work_item_properties` → `settings.options[].id` |
