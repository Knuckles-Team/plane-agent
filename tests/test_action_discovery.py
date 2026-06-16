"""Action-discovery behavior for plane-agent's action-routed MCP tools.

Verifies the shared agent-utilities ``resolve_action`` helper, wired into every
action-routed tool in ``plane_agent.mcp_server``, provides:
  * ``list_actions`` discovery (returns the bounded action names), and
  * a rich did-you-mean ``ValueError`` mentioning ``list_actions`` on an unknown
    action.
"""

from agent_utilities.mcp_utilities import resolve_action

# Mirrors the bounded action set declared in plane_projects (mcp_server.py).
PROJECTS_ACTIONS = ("list_projects", "retrieve_project")


def test_list_actions_returns_names():
    payload = resolve_action("list_actions", PROJECTS_ACTIONS, service="plane-agent")
    assert isinstance(payload, dict)
    assert payload["service"] == "plane-agent"
    assert set(payload["actions"]) == set(PROJECTS_ACTIONS)


def test_canonical_action_passthrough():
    assert (
        resolve_action("list_projects", PROJECTS_ACTIONS, service="plane-agent")
        == "list_projects"
    )


def test_plural_alias_resolves_to_singular():
    # retrieve_projects -> retrieve_project (plural->singular did-you-mean alias)
    assert (
        resolve_action("retrieve_projects", PROJECTS_ACTIONS, service="plane-agent")
        == "retrieve_project"
    )


def test_bogus_action_raises_with_list_actions_hint():
    import pytest

    with pytest.raises(ValueError) as excinfo:
        resolve_action("totally_bogus", PROJECTS_ACTIONS, service="plane-agent")
    assert "list_actions" in str(excinfo.value)
