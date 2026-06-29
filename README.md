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

*Version: 1.0.0*

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> interfaces, and guidance for provisioning a self-hosted Plane instance are
> maintained in the [official documentation](https://knuckles-team.github.io/plane-agent/).

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [CLI or API](#cli-or-api)
- [MCP](#mcp)
  - [Available MCP Tools](#available-mcp-tools)
  - [MCP Configuration Examples](#mcp-configuration-examples)
  - [Dynamic Tool Selection & Visibility](#dynamic-tool-selection--visibility)
- [Agent](#agent)
  - [Running the Agent CLI](#running-the-agent-cli)
  - [Docker Compose Orchestration](#docker-compose-orchestration)
- [Security & Governance](#security-governance)
- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Documentation](#documentation)
- [Repository Owners](#repository-owners)
- [Contribute](#contribute)

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

Detailed instructions on how to use the underlying API wrappers, extended schema bindings, and developer SDK references are maintained in [docs/index.md](docs/index.md).

---

## MCP

This server utilizes dynamic Action-Routed tools to optimize token overhead and maximize IDE compatibility.

### Available MCP Tools

This table is auto-generated from the live server — do not edit by hand.

<!-- MCP-TOOLS-TABLE:START -->

#### Condensed action-routed tools (default — `MCP_TOOL_MODE=condensed`)

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `plane_cycles` | `CYCLESTOOL` | Manage plane cycles operations. |
| `plane_epics` | `EPICSTOOL` | Manage plane epics operations. |
| `plane_initiatives` | `INITIATIVESTOOL` | Manage plane initiatives operations. |
| `plane_intake` | `INTAKETOOL` | Manage plane intake operations. |
| `plane_labels` | `LABELSTOOL` | Manage plane labels operations. |
| `plane_milestones` | `MILESTONESTOOL` | Manage plane milestones operations. |
| `plane_modules` | `MODULESTOOL` | Manage plane modules operations. |
| `plane_pages` | `PAGESTOOL` | Manage plane pages operations. |
| `plane_projects` | `PROJECTSTOOL` | Manage plane projects operations. |
| `plane_states` | `STATESTOOL` | Manage plane states operations. |
| `plane_users` | `USERSTOOL` | Manage plane users operations. |
| `plane_work_items` | `WORK_ITEMSTOOL` | Manage plane work items operations. |
| `plane_workspaces` | `WORKSPACESTOOL` | Manage plane workspaces operations. |

#### Verbose 1:1 API-mapped tools (`MCP_TOOL_MODE=verbose` or `both`)

<details>
<summary>102 per-operation tools — one per public API method (click to expand)</summary>

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `plane_add_work_items_to_cycle` | `APITOOL` | Add work items to a cycle. |
| `plane_add_work_items_to_milestone` | `APITOOL` | Add work items to a milestone. |
| `plane_add_work_items_to_module` | `APITOOL` | Add work items to a module. |
| `plane_advanced_search_work_items` | `APITOOL` | Advanced search for work items. |
| `plane_archive_module` | `APITOOL` | Archive a module. |
| `plane_create_cycle` | `APITOOL` | Create a new cycle. |
| `plane_create_epic` | `APITOOL` | Create a new epic (technically a work item with epic type). |
| `plane_create_initiative` | `APITOOL` | Create a new initiative in the workspace. |
| `plane_create_intake_work_item` | `APITOOL` | Create a new intake work item in a project. |
| `plane_create_label` | `APITOOL` | Create a new label. |
| `plane_create_milestone` | `APITOOL` | Create a new milestone. |
| `plane_create_module` | `APITOOL` | Create a new module. |
| `plane_create_project_page` | `APITOOL` | Create a new project page. |
| `plane_create_state` | `APITOOL` | Create a new state. |
| `plane_create_work_item` | `APITOOL` | Create a new work item. |
| `plane_create_work_item_comment` | `APITOOL` | Create a comment for a work item. |
| `plane_create_work_item_link` | `APITOOL` | Create a link for a work item. |
| `plane_create_work_item_property` | `APITOOL` | Create a new work item property. |
| `plane_create_work_item_relation` | `APITOOL` | Create relations for a work item. |
| `plane_create_work_item_type` | `APITOOL` | Create a new work item type. |
| `plane_create_work_log` | `APITOOL` | Create a work log for a work item. |
| `plane_delete_cycle` | `APITOOL` | Delete a cycle by ID. |
| `plane_delete_epic` | `APITOOL` | Delete an epic by ID. |
| `plane_delete_initiative` | `APITOOL` | Delete an initiative by ID. |
| `plane_delete_intake_work_item` | `APITOOL` | Delete an intake work item by work item ID. |
| `plane_delete_milestone` | `APITOOL` | Delete a milestone by ID. |
| `plane_delete_module` | `APITOOL` | Delete a module by ID. |
| `plane_delete_project` | `APITOOL` | Delete a project by ID. |
| `plane_delete_state` | `APITOOL` | Delete a state by ID. |
| `plane_delete_work_item` | `APITOOL` | Delete a work item by ID. |
| `plane_delete_work_item_comment` | `APITOOL` | Delete a comment for a work item. |
| `plane_delete_work_item_link` | `APITOOL` | Delete a link for a work item. |
| `plane_delete_work_item_property` | `APITOOL` | Delete a work item property by ID. |
| `plane_delete_work_item_type` | `APITOOL` | Delete a work item type by ID. |
| `plane_delete_work_log` | `APITOOL` | Delete a work log for a work item. |
| `plane_get_me` | `APITOOL` | Get current user information. |
| `plane_get_project_features` | `APITOOL` | Get features of a project. |
| `plane_get_project_members` | `APITOOL` | Get all members of a project. |
| `plane_get_project_worklog_summary` | `APITOOL` | Get work log summary for a project. |
| `plane_get_workspace` | `APITOOL` | Get current workspace details. |
| `plane_get_workspace_features` | `APITOOL` | Get features of the current workspace. |
| `plane_get_workspace_members` | `APITOOL` | Get all members of the current workspace. |
| `plane_list_archived_cycles` | `APITOOL` | List archived cycles in a project. |
| `plane_list_archived_modules` | `APITOOL` | List archived modules in a project. |
| `plane_list_cycle_work_items` | `APITOOL` | List work items in a cycle. |
| `plane_list_cycles` | `APITOOL` | List all cycles in a project. |
| `plane_list_epics` | `APITOOL` | List all epics in a project. |
| `plane_list_initiatives` | `APITOOL` | List all initiatives in the workspace. |
| `plane_list_intake_work_items` | `APITOOL` | List all intake work items in a project. |
| `plane_list_labels` | `APITOOL` | List all labels in a project. |
| `plane_list_milestone_work_items` | `APITOOL` | List work items in a milestone. |
| `plane_list_milestones` | `APITOOL` | List all milestones in a project. |
| `plane_list_module_work_items` | `APITOOL` | List work items in a module. |
| `plane_list_modules` | `APITOOL` | List all modules in a project. |
| `plane_list_projects` | `APITOOL` | List all projects in the workspace. |
| `plane_list_states` | `APITOOL` | List all states in a project. |
| `plane_list_users` | `APITOOL` | List all users in the workspace. |
| `plane_list_work_item_activities` | `APITOOL` | List activities for a work item. |
| `plane_list_work_item_comments` | `APITOOL` | List comments for a work item. |
| `plane_list_work_item_links` | `APITOOL` | List links for a work item. |
| `plane_list_work_item_properties` | `APITOOL` | List work item properties for a work item type. |
| `plane_list_work_item_relations` | `APITOOL` | List relations for a work item. |
| `plane_list_work_item_types` | `APITOOL` | List work item types in a project. |
| `plane_list_work_items` | `APITOOL` | List work items in a project. |
| `plane_list_work_logs` | `APITOOL` | List work logs for a work item. |
| `plane_remove_work_item_from_cycle` | `APITOOL` | Remove a work item from a cycle. |
| `plane_remove_work_item_from_module` | `APITOOL` | Remove a work item from a module. |
| `plane_remove_work_item_relation` | `APITOOL` | Remove a relation from a work item. |
| `plane_remove_work_items_from_milestone` | `APITOOL` | Remove work items from a milestone. |
| `plane_retrieve_cycle` | `APITOOL` | Retrieve a cycle by ID. |
| `plane_retrieve_epic` | `APITOOL` | Retrieve an epic by ID. |
| `plane_retrieve_initiative` | `APITOOL` | Retrieve an initiative by ID. |
| `plane_retrieve_intake_work_item` | `APITOOL` | Retrieve an intake work item by work item ID. |
| `plane_retrieve_milestone` | `APITOOL` | Retrieve a milestone by ID. |
| `plane_retrieve_module` | `APITOOL` | Retrieve a module by ID. |
| `plane_retrieve_project` | `APITOOL` | Retrieve a project by ID. |
| `plane_retrieve_project_page` | `APITOOL` | Retrieve a project page by ID. |
| `plane_retrieve_state` | `APITOOL` | Retrieve a state by ID. |
| `plane_retrieve_work_item` | `APITOOL` | Retrieve a work item by ID. |
| `plane_retrieve_work_item_activity` | `APITOOL` | Retrieve a specific activity for a work item. |
| `plane_retrieve_work_item_by_identifier` | `APITOOL` | Retrieve a work item by project identifier and issue sequence number. |
| `plane_retrieve_work_item_comment` | `APITOOL` | Retrieve a specific comment for a work item. |
| `plane_retrieve_work_item_link` | `APITOOL` | Retrieve a specific link for a work item. |
| `plane_retrieve_work_item_property` | `APITOOL` | Retrieve a work item property by ID. |
| `plane_search_work_items` | `APITOOL` | Search work items across a workspace. |
| `plane_transfer_cycle_work_items` | `APITOOL` | Transfer work items from one cycle to another. |
| `plane_unarchive_module` | `APITOOL` | Unarchive a module. |
| `plane_update_cycle` | `APITOOL` | Update a cycle by ID. |
| `plane_update_epic` | `APITOOL` | Update an epic by ID. |
| `plane_update_initiative` | `APITOOL` | Update an initiative by ID. |
| `plane_update_intake_work_item` | `APITOOL` | Update an intake work item by work item ID. |
| `plane_update_milestone` | `APITOOL` | Update a milestone by ID. |
| `plane_update_module` | `APITOOL` | Update a module by ID. |
| `plane_update_project_features` | `APITOOL` | Update features of a project. |
| `plane_update_state` | `APITOOL` | Update a state by ID. |
| `plane_update_work_item` | `APITOOL` | Update a work item by ID. |
| `plane_update_work_item_comment` | `APITOOL` | Update a comment for a work item. |
| `plane_update_work_item_link` | `APITOOL` | Update a link for a work item. |
| `plane_update_work_item_property` | `APITOOL` | Update a work item property by ID. |
| `plane_update_work_item_type` | `APITOOL` | Update a work item type by ID. |
| `plane_update_work_log` | `APITOOL` | Update a work log for a work item. |
| `plane_update_workspace_features` | `APITOOL` | Update features of the current workspace. |

</details>

_13 action-routed tool(s) (default) · 102 verbose 1:1 tool(s). Each is enabled unless its `<DOMAIN>TOOL` toggle is set false; `MCP_TOOL_MODE` selects the surface (`condensed` default · `verbose` 1:1 · `both`). Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

Detailed tool schemas, parameter shapes, and validation constraints are preserved in [docs/index.md](docs/index.md).

### Dynamic Tool Selection & Visibility

This MCP server supports dynamic toolset selection and visibility filtering at runtime. This allows you to restrict the set of exposed tools in order to prevent blowing up the LLM's context window.

You can configure tool filtering via multiple input channels:

- **CLI Arguments:** Pass `--tools` or `--toolsets` (or their disabled counterparts `--disabled-tools` and `--disabled-toolsets`) during startup.
- **Environment Variables:** Define standard environment variables:
  - `MCP_ENABLED_TOOLS` / `MCP_DISABLED_TOOLS`
  - `MCP_ENABLED_TAGS` / `MCP_DISABLED_TAGS`
- **HTTP SSE Request Headers:** Pass custom headers during transport initialization:
  - `x-mcp-enabled-tools` / `x-mcp-disabled-tools`
  - `x-mcp-enabled-tags` / `x-mcp-disabled-tags`
- **HTTP SSE Request Query Parameters:** Append query parameters directly to your transport connection URL:
  - `?tools=tool1,tool2`
  - `?tags=tag1`

When query strings or parameters are supplied, an LLM-free **Knowledge Graph resolution layer** (using `DynamicToolOrchestrator`) matches query intents against known tool tags, names, or descriptions, with safe fallback and automated 24-hour background cache refreshing.

---

### MCP Configuration Examples

> **Install the slim `[mcp]` extra.** All examples below install
> `plane-agent[mcp]` — the MCP-server extra that pulls only the FastMCP /
> FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

#### stdio Transport (Recommended for local IDEs e.g., Cursor, Claude Desktop)
Configure your IDE's `mcp.json` to launch the MCP server via `uvx`:

```json
{
  "mcpServers": {
    "plane-agent": {
      "command": "uvx",
      "args": [
        "--from",
        "plane-agent[mcp]",
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
        "plane-agent[mcp]",
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
  knucklessg1/plane-agent:mcp
```

> The `:mcp` tag is the **slim MCP-server image** (built from
> `docker/Dockerfile --target mcp`, installing `plane-agent[mcp]`). The default
> `:latest` tag is the **full agent image** (`--target agent`, `plane-agent[agent]`)
> which also bundles the Pydantic AI agent and the epistemic-graph engine — use it
> when you run `plane-agent` (the agent), not just the MCP server. See
> [Container images](#container-images-mcp-vs-agent).

---

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`plane-agent` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/plane-agent/deployment/) has full, copy-paste
`mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://plane-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

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
    image: knucklessg1/plane-agent:mcp
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

Detailed graph node architecture explanations, custom skill configurations, and agentic trace guides are available in [docs/overview.md](docs/overview.md) and [docs/index.md](docs/index.md).

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

## Environment Variables

<!-- ENV-VARS-TABLE:START -->

#### Package environment variables

| Variable | Example | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` |  |
| `PORT` | `8000` |  |
| `TRANSPORT` | `stdio` | options: stdio, streamable-http, sse |
| `ENABLE_OTEL` | `True` |  |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:8080/api/public/otel` |  |
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | `pk-...` |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | `sk-...` |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `PLANE_BASE_URL` | `https://api.plane.so` |  |
| `PLANE_WORKSPACE_SLUG` | — |  |
| `DEBUG` | `False` |  |
| `PYTHONUNBUFFERED` | `1` |  |
| `PLANE_API_KEY` | `your_plane_api_key_here` |  |
| `PROJECTSTOOL` | `True` |  |
| `WORK_ITEMSTOOL` | `True` |  |
| `CYCLESTOOL` | `True` |  |
| `EPICSTOOL` | `True` |  |
| `MILESTONESTOOL` | `True` |  |
| `MODULESTOOL` | `True` |  |
| `STATESTOOL` | `True` |  |
| `USERSTOOL` | `True` |  |
| `WORKSPACESTOOL` | `True` |  |
| `INITIATIVESTOOL` | `True` |  |
| `INTAKETOOL` | `True` |  |
| `LABELSTOOL` | `True` |  |
| `PAGESTOOL` | `True` |  |
| `DEFAULT_AGENT_NAME` | `plane-agent` |  |
| `AGENT_UTILITIES_TESTING` | `False` |  |
| `GRAPH_BACKEND` | `networkx` |  |
| `LLM_API_KEY` | — |  |
| `LLM_BASE_URL` | — |  |
| `MCP_URL` | `http://localhost:8000/mcp` |  |
| `MODEL_ID` | `gpt-4o` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `condensed` | Tool surface: `condensed` | `verbose` | `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP auth (`oidc-client-credentials` for fleet calls) |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET` | — | OIDC client secret (service-account auth) |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_36 package + 10 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
<!-- ENV-VARS-TABLE:END -->


The Plane Agent supports the following environment variables for configuration and integration:

| Variable | Description |
|----------|-------------|
| `PLANE_BASE_URL` | The base URL of the Plane instance. |
| `PLANE_WORKSPACE_SLUG` | The workspace slug of the Plane workspace. |
| `PLANE_API_KEY` | The API key for authentication with Plane. |
| `MCP_URL` | The URL of the MCP server. |
| `MODEL_ID` | Default LLM model identifier (e.g. `gpt-4o`). |
| `PROVIDER` | The LLM provider (e.g. `openai`, `anthropic`). |
| `ENABLE_WEB_UI` | Set to `True` to enable the built-in Web UI. |
| `ENABLE_OTEL` | Set to `True` to enable OpenTelemetry telemetry. |
| `AGENT_UTILITIES_TESTING` | Set to `True` during testing to bypass production setups. |
| `AUTH_TYPE` | The authentication type to use (e.g., jwt, none). |
| `DEFAULT_API_KEY` | Default API key for fast server fallback authentication. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | The OpenTelemetry OTLP endpoint. |
| `PROJECTSTOOL` | Set to `True`/`False` to toggle the Projects tool module. |
| `WORK_ITEMSTOOL` | Set to `True`/`False` to toggle the Work Items tool module. |
| `CYCLESTOOL` | Set to `True`/`False` to toggle the Cycles tool module. |
| `EPICSTOOL` | Set to `True`/`False` to toggle the Epics tool module. |
| `MILESTONESTOOL` | Set to `True`/`False` to toggle the Milestones tool module. |
| `MODULESTOOL` | Set to `True`/`False` to toggle the Modules tool module. |
| `STATESTOOL` | Set to `True`/`False` to toggle the States tool module. |
| `USERSTOOL` | Set to `True`/`False` to toggle the Users tool module. |
| `WORKSPACESTOOL` | Set to `True`/`False` to toggle the Workspaces tool module. |
| `INITIATIVESTOOL` | Set to `True`/`False` to toggle the Initiatives tool module. |
| `INTAKETOOL` | Set to `True`/`False` to toggle the Intake tool module. |
| `LABELSTOOL` | Set to `True`/`False` to toggle the Labels tool module. |
| `PAGESTOOL` | Set to `True`/`False` to toggle the Pages tool module. |

---

## Installation

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `plane-agent[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `plane-agent[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `plane-agent[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "plane-agent[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "plane-agent[agent]"

# Everything (development)
uv pip install "plane-agent[all]"      # or: python -m pip install "plane-agent[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/plane-agent:mcp` | `--target mcp` | `plane-agent[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `plane-mcp` |
| `knucklessg1/plane-agent:latest` | `--target agent` (default) | `plane-agent[agent]` — **full** agent runtime + epistemic-graph engine | `plane-agent` |

```bash
docker build --target mcp   -t knucklessg1/plane-agent:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/plane-agent:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

---

## Documentation

The complete documentation is published as the
[official documentation site](https://knuckles-team.github.io/plane-agent/) and is the
recommended reference for installation, deployment, and day-to-day operation.

| Page | Contents |
|---|---|
| [Installation](https://knuckles-team.github.io/plane-agent/installation/) | pip, source, uv, prebuilt Docker image |
| [Deployment](https://knuckles-team.github.io/plane-agent/deployment/) | run the MCP server and agent, Compose, Caddy + Technitium, env config |
| [Usage](https://knuckles-team.github.io/plane-agent/usage/) | the MCP tools, the `Api` client, the CLI |
| [Backing Platform](https://knuckles-team.github.io/plane-agent/platform/) | deploy a self-hosted Plane instance with Docker |
| [Overview](https://knuckles-team.github.io/plane-agent/overview/) | ecosystem role, enterprise posture, architecture |
| [Concepts](https://knuckles-team.github.io/plane-agent/concepts/) | concept registry (`CONCEPT:PLANE-*`) |

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


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `plane-agent` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx plane-mcp` · or `uv tool install plane-agent` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/plane-agent:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
