"""MCP tools for states operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from plane_agent.auth import get_client


def register_states_tools(mcp: FastMCP):
    # CONCEPT:ECO-4.1
    @mcp.tool(tags={"states"})
    async def plane_states(
        # CONCEPT:ECO-4.1
        action: str = Field(
            description="Action to perform. Must be one of: 'list_states', 'create_state'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane states operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_states":
            return client.list_states(**kwargs)
        if action == "create_state":
            return client.create_state(**kwargs)
        raise ValueError(f"Unknown action: {action}")
