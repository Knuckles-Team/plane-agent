import pytest
from fastmcp import FastMCP

from agent_connector_sdk.connector import build_server


@pytest.mark.concept("AU-ECO.mcp.fastmcp-middleware")
def test_mcp_instance_creation():
    """Test that the MCP instance can be created successfully.

    CONCEPT:AU-ECO.mcp.fastmcp-middleware
    """
    _, mcp = build_server("plane_agent", command_args=[])
    assert isinstance(mcp, FastMCP)
    assert "plane" in mcp.name
