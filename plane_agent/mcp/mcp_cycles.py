"""MCP tools for cycles operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from plane_agent.auth import get_client


def register_cycles_tools(mcp: FastMCP):
    # CONCEPT:AU-ECO.mcp.fastmcp-middleware
    @mcp.tool(tags={"cycles"})
    async def plane_cycles(
        # CONCEPT:AU-ECO.mcp.fastmcp-middleware
        action: str = Field(
            description="Action to perform. Must be one of: 'list_cycles', 'create_cycle', 'retrieve_cycle', 'update_cycle', 'delete_cycle', 'list_cycle_work_items', 'add_work_items_to_cycle'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane cycles operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = (
            "list_cycles",
            "create_cycle",
            "retrieve_cycle",
            "update_cycle",
            "delete_cycle",
            "list_cycle_work_items",
            "add_work_items_to_cycle",
        )
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "list_cycles":
            return await run_blocking(client.list_cycles, **kwargs)
        if action == "create_cycle":
            return await run_blocking(client.create_cycle, **kwargs)
        if action == "retrieve_cycle":
            return await run_blocking(client.retrieve_cycle, **kwargs)
        if action == "update_cycle":
            return await run_blocking(client.update_cycle, **kwargs)
        if action == "delete_cycle":
            return await run_blocking(client.delete_cycle, **kwargs)
        if action == "list_cycle_work_items":
            return await run_blocking(client.list_cycle_work_items, **kwargs)
        if action == "add_work_items_to_cycle":
            return await run_blocking(client.add_work_items_to_cycle, **kwargs)
        raise ValueError(f"Unknown action: {action}")
