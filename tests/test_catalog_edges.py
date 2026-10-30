"""Owner and assignee edges declared on the ingest sources (CONN-PLANE-AGENT-CONNECTOR-CONTENT-R005)."""

from __future__ import annotations

from pathlib import Path

import pytest
from scion_sdk.ingest.live_declaration import load_declaration
from scion_sdk.ingest.model import EntityRef
from scion_sdk.ingest.source_sync import _edges  # noqa: PLC2701

import plane_agent

ONTOLOGY = Path(plane_agent.__file__).parent / "ontology" / "plane.ttl"


def _domain_and_range(name: str) -> tuple[str, str]:
    block = ONTOLOGY.read_text(encoding="utf-8").split(f"\n:{name} a owl:ObjectProperty")[1]
    block = block.split(" .\n")[0]
    return block.split("rdfs:domain :")[1].split()[0], block.split("rdfs:range :")[1].split()[0]


@pytest.mark.spec("CONN-PLANE-AGENT-CONNECTOR-CONTENT-R005")
def test_every_declared_edge_is_an_ontology_property_of_its_record_type() -> None:
    declaration = load_declaration("plane_agent")
    seen = set()
    for source in declaration.sources:
        for edge in source.edges:
            assert _domain_and_range(edge.relationship) == (source.record_type, edge.target_type)
            assert edge.target_type in declaration.schema_mappings
            seen.add((source.source_id, edge.relationship))
    assert seen == {
        ("projects", "projectLedBy"),
        ("work-items", "assignedTo"),
        ("work-items", "workItemOfProject"),
    }


@pytest.mark.spec("CONN-PLANE-AGENT-CONNECTOR-CONTENT-R005")
def test_project_and_work_item_references_become_lead_assignee_and_project_edges() -> None:
    declaration = load_declaration("plane_agent")
    project = {"id": "p1", "project_lead": "u1"}
    item = {"id": "w1", "assignees": ["u1", "u2"], "project": "p1"}
    leads = {(r.relationship, r.target) for _, r in _edges("p1", project, declaration.source("projects"))}
    items = {(r.relationship, r.target) for _, r in _edges("w1", item, declaration.source("work-items"))}
    assert leads == {("projectLedBy", "user:u1")}
    assert items == {
        ("assignedTo", "user:u1"),
        ("assignedTo", "user:u2"),
        ("workItemOfProject", EntityRef(id="p1", stream="projects")),
    }
