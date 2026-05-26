"""MCP tools for initiatives operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from plane_agent.auth import get_client


def register_initiatives_tools(mcp: FastMCP):
    # CONCEPT:ECO-4.1
    @mcp.tool(tags={"initiatives"})
    async def plane_initiatives(
        # CONCEPT:ECO-4.1
        action: str = Field(
            description="Action to perform. Must be one of: 'list_initiatives', 'create_initiative'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane initiatives operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_initiatives":
            return client.list_initiatives(**kwargs)
        if action == "create_initiative":
            return client.create_initiative(**kwargs)
        raise ValueError(f"Unknown action: {action}")
