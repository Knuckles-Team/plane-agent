---
name: plane-agent-development
skill_type: skill
domain: development
description: >-
  Develop, test, gate, and release the plane-agent connector while preserving
  its SDK Connector boundary, Plane API mappings, workspace authentication,
  packaged content, and source-backed publication contract.
license: MIT
tags: [plane-agent, development, connector, test, gates, plane]
tier: repository
metadata:
  author: Repository Maintainers
  version: '0.1.0'
---

# Plane Agent development

This repository owns the Plane transport, API mappings, MCP action tools,
knowledge-graph ingestion mappings, packaged skills, and connector
documentation. Shared connector transport and admission behavior belongs to
the SDK and its owning repositories. Read `AGENTS.md` before changing code;
keep credentials, private endpoints, and generated runtime data out of source,
logs, and skill content.

## Repository map and runtime boundary

- `plane_agent/__init__.py` creates the `agent-connector-sdk` `Connector` with
  `Api`, `get_client`, and `plane_agent.mcp_server` as its tool module.
  Preserve the connector identity and the `plane-mcp` entry points in
  `pyproject.toml`.
- `plane_agent/mcp_server.py` owns the action-routed `plane_*` MCP tools and
  the best-effort list-flow KG ingestion. Preserve action names, parameter
  JSON shapes, tool tags, and the `PLANE_KG_INGEST` default-on behavior.
- `plane_agent/api_client.py` composes the domain clients in `plane_agent/api/`
  for projects, work items, cycles, epics, initiatives, intake, milestones,
  modules, states, and workspaces. Reuse these clients rather than adding a
  second HTTP path.
- `plane_agent/auth.py` reads `PLANE_BASE_URL`, `PLANE_API_KEY`,
  `PLANE_WORKSPACE_SLUG`, `PLANE_TLS_PROFILE`, and
  `PLANE_TLS_PROFILE_REF`. Authentication failures must remain typed and must
  not expose the API key or TLS material.
- `plane_agent/ontology/plane.ttl`, `plane_agent/prompts/`,
  `plane_agent/connectors/`, and `plane_agent/skills/` are packaged content.
  `pyproject.toml` already includes these trees through `skills/**`,
  `ontology/**`, `connectors/**`, and `prompts/**` package data.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver small, reviewable slices and cite the
owning spec row in the commit trailer. This skill supplies the repository
contract for `PIPE-CONNSPEC-R152.4`.

- Find the owning row first with `git grep -n "<term>" -- specs` and extend
  that spec before adding new requirement text.
- Inspect the SDK `Connector`, action dispatch, domain client, auth/TLS path,
  package-data declaration, and focused tests before changing runtime or
  packaged content.
- Keep changes inside this connector. SDK transport, shared Pages rendering,
  admission, and durable graph state belong to their owner repositories.
- Preserve workspace scoping through `PLANE_WORKSPACE_SLUG`, the governed TLS
  profile, action payload schemas, ontology mappings, and the existing
  best-effort KG ingestion boundary.
- Every delivered local requirement needs a bound test. Generated
  `specs/*/status.json` files are produced by `pipelines-hook spec-status`; do
  not edit them by hand.
- Run focused tests through the narrow test-slot wrapper and run repository
  hooks normally. Never use `--no-verify`, skip gates, or live credentials.

## Setup and focused gates

From the repository root:

```bash
uv sync --locked

/var/tmp/arbora-delivery/scale/run-narrow-test-slot.sh \
  uv run --locked --extra test pytest -q \
    tests/test_publication_workflow.py \
    tests/test_action_discovery.py \
    tests/test_access_contracts.py \
    tests/test_ingest_sources.py \
    tests/test_startup.py

uvx pre-commit run --all-files
uvx pre-commit run --all-files --hook-stage pre-push
```

Mock Plane responses in tests. Do not use `PLANE_API_KEY` or a live Plane
workspace in local validation.

## Pages and package publication

`.github/workflows/pages.yml` is the repository's Pages caller. It invokes
`Knuckles-Team/pipelines/.github/workflows/pages_pipeline.yml@main` with
`content_source: docs`, `spec_dashboard_enabled: true`, and
`.github/spec-dashboard.json`. The workflow rebuilds for documentation, specs,
the dashboard configuration, and the caller itself. The dashboard source is
the v1 `specs/*/status.json` set.

The package workflow owns release publication through the shared connector and
container callers. Keep its existing `connector: true` and
`render_connector: true` flags intact when changing publication wiring.

After a merge, verify the exact successful Pages run and then inspect the
public `/spec-delivery/` page and `snapshot.json` over HTTPS. Local source
inspection does not prove a served deployment.

## Change discipline

- Keep Plane API calls, MCP schemas, auth settings, TLS resolution, ontology
  mappings, and metadata ingestion under their existing boundaries.
- Use injected `PLANE_*` configuration only. Never print or commit API keys,
  workspace secrets, private URLs, TLS material, or generated state.
- Preserve the current action-to-client mappings and workspace scope. Mock
  external calls and assert typed failures for missing credentials.
- Keep generated status files under the Pipelines/status owner; this skill does
  not authorize editing `specs/*/status.json`.
