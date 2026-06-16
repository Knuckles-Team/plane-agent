"""MCP tools for epics operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from plane_agent.auth import get_client


def register_epics_tools(mcp: FastMCP):
    # CONCEPT:ECO-4.1
    @mcp.tool(tags={"epics"})
    async def plane_epics(
        # CONCEPT:ECO-4.1
        action: str = Field(
            description="Action to perform. Must be one of: 'list_epics', 'create_epic', 'retrieve_epic', 'update_epic', 'delete_epic'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane epics operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = (
            "list_epics",
            "create_epic",
            "retrieve_epic",
            "update_epic",
            "delete_epic",
        )
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "list_epics":
            return await run_blocking(client.list_epics, **kwargs)
        if action == "create_epic":
            return await run_blocking(client.create_epic, **kwargs)
        if action == "retrieve_epic":
            return await run_blocking(client.retrieve_epic, **kwargs)
        if action == "update_epic":
            return await run_blocking(client.update_epic, **kwargs)
        if action == "delete_epic":
            return await run_blocking(client.delete_epic, **kwargs)
        raise ValueError(f"Unknown action: {action}")
