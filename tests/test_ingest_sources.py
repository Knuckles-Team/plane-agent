"""The packaged ingestible-source declaration (CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003)."""

from __future__ import annotations

from pathlib import Path

import pytest
from agent_connector_sdk.ingest import load_declaration
from agent_connector_sdk.mcp.tool_surface import operation_prefix


REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.spec("CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003")
def test_declares_ingestible_sources() -> None:
    declaration = load_declaration("plane_agent")
    assert declaration is not None
    assert declaration.connector == "plane-mcp"
    prefix = operation_prefix("plane-agent")
    expected = {
        "projects": ("SoftwareProject", f"{prefix}_list_projects"),
        "work-items": ("Issue", f"{prefix}_list_work_items"),
        "project-states": ("ProjectState", f"{prefix}_list_states"),
    }
    assert [s.source_id for s in declaration.sources] == list(expected)
    for source in declaration.sources:
        record_type, tool = expected[source.source_id]
        assert source.record_type == record_type
        assert source.tools == (tool,)
        # The engine admits a record only under the pack mapping of its type.
        assert record_type in declaration.schema_mappings


@pytest.mark.spec("CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003")
def test_work_items_fan_out_per_project_and_map_to_issue_state() -> None:
    declaration = load_declaration("plane_agent")
    for source_id in ("work-items", "project-states"):
        source = declaration.source(source_id)
        assert source is not None and source.for_each is not None
        assert source.for_each.source == "projects"
        assert (source.for_each.argument, source.for_each.field) == (
            "project_id",
            "id",
        )
    work_items = declaration.source("work-items")
    assert work_items is not None
    assert (work_items.id_field, work_items.title_field) == ("id", "name")
    assert work_items.records_path == "data.results"
    mapping = declaration.schema_mappings["Issue"]
    assert mapping.ontology_class == "WorkItem"
    assert "state" in mapping.fields
    ontology = (REPO_ROOT / "plane_agent" / "ontology" / "plane.ttl").read_text()
    assert "Issue" in ontology and "state" in ontology


@pytest.mark.spec("CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003")
def test_sources_name_read_only_tools() -> None:
    source_text = (REPO_ROOT / "plane_agent" / "mcp_server.py").read_text()
    declaration = load_declaration("plane_agent")
    for source in declaration.sources:
        assert not any(
            verb in tool for tool in source.tools for verb in ("create", "update", "delete")
        )
    assert "list_work_items" in source_text and "list_states" in source_text
