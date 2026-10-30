"""Keep the connector's Pages and packaged development contracts explicit."""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _actions_on(workflow: dict):
    # PyYAML's YAML 1.1 reader represents the Actions ``on`` key as True.
    return workflow["on"] if "on" in workflow else workflow[True]


def test_pages_publishes_spec_dashboard_and_supports_manual_refresh():

    config = json.loads((ROOT / ".github/spec-dashboard.json").read_text())
    assert config == {
        "version": 1,
        "sources": [{"glob": "specs/*/status.json", "kind": "spec"}],
    }
    assert not (ROOT / ".github/workflows/docs.yml").exists()


def test_development_skill_is_source_backed():
    skill = ROOT / "plane_agent/skills/plane-agent-development/SKILL.md"
    content = skill.read_text()

    assert "name: plane-agent-development" in content
    assert "## Rapid delivery: the 5-minute contract" in content
    for path in (
        "plane_agent/__init__.py",
        "plane_agent/auth.py",
        "plane_agent/api_client.py",
        "plane_agent/mcp_server.py",
        "plane_agent/ontology/plane.ttl",
        "tests/test_publication_workflow.py",
        "tests/test_action_discovery.py",
        "tests/test_access_contracts.py",
        "tests/test_ingest_sources.py",
        "tests/test_startup.py",
    ):
        assert path in content
        assert (ROOT / path).exists(), path
    for runtime_name in (
        "scion-sdk",
        "PLANE_BASE_URL",
        "PLANE_API_KEY",
        "PLANE_WORKSPACE_SLUG",
        "PLANE_KG_INGEST",
        "PLANE_TLS_PROFILE",
        "plane-mcp",
    ):
        assert runtime_name in content

    project_data = tomllib.loads((ROOT / "pyproject.toml").read_text())
    project = project_data["project"]
    package_data = project_data["tool"]["setuptools"]["package-data"]["plane_agent"]
    assert "skills/**" in package_data
    assert re.search(
        rf'^name = "plane-agent"\nversion = "{re.escape(project["version"])}"$',
        (ROOT / "uv.lock").read_text(),
        re.MULTILINE,
    )
    assert project["name"] == "plane-agent"
