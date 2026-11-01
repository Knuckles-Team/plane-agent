# CONN-PLANE-AGENT-CONNECTOR-CONTENT — Implementation plan

Governing spec: [spec.md](spec.md). Rows: [requirements.md](requirements.md).

## Summary

This plan states how `plane-agent` delivers the rows of `CONN-PLANE-AGENT-CONNECTOR-CONTENT`. The live caller is the `plane-mcp` console script. The owner is the `plane_agent` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

## Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 6 active row(s) in this spec

## Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

## Project Structure

- `pyproject.toml` (existing)
- `plane_agent/__init__.py` (existing)
- `plane_agent/ontology/plane.ttl` (existing)
- `tests/test_ontology_parent_link.py` (existing)
- `plane_agent/connector_sources.py` (existing)
- `plane_agent/kg_ingest.py` (existing)
- `plane_agent/ontology/mappings/source.yaml` (existing)
- `tests/test_ingest_sources.py` (existing)
- `tests/test_cq_paths.py` (existing)
- `tests/test_catalog_edges.py` (existing)
- `plane_agent/ontology/access_contracts.ttl` (existing)
- `plane_agent/mcp_server.py` (existing)
- `tests/test_access_contracts.py` (existing)
- `tests/test_default_content_surfaces.py` (new, planned)

## Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

## Phase 1: Design

### Summary

This plan states how `plane-agent` delivers the rows of `CONN-PLANE-AGENT-CONNECTOR-CONTENT`. The live caller is the `plane-mcp` console script. The owner is the `plane_agent` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

### Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 6 active row(s) in this spec

### Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

### Project Structure

- `pyproject.toml` (existing)
- `plane_agent/__init__.py` (existing)
- `tests/test_ontology_parent_link.py` (existing)
- `plane_agent/connector_sources.py` (existing)
- `plane_agent/kg_ingest.py` (existing)
- `plane_agent/ontology/mappings/source.yaml` (existing)
- `tests/test_ingest_sources.py` (existing)
- `tests/test_kg_ingest.py` (existing)
- `tests/test_cq_paths.py` (existing)
- `tests/test_catalog_edges.py` (existing)
- `plane_agent/ontology/access_contracts.ttl` (existing)
- `plane_agent/mcp_server.py` (existing)
- `tests/test_access_contracts.py` (existing)
- `tests/test_default_content_surfaces.py` (new, planned)

### Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

### Phase 1: Design

### Summary

This plan states how `plane-agent` delivers the rows of `CONN-PLANE-AGENT-CONNECTOR-CONTENT`. The live caller is the `plane-mcp` console script. The owner is the `plane_agent` package. The rows reuse the `scion-sdk` helpers and add no second authority. The plan changes no runtime code.

### Technical Context

- **Language/Version**: Python >=3.12, <3.15
- **Primary Dependencies**: scion-sdk[mcp]>=0.6.4,<0.7.0; fastmcp; further pins in `pyproject.toml` (scion-sdk[mcp]>=0.6.4,<0.7.0, requests>=2.34.2)
- **Storage**: N/A, the connector keeps no store of its own
- **Testing**: pytest; each row names the proving test as `path::name`
- **Target Platform**: Linux container and stdio or streamable HTTP MCP clients
- **Project Type**: connector
- **Performance Goals**: N/A, the vendor service sets the latency
- **Constraints**: vendor calls go through the SDK governed client; no connector-local transport
- **Scale/Scope**: 6 active row(s) in this spec

### Constitution Check

- Organization constitution 1.5.0, spec-first change: pass. Every behaviour is a row of this spec with a bound or planned test.
- Repository article R-I, connector scope: pass. The rows stay inside this connector's one external system and reuse the SDK for shared capabilities.

### Project Structure

