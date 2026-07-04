"""Native epistemic-graph ingestion for Plane records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. plane-agent natively pushes its data
into the ONE epistemic-graph knowledge graph as **typed OWL nodes** (:SoftwareProject,
:Issue, :Cycle, :Workspace, :ProjectState, :Person) + links, using the lightweight engine
client (``GraphComputeEngine()._client`` + ``txn``) — the same fast client the blob
``MediaStore`` uses, NOT the heavy in-process ingestion engine.

This is a thin mapper: the txn write path lives in the shared primitive
``agent_utilities.knowledge_graph.memory.native_ingest``. That import is GUARDED — when the
primitive isn't present (older installed agent_utilities) we fall back to a self-contained
txn dance. Either way everything is dependency-/engine-guarded: with no KG stack or no
reachable engine every entry point **no-ops** (returns ``None``), so the connector keeps
working with zero KG infrastructure. Node ids follow ``plane:<class>:<externalId>`` and the
``type`` on each entity matches a class the package's ``ontology`` .ttl federates.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("plane_agent.kg")

_SOURCE = "plane-agent"
_DOMAIN = "plane"
_DEFAULT_GRAPH = "__commons__"


def _native_client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable."""
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        return client, (getattr(engine, "graph_name", None) or _DEFAULT_GRAPH)
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def _fallback_write(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None,
    *,
    source: str,
    domain: str,
    client: Any | None,
    graph: str | None,
) -> dict[str, int] | None:
    """Self-contained txn write, used when the shared primitive isn't installed."""
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    if client is None:
        client, graph = _native_client()
    if client is None:
        return None
    graph = graph or _DEFAULT_GRAPH
    try:
        txn = client.txn.begin(graph=graph)
        for ent in entities:
            props = {k: v for k, v in ent.items() if k != "id" and v is not None}
            props.setdefault("source", source)
            props.setdefault("domain", domain)
            client.txn.add_node(txn, ent["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)

    logger.info("KG ingest: wrote %d nodes, %d edges", len(entities), edges)
    return {"nodes": len(entities), "edges": edges}


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph.

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":<link>}]``.
    Prefers the shared ``native_ingest`` primitive; falls back to a self-contained txn.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (no engine / failure; never raises).
    """
    if not entities:
        return None
    try:
        from agent_utilities.knowledge_graph.memory.native_ingest import (
            ingest_entities as _shared,
        )
    except Exception:  # noqa: BLE001 — primitive not yet installed
        return _fallback_write(
            entities,
            relationships,
            source=source,
            domain=domain,
            client=client,
            graph=graph,
        )
    return _shared(
        entities,
        relationships,
        source=source,
        domain=domain,
        client=client,
        graph=graph,
    )


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records (e.g. work-item descriptions) as :Document nodes.

    Best-effort passthrough to the shared primitive; no-ops when it or the engine is
    unavailable (documents are optional fodder, so there is no self-contained fallback).
    """
    if not documents:
        return None
    try:
        from agent_utilities.knowledge_graph.memory.native_ingest import (
            ingest_documents as _shared,
        )
    except Exception:  # noqa: BLE001 — primitive not yet installed
        return None
    return _shared(documents, source=source, domain=domain, client=client, graph=graph)


def _assignee_ids(work_item: dict[str, Any]) -> list[str]:
    """Extract assignee ids from a work-item record (list of ids or member dicts)."""
    out: list[str] = []
    for a in work_item.get("assignees") or []:
        aid = a.get("id") if isinstance(a, dict) else a
        if aid:
            out.append(str(aid))
    return out


def ingest_projects(
    projects: list[dict[str, Any]],
    *,
    workspace_slug: str | None = None,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Plane project records → :SoftwareProject (+ :Workspace) nodes and ingest."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    ws_slug = None
    for proj in projects or []:
        pid = proj.get("id")
        if pid is None:
            continue
        entities.append(
            {
                "id": f"plane:softwareproject:{pid}",
                "type": "SoftwareProject",
                "name": proj.get("name"),
                "identifier": proj.get("identifier"),
                "description": proj.get("description"),
                "externalToolId": str(pid),
            }
        )
        ws = proj.get("workspace") or workspace_slug
        if ws:
            ws_slug = ws
            entities.append(
                {
                    "id": f"plane:workspace:{ws}",
                    "type": "Workspace",
                    "name": str(ws),
                }
            )
            relationships.append(
                {
                    "source": f"plane:softwareproject:{pid}",
                    "target": f"plane:workspace:{ws}",
                    "type": "inWorkspace",
                }
            )
    logger.debug("ingest_projects workspace=%s", ws_slug)
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_work_items(
    work_items: list[dict[str, Any]],
    *,
    project_id: str | None = None,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Plane work-item records → :Issue nodes (+ :belongsToProject / :assignedTo /
    :hasState / :inCycle links) and ingest."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for wi in work_items or []:
        wid = wi.get("id")
        if wid is None:
            continue
        pid = wi.get("project") or project_id
        entities.append(
            {
                "id": f"plane:issue:{wid}",
                "type": "Issue",
                "name": wi.get("name"),
                "sequenceId": wi.get("sequence_id"),
                "priority": wi.get("priority"),
                "description": wi.get("description"),
                "created_at": wi.get("created_at"),
                "updated_at": wi.get("updated_at"),
                "externalToolId": str(wid),
            }
        )
        if pid:
            relationships.append(
                {
                    "source": f"plane:issue:{wid}",
                    "target": f"plane:softwareproject:{pid}",
                    "type": "belongsToProject",
                }
            )
        state = wi.get("state")
        if state:
            entities.append({"id": f"plane:state:{state}", "type": "ProjectState"})
            relationships.append(
                {
                    "source": f"plane:issue:{wid}",
                    "target": f"plane:state:{state}",
                    "type": "hasState",
                }
            )
        cycle = wi.get("cycle")
        if cycle:
            relationships.append(
                {
                    "source": f"plane:issue:{wid}",
                    "target": f"plane:cycle:{cycle}",
                    "type": "inCycle",
                }
            )
        for aid in _assignee_ids(wi):
            entities.append({"id": f"plane:person:{aid}", "type": "Person"})
            relationships.append(
                {
                    "source": f"plane:issue:{wid}",
                    "target": f"plane:person:{aid}",
                    "type": "assignedTo",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_cycles(
    cycles: list[dict[str, Any]],
    *,
    project_id: str | None = None,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Plane cycle records → :Cycle nodes (+ :belongsToProject) and ingest."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for cy in cycles or []:
        cid = cy.get("id")
        if cid is None:
            continue
        pid = cy.get("project") or project_id
        entities.append(
            {
                "id": f"plane:cycle:{cid}",
                "type": "Cycle",
                "name": cy.get("name"),
                "startDate": cy.get("start_date"),
                "endDate": cy.get("end_date"),
                "externalToolId": str(cid),
            }
        )
        if pid:
            relationships.append(
                {
                    "source": f"plane:cycle:{cid}",
                    "target": f"plane:softwareproject:{pid}",
                    "type": "belongsToProject",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)
