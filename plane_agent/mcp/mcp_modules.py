"""MCP tools for modules operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from plane_agent.auth import get_client


def register_modules_tools(mcp: FastMCP):
    # CONCEPT:ECO-4.1
    @mcp.tool(tags={"modules"})
    async def plane_modules(
        # CONCEPT:ECO-4.1
        action: str = Field(
            description="Action to perform. Must be one of: 'list_modules', 'create_module', 'retrieve_module', 'update_module', 'delete_module'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane modules operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = (
            "list_modules",
            "create_module",
            "retrieve_module",
            "update_module",
            "delete_module",
        )
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "list_modules":
            return await run_blocking(client.list_modules, **kwargs)
        if action == "create_module":
            return await run_blocking(client.create_module, **kwargs)
        if action == "retrieve_module":
            return await run_blocking(client.retrieve_module, **kwargs)
        if action == "update_module":
            return await run_blocking(client.update_module, **kwargs)
        if action == "delete_module":
            return await run_blocking(client.delete_module, **kwargs)
        raise ValueError(f"Unknown action: {action}")
