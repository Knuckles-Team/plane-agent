# CONN-PLANE-AGENT-CONNECTOR-CONTENT — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R001` | **Default content.** `pyproject.toml` declares `plane-mcp` as the single `agent_connector_sdk.connector` entry point. The server lists the packaged `skill://` and `ontology://` resources and the packaged prompts with no `content=` argument. Proving test: `tests/test_default_content_surfaces.py`. | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. |
| `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R002` | **Ontology joins the parent graph.** Each `<package>/ontology/*.ttl` that declares classes imports `http://knuckles.team/kg`, and each class reaches an epistemic-graph parent class through `rdfs:subClassOf`. No class is pending. Proving test: `tests/test_ontology_parent_link.py`. | The test parses each ontology and finds no orphan class beyond the pending list. |
| `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003` | **Declared ingest sources.** `plane_agent/ontology/ingest_sources.json` declares the connector `plane-mcp` and its `projects` source (record type `SoftwareProject`, tool `plane_list_projects`), which loads with `agent_connector_sdk.ingest.sources.load_ingest_sources` and ships in the wheel. Proving test: `tests/test_ingest_sources.py`. | The declaration loads, names a tool the connector serves, and its record type has a `schema_mappings` entry in the connector manifest. |
| `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R004` | **Competency-question paths.** `plane.ttl` declares `state` on `Issue` (the work-item type that the shared `WorkItem` parent carries `priority` and `state` for); `Workspace` extends `Namespace`, `Cycle` extends `Iteration`, `PlaneModule` (the Plane module, distinct from the code `Module`) extends `Collection` and `ProjectState` extends `Concept`; no `schema_mappings` entry has a null `ontology_class`. Proving test: `tests/test_cq_paths.py`. | The test finds `state` and `priority` on `Issue` and no null mapping. |
