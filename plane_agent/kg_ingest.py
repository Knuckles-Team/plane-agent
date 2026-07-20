"""Native epistemic-graph ingestion for Plane work-management records.

All writes use the required ``agent_utilities.knowledge_graph.memory.native_ingest``
primitive. Nodes use canonical ``node_type`` and edges use canonical ``relationship``;
nodes and edges commit in one native transaction. Missing engine dependencies, rejected
records, conflicts, and transaction failures propagate as ``NativeIngestError``.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_documents as _native_ingest_documents,
)
from agent_utilities.knowledge_graph.memory.native_ingest import (
    ingest_entities as _native_ingest_entities,
)

logger = logging.getLogger("plane_agent.kg")

_SOURCE = "plane-agent"
_DOMAIN = "plane"


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write canonical typed nodes and relationships in one native transaction."""
    return _native_ingest_entities(
        entities, relationships, source=source, domain=domain, client=client, graph=graph
    )


def ingest_documents(
    documents: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
    """Write text records as canonical Document nodes."""
    return _native_ingest_documents(
        documents, source=source, domain=domain, client=client, graph=graph
    )


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
) -> dict[str, int]:
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
                "node_type": "SoftwareProject",
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
                    "node_type": "Workspace",
                    "name": str(ws),
                }
            )
            relationships.append(
                {
                    "source": f"plane:softwareproject:{pid}",
                    "target": f"plane:workspace:{ws}",
                    "relationship": "inWorkspace",
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
) -> dict[str, int]:
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
                "node_type": "Issue",
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
                    "relationship": "belongsToProject",
                }
            )
        state = wi.get("state")
        if state:
            entities.append({"id": f"plane:state:{state}", "node_type": "ProjectState"})
            relationships.append(
                {
                    "source": f"plane:issue:{wid}",
                    "target": f"plane:state:{state}",
                    "relationship": "hasState",
                }
            )
        cycle = wi.get("cycle")
        if cycle:
            relationships.append(
                {
                    "source": f"plane:issue:{wid}",
                    "target": f"plane:cycle:{cycle}",
                    "relationship": "inCycle",
                }
            )
        for aid in _assignee_ids(wi):
            entities.append({"id": f"plane:person:{aid}", "node_type": "Person"})
            relationships.append(
                {
                    "source": f"plane:issue:{wid}",
                    "target": f"plane:person:{aid}",
                    "relationship": "assignedTo",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_cycles(
    cycles: list[dict[str, Any]],
    *,
    project_id: str | None = None,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int]:
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
                "node_type": "Cycle",
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
                    "relationship": "belongsToProject",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)
