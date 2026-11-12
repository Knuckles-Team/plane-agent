"""Plane's read-only source access contracts stay source-local."""

from __future__ import annotations

from pathlib import Path

from scion_sdk.access_contract import parse_access_contracts

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
