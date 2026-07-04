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
import sys
from typing import Any

from agent_utilities.core.config import setting
from agent_utilities.mcp_utilities import (
    create_mcp_server,
    load_config,
    register_tool_surface,
    resolve_action,
    run_blocking,
)
from starlette.requests import Request
from starlette.responses import JSONResponse

from plane_agent.api_client import Api
from plane_agent.auth import get_client

__version__ = "0.1.37"

logger = get_logger(name="plane-agent")
logger.setLevel(logging.INFO)

# Native KG ingestion is default-on; set PLANE_KG_INGEST=false to disable the
# best-effort push that rides the list_* fetch flow. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
_KG_AUTO_INGEST = str(setting("PLANE_KG_INGEST", "true")).lower() not in (
    "0",
    "false",
    "no",
)


def _kg_records(result: Any, key: str = "results") -> list[dict[str, Any]]:
    """Normalize a client Response/list into a list of plain record dicts."""
    data = getattr(result, "data", result)
    if isinstance(data, dict):
        data = data.get(key, data.get("data", data))
    records = data if isinstance(data, list) else [data]
    out: list[dict[str, Any]] = []
    for r in records:
        if r is None:
            continue
        out.append(r.model_dump() if hasattr(r, "model_dump") else r)
    return [r for r in out if isinstance(r, dict)]


def _auto_ingest(kind: str, result: Any, **ctx: Any) -> None:
    """Best-effort push of freshly-listed records into the KG (never raises)."""
    if not _KG_AUTO_INGEST:
        return
    try:
        from plane_agent import kg_ingest

        records = _kg_records(result)
        if kind == "projects":
            kg_ingest.ingest_projects(records, workspace_slug=ctx.get("workspace_slug"))
        elif kind == "work_items":
            kg_ingest.ingest_work_items(records, project_id=ctx.get("project_id"))
        elif kind == "cycles":
            kg_ingest.ingest_cycles(records, project_id=ctx.get("project_id"))
    except Exception as e:  # noqa: BLE001 — ingestion is best-effort
        logger.debug("KG auto-ingest skipped (%s): %s", kind, e)


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

        valid_actions = ("list_projects", "retrieve_project")
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "list_projects":
            result = await run_blocking(client.list_projects, **kwargs)
            _auto_ingest(
                "projects",
                result,
                workspace_slug=getattr(client, "workspace_slug", None),
            )
            return result
        if action == "retrieve_project":
            return await run_blocking(client.retrieve_project, **kwargs)
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

        valid_actions = (
            "list_work_items",
            "create_work_item",
            "update_work_item",
            "delete_work_item",
            "search_work_items",
            "retrieve_work_item_by_identifier",
            "retrieve_work_item",
            "list_work_item_activities",
            "list_work_item_comments",
            "create_work_item_comment",
            "list_work_item_links",
            "create_work_item_link",
            "list_work_item_relations",
            "list_work_item_types",
            "list_work_logs",
            "create_work_log",
        )
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "list_work_items":
            result = await run_blocking(client.list_work_items, **kwargs)
            _auto_ingest("work_items", result, project_id=kwargs.get("project_id"))
            return result
        if action == "create_work_item":
            return await run_blocking(client.create_work_item, **kwargs)
        if action == "update_work_item":
            return await run_blocking(client.update_work_item, **kwargs)
        if action == "delete_work_item":
            return await run_blocking(client.delete_work_item, **kwargs)
        if action == "search_work_items":
            return await run_blocking(client.search_work_items, **kwargs)
        if action == "retrieve_work_item_by_identifier":
            return await run_blocking(client.retrieve_work_item_by_identifier, **kwargs)
        if action == "retrieve_work_item":
            return await run_blocking(client.retrieve_work_item, **kwargs)
        if action == "list_work_item_activities":
            return await run_blocking(client.list_work_item_activities, **kwargs)
        if action == "list_work_item_comments":
            return await run_blocking(client.list_work_item_comments, **kwargs)
        if action == "create_work_item_comment":
            return await run_blocking(client.create_work_item_comment, **kwargs)
        if action == "list_work_item_links":
            return await run_blocking(client.list_work_item_links, **kwargs)
        if action == "create_work_item_link":
            return await run_blocking(client.create_work_item_link, **kwargs)
        if action == "list_work_item_relations":
            return await run_blocking(client.list_work_item_relations, **kwargs)
        if action == "list_work_item_types":
            return await run_blocking(client.list_work_item_types, **kwargs)
        if action == "list_work_logs":
            return await run_blocking(client.list_work_logs, **kwargs)
        if action == "create_work_log":
            return await run_blocking(client.create_work_log, **kwargs)
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
            result = await run_blocking(client.list_cycles, **kwargs)
            _auto_ingest("cycles", result, project_id=kwargs.get("project_id"))
            return result
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

        valid_actions = (
            "list_milestones",
            "create_milestone",
            "retrieve_milestone",
            "update_milestone",
            "delete_milestone",
        )
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "list_milestones":
            return await run_blocking(client.list_milestones, **kwargs)
        if action == "create_milestone":
            return await run_blocking(client.create_milestone, **kwargs)
        if action == "retrieve_milestone":
            return await run_blocking(client.retrieve_milestone, **kwargs)
        if action == "update_milestone":
            return await run_blocking(client.update_milestone, **kwargs)
        if action == "delete_milestone":
            return await run_blocking(client.delete_milestone, **kwargs)
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

        valid_actions = ("list_users", "get_me")
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "list_users":
            return await run_blocking(client.list_users, **kwargs)
        if action == "get_me":
            return await run_blocking(client.get_me, **kwargs)
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

        valid_actions = ("list_initiatives", "create_initiative")
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "list_initiatives":
            return await run_blocking(client.list_initiatives, **kwargs)
        if action == "create_initiative":
            return await run_blocking(client.create_initiative, **kwargs)
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

        valid_actions = ("list_labels", "create_label")
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        if action == "list_labels":
            return await run_blocking(client.list_labels, **kwargs)
        if action == "create_label":
            return await run_blocking(client.create_label, **kwargs)
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


