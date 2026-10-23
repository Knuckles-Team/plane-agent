"""The packaged ingestible-source declaration (CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from agent_connector_sdk.ingest.sources import load_ingest_sources
from agent_connector_sdk.mcp.tool_surface import operation_prefix

import plane_agent

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.mark.spec("CONN-PLANE-AGENT-CONNECTOR-CONTENT-R003")
def test_declares_ingestible_sources() -> None:
    declaration = load_ingest_sources(Path(plane_agent.__file__).parent)
    assert declaration is not None
    assert declaration.connector == "plane-mcp"
    source = declaration.source("projects")
    assert source is not None and source.record_type == "SoftwareProject"
    prefix = operation_prefix("plane-agent")
    assert source.tools == (f"{prefix}_list_projects",)
    # The engine admits a record only under the pack mapping of its type.
    manifest = yaml.safe_load(
        (REPO_ROOT / "connector_manifest.yml").read_text("utf-8")
    )
    assert source.record_type in manifest["schema_mappings"]
    # Work items are project-scoped, so only the projects source is declared.
    assert [s.source_id for s in declaration.sources] == ["projects"]
