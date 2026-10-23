# CONN-PLANE-AGENT-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `plane-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `plane_agent` from it.
