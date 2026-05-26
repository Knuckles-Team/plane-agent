"""MCP tools for projects operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from plane_agent.auth import get_client


def register_projects_tools(mcp: FastMCP):
    # CONCEPT:ECO-4.1
    @mcp.tool(tags={"projects"})
    async def plane_projects(
        # CONCEPT:ECO-4.1
        action: str = Field(
            description="Action to perform. Must be one of: 'list_projects', 'retrieve_project'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane projects operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_projects":
            return client.list_projects(**kwargs)
        if action == "retrieve_project":
            return client.retrieve_project(**kwargs)
        raise ValueError(f"Unknown action: {action}")
