"""Competency-question paths of the Plane pack (CONN-PLANE-AGENT-CONNECTOR-CONTENT-R004)."""

from __future__ import annotations

from scion_sdk.ingest import load_declaration
import re
from pathlib import Path

import pytest

import plane_agent

pytestmark = pytest.mark.spec("CONN-PLANE-AGENT-CONNECTOR-CONTENT-R004")

PACKAGE = Path(plane_agent.__file__).parent
TTL = (PACKAGE / "ontology" / "plane.ttl").read_text("utf-8")


def _block(name: str) -> str:
    match = re.search(rf"^:{name} a [^\n]*\n(?:[^\n]+\n)*", TTL, flags=re.M)
    assert match, name
    return match.group(0)


def test_issue_carries_state_and_priority() -> None:
    for prop in ("state", "priority"):
        assert "rdfs:domain :Issue" in _block(prop), prop


@pytest.mark.parametrize(
    ("name", "parent"),
    (
        ("Workspace", "Namespace"),
        ("Cycle", "Iteration"),
        ("PlaneModule", "Collection"),
        ("ProjectState", "Concept"),
    ),
)
def test_classes_extend_a_shared_parent(name: str, parent: str) -> None:
    assert f"rdfs:subClassOf :{parent}" in _block(name)



def test_no_mapping_has_a_null_ontology_class() -> None:
    unmapped = [
        name
        for name, mapping in load_declaration("plane_agent").schema_mappings.items()
        if not mapping.ontology_class
    ]
    assert unmapped == []