- `pyproject.toml` (existing)
- `plane_agent/__init__.py` (existing)
- `tests/test_ontology_parent_link.py` (existing)
- `plane_agent/connector_sources.py` (existing)
- `plane_agent/kg_ingest.py` (existing)
- `plane_agent/ontology/mappings/source.yaml` (existing)
- `tests/test_ingest_sources.py` (existing)
- `tests/test_kg_ingest.py` (existing)
- `tests/test_cq_paths.py` (existing)
- `tests/test_catalog_edges.py` (existing)
- `plane_agent/ontology/access_contracts.ttl` (existing)
- `plane_agent/mcp_server.py` (existing)
- `tests/test_access_contracts.py` (existing)
- `tests/test_default_content_surfaces.py` (new, planned)

### Phase 0: Research

No unknowns. Every row names its code and test; the caller chain of each row was read from the code.

### Phase 1: Design

### Architecture

`pyproject.toml` declares `plane-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `plane_agent` from it.

### Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

### Complexity Tracking

None. The constitution check passed.

### Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

### Production caller chain

- `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R001`: `plane-mcp` in `pyproject.toml` runs `scion_sdk.cli:serve`, which builds the server from the `scion_sdk.connector` entry point `plane_agent:connector` (`plane_agent/__init__.py:6`); the SDK `Connector` then lists the packaged skills, ontology and prompts.
- `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R006`: arbora `fleet.call` reaches the existing read tool of `plane_agent/mcp_server.py`, whose result is validated against the `ac:AccessContract` rows declared in `plane_agent/ontology/access_contracts.ttl`.

### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

### Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

### Complexity Tracking

None. The constitution check passed.

### Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

### Production caller chain

- `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R001`: `plane-mcp` in `pyproject.toml` runs `scion_sdk.cli:serve`, which builds the server from the `scion_sdk.connector` entry point `plane_agent:connector` (`plane_agent/__init__.py:6`); the SDK `Connector` then lists the packaged skills, ontology and prompts.
- `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R006`: arbora `fleet.call` reaches the existing read tool of `plane_agent/mcp_server.py`, whose result is validated against the `ac:AccessContract` rows declared in `plane_agent/ontology/access_contracts.ttl`.

### Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.

## Phase 2: Task approach

`tasks.md` holds one task per row, producer first. Rows that depend on none run in parallel. A task is checked when its `Spec:` trailer is on the default branch.

## Complexity Tracking

None. The constitution check passed.

## Build contract

- `pre-commit run --all-files` runs ruff check, ruff format, the shared `connector-standard`, `spec`, `secrets` and `dependency-readiness` gates at the pinned shared revision.
- `uv run pytest tests` runs the proving tests; the shared complexity, duplication and KISS gates apply their org thresholds and this repository sets no local override.
- A change adds no scanner suppression and no duplicate implementation of an SDK helper.

## Production caller chain

- `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R001`: `plane-mcp` in `pyproject.toml` runs `scion_sdk.cli:serve`, which builds the server from the `scion_sdk.connector` entry point `plane_agent:connector` (`plane_agent/__init__.py:6`); the SDK `Connector` then lists the packaged skills, ontology and prompts.
- `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R002`: the SDK ontology loader reads `plane_agent/ontology/` when the server builds the `connector` object (`plane_agent/__init__.py:6`).
- `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003`: the SDK source ingest runner reads the declaration of `plane_agent/connector_sources.py` (served at `connector://resources`) and calls the read-only tools `plane_list_projects`, `plane_list_work_items` and `plane_list_states`.
- `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R004`: the SDK ontology loader reads `plane_agent/ontology/` when the server builds the `connector` object (`plane_agent/__init__.py:6`).
- `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R005`: the SDK source ingest runner reads the `EdgeSpec` declarations of `plane_agent/connector_sources.py` and writes the edges while it ingests `projects` and `work-items`.
- `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R006`: arbora `fleet.call` reaches the existing read tool of `plane_agent/mcp_server.py`, whose result is validated against the `ac:AccessContract` rows declared in `plane_agent/ontology/access_contracts.ttl`.

## Cross-repo seams

None. The rows depend only on the published `scion-sdk` package, which the connector imports.
