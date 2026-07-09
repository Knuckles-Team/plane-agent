# Plane `list_work_items` filter recipes & state-group exclusion

Plane has no JQL. You filter by passing Plane's own query params through `params_json`
(they become `**kwargs` on the API client, i.e. URL query params). Every call is scoped to
`PLANE_WORKSPACE_SLUG` and to one `project_id`.

## Assigned to me, open, one project
```json
{"project_id":"<project_uuid>","assignees":"<member_id>","per_page":100}
```
`plane_work_items` `action="list_work_items"`. Resolve `<member_id>` once via
`plane_users get_me`. Repeat per project (there is no workspace-wide item list).

## Paging the cursor envelope
The response is `{"results":[...], "next_cursor":"...", "count":N, "next_page_results":bool}`.
If `next_page_results` is true, repeat with the cursor:
```json
{"project_id":"<project_uuid>","assignees":"<member_id>","per_page":100,"cursor":"<next_cursor>"}
```

## Dropping finished work (the "not Done" equivalent)
Jira uses `statusCategory != Done`. Plane states are per-project and carry a `group`. First
list the states:
```json
{"project_id":"<project_uuid>"}
```
`plane_states` `action="list_states"` → each state has `id`, `name`, and
`group` ∈ {`backlog`, `unstarted`, `started`, `completed`, `cancelled`}. Build the set of
state ids whose group is `completed` or `cancelled`, then **exclude items whose `state`
matches** after listing. (Plane also accepts a server-side `state_group` filter on some
deployments — `{"project_id":"…","assignees":"…","state_group":"backlog,unstarted,started"}`
— but client-side exclusion via `list_states` is the portable path.)

## Other useful filters (pass through `params_json`)
| Param | Meaning |
|-------|---------|
| `assignees` | member id(s), comma-separated |
| `state` | state uuid(s) |
| `priority` | `urgent,high,medium,low,none` |
| `labels` | label uuid(s) |
| `created_by` | member id |
| `target_date` | due date filter (ISO date) |
| `per_page` / `cursor` | pagination |

## Building the ranked queue
Collect the `results` arrays from every project into a single JSON array (or a JSON list of
the raw per-project envelopes — the script accepts both) and pipe through
`scripts/rank_items.py`. The script maps `urgent=5…none=1`, computes staleness from
`updated_at`, flags `> 7d` as `⚠STALE`, and sorts by the composite score.
