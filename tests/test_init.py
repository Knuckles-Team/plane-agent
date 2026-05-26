import pytest
from fastmcp import FastMCP

from plane_agent.mcp_server import get_mcp_instance


@pytest.mark.concept("ECO-4.1")
def test_mcp_instance_creation():
    """Test that the MCP instance can be created successfully.

    CONCEPT:ECO-4.1
    """
    mcp, args, middlewares = get_mcp_instance()
    assert isinstance(mcp, FastMCP)
    assert "plane" in mcp.name


@pytest.mark.concept("ECO-4.1")
def test_import_plane_agent():
    """Test that the package can be imported.

    CONCEPT:ECO-4.1
    """
    import plane_agent

    assert plane_agent.__version__ is not None
