"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_projects`` / ``ingest_work_items`` /
``ingest_cycles`` seam with a fake engine client (no engine required), asserting the txn
add_node/commit + edge calls and the Plane record → :SoftwareProject / :Issue / :Cycle
mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.memory.native_ingest import NativeIngestError
from agent_utilities.security.brain_context import ActorContext, use_actor
from agent_utilities.models.company_brain import ActorType
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session

from plane_agent.kg_ingest import (
    ingest_cycles,
    ingest_entities,
    ingest_projects,
    ingest_work_items,
)


@pytest.fixture(autouse=True)
def _governed_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "SoftwareProject", "name": "p"},
            {"id": "b", "node_type": "Workspace"},
        ],
        [{"source": "a", "target": "b", "relationship": "inWorkspace"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert len(c.changes.applied) == 1
    assert set(c.nodes.values) == {"a", "b"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "plane-agent"
    assert c.nodes.values["a"]["domain"] == "plane"
    assert c.changes.edges == [("a", "b", {"relationship": "inWorkspace"})]


def test_ingest_projects_maps_project_and_workspace():
    c = _FakeClient()
    res = ingest_projects(
        [
            {
                "id": "p1",
                "name": "Demo",
                "identifier": "DEMO",
                "description": "d",
                "workspace": "acme",
            }
        ],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    proj = c.nodes.values["plane:softwareproject:p1"]
    assert proj["node_type"] == "SoftwareProject"
    assert proj["identifier"] == "DEMO"
    assert proj["externalToolId"] == "p1"
    assert c.nodes.values["plane:workspace:acme"]["node_type"] == "Workspace"
    assert c.changes.edges == [
        ("plane:softwareproject:p1", "plane:workspace:acme", {"relationship": "inWorkspace"})
    ]


def test_ingest_work_items_maps_issue_and_links():
    c = _FakeClient()
    res = ingest_work_items(
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
        client=c,
    )
    # 1 issue + 1 state + 2 persons
    assert res == {"nodes": 4, "edges": 5}
    issue = c.nodes.values["plane:issue:wi1"]
    assert issue["node_type"] == "Issue"
    assert issue["sequenceId"] == 42
    assert issue["priority"] == "high"
    assert c.nodes.values["plane:state:s1"]["node_type"] == "ProjectState"
    assert c.nodes.values["plane:person:u1"]["node_type"] == "Person"
    assert c.nodes.values["plane:person:u2"]["node_type"] == "Person"
    edge_types = sorted(p["relationship"] for _, _, p in c.changes.edges)
    assert edge_types == [
        "assignedTo",
        "assignedTo",
        "belongsToProject",
        "hasState",
        "inCycle",
    ]


def test_ingest_work_items_uses_fallback_project_id():
    c = _FakeClient()
    ingest_work_items([{"id": "wi9", "name": "Task"}], project_id="pX", client=c)
    assert (
        "plane:issue:wi9",
        "plane:softwareproject:pX",
        {"relationship": "belongsToProject"},
    ) in c.changes.edges


def test_ingest_cycles_maps_cycle_and_project_link():
    c = _FakeClient()
    res = ingest_cycles(
        [
            {
                "id": "cy1",
                "name": "Sprint 1",
                "project": "p1",
                "start_date": "2026-07-07",
                "end_date": "2026-07-20",
            }
        ],
        client=c,
    )
    assert res == {"nodes": 1, "edges": 1}
    cyc = c.nodes.values["plane:cycle:cy1"]
    assert cyc["node_type"] == "Cycle"
    assert cyc["startDate"] == "2026-07-07"
    assert cyc["endDate"] == "2026-07-20"
    assert c.changes.edges == [
        ("plane:cycle:cy1", "plane:softwareproject:p1", {"relationship": "belongsToProject"})
    ]


def test_retired_structural_alias_is_rejected():
    with pytest.raises(NativeIngestError, match="canonical node_type"):
        ingest_entities([{"id": "a", "type": "Issue"}], client=_FakeClient())


def test_empty_native_ingest_is_rejected():
    with pytest.raises(NativeIngestError, match="at least one entity"):
        ingest_entities([], client=_FakeClient())
