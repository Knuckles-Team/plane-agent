#!/usr/bin/python
import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from starlette.requests import Request
from starlette.responses import JSONResponse

from plane_agent.auth import get_client

__version__ = "0.1.37"

logger = get_logger(name="plane-agent")
logger.setLevel(logging.INFO)


def register_projects_tools(mcp: FastMCP):
    @mcp.tool(tags={"projects"})
    async def plane_projects(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_projects', 'retrieve_project'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane projects operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_projects":
            return client.list_projects(**kwargs)
        if action == "retrieve_project":
            return client.retrieve_project(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_work_items_tools(mcp: FastMCP):
    @mcp.tool(tags={"work_items"})
    async def plane_work_items(
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


def register_cycles_tools(mcp: FastMCP):
    @mcp.tool(tags={"cycles"})
    async def plane_cycles(
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

        if action == "list_cycles":
            return client.list_cycles(**kwargs)
        if action == "create_cycle":
            return client.create_cycle(**kwargs)
        if action == "retrieve_cycle":
            return client.retrieve_cycle(**kwargs)
        if action == "update_cycle":
            return client.update_cycle(**kwargs)
        if action == "delete_cycle":
            return client.delete_cycle(**kwargs)
        if action == "list_cycle_work_items":
            return client.list_cycle_work_items(**kwargs)
        if action == "add_work_items_to_cycle":
            return client.add_work_items_to_cycle(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_epics_tools(mcp: FastMCP):
    @mcp.tool(tags={"epics"})
    async def plane_epics(
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

        if action == "list_epics":
            return client.list_epics(**kwargs)
        if action == "create_epic":
            return client.create_epic(**kwargs)
        if action == "retrieve_epic":
            return client.retrieve_epic(**kwargs)
        if action == "update_epic":
            return client.update_epic(**kwargs)
        if action == "delete_epic":
            return client.delete_epic(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_milestones_tools(mcp: FastMCP):
    @mcp.tool(tags={"milestones"})
    async def plane_milestones(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_milestones', 'create_milestone', 'retrieve_milestone', 'update_milestone', 'delete_milestone'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane milestones operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_milestones":
            return client.list_milestones(**kwargs)
        if action == "create_milestone":
            return client.create_milestone(**kwargs)
        if action == "retrieve_milestone":
            return client.retrieve_milestone(**kwargs)
        if action == "update_milestone":
            return client.update_milestone(**kwargs)
        if action == "delete_milestone":
            return client.delete_milestone(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_modules_tools(mcp: FastMCP):
    @mcp.tool(tags={"modules"})
    async def plane_modules(
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

        if action == "list_modules":
            return client.list_modules(**kwargs)
        if action == "create_module":
            return client.create_module(**kwargs)
        if action == "retrieve_module":
            return client.retrieve_module(**kwargs)
        if action == "update_module":
            return client.update_module(**kwargs)
        if action == "delete_module":
            return client.delete_module(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_states_tools(mcp: FastMCP):
    @mcp.tool(tags={"states"})
    async def plane_states(
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


def register_users_tools(mcp: FastMCP):
    @mcp.tool(tags={"users"})
    async def plane_users(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_users', 'get_me'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane users operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_users":
            return client.list_users(**kwargs)
        if action == "get_me":
            return client.get_me(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_workspaces_tools(mcp: FastMCP):
    @mcp.tool(tags={"workspaces"})
    async def plane_workspaces(
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

        if action == "get_workspace":
            return client.get_workspace(**kwargs)
        if action == "get_workspace_members":
            return client.get_workspace_members(**kwargs)
        if action == "get_workspace_features":
            return client.get_workspace_features(**kwargs)
        if action == "update_workspace_features":
            return client.update_workspace_features(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_initiatives_tools(mcp: FastMCP):
    @mcp.tool(tags={"initiatives"})
    async def plane_initiatives(
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


def register_intake_tools(mcp: FastMCP):
    @mcp.tool(tags={"intake"})
    async def plane_intake(
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
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_intake_work_items":
            return client.list_intake_work_items(**kwargs)
        if action == "create_intake_work_item":
            return client.create_intake_work_item(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_labels_tools(mcp: FastMCP):
    @mcp.tool(tags={"labels"})
    async def plane_labels(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_labels', 'create_label'"
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage plane labels operations."""
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "list_labels":
            return client.list_labels(**kwargs)
        if action == "create_label":
            return client.create_label(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def register_pages_tools(mcp: FastMCP):
    @mcp.tool(tags={"pages"})
    async def plane_pages(
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
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if action == "retrieve_project_page":
            return client.retrieve_project_page(**kwargs)
        if action == "create_project_page":
            return client.create_project_page(**kwargs)
        raise ValueError(f"Unknown action: {action}")


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance.

        Ecosystem Concepts:
    (MCP & Universal Skills)
    (Guardrail Engine)
    """
    load_dotenv(find_dotenv())
    args, mcp, middlewares = create_mcp_server(
        name="plane-agent MCP",
        version=__version__,
        instructions="plane-agent MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    DEFAULT_PROJECTSTOOL = to_boolean(os.getenv("PROJECTSTOOL", "True"))
    if DEFAULT_PROJECTSTOOL:
        register_projects_tools(mcp)
    DEFAULT_WORK_ITEMSTOOL = to_boolean(os.getenv("WORK_ITEMSTOOL", "True"))
    if DEFAULT_WORK_ITEMSTOOL:
        register_work_items_tools(mcp)
    DEFAULT_CYCLESTOOL = to_boolean(os.getenv("CYCLESTOOL", "True"))
    if DEFAULT_CYCLESTOOL:
        register_cycles_tools(mcp)
    DEFAULT_EPICSTOOL = to_boolean(os.getenv("EPICSTOOL", "True"))
    if DEFAULT_EPICSTOOL:
        register_epics_tools(mcp)
    DEFAULT_MILESTONESTOOL = to_boolean(os.getenv("MILESTONESTOOL", "True"))
    if DEFAULT_MILESTONESTOOL:
        register_milestones_tools(mcp)
    DEFAULT_MODULESTOOL = to_boolean(os.getenv("MODULESTOOL", "True"))
    if DEFAULT_MODULESTOOL:
        register_modules_tools(mcp)
    DEFAULT_STATESTOOL = to_boolean(os.getenv("STATESTOOL", "True"))
    if DEFAULT_STATESTOOL:
        register_states_tools(mcp)
    DEFAULT_USERSTOOL = to_boolean(os.getenv("USERSTOOL", "True"))
    if DEFAULT_USERSTOOL:
        register_users_tools(mcp)
    DEFAULT_WORKSPACESTOOL = to_boolean(os.getenv("WORKSPACESTOOL", "True"))
    if DEFAULT_WORKSPACESTOOL:
        register_workspaces_tools(mcp)
    DEFAULT_INITIATIVESTOOL = to_boolean(os.getenv("INITIATIVESTOOL", "True"))
    if DEFAULT_INITIATIVESTOOL:
        register_initiatives_tools(mcp)
    DEFAULT_INTAKETOOL = to_boolean(os.getenv("INTAKETOOL", "True"))
    if DEFAULT_INTAKETOOL:
        register_intake_tools(mcp)
    DEFAULT_LABELSTOOL = to_boolean(os.getenv("LABELSTOOL", "True"))
    if DEFAULT_LABELSTOOL:
        register_labels_tools(mcp)
    DEFAULT_PAGESTOOL = to_boolean(os.getenv("PAGESTOOL", "True"))
    if DEFAULT_PAGESTOOL:
        register_pages_tools(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    mcp, args, middlewares = get_mcp_instance()
    print(f"plane-agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error("Invalid transport", extra={"transport": args.transport})
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
