"""Plane's read-only source access contracts stay source-local."""

from __future__ import annotations

from pathlib import Path

from scion_sdk.access_contract import parse_access_contracts


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "plane_agent" / "ontology" / "access_contracts.ttl"
KG = "http://knuckles.team/kg#"

EXPECTED = {
    "Workspace": ("plane_workspaces", "workspace", "slug", "none"),
    "SoftwareProject": ("plane_projects", "project", "id", "cursor"),
    "Issue": ("plane_work_items", "work_item", "id", "cursor"),
    "Cycle": ("plane_cycles", "cycle", "id", "cursor"),
    "PlaneModule": ("plane_modules", "module", "id", "cursor"),
    "ProjectState": ("plane_states", "state", "id", "cursor"),
    "Label": ("plane_labels", "label", "id", "cursor"),
}


def _contracts():
    return parse_access_contracts(CONTRACTS.read_text(encoding="utf-8"))


def test_every_declared_plane_class_has_a_typed_read_contract() -> None:
    contracts = _contracts()
    by_class = {contract.class_iri.rsplit("#", 1)[-1]: contract for contract in contracts}

    assert set(by_class) == set(EXPECTED)
    for class_name, (operation, entity, key_field, pagination) in EXPECTED.items():
        contract = by_class[class_name]
        assert contract.class_iri == KG + class_name
        assert contract.source_id == "plane-agent"
        assert contract.access_kind == "mcp_tool"
        assert contract.operation == operation
        assert contract.entity == entity
        assert contract.key_field == key_field
        assert contract.parameters == ("action", "params_json")
        assert contract.auth_ref == "env://PLANE_API_KEY"
        assert contract.pagination == pagination
        if pagination == "none":
            assert contract.pushdown == frozenset()
        else:
            assert contract.pushdown == frozenset({"filter", "limit", "sort"})


def test_plane_contracts_do_not_promote_draft_crosswalks() -> None:
    contracts = _contracts()

    assert all(contract.class_iri.startswith(KG) for contract in contracts)
    assert all(contract.class_iri != KG + "Incident" for contract in contracts)
    assert all(contract.source_id == "plane-agent" for contract in contracts)


def test_plane_contract_artifact_is_packaged_under_ontology() -> None:
    assert CONTRACTS.is_file()


def test_plane_contract_bindings_use_declared_fields() -> None:
    contracts = {contract.class_iri.rsplit("#", 1)[-1]: contract for contract in _contracts()}

    assert (KG + "identifier", "identifier") in contracts["SoftwareProject"].predicates
    assert (KG + "sequenceId", "sequence_id") in contracts["Issue"].predicates
    assert (KG + "startDate", "start_date") in contracts["Cycle"].predicates
