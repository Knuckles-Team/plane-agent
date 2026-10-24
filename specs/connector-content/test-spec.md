# CONN-PLANE-AGENT-CONNECTOR-CONTENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R001` | `tests/test_default_content_surfaces.py` | The listings include the packaged skills, ontology and prompts. |
| T-002 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R002` | `tests/test_ontology_parent_link.py` | Every declared class reaches a parent class; the import of the parent IRI is present. |
| T-003 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003` | `tests/test_ingest_sources.py` | Each source names a read-only tool and maps to a declared record type. `work-items` maps to `Issue` with `state` and fans out per project. The ingest binding connector equals `connector_name("plane_agent")` (`plane-mcp`). |
| T-004 | `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R004` | `tests/test_cq_paths.py` | The test finds `state` and `priority` on `Issue` and no null mapping. |
