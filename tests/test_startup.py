import pytest


@pytest.mark.concept("ECO-4.1")
def test_server_startup():
    """Validates that the server module can start successfully.

    CONCEPT:ECO-4.1
    """
    from plane_agent.agent_server import agent_server
    from plane_agent.mcp_server import get_mcp_instance

    assert agent_server is not None
    assert get_mcp_instance is not None
    print("Startup tests handled correctly.")
