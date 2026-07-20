# Deployment

<!-- BEGIN GENERATED: deployment-options -->
## Deployment Options

`plane-agent` supports local stdio, a loopback-only development listener, a
least-privilege stdio container, and a remote authenticated HTTPS boundary.
Provider endpoint, credential, selector, identity, and trust material are supplied
at runtime through `AgentConfig`; none is stored in this repository.

### Installed stdio process

```json
{
  "mcpServers": {
    "plane": {
      "command": "plane-mcp",
      "args": [],
      "env": {"MCP_TOOL_MODE": "intent"}
    }
  }
}
```

### Loopback development listener

```bash
plane-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

Do not expose this listener beyond loopback. Network deployments require direct TLS
or an explicitly trusted TLS-terminating ingress, configured authentication, exact
`MCP_ALLOWED_HOSTS`, and an exact trusted-proxy CIDR policy.

### Least-privilege local container

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  registry.example.invalid/plane-agent@sha256:<digest> plane-mcp
```

The operator projects the selected AgentConfig profile into the process at runtime;
the image remains immutable and contains no environment connection profile.

### Remote authenticated HTTPS endpoint

```json
{
  "mcpServers": {
    "plane": {"url": "https://service.example.invalid/mcp"}
  }
}
```

Store the real remote URL, outbound identity reference, and TLS-profile reference in
`AgentConfig`, not in MCP client JSON or documentation.
<!-- END GENERATED: deployment-options -->

This page covers running `plane-agent` as a long-lived service: the transports, the
optional A2A agent server, a Docker Compose stack, putting it behind a Caddy reverse
proxy, and giving it a DNS name with Technitium. To provision the **Plane platform**
it connects to, see [Backing Platform](platform.md).

> `plane-agent` ships an **MCP server** (console script `plane-mcp`) and a separate
> **A2A agent server** (console script `plane-agent`). The MCP server is the typed,
> deterministic tool surface; the agent server is a Pydantic-AI agent that connects
> to the MCP server over `MCP_URL` and exposes the tools conversationally.

## Run the MCP server

The transport is selected with `--transport` (or the `TRANSPORT` env var):

=== "stdio (default)"

    ```bash
    plane-mcp
    ```
    For IDE / desktop MCP clients that launch the server as a subprocess.

=== "streamable-http"

    ```bash
    plane-mcp --transport streamable-http --host 0.0.0.0 --port 8000
    ```
    A network server with a `/health` endpoint and `/mcp` route.

=== "sse"

    ```bash
    plane-mcp --transport sse --host 0.0.0.0 --port 8000
    ```

Health check (HTTP transports):

```bash
curl -s http://localhost:8000/health        # {"status":"OK"}
```

## Configuration (environment)

`plane-agent` is configured entirely from the environment. The **required** set:

| Var | Default | Meaning |
|---|---|---|
| `PLANE_BASE_URL` | `https://api.plane.so` | Plane API base URL |
| `PLANE_API_KEY` | _(unset)_ | Plane personal API key — required |
| `PLANE_WORKSPACE_SLUG` | _(unset)_ | Target workspace slug — required |
| `HOST` | `0.0.0.0` | Bind address (HTTP transports) |
| `PORT` | `8000` | Bind port (HTTP transports) |
| `TRANSPORT` | `stdio` | `stdio`, `streamable-http`, or `sse` |

Each Plane resource domain has its own **tool toggle** (default `True`) so you can
register only the surface you need: `PROJECTSTOOL`, `WORK_ITEMSTOOL`, `CYCLESTOOL`,
`EPICSTOOL`, `MILESTONESTOOL`, `MODULESTOOL`, `STATESTOOL`, `USERSTOOL`,
`WORKSPACESTOOL`, `INITIATIVESTOOL`, `INTAKETOOL`, `LABELSTOOL`, `PAGESTOOL`.

