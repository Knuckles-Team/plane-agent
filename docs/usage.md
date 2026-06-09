# Usage — API / CLI / MCP

`plane-agent` exposes the same capability three ways: as **MCP tools** an agent calls,
as a **Python API** (`Api`) you import, and as **CLI** entry points. The ecosystem
role and architecture are described in [Overview](overview.md).

## As an MCP server

Once [deployed](deployment.md), the server registers a tool domain for each Plane
resource. Every domain is gated by its own `*TOOL` environment toggle (default
`True`), so you can register only the surface you need.

| Domain | Toggle | Covers |
|---|---|---|
| Projects | `PROJECTSTOOL` | list / retrieve / create / delete projects |
| Work items | `WORK_ITEMSTOOL` | issues, work items, sub-items |
| Cycles | `CYCLESTOOL` | sprint cycles and cycle issues |
| Epics | `EPICSTOOL` | epics and epic links |
| Milestones | `MILESTONESTOOL` | milestones |
| Modules | `MODULESTOOL` | modules and module issues |
| States | `STATESTOOL` | workflow states |
| Initiatives | `INITIATIVESTOOL` | initiatives |
| Intake | `INTAKETOOL` | intake / inbox issues |
| Labels | `LABELSTOOL` | labels |
| Pages | `PAGESTOOL` | pages |
| Users | `USERSTOOL` | members and assignees |
| Workspaces | `WORKSPACESTOOL` | workspace metadata |

Example agent prompts that map onto these tools:

- *"List the projects in my workspace"* → projects domain
- *"Create a work item titled 'Fix login bug' in project `<id>`"* → work items domain
- *"What cycles are active for project `<id>`?"* → cycles domain

## As a Python API

`Api` (`plane_agent.api_client.Api`) is a composed REST client over the Plane
workspace API. It authenticates on construction and exposes typed read and write
methods per domain.

```python
from plane_agent.api_client import Api

api = Api(
    url="https://api.plane.so",
    api_key="your_plane_api_key",
    workspace_slug="your-workspace",
    verify=True,
)

# Reads
projects = api.list_projects()                       # Response with parsed Project list
project = api.retrieve_project(project_id)            # a single Project
items = api.list_work_items(project_id)               # Response with parsed WorkItem list
item = api.retrieve_work_item(project_id, item_id)    # a single WorkItem
```

Build a client straight from the environment:

```python
from plane_agent.auth import get_client
api = get_client()        # reads PLANE_BASE_URL / PLANE_API_KEY / PLANE_WORKSPACE_SLUG
```

### Writes

```python
api.create_work_item(project_id, {"name": "Fix login bug", "priority": "high"})
api.update_work_item(project_id, work_item_id, {"state": state_id})
api.delete_work_item(project_id, work_item_id)
```

## As a CLI

Two console scripts are installed with the package:

```bash
# The MCP server
plane-mcp --transport streamable-http --host 0.0.0.0 --port 8000

# The A2A agent server (connects to the MCP server over MCP_URL)
MCP_URL=http://localhost:8000/mcp plane-agent --host 0.0.0.0 --port 9004
```

Both accept `--help` for the full flag list. See [Deployment](deployment.md) for the
transport, environment, and agent-wiring details.
