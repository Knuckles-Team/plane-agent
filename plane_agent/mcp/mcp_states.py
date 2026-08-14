"""MCP tools for states operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from plane_agent.auth import get_client


def register_states_tools(mcp: FastMCP):
    # CONCEPT:AU-ECO.mcp.fastmcp-middleware
    @mcp.tool(tags={"states"})
    async def plane_states(
        # CONCEPT:AU-ECO.mcp.fastmcp-middleware
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
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ("list_states", "create_state")
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "list_states":
            return await run_blocking(client.list_states, **kwargs)
        if action == "create_state":
            return await run_blocking(client.create_state, **kwargs)
        raise ValueError(f"Unknown action: {action}")
