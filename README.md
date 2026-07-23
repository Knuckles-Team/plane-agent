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

*Version: 2.0.0*

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

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the connector-focused `[mcp]` extra.** Examples use `plane-agent[mcp]` to add
> FastMCP / FastAPI through `agent-utilities[mcp]`; the required Agent Utilities core
> still carries `epistemic-graph[full]`. The `[agent-runtime]` extra additionally
> enables model orchestration.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "plane-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "plane-agent[mcp]",
        "plane-mcp"
      ],
      "env": {
        "MCP_TOOL_MODE": "intent",
        "CYCLESTOOL": "True",
        "EPICSTOOL": "True",
        "INITIATIVESTOOL": "True",
        "INTAKETOOL": "True",
        "KGTOOL": "True",
        "LABELSTOOL": "True",
        "MILESTONESTOOL": "True",
        "MODULESTOOL": "True",
        "PAGESTOOL": "True",
        "PLANE_API_KEY": "your_plane_api_key_here",
        "PLANE_BASE_URL": "https://api.plane.so",
        "PLANE_KG_INGEST": "true",
        "PLANE_TLS_PROFILE": "system",
        "PROJECTSTOOL": "True",
        "STATESTOOL": "True",
        "USERSTOOL": "True",
        "WORKSPACESTOOL": "True",
        "WORK_ITEMSTOOL": "True"
      }
    }
  }
}
```

Runtime references require an alias-aware launcher such as GraphOS. Other
launchers must omit those entries and inject the resolved values through their
own runtime secret boundary.

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "plane-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "plane-agent[mcp]",
        "plane-mcp",
        "--transport",
        "streamable-http",
        "--port",
        "8000"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "MCP_TOOL_MODE": "intent",
        "CYCLESTOOL": "True",
        "EPICSTOOL": "True",
        "INITIATIVESTOOL": "True",
        "INTAKETOOL": "True",
        "KGTOOL": "True",
        "LABELSTOOL": "True",
        "MILESTONESTOOL": "True",
        "MODULESTOOL": "True",
        "PAGESTOOL": "True",
        "PLANE_API_KEY": "your_plane_api_key_here",
        "PLANE_BASE_URL": "https://api.plane.so",
        "PLANE_KG_INGEST": "true",
        "PLANE_TLS_PROFILE": "system",
        "PROJECTSTOOL": "True",
        "STATESTOOL": "True",
        "USERSTOOL": "True",
        "WORKSPACESTOOL": "True",
        "WORK_ITEMSTOOL": "True"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed Streamable-HTTP instance by `url`:

```json
{
  "mcpServers": {
    "plane-mcp": {
      "url": "http://localhost:8000/plane-mcp/mcp"
    }
  }
}
```

Run a reviewed container image as a least-privilege stdio child (no
listener or published port):

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  -e MCP_TOOL_MODE=intent \
  -e CYCLESTOOL=True \
  -e EPICSTOOL=True \
  -e INITIATIVESTOOL=True \
  -e INTAKETOOL=True \
  -e KGTOOL=True \
  -e LABELSTOOL=True \
  -e MILESTONESTOOL=True \
  -e MODULESTOOL=True \
  -e PAGESTOOL=True \
  -e PLANE_API_KEY=your_plane_api_key_here \
  -e PLANE_BASE_URL=https://api.plane.so \
  -e PLANE_KG_INGEST=true \
  -e PLANE_TLS_PROFILE=system \
  -e PROJECTSTOOL=True \
  -e STATESTOOL=True \
  -e USERSTOOL=True \
  -e WORKSPACESTOOL=True \
  -e WORK_ITEMSTOOL=True \
  registry.example.invalid/plane-agent@sha256:<digest> plane-mcp
```

