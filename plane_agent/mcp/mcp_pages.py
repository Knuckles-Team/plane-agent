"""MCP tools for pages operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from plane_agent.auth import get_client


def register_pages_tools(mcp: FastMCP):
    # CONCEPT:ECO-4.1
    @mcp.tool(tags={"pages"})
    async def plane_pages(
        # CONCEPT:ECO-4.1
        action: str = Field(
            description="Action to perform. Must be one of: 'retrieve_project_page', 'create_project_page'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane pages operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "retrieve_project_page":
            return client.retrieve_project_page(**kwargs)
        if action == "create_project_page":
            return client.create_project_page(**kwargs)
        raise ValueError(f"Unknown action: {action}")
