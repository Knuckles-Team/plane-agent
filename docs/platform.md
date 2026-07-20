# Backing Platform — Plane

`plane-agent` is a **client** of a Plane workspace. Plane is available as a managed
SaaS ([Plane Cloud](https://app.plane.so/)) and as a self-hostable platform. This
page provides a Docker recipe for deploying a local Plane instance to serve as the
target of `PLANE_BASE_URL`. For production topologies, follow the upstream
[Plane self-hosting documentation](https://docs.plane.so/self-hosting/overview).

!!! note "Backing-system recipe"
    Each connector in the ecosystem follows the same convention — a
    `docs/platform.md` recipe for the system it integrates with, accompanied by a
    sample Compose stack that mirrors [`services/`](https://github.com/Knuckles-Team).
    Systems offered only as a managed service have no local recipe; Plane offers
    both managed and self-hosted options.

## Single-node deployment (Compose)

Plane publishes an all-in-one community image. The following stack runs the Plane
application alongside its PostgreSQL, Redis, RabbitMQ, and MinIO dependencies:

```yaml
# docker/plane.compose.yml
services:
  plane-aio:
    image: artifacts.plane.so/makeplane/plane-aio-community:stable
    environment:
      DOMAIN_NAME: "plane.example.invalid"
      DATABASE_URL: "postgresql://plane:plane@plane-db:5432/plane"
      REDIS_URL: "redis://plane-redis:6379"
      AMQP_URL: "amqp://plane:plane@plane-mq:5672/plane"
      FILE_SIZE_LIMIT: "10485760"
      AWS_REGION: "us-east-1"
      AWS_ACCESS_KEY_ID: "${MINIO_ACCESS_KEY}"
      AWS_SECRET_ACCESS_KEY: "${MINIO_SECRET_KEY}"
      AWS_S3_BUCKET_NAME: "plane-app"
      AWS_S3_ENDPOINT_URL: "http://minio:9000"
    ports:
      - "80:80"
    depends_on: [ plane-db, plane-redis, plane-mq, minio ]

  minio:
    image: docker.io/minio/minio@sha256:<digest>
    environment:
      MINIO_ROOT_USER: ${MINIO_ACCESS_KEY}
      MINIO_ROOT_PASSWORD: ${MINIO_SECRET_KEY}
    command: server /data --console-address ":9001"
    volumes: [ "plane_minio:/data" ]

  plane-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: plane
      POSTGRES_PASSWORD: plane
      POSTGRES_DB: plane
    volumes: [ "plane_db:/var/lib/postgresql/data" ]

  plane-redis:
    image: redis:7-alpine
    volumes: [ "plane_redis:/data" ]

  plane-mq:
    image: rabbitmq:3-management-alpine
    environment:
      RABBITMQ_DEFAULT_USER: plane
      RABBITMQ_DEFAULT_PASS: plane
      RABBITMQ_DEFAULT_VHOST: plane
    volumes: [ "plane_mq:/var/lib/rabbitmq" ]

volumes:
  plane_db:
  plane_redis:
  plane_mq:
  plane_minio:
```

```bash
docker compose -f docker/plane.compose.yml up -d

# Wait for the application to answer
curl -sf http://localhost/ >/dev/null && echo "Plane is up"
```

Once the instance is running, sign in to the web UI, create a workspace, and
generate a personal API key from your account settings — these become
`PLANE_WORKSPACE_SLUG` and `PLANE_API_KEY`.

## Connect plane-agent

```bash
export PLANE_BASE_URL=http://localhost          # your self-hosted instance
export PLANE_API_KEY=your_plane_api_key
export PLANE_WORKSPACE_SLUG=your-workspace

plane-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

## Combined deployment

A combined stack places the Plane instance and the MCP server on one Docker network,
so the server reaches Plane by container name:

```yaml
# docker/stack.compose.yml
services:
  plane-aio:
    image: artifacts.plane.so/makeplane/plane-aio-community:stable
    hostname: plane-aio
    ports: ["80:80"]
    # …database / redis / mq / minio as above…

  plane-agent-mcp:
    image: example/plane-agent@sha256:<digest>
    depends_on: [ plane-aio ]
    environment:
      - PLANE_BASE_URL=http://plane-aio
      - PLANE_API_KEY=your_plane_api_key
      - PLANE_WORKSPACE_SLUG=your-workspace
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8000
    ports: ["8000:8000"]
```

```bash
docker compose -f docker/stack.compose.yml up -d
```

A homelab-oriented stack — placement constraints, the `caddy` ingress network, and
persistent volumes under `${APPS_DIR}` — is maintained at
[`services/plane`](https://github.com/Knuckles-Team).
