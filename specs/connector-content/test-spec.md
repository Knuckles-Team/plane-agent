# CONN-PLANE-AGENT-CONNECTOR-CONTENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R001` | `tests/test_default_content_surfaces.py::test_default_content_surfaces` (planned) | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. |
| T-002 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R002` | `tests/test_ontology_parent_link.py::test_ontology_joins_the_parent_graph` | The test parses each ontology and finds no orphan class beyond the pending list. |
| T-003 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003` | `tests/test_ingest_sources.py::test_declares_ingestible_sources` | The declaration names a read-only tool for each source, maps `work-items` to `Issue` with `state`, and fans out per project. |
| T-004 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R004` | `tests/test_cq_paths.py::test_issue_carries_state_and_priority` | The test finds `state` and `priority` on `Issue` and no null mapping. |
| T-005 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R005` | `tests/test_catalog_edges.py::test_every_declared_edge_is_an_ontology_property_of_its_record_type` | `tests/test_catalog_edges.py::test_every_declared_edge_is_an_ontology_property_of_its_record_type` and `::test_project_and_work_item_references_become_lead_assignee_and_project_edges`. |
| T-006 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R006` | `tests/test_access_contracts.py::test_competency_contracts_certified` (planned) | Test: `tests/test_access_contracts.py::test_competency_contracts_certified` (L2) runs the connector ontology certification and validates each recording against its contract. |

## Negative and boundary cases

Each proving test above includes the refusal or error case that its row names. A vendor outage or an unauthorised call must return the SDK typed error.

## Quality and release proof

Run `uv run pytest tests` and `pre-commit run --all-files` from the repository root. A planned test is added by the code change that lands the row.
