# CONN-PLANE-AGENT-CONNECTOR-CONTENT — The connector serves its packaged content

Owner: plane-agent. Cross-repo IDs: `SCION-CONNECTOR-CONTROL-R071`, `SCION-CONNECTOR-CONTROL-R073`.

## Purpose and user stories

The `plane-mcp` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

## Delivery mapping

Component: plane-agent connector

Code: ../../plane_agent/__init__.py

## Why a new spec

Searched `specs/` of `plane-agent` with `git grep` for the terms of this spec. No other spec of this repository owns the capability, so this spec owns it.

## User Scenarios & Testing

### User Story 1 - Default content (Priority: P1)

The fleet operator and the engine rely on this behaviour of `plane-agent`: `pyproject.toml` declares `plane-mcp` as the single `scion_sdk.connector` entry point. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `plane-agent` connector built from the default branch, **When** `tests/test_default_content_surfaces.py::test_default_content_surfaces` runs, **Then** `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt.

### User Story 2 - Ontology joins the parent graph (Priority: P1)

The fleet operator and the engine rely on this behaviour of `plane-agent`: Each `<package>/ontology/*.ttl` that declares classes imports `http://knuckles.team/kg`, and each class reaches an medulla parent class through `rdfs:subClassOf`. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `plane-agent` connector built from the default branch, **When** `tests/test_ontology_parent_link.py::test_ontology_joins_the_parent_graph` runs, **Then** the test parses each ontology and finds no orphan class beyond the pending list.

### User Story 3 - Declared ingest sources (Priority: P1)

The fleet operator and the engine rely on this behaviour of `plane-agent`: `plane_agent/connector_sources.py` declares the connector `plane-mcp` with `source_meta`. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `plane-agent` connector built from the default branch, **When** `tests/test_ingest_sources.py::test_declares_ingestible_sources` runs, **Then** the declaration names a read-only tool for each source, maps `work-items` to `Issue` with `state`, and fans out per project.

### User Story 4 - Competency-question paths (Priority: P2)

The fleet operator and the engine rely on this behaviour of `plane-agent`: `plane.ttl` declares `state` on `Issue` (the work-item type that the shared `WorkItem` parent carries `priority` and `state` for); `Workspace` extends `Namespace`, `Cycle` extends `Iteration`, `PlaneModule` (the Plane module, distinct from the code `Module`) extends `Collection` and `ProjectState` extends `Concept`; no `schema_mappings` entry has a null `ontology_class`. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `plane-agent` connector built from the default branch, **When** `tests/test_cq_paths.py::test_issue_carries_state_and_priority` runs, **Then** the test finds `state` and `priority` on `Issue` and no null mapping.

### User Story 5 - Owner and assignee edges (Priority: P2)

The fleet operator and the engine rely on this behaviour of `plane-agent`: The ingest sources declare edges with SDK `EdgeSpec`. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `plane-agent` connector built from the default branch, **When** `tests/test_catalog_edges.py::test_every_declared_edge_is_an_ontology_property_of_its_record_type` runs, **Then** `tests/test_catalog_edges.py::test_every_declared_edge_is_an_ontology_property_of_its_record_type` and `::test_project_and_work_item_references_become_lead_assignee_and_project_edges`.

### User Story 6 - Declare access contracts for the competency reads of plane-agent (Priority: P2)

The fleet operator and the engine rely on this behaviour of `plane-agent`: Subsystem: connector `plane-agent`. It is proven independently of the other stories.

**Acceptance Scenarios**:

1. **Given** the `plane-agent` connector built from the default branch, **When** `tests/test_access_contracts.py::test_competency_contracts_certified` runs, **Then** test: `tests/test_access_contracts.py::test_competency_contracts_certified` (L2) runs the connector ontology certification and validates each recording against its contract.

### Edge Cases

- The vendor service is unreachable or rejects the credential: the connector returns the SDK typed error and never a partial result.
- An argument outside the documented inputs is refused with the SDK typed refusal and causes no effect on the vendor service.

## Requirements

- **FR-001**: Default content. Rows: `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R001`.
- **FR-002**: Ontology joins the parent graph. Rows: `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R002`.
- **FR-003**: Declared ingest sources. Rows: `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003`.
- **FR-004**: Competency-question paths. Rows: `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R004`.
- **FR-005**: Owner and assignee edges. Rows: `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R005`.
- **FR-006**: Declare access contracts for the competency reads of plane-agent. Rows: `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R006`.

## Success Criteria

- **SC-001**: `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Rows: `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R001`.
- **SC-002**: The test parses each ontology and finds no orphan class beyond the pending list. Rows: `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R002`.
- **SC-003**: The declaration names a read-only tool for each source, maps `work-items` to `Issue` with `state`, and fans out per project. Rows: `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003`.
- **SC-004**: The test finds `state` and `priority` on `Issue` and no null mapping. Rows: `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R004`.
- **SC-005**: `tests/test_catalog_edges.py::test_every_declared_edge_is_an_ontology_property_of_its_record_type` and `::test_project_and_work_item_references_become_lead_assignee_and_project_edges`. Rows: `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R005`.
- **SC-006**: Test: `tests/test_access_contracts.py::test_competency_contracts_certified` (L2) runs the connector ontology certification and validates each recording against its contract. Rows: `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R006`.

## Assumptions

- The `plane-agent` package keeps the entry point and module layout named in the rows.
- The shared SDK supplies the transport, authentication, retry and certification helpers the rows reuse.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R001` | plan.md Production caller chain | T-001 | tests/test_default_content_surfaces.py::test_default_content_surfaces |
| FR-002 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R002` | plan.md Production caller chain | T-002 | tests/test_ontology_parent_link.py::test_ontology_joins_the_parent_graph |
| FR-003 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003` | plan.md Production caller chain | T-003 | tests/test_ingest_sources.py::test_declares_ingestible_sources |
| FR-004 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R004` | plan.md Production caller chain | T-004 | tests/test_cq_paths.py::test_issue_carries_state_and_priority |
| FR-005 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R005` | plan.md Production caller chain | T-005 | tests/test_catalog_edges.py::test_every_declared_edge_is_an_ontology_property_of_its_record_type |
| FR-006 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R006` | plan.md Production caller chain | T-006 | tests/test_access_contracts.py::test_competency_contracts_certified |
