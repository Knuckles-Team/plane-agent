"""Plane's read-only source access contracts stay source-local."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from scion_sdk.access_contract import parse_access_contracts
from scion_sdk.connector import build_server
from scion_sdk.testing.surface_check import served_surface

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "plane_agent" / "ontology" / "access_contracts.ttl"
KG = "https://knuckles-team.github.io/ontology/core#"
CONNECTOR_NS = "https://knuckles-team.github.io/ontology/connector/plane#"

EXPECTED = {
    "Workspace": ("plane_get_workspace", "workspace", "slug", "none"),
    "SoftwareProject": ("plane_list_projects", "project", "id", "cursor"),
    "Issue": ("plane_list_work_items", "work_item", "id", "cursor"),
    "Cycle": ("plane_list_cycles", "cycle", "id", "cursor"),
    "PlaneModule": ("plane_list_modules", "module", "id", "cursor"),
    "ProjectState": ("plane_list_states", "state", "id", "cursor"),
    "Label": ("plane_list_labels", "label", "id", "cursor"),
}

PARAMETERS = {
    "plane_get_workspace": (),
    "plane_list_projects": ("per_page", "cursor", "order_by"),
    **{
        name: ("project_id", "params_json")
        for name in (
            "plane_list_work_items",
            "plane_list_cycles",
            "plane_list_modules",
            "plane_list_states",
            "plane_list_labels",
        )
    },
}


def _contracts():
    return parse_access_contracts(CONTRACTS.read_text(encoding="utf-8"))


def test_every_declared_plane_class_has_a_typed_read_contract() -> None:
    contracts = _contracts()
    by_class = {
        contract.class_iri.rsplit("#", 1)[-1]: contract for contract in contracts
    }

    assert set(by_class) == set(EXPECTED)
    for class_name, (operation, entity, key_field, pagination) in EXPECTED.items():
        contract = by_class[class_name]
        assert contract.class_iri in (CONNECTOR_NS + class_name, KG + class_name)
        assert contract.source_id == "plane-agent"
        assert contract.access_kind == "mcp_tool"
        assert contract.operation == operation
        assert contract.entity == entity
        assert contract.key_field == key_field
        assert tuple(sorted(contract.parameters)) == tuple(
            sorted(PARAMETERS[operation])
        )
        assert contract.auth_ref == "env://PLANE_API_KEY"
        assert contract.pagination == pagination
        if pagination == "none":
            assert contract.pushdown == frozenset()
        else:
            assert contract.pushdown == frozenset({"filter", "limit", "sort"})


def test_plane_contracts_do_not_promote_draft_crosswalks() -> None:
    contracts = _contracts()

    assert all(contract.class_iri.startswith((CONNECTOR_NS, KG)) for contract in contracts)
    assert all(contract.class_iri != KG + "Incident" for contract in contracts)
    assert all(contract.source_id == "plane-agent" for contract in contracts)


def test_plane_contract_artifact_is_packaged_under_ontology() -> None:
    assert CONTRACTS.is_file()


def test_plane_contract_bindings_use_declared_fields() -> None:
    contracts = {
        contract.class_iri.rsplit("#", 1)[-1]: contract for contract in _contracts()
    }

    assert (CONNECTOR_NS + "identifier", "identifier") in contracts["SoftwareProject"].predicates
    assert (CONNECTOR_NS + "sequenceId", "sequence_id") in contracts["Issue"].predicates
    assert (CONNECTOR_NS + "startDate", "start_date") in contracts["Cycle"].predicates


ROW_ID = "CONN-PLANE-AGENT-CONNECTOR-CONTENT-R006"
RECORDINGS = ROOT / "tests" / "recordings"
COMPETENCY = {
    "work_item": {
        "class": "Issue",
        "key": "id",
        "operation": "plane_list_work_items",
        "columns": ("state", "pullRequestUrl"),
    },
}


def _local(iri: str) -> str:
    return re.split(r"[#/]", iri)[-1]


def _declared_terms() -> set[str]:
    text = (CONTRACTS.parent / "plane.ttl").read_text(encoding="utf-8")
    return set(re.findall(r"^:(\w+)\s+a\s+owl:", text, flags=re.M))


def _competency_findings(contracts, tools: set[str], terms: set[str], recordings: Path) -> list[str]:
    found: list[str] = []
    by_entity = {c.entity: c for c in contracts}
    for entity, want in COMPETENCY.items():
        contract = by_entity.get(entity)
        if contract is None:
            found.append(f"{entity}: no contract")
            continue
        if contract.operation not in tools:
            found.append(f"{entity}: tool {contract.operation} is not served")
        if _local(contract.class_iri) != want["class"] or want["class"] not in terms:
            found.append(f"{entity}: class {contract.class_iri} not in ontology")
        if contract.key_field != want["key"] or contract.access_kind != "mcp_tool":
            found.append(f"{entity}: wrong key or access kind")
        bound = {field: prop for prop, field in contract.predicates}
        for field in want["columns"]:
            if field not in bound or _local(bound[field]) != field or field not in terms:
                found.append(f"{entity}: column {field} is not an ontology property")
        path = recordings / f"{entity}.json"
        if not path.is_file():
            found.append(f"{entity}: recording missing")
            continue
        records = json.loads(path.read_text(encoding="utf-8"))
        if not records:
            found.append(f"{entity}: recording is empty")
        for record in records:
            for field in {contract.key_field} | set(want["columns"]):
                if field not in record:
                    found.append(f"{entity}: recording lacks {field}")
    return found


def _competency_contracts():
    return parse_access_contracts(CONTRACTS.read_text(encoding="utf-8"))


@pytest.mark.spec(ROW_ID)
def test_competency_contracts_certified() -> None:
    tools = served_surface(build_server("plane_agent", command_args=[])[1]).tools
    assert _competency_findings(_competency_contracts(), tools, _declared_terms(), RECORDINGS) == []


@pytest.mark.spec(ROW_ID)
def test_missing_tool_or_column_fails_certification(tmp_path: Path) -> None:
    entity, want = next(iter(COMPETENCY.items()))
    (tmp_path / f"{entity}.json").write_text(json.dumps([{want["key"]: "x"}]))
    found = _competency_findings(_competency_contracts(), set(), _declared_terms(), tmp_path)
    assert any("is not served" in f for f in found)
    assert any("recording lacks" in f for f in found)
