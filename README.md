# Plane Agent
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/plane-agent)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/plane-agent)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/plane-agent)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/plane-agent)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/plane-agent)
![PyPI - License](https://img.shields.io/pypi/l/plane-agent)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/plane-agent)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/plane-agent)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/plane-agent)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/plane-agent)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/plane-agent)
![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/plane-agent)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/plane-agent)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/plane-agent)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/plane-agent)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/plane-agent)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/plane-agent)

*Version: 0.13.0*

---

## Overview

**Plane Agent** is a production-grade Agent and Model Context Protocol (MCP) server designed to interface directly with Plane MCP Agent.

---

## Key Features

- **Consolidated Action-Routed MCP Tools:** Minimizes token overhead and eliminates tool bloat in LLM contexts by grouping methods into optimized, togglable tool modules.
- **Enterprise-Grade Security:** Comprehensive support for Eunomia policies, OIDC token delegation, and granular execution context tracking.
- **Integrated Graph Agent:** Built-in Pydantic AI agent supporting the Agent Control Protocol (ACP) and standard Web interfaces (AG-UI).
- **Native Telemetry & Tracing:** Out-of-the-box OpenTelemetry exports and native Langfuse tracing.

---

## CLI or API

This agent wraps the Plane MCP Agent API. You can interact with it programmatically or via its integrated execution entrypoints.

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](file:///home/apps/workspace/agent-packages/agents/plane-agent/docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools
| Tool Module | Toggle Env Var | Enabled by Default | Description & Nested Methods |
|-------------|----------------|--------------------|------------------------------|
| **Projects** | `PROJECTSTOOL` | `True` | Manage plane projects operations. Action-routed methods: `list_projects`, `retrieve_project`. |
| **Work Items** | `WORK_ITEMSTOOL` | `True` | Manage plane work items operations. Action-routed methods: `list_work_items`, `create_work_item`, `update_work_item`, `delete_work_item`, `search_work_items`, `retrieve_work_item_by_identifier`, `retrieve_work_item`, `list_work_item_activities`, `list_work_item_comments`, `create_work_item_comment`, `list_work_item_links`, `create_work_item_link`, `list_work_item_relations`, `list_work_item_types`, `list_work_logs`, `create_work_log`. |
| **Cycles** | `CYCLESTOOL` | `True` | Manage plane cycles operations. Action-routed methods: `list_cycles`, `create_cycle`, `retrieve_cycle`, `update_cycle`, `delete_cycle`, `list_cycle_work_items`, `add_work_items_to_cycle`. |
| **Epics** | `EPICSTOOL` | `True` | Manage plane epics operations. Action-routed methods: `list_epics`, `create_epic`, `retrieve_epic`, `update_epic`, `delete_epic`. |
| **Milestones** | `MILESTONESTOOL` | `True` | Manage plane milestones operations. Action-routed methods: `list_milestones`, `create_milestone`, `retrieve_milestone`, `update_milestone`, `delete_milestone`. |
| **Modules** | `MODULESTOOL` | `True` | Manage plane modules operations. Action-routed methods: `list_modules`, `create_module`, `retrieve_module`, `update_module`, `delete_module`. |
| **States** | `STATESTOOL` | `True` | Manage plane states operations. Action-routed methods: `list_states`, `create_state`. |
| **Users** | `USERSTOOL` | `True` | Manage plane users operations. Action-routed methods: `list_users`, `get_me`. |
| **Workspaces** | `WORKSPACESTOOL` | `True` | Manage plane workspaces operations. Action-routed methods: `get_workspace`, `get_workspace_members`, `get_workspace_features`, `update_workspace_features`. |
| **Initiatives** | `INITIATIVESTOOL` | `True` | Manage plane initiatives operations. Action-routed methods: `list_initiatives`, `create_initiative`. |
| **Intake** | `INTAKETOOL` | `True` | Manage plane intake operations. Action-routed methods: `list_intake_work_items`, `create_intake_work_item`. |
| **Labels** | `LABELSTOOL` | `True` | Manage plane labels operations. Action-routed methods: `list_labels`, `create_label`. |
| **Pages** | `PAGESTOOL` | `True` | Manage plane pages operations. Action-routed methods: `retrieve_project_page`, `create_project_page`. |

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/mcp.md](file:///home/apps/workspace/agent-packages/agents/plane-agent/docs/mcp.md).

### MCP Configuration Examples

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "plane-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "plane-agent",
        "plane-mcp"
      ],
      "env": {
        "PLANE_BASE_URL": "your_plane_base_url_here",
        "PLANE_WORKSPACE_SLUG": "your_plane_workspace_slug_here",
        "DEBUG": "your_debug_here",
        "PYTHONUNBUFFERED": "your_pythonunbuffered_here",
        "PLANE_API_KEY": "your_plane_api_key_here"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (Recommended for production deployments)
Configure your client's `mcp.json` to launch the Streamable-HTTP server via `uvx` with explicit host and port definition:

```json
{
  "mcpServers": {
    "plane-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "plane-agent",
        "plane-mcp"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "PLANE_BASE_URL": "your_plane_base_url_here",
        "PLANE_WORKSPACE_SLUG": "your_plane_workspace_slug_here",
        "DEBUG": "your_debug_here",
        "PYTHONUNBUFFERED": "your_pythonunbuffered_here",
        "PLANE_API_KEY": "your_plane_api_key_here"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed remote or local Streamable-HTTP instance:

```json
{
  "mcpServers": {
    "plane-agent": {
      "url": "http://localhost:8000/plane-agent/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name plane-agent-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e PORT=8000 \
  -e PLANE_BASE_URL="your_value" \
  -e PLANE_WORKSPACE_SLUG="your_value" \
  -e DEBUG="your_value" \
  -e PYTHONUNBUFFERED="your_value" \
  -e PLANE_API_KEY="your_value" \
  knucklessg1/plane-agent:latest
```

---

## Agent

This repository features a fully integrated Pydantic AI Graph Agent. It communicates over the **Agent Control Protocol (ACP)** and interacts seamlessly with the **Agent Web UI (AG-UI)** and Terminal interface.

### Running the Agent CLI
To start the interactive command-line agent:

```bash
# Set credentials
export PLANE_BASE_URL="your_value"
export PLANE_WORKSPACE_SLUG="your_value"
export DEBUG="your_value"
export PYTHONUNBUFFERED="your_value"
export PLANE_API_KEY="your_value"

# Run the agent server
plane-agent --provider openai --model-id gpt-4o
```

### Docker Compose Orchestration
The following `docker/agent.compose.yml` configures the Agent, Web UI, and Terminal Interface together:

```yaml
version: '3.8'

services:
  plane-agent-mcp:
    image: knucklessg1/plane-agent:latest
    container_name: plane-agent-mcp
    hostname: plane-agent-mcp
    restart: always
    env_file:
      - ../.env
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=8000
      - TRANSPORT=streamable-http
    ports:
      - "8000:8000"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  plane-agent-agent:
    image: knucklessg1/plane-agent:latest
    container_name: plane-agent-agent
    hostname: plane-agent-agent
    restart: always
    depends_on:
      - plane-agent-mcp
    env_file:
      - ../.env
    command: [ "plane-agent" ]
    environment:
      - PYTHONUNBUFFERED=1
      - HOST=0.0.0.0
      - PORT=9004
      - MCP_URL=http://plane-agent-mcp:8000/mcp
      - PROVIDER=${PROVIDER:-openai}
      - MODEL_ID=${MODEL_ID:-gpt-4o}
      - ENABLE_WEB_UI=True
      - ENABLE_OTEL=True
    ports:
      - "9004:9004"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:9004/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

```

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/agent.md](file:///home/apps/workspace/agent-packages/agents/plane-agent/docs/agent.md).

---

## Security & Governance

Built directly upon the enterprise-ready [`agent-utilities`](https://github.com/Knuckles-Team/agent-utilities) core, standard security parameters are fully supported:

### Access Control & Policy Enforcement
- **Eunomia Policies:** Fine-grained, policy-driven tool authorization. Supports `none`, local `embedded` (`mcp_policies.json`), or centralized `remote` modes.
- **OIDC Token Delegation:** Compliant with RFC 8693 token exchange for flowing authenticating user credentials from Web UI / ACP → Agent → MCP.
- **Scoped Credentials:** Execution context runs restricted to the specific caller identity.

### Runtime Security Grid
| Feature | Functionality | Enablement |
|---------|---------------|------------|
| **Tool Guard** | Sensitivity inspection with human-in-the-loop validation | Enabled by default |
| **Prompt Injection Defense** | Input scanning, repetition monitoring, and recursive loop blocks | Enabled by default |
| **Context Safety Guard** | Stuck-loop detectors and contextual overflow preemptive alerts | Enabled by default |

---

## Installation

Install the Python package locally:

```bash
# Using uv (highly recommended)
uv pip install plane-agent[all]

# Using standard pip
python -m pip install plane-agent[all]
```

---

## Repository Owners

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`
