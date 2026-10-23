"""The packaged ingestible-source declaration (CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003)."""

from __future__ import annotations

from pathlib import Path

import pytest
from plane_agent.connector_sources import declaration as declared_sources
from agent_connector_sdk.mcp.tool_surface import operation_prefix


REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.spec("CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003")
def test_declares_ingestible_sources() -> None:
    declaration = declared_sources()
    assert declaration is not None
    assert declaration.connector == "plane-mcp"
    source = declaration.source("projects")
    assert source is not None and source.record_type == "SoftwareProject"
    prefix = operation_prefix("plane-agent")
    assert source.tools == (f"{prefix}_list_projects",)
    # The engine admits a record only under the pack mapping of its type.
    assert source.record_type in declared_sources().schema_mappings
    # Work items are project-scoped, so only the projects source is declared.
    assert [s.source_id for s in declaration.sources] == ["projects"]
