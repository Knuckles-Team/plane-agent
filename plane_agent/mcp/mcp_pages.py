"""MCP tools for pages operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp.action_dispatch import resolve_action
from agent_utilities.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from plane_agent.auth import get_client


def register_pages_tools(mcp: FastMCP):
    # CONCEPT:AU-ECO.mcp.fastmcp-middleware
    @mcp.tool(tags={"pages"})
    async def plane_pages(
        # CONCEPT:AU-ECO.mcp.fastmcp-middleware
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
        except Exception:
            return {"error": "Operation failed"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ("retrieve_project_page", "create_project_page")
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "retrieve_project_page":
            return await run_blocking(client.retrieve_project_page, **kwargs)
        if action == "create_project_page":
            return await run_blocking(client.create_project_page, **kwargs)
        raise ValueError(f"Unknown action: {action}")
