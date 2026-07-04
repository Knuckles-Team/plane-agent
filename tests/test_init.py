import pytest
from fastmcp import FastMCP

from plane_agent.mcp_server import get_mcp_instance


@pytest.mark.concept("AU-ECO.mcp.fastmcp-middleware")
def test_mcp_instance_creation():
    """Test that the MCP instance can be created successfully.

    CONCEPT:AU-ECO.mcp.fastmcp-middleware
    """
    mcp, args, middlewares = get_mcp_instance()
    assert isinstance(mcp, FastMCP)
    assert "plane" in mcp.name


@pytest.mark.concept("AU-ECO.mcp.fastmcp-middleware")
def test_import_plane_agent():
    """Test that the package can be imported.

    CONCEPT:AU-ECO.mcp.fastmcp-middleware
    """
    import plane_agent

    assert plane_agent.__version__ is not None
