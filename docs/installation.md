# Installation

`plane-agent` is a standard Python package and a prebuilt container image. Pick the
path that matches how you want to run it.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable **Plane workspace** — either [Plane Cloud](https://app.plane.so/) or a
  self-hosted instance (see [Backing Platform](platform.md) to deploy one locally),
  plus a `PLANE_API_KEY` and `PLANE_WORKSPACE_SLUG`.

## From PyPI (recommended)

```bash
pip install plane-agent
```

The base install already pulls in `agent-utilities[agent,logfire]`, so both the
**MCP server** (`plane-mcp`) and the **A2A agent** (`plane-agent`) console scripts
are available immediately, with Logfire tracing enabled.

### Optional extras

| Extra | Install | Pulls in |
|---|---|---|
| `test` | `pip install "plane-agent[test]"` | `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-xdist` for the test suite |

```bash
# Typical: run the MCP server and the agent
pip install plane-agent
```

## From source

```bash
git clone https://github.com/Knuckles-Team/plane-agent.git
cd plane-agent
pip install -e ".[test]"          # editable install with the test extra
```

With [`uv`](https://docs.astral.sh/uv/):

```bash
uv pip install -e ".[test]"
uv run plane-mcp
```

## Prebuilt Docker image

A multi-stage, slim image is published on every release (entrypoint `plane-mcp`):

```bash
docker pull knucklessg1/plane-agent:latest

docker run --rm -i \
  -e PLANE_BASE_URL=https://api.plane.so \
  -e PLANE_API_KEY=your_plane_api_key \
  -e PLANE_WORKSPACE_SLUG=your-workspace \
  knucklessg1/plane-agent:latest        # stdio transport (default)
```

For an HTTP server with a published port and the agent server, see
[Deployment](deployment.md).

## Verify the install

```bash
plane-mcp --help
plane-agent --help
python -c "import plane_agent; print(plane_agent.__version__)"
```

## Next steps

- **[Deployment](deployment.md)** — run it as a long-lived MCP server and agent behind Caddy + DNS.
- **[Usage](usage.md)** — call the tools, the API, and the CLI.
- **[Configuration](deployment.md#configuration-environment)** — every environment variable.
