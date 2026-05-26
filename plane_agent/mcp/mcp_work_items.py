"""MCP tools for work items operations.

Auto-generated from mcp_server.py during ecosystem standardization.
"""

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from plane_agent.auth import get_client


def register_work_items_tools(mcp: FastMCP):
    # CONCEPT:ECO-4.1
    @mcp.tool(tags={"work_items"})
    async def plane_work_items(
        # CONCEPT:ECO-4.1
        action: str = Field(
            description="Action to perform. Must be one of: 'list_work_items', 'create_work_item', 'update_work_item', 'delete_work_item', 'search_work_items', 'retrieve_work_item_by_identifier', 'retrieve_work_item', 'list_work_item_activities', 'list_work_item_comments', 'create_work_item_comment', 'list_work_item_links', 'create_work_item_link', 'list_work_item_relations', 'list_work_item_types', 'list_work_logs', 'create_work_log'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane work items operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_work_items":
            return client.list_work_items(**kwargs)
        if action == "create_work_item":
            return client.create_work_item(**kwargs)
        if action == "update_work_item":
            return client.update_work_item(**kwargs)
        if action == "delete_work_item":
            return client.delete_work_item(**kwargs)
        if action == "search_work_items":
            return client.search_work_items(**kwargs)
        if action == "retrieve_work_item_by_identifier":
            return client.retrieve_work_item_by_identifier(**kwargs)
        if action == "retrieve_work_item":
            return client.retrieve_work_item(**kwargs)
        if action == "list_work_item_activities":
            return client.list_work_item_activities(**kwargs)
        if action == "list_work_item_comments":
            return client.list_work_item_comments(**kwargs)
        if action == "create_work_item_comment":
            return client.create_work_item_comment(**kwargs)
        if action == "list_work_item_links":
            return client.list_work_item_links(**kwargs)
        if action == "create_work_item_link":
            return client.create_work_item_link(**kwargs)
        if action == "list_work_item_relations":
            return client.list_work_item_relations(**kwargs)
        if action == "list_work_item_types":
            return client.list_work_item_types(**kwargs)
        if action == "list_work_logs":
            return client.list_work_logs(**kwargs)
        if action == "create_work_log":
            return client.create_work_log(**kwargs)
        raise ValueError(f"Unknown action: {action}")
