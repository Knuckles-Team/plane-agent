from agent_connector_sdk.connector import Connector

from plane_agent.api_client import Api
from plane_agent.auth import get_client

connector = Connector(
    api=Api,
    get_client=get_client,
    tools="plane_agent.mcp_server",
    instructions="plane-agent MCP Server — Condensed Action-Routed Tools.",
)
