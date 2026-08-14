"""MCP tools for intake operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from plane_agent.auth import get_client


def register_intake_tools(mcp: FastMCP):
    # CONCEPT:AU-ECO.mcp.fastmcp-middleware
    @mcp.tool(tags={"intake"})
    async def plane_intake(
        # CONCEPT:AU-ECO.mcp.fastmcp-middleware
        action: str = Field(
            description="Action to perform. Must be one of: 'list_intake_work_items', 'create_intake_work_item'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane intake operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ("list_intake_work_items", "create_intake_work_item")
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "list_intake_work_items":
            return await run_blocking(client.list_intake_work_items, **kwargs)
        if action == "create_intake_work_item":
            return await run_blocking(client.create_intake_work_item, **kwargs)
        raise ValueError(f"Unknown action: {action}")
