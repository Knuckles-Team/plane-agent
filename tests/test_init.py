import pytest
from plane_agent.mcp_server import get_mcp_instance
from fastmcp import FastMCP


def test_mcp_instance_creation():
    """Test that the MCP instance can be created successfully."""
    mcp, args, middlewares, registered_tags = get_mcp_instance()
    assert isinstance(mcp, FastMCP)
    assert "plane" in mcp.name


def test_import_plane_agent():
    """Test that the package can be imported."""
    import plane_agent

    assert plane_agent.__version__ is not None
