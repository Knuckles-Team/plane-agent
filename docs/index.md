# plane-agent

Plane project-management **MCP server + A2A agent** for the agent-utilities
ecosystem — typed, deterministic tools over the Plane REST API for projects,
work items, cycles, modules, and the rest of the Plane work-management surface.

!!! info "Official documentation"
    This site is the canonical reference for `plane-agent`, maintained alongside every
    release.

[![PyPI](https://img.shields.io/pypi/v/plane-agent)](https://pypi.org/project/plane-agent/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/plane-agent)](https://github.com/Knuckles-Team/plane-agent/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/plane-agent)

## Overview

`plane-agent` wraps the [Plane](https://plane.so/) REST API with typed,
deterministic MCP tools and ships an optional A2A agent server that drives those
tools conversationally. It provides:

- **`Api`** — a composed REST client (`plane_agent.api_client.Api`) over the Plane
  workspace API, organized by domain (projects, work items, cycles, modules,
  states, initiatives, intake, milestones, workspaces).
- **A broad MCP tool surface** — action-routed tool domains for every Plane
  resource, gated individually by `*TOOL` environment toggles.
- **An A2A agent server** (`plane-agent` console script) that connects to the MCP
  server over `MCP_URL` and exposes the tools to a Pydantic-AI agent.

The agent **remains inactive when credentials are absent** — a `PLANE_API_KEY`
and `PLANE_WORKSPACE_SLUG` are required before any tool will execute.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, uv, and the prebuilt Docker image.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP server and agent, Docker Compose, Caddy + Technitium.
- :material-console: **[Usage](usage.md)** — the MCP tools, the `Api` client, and the CLI.
- :material-database-cog: **[Backing Platform](platform.md)** — deploy a self-hosted Plane instance with Docker.
- :material-sitemap: **[Overview](overview.md)** — ecosystem role, enterprise posture, and architecture.
- :material-tag-multiple: **[Concepts](concepts.md)** — the `CONCEPT:PLANE-*` registry.

</div>

## Quick start

```bash
pip install plane-agent
plane-mcp                       # stdio MCP server (default transport)
```

Connect it to a Plane workspace:

```bash
export PLANE_BASE_URL=https://api.plane.so
export PLANE_API_KEY=your_plane_api_key
export PLANE_WORKSPACE_SLUG=your-workspace
plane-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

See **[Installation](installation.md)** and **[Deployment](deployment.md)** for the
full matrix (PyPI install, Docker image, all transports, the agent server, reverse
proxy, DNS).
