# CONN-PLANE-AGENT-CONNECTOR-CONTENT — Data model

Entities and records that the rows add or declare.

| Row | Entity or record | Definition |
|---|---|---|
| `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R002` | Ontology joins the parent graph | Each `<package>/ontology/*.ttl` that declares classes imports `https://knuckles-team.github.io/ontology/core`, and each class reaches an medulla parent class through `rdfs:subClassOf`. |
| `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R004` | Competency-question paths | `plane_agent/ontology/plane.ttl` declares `state` on `Issue` (the work-item type that the shared `WorkItem` parent carries `priority` and `state` for); `Workspace` extends `Namespace`, `Cycle` extends `Iteration`, `PlaneModule` (the Plane module, distinct from the code `Module`) extends `Collection` and `ProjectState` extends `Concept`; no `schema_mappings` entry has a null `ontology_class`. |
| `CONN-PLANE-AGENT-CONNECTOR-CONTENT-R006` | Declare access contracts for the competency reads of plane-agent | Subsystem: connector `plane-agent`. |

Relations follow the row text; the connector adds no table of its own.
