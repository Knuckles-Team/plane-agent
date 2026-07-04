"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_projects`` / ``ingest_work_items`` /
``ingest_cycles`` seam with a fake engine client (no engine required), asserting the txn
add_node/commit + edge calls and the Plane record → :SoftwareProject / :Issue / :Cycle
mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from plane_agent.kg_ingest import (
    ingest_cycles,
    ingest_entities,
    ingest_projects,
    ingest_work_items,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "type": "SoftwareProject", "name": "p"},
            {"id": "b", "type": "Workspace"},
        ],
        [{"source": "a", "target": "b", "type": "inWorkspace"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "b"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "plane-agent"
    assert c.txn.nodes["a"]["domain"] == "plane"
    assert c.edges.edges == [("a", "b", {"type": "inWorkspace"})]


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
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    proj = c.txn.nodes["plane:softwareproject:p1"]
    assert proj["type"] == "SoftwareProject"
    assert proj["identifier"] == "DEMO"
    assert proj["externalToolId"] == "p1"
    assert c.txn.nodes["plane:workspace:acme"]["type"] == "Workspace"
    assert c.edges.edges == [
        ("plane:softwareproject:p1", "plane:workspace:acme", {"type": "inWorkspace"})
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
    issue = c.txn.nodes["plane:issue:wi1"]
    assert issue["type"] == "Issue"
    assert issue["sequenceId"] == 42
    assert issue["priority"] == "high"
    assert c.txn.nodes["plane:state:s1"]["type"] == "ProjectState"
    assert c.txn.nodes["plane:person:u1"]["type"] == "Person"
    assert c.txn.nodes["plane:person:u2"]["type"] == "Person"
    edge_types = sorted(p["type"] for _, _, p in c.edges.edges)
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
        {"type": "belongsToProject"},
    ) in c.edges.edges


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
    cyc = c.txn.nodes["plane:cycle:cy1"]
    assert cyc["type"] == "Cycle"
    assert cyc["startDate"] == "2026-07-07"
    assert cyc["endDate"] == "2026-07-20"
    assert c.edges.edges == [
        ("plane:cycle:cy1", "plane:softwareproject:p1", {"type": "belongsToProject"})
    ]


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "Issue"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_projects([], client=_FakeClient()) is None
    assert ingest_work_items([], client=_FakeClient()) is None
    assert ingest_cycles([], client=_FakeClient()) is None
