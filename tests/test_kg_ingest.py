"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_projects`` / ``ingest_work_items`` /
``ingest_cycles`` seam against a fake SDK ingest transport (no engine required),
asserting the committed node/edge payloads and the Plane record → :SoftwareProject /
:Issue / :Cycle mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import IngestError, KnowledgeIngest

from plane_agent.kg_ingest import (
    ingest_cycles,
    ingest_entities,
    ingest_projects,
    ingest_work_items,
)


class _FakeTransport:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def source_status(self, connector: str, stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: Any) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data: bytes) -> str:
        raise AssertionError("this connector's typed-node ingestion carries no media")


@pytest.fixture
def ingest():
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


def _node(transport: _FakeTransport, record_id: str) -> dict[str, Any]:
    for record in transport.requests[-1].records:
        if record.record_id == record_id:
            return dict(record.payload)
    raise AssertionError(f"no record {record_id!r} was submitted")


def _edges(transport: _FakeTransport) -> list[tuple[str, str, str]]:
    return [
        (rel.source.record_id, rel.target.record_id, rel.relation_reference.rsplit("/", 1)[-1])
        for rel in transport.requests[-1].relationships
    ]


@pytest.mark.asyncio
async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "SoftwareProject", "name": "p"},
            {"id": "b", "node_type": "Workspace"},
        ],
        [{"source": "a", "target": "b", "relationship": "inWorkspace"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert _node(transport, "a")["name"] == "p"
    assert ("a", "b", "inWorkspace") in _edges(transport)


@pytest.mark.asyncio
async def test_ingest_projects_maps_project_and_workspace(ingest):
    service, transport = ingest
    res = await ingest_projects(
        [
            {
                "id": "p1",
                "name": "Demo",
                "identifier": "DEMO",
                "description": "d",
                "workspace": "acme",
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    proj = _node(transport, "plane:softwareproject:p1")
    assert proj["identifier"] == "DEMO"
    assert proj["externalToolId"] == "p1"
    assert _node(transport, "plane:workspace:acme")
    assert ("plane:softwareproject:p1", "plane:workspace:acme", "inWorkspace") in _edges(
        transport
    )


@pytest.mark.asyncio
async def test_ingest_work_items_maps_issue_and_links(ingest):
    service, transport = ingest
    res = await ingest_work_items(
        [
            {
                "id": "wi1",
                "name": "Bug",
                "project": "p1",
                "state": "s1",
                "cycle": "c1",
                "priority": "high",
                "sequence_id": 42,
                "assignees": [{"id": "u1"}, "u2"],
            }
        ],
        ingest=service,
    )
    # 1 issue + 1 state + 2 persons
    assert res == {"nodes": 4, "edges": 5}
    issue = _node(transport, "plane:issue:wi1")
    assert issue["sequenceId"] == 42
    assert issue["priority"] == "high"
    _node(transport, "plane:state:s1")
    _node(transport, "plane:person:u1")
    _node(transport, "plane:person:u2")
    edge_types = sorted(rel for _, _, rel in _edges(transport))
    assert edge_types == [
        "assignedTo",
        "assignedTo",
        "belongsToProject",
        "hasState",
        "inCycle",
    ]


@pytest.mark.asyncio
async def test_ingest_work_items_uses_fallback_project_id(ingest):
    service, transport = ingest
    await ingest_work_items([{"id": "wi9", "name": "Task"}], project_id="pX", ingest=service)
    assert ("plane:issue:wi9", "plane:softwareproject:pX", "belongsToProject") in _edges(
        transport
    )


@pytest.mark.asyncio
async def test_ingest_cycles_maps_cycle_and_project_link(ingest):
    service, transport = ingest
    res = await ingest_cycles(
        [
            {
                "id": "cy1",
                "name": "Sprint 1",
                "project": "p1",
                "start_date": "2026-07-07",
                "end_date": "2026-07-20",
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 1}
    cyc = _node(transport, "plane:cycle:cy1")
    assert cyc["startDate"] == "2026-07-07"
    assert cyc["endDate"] == "2026-07-20"
    assert ("plane:cycle:cy1", "plane:softwareproject:p1", "belongsToProject") in _edges(
        transport
    )


@pytest.mark.asyncio
async def test_empty_ingest_entities_is_rejected(ingest):
    service, _transport = ingest
    with pytest.raises(IngestError, match="at least one entity"):
        await ingest_entities([], ingest=service)
