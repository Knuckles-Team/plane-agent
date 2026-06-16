"""MCP tools for workspaces operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from plane_agent.auth import get_client


def register_workspaces_tools(mcp: FastMCP):
    # CONCEPT:ECO-4.1
    @mcp.tool(tags={"workspaces"})
    async def plane_workspaces(
        # CONCEPT:ECO-4.1
        action: str = Field(
            description="Action to perform. Must be one of: 'get_workspace', 'get_workspace_members', 'get_workspace_features', 'update_workspace_features'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane workspaces operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = (
            "get_workspace",
            "get_workspace_members",
            "get_workspace_features",
            "update_workspace_features",
        )
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "get_workspace":
            return await run_blocking(client.get_workspace, **kwargs)
        if action == "get_workspace_members":
            return await run_blocking(client.get_workspace_members, **kwargs)
        if action == "get_workspace_features":
            return await run_blocking(client.get_workspace_features, **kwargs)
        if action == "update_workspace_features":
            return await run_blocking(client.update_workspace_features, **kwargs)
        raise ValueError(f"Unknown action: {action}")