For containerized network HTTP, supply an authenticated TLS ingress (or
direct server TLS), exact `MCP_ALLOWED_HOSTS`, and an exact trusted-proxy
CIDR policy through the operator-owned deployment profile. The generator
does not emit an unauthenticated non-loopback listener.

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`plane-agent` can run as a local stdio process or container, or behind a remote
network boundary. The
[Deployment guide](https://knuckles-team.github.io/plane-agent/deployment/) carries
the detailed transport contract.

- **Local container** — launch a reviewed immutable image as a least-privilege
  stdio child with no listener or published port.
- **Remote URL** — connect through an operator-supplied authenticated HTTPS
  ingress. Keep its URL, outbound identity references, trust profile, and exact
  `MCP_ALLOWED_HOSTS` in `AgentConfig`.
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
    image: example/plane-agent:mcp
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
    image: example/plane-agent@sha256:<digest>
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
| `OTEL_EXPORTER_OTLP_PUBLIC_KEY` | secret-injected |  |
| `OTEL_EXPORTER_OTLP_SECRET_KEY` | secret-injected |  |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |  |
| `EUNOMIA_TYPE` | `none` | options: none, embedded, remote |
| `EUNOMIA_POLICY_FILE` | `mcp_policies.json` |  |
| `EUNOMIA_REMOTE_URL` | `http://eunomia-server:8000` |  |
| `PLANE_BASE_URL` | `https://api.plane.so` |  |
| `PLANE_WORKSPACE_SLUG` | — |  |
| `PLANE_TLS_PROFILE` | `system` | Named outbound TLS policy from AgentConfig. Use a reference for runtime-only trust material; peer and hostname verification remain mandatory. |
| `PLANE_TLS_PROFILE_REF` | — |  |
| `PLANE_KG_INGEST` | `true` |  |
| `DEBUG` | `False` |  |
| `PYTHONUNBUFFERED` | `1` |  |
| `PLANE_API_KEY` | secret-injected |  |
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
| `KGTOOL` | `True` |  |

#### Inherited agent-utilities variables (apply to every connector)

| Variable | Example | Description |
|----------|---------|-------------|
| `MCP_TOOL_MODE` | `intent` | Tool surface: `intent` \| `condensed` \| `verbose` \| `both` |
| `MCP_ENABLED_TOOLS` | — | Comma-separated tool allow-list |
| `MCP_DISABLED_TOOLS` | — | Comma-separated tool deny-list |
| `MCP_ENABLED_TAGS` | — | Comma-separated tag allow-list |
| `MCP_DISABLED_TAGS` | — | Comma-separated tag deny-list |
| `MCP_CLIENT_AUTH` | — | Outbound MCP child auth: `oidc-client-credentials` \| `basic` \| `none` |
| `OIDC_CLIENT_ID` | — | OIDC client id (service-account auth) |
| `OIDC_CLIENT_SECRET_REF` | `secret://identity/oidc-client-secret` | Runtime secret reference for the OIDC service account |
| `MCP_BASIC_AUTH_USERNAME` | — | HTTP Basic username (`MCP_CLIENT_AUTH=basic`) |
| `MCP_BASIC_AUTH_PASSWORD_REF` | `secret://identity/mcp-basic-password` | Runtime secret reference for HTTP Basic auth (`MCP_CLIENT_AUTH=basic`) |
| `MCP_URL` | `http://localhost:8000/mcp` | URL of the MCP server the agent connects to |
| `PROVIDER` | `openai` | LLM provider for the agent |
| `MODEL_ID` | `gpt-4o` | Model id for the agent |
| `ENABLE_WEB_UI` | `True` | Serve the AG-UI web interface |

_33 package + 14 inherited variable(s). Auto-generated from `.env.example` + the shared agent-utilities set — do not edit._
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
| `plane-agent[mcp]` | Connector-focused MCP server (`agent-utilities[mcp]` — FastMCP/FastAPI + `epistemic-graph[full]`) | You only run the **MCP server** (smallest install / image) |
| `plane-agent[agent]` | Agent runtime (`agent-utilities[agent-runtime,logfire]` — model orchestration + `epistemic-graph[full]`) | You run the **integrated agent** |
| `plane-agent[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

```bash
# Connector-focused MCP server (includes the shared graph engine)
uv pip install "plane-agent[mcp]"

# Agent runtime (adds model orchestration to the shared graph engine)
uv pip install "plane-agent[agent]"

# Everything (development)
uv pip install "plane-agent[all]"      # or: python -m pip install "plane-agent[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `example/plane-agent:mcp` | `--target mcp` | `plane-agent[mcp]` — **connector-focused**, includes `epistemic-graph[full]`; no model-orchestration stack | `plane-mcp` |
| `example/plane-agent@sha256:<digest>` | `--target agent` (default) | `plane-agent[agent]` — **agent runtime**, model orchestration + `epistemic-graph[full]` | `plane-agent` |

```bash
docker build --target mcp   -t example/plane-agent:mcp    docker/   # connector-focused MCP server
docker build --target agent -t example/plane-agent:agent-local docker/   # agent runtime
```

`docker/mcp.compose.yml` runs the connector-focused `:mcp` server; `docker/agent.compose.yml` runs the
agent (`immutable agent digest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

Both `[mcp]` and `[agent]` carry the **epistemic-graph** engine through the required
Agent Utilities core dependency (`epistemic-graph[full]`). The `[mcp]` extra keeps
the server connector-focused; `[agent]` additionally enables model orchestration. Local
deployments can use the bundled engine. For production or shared state, run
**epistemic-graph as a dedicated database service** and configure the runtime to use it.
Deployment recipes (single-node + Raft HA), connection configuration, and architecture
diagrams are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).

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

<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=example&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/example)
![GitHub User's stars](https://img.shields.io/github/stars/example)

---

## Contribute

Contributions are welcome! Please ensure code quality by executing local checks before submitting pull requests:
- Format code using `ruff format .`
- Lint code using `ruff check .`
- Validate type-safety with `mypy .`
- Execute test suites using `pytest`


<!-- BEGIN agent-utilities-deployment (generated; do not edit between markers) -->

## Deploy with `agent-utilities-deployment`

Provision this package with the consolidated **`agent-utilities-deployment`**
workflow. It selects an installed-package, editable-source, or immutable-container
path; records only runtime secret and TLS-profile references in `AgentConfig`; and
runs doctor, registration, policy, observability, and rollback gates. Ask your agent
to **"deploy `plane-agent` with agent-utilities-deployment"**.

| Install mode | Command |
|------|---------|
| Installed package | `uv tool install "plane-agent[mcp]"`, then run `plane-mcp` |
| Editable source | `uv pip install -e ".[agent]"`, then run `plane-mcp` |
| Immutable container | deploy `registry.example.invalid/plane-agent@sha256:<digest>` through the operator-selected orchestrator |

The repository embeds no deployment profile, credential value, certificate path, or
environment-specific endpoint. Supply those at runtime through `AgentConfig` and the
configured secret provider.

<!-- END agent-utilities-deployment -->

<!-- GOVERNED-CAPABILITY:START -->
## Governed capability contract

This package ships a compact canonical skill surface with specialist procedures
kept as referenced workflows. The current MCP tools, skill metadata,
`connector_manifest.yml`, ontology, mappings, shapes, fixtures, migrations,
tool-schema fingerprints, and certification metadata form one versioned
capability contract. Validate them together; do not rely on stale tool names or
historical per-task skill wrappers.

Runtime endpoints, credentials, certificate trust, tenant identity, retention,
and observability policy are deployment inputs and are never packaged values.
See [Configuration, trust, and privacy](docs/configuration.md) before enabling a
network transport, connector ingestion, GraphOS delegation, or trace export.
<!-- GOVERNED-CAPABILITY:END -->