def register_kg_tools(mcp: FastMCP):
    @mcp.tool(tags={"kg"})
    async def plane_ingest(
        action: str = Field(
            description="Action to perform. Must be one of: 'ingest_projects', 'ingest_work_items', 'ingest_cycles'"
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of the underlying list_* params (ingest_work_items / ingest_cycles require 'project_id').",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Natively ingest Plane records into epistemic-graph as typed OWL nodes.

        Lists records via the Plane API, then pushes them as typed nodes + links via the
        fast engine client (best-effort — returns ``{"ingested": null}`` with no engine):
        'ingest_projects' → :SoftwareProject (+ :Workspace / :inWorkspace);
        'ingest_work_items' → :Issue (+ :belongsToProject / :assignedTo / :hasState / :inCycle);
        'ingest_cycles' → :Cycle (+ :belongsToProject).
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        if ctx:
            await ctx.info("Executing tool...")
        import json

        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}

        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        valid_actions = ("ingest_projects", "ingest_work_items", "ingest_cycles")
        resolved = resolve_action(action, valid_actions, service="plane-agent")
        if isinstance(resolved, dict):
            return resolved
        action = resolved

        from plane_agent import kg_ingest

        if action == "ingest_projects":
            result = await run_blocking(client.list_projects, **kwargs)
            records = _kg_records(result)
            ingested = kg_ingest.ingest_projects(
                records, workspace_slug=getattr(client, "workspace_slug", None)
            )
            return {"listed": len(records), "ingested": ingested}
        if action == "ingest_work_items":
            result = await run_blocking(client.list_work_items, **kwargs)
            records = _kg_records(result)
            ingested = kg_ingest.ingest_work_items(
                records, project_id=kwargs.get("project_id")
            )
            return {"listed": len(records), "ingested": ingested}
        if action == "ingest_cycles":
            result = await run_blocking(client.list_cycles, **kwargs)
            records = _kg_records(result)
            ingested = kg_ingest.ingest_cycles(
                records, project_id=kwargs.get("project_id")
            )
            return {"listed": len(records), "ingested": ingested}
        raise ValueError(f"Unknown action: {action}")

    return None


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance.

        Ecosystem Concepts:
    (MCP & Universal Skills)
    (Guardrail Engine)
    """
    load_config()
    args, mcp, middlewares = create_mcp_server(
        name="plane-agent MCP",
        version=__version__,
        instructions="plane-agent MCP Server — Condensed Action-Routed Tools.",
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    register_tool_surface(
        mcp,
        client_cls=Api,
        get_client=get_client,
        service="plane-agent",
        tools_module=sys.modules[__name__],
    )

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