The full set — including telemetry (OTEL), access governance (Eunomia), and the
agent settings below — is documented in
[`.env.example`](https://github.com/Knuckles-Team/plane-agent/blob/main/.env.example).
Copy it to `.env` and fill in only what you use. The agent
**remains inactive when credentials are absent**.

### Backing Service

`plane-agent` connects to a Plane workspace. Plane is available both as a managed
SaaS ([Plane Cloud](https://app.plane.so/)) and as a self-hostable platform. When
using Plane Cloud only the connection configuration above is required; to deploy a
local Plane instance, see [Backing Platform](platform.md).

## Docker Compose

The repo ships [`docker/mcp.compose.yml`](https://github.com/Knuckles-Team/plane-agent/blob/main/docker/mcp.compose.yml).
It reads a sibling `.env` and publishes the HTTP server on `:8000`:

```yaml
services:
  plane-agent-mcp:
    image: example/plane-agent@sha256:<digest>
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
```

```bash
cp .env.example .env          # then edit PLANE_* values
docker compose -f docker/mcp.compose.yml up -d
docker compose -f docker/mcp.compose.yml logs -f
```

## Run the agent server

When `server_type` is **mcp+agent**, the A2A agent server is exposed through the
`plane-agent` console script and the
[`docker/agent.compose.yml`](https://github.com/Knuckles-Team/plane-agent/blob/main/docker/agent.compose.yml)
stack. The agent connects to the MCP server over `MCP_URL` and listens on port
`9004`:

```bash
# Locally — point the agent at a running MCP server
export MCP_URL=http://localhost:8000/mcp
export MODEL_ID=gpt-4o
export LLM_API_KEY=your_model_api_key
plane-agent --host 0.0.0.0 --port 9004
```

The `agent.compose.yml` stack runs both services together — the MCP server on
`:8000` and the agent on `:9004`, wired by container name:

```yaml
services:
  plane-agent-mcp:
    image: example/plane-agent@sha256:<digest>
    hostname: plane-agent-mcp
    env_file: [ ../.env ]
    environment:
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8000
    ports: ["8000:8000"]

  plane-agent-agent:
    image: example/plane-agent@sha256:<digest>
    depends_on: [ plane-agent-mcp ]
    command: [ "plane-agent" ]
    env_file: [ ../.env ]
    environment:
      - HOST=0.0.0.0
      - PORT=9004
      - MCP_URL=http://plane-agent-mcp:8000/mcp
      - MODEL_ID=${MODEL_ID:-gpt-4o}
    ports: ["9004:9004"]
```

```bash
docker compose -f docker/agent.compose.yml up -d
```

| Setting | Default | Meaning |
|---|---|---|
| `MCP_URL` | `http://localhost:8000/mcp` | MCP server the agent connects to |
| `MODEL_ID` | `gpt-4o` | Model the agent reasons with |
| `LLM_API_KEY` | _(unset)_ | Credential for the model provider |
| `LLM_BASE_URL` | _(unset)_ | Optional custom model endpoint |
| `PORT` | `9004` | Agent server port |

## Behind a Caddy reverse proxy

Expose the HTTP server on a hostname with automatic TLS. Add to your `Caddyfile`:

```caddy
# Internal (self-signed) — homelab .example.invalid zone
plane-agent.example.invalid {
    tls internal
    reverse_proxy plane-agent-mcp:8000
}
```

```caddy
# Public — automatic Let's Encrypt
plane-agent.example.com {
    reverse_proxy plane-agent-mcp:8000
}
```

Reload Caddy:

```bash
docker compose -f services/caddy/compose.yml exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## DNS with Technitium

Point the hostname at the host running Caddy. Via the Technitium API:

```bash
curl -s "http://technitium.example.invalid:5380/api/zones/records/add" \
  --data-urlencode "token=$TECHNITIUM_DNS_TOKEN" \
  --data-urlencode "domain=plane-agent.example.invalid" \
  --data-urlencode "zone=arpa" \
  --data-urlencode "type=A" \
  --data-urlencode "ipAddress=192.0.2.10" \
  --data-urlencode "ttl=3600"
```

…or add an **A record** `plane-agent.example.invalid → <caddy-host-ip>` in the Technitium web
console (`http://technitium.example.invalid:5380`). The ecosystem
[`technitium-dns-mcp`](https://knuckles-team.github.io/technitium-dns-mcp/) automates
this as a tool.

## Register with an MCP client

Add to your client's `mcp_config.json`:

```json
{
  "mcpServers": {
    "plane-agent": {
      "command": "uv",
      "args": ["run", "plane-mcp"],
      "env": {
        "PLANE_BASE_URL": "https://api.plane.so",
        "PLANE_API_KEY": "your_plane_api_key",
        "PLANE_WORKSPACE_SLUG": "your-workspace"
      }
    }
  }
}
```

For a remote HTTP server, point the client at `http://plane-agent.example.invalid/mcp` instead.
