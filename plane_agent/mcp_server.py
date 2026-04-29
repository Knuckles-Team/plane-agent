#!/usr/bin/python
import warnings

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

# General urllib3/chardet mismatch warnings
warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import (
    config,
    create_mcp_server,
    ctx_confirm_destructive,
    ctx_progress,
)
from dotenv import find_dotenv, load_dotenv
from fastmcp import Context, FastMCP
from fastmcp.utilities.logging import get_logger
from pydantic import Field

from plane_agent.auth import get_client
from plane_agent.plane_models import Response

__version__ = "0.1.37"
print(f"Plane MCP v{__version__}", file=sys.stderr)

logger = get_logger(name="mcp_server")
logger.setLevel(logging.DEBUG)


DEFAULT_PLANE_URL = os.getenv("PLANE_BASE_URL", "https://api.plane.so")
DEFAULT_PLANE_KEY = os.getenv("PLANE_API_KEY", None)
DEFAULT_PLANE_WORKSPACE = os.getenv("PLANE_WORKSPACE_SLUG", None)


def register_projects_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"projects"},
    )
    def list_projects(
        plane_url: str | None = Field(
            description="Base URL of Plane instance",
            default=os.environ.get("PLANE_URL", DEFAULT_PLANE_URL),
        ),
        api_key: str | None = Field(
            description="Plane API key",
            default=os.environ.get("PLANE_API_KEY", DEFAULT_PLANE_KEY),
        ),
        workspace_slug: str | None = Field(
            description="Plane workspace slug",
            default=os.environ.get("PLANE_WORKSPACE_SLUG", DEFAULT_PLANE_WORKSPACE),
        ),
        verify: bool | None = Field(
            description="Verify SSL certificate",
            default=True,
        ),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List all projects in the workspace."""
        client = get_client(
            url=plane_url,
            api_key=api_key,
            workspace_slug=workspace_slug,
            verify=verify,
            config=config,
        )
        return client.list_projects()

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"projects"},
    )
    def retrieve_project(
        project_id: str = Field(description="UUID of the project"),
        plane_url: str | None = Field(
            description="Base URL of Plane instance",
            default=os.environ.get("PLANE_URL", DEFAULT_PLANE_URL),
        ),
        api_key: str | None = Field(
            description="Plane API key",
            default=os.environ.get("PLANE_API_KEY", DEFAULT_PLANE_KEY),
        ),
        workspace_slug: str | None = Field(
            description="Plane workspace slug",
            default=os.environ.get("PLANE_WORKSPACE_SLUG", DEFAULT_PLANE_WORKSPACE),
        ),
        verify: bool | None = Field(
            description="Verify SSL certificate",
            default=True,
        ),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Retrieve a project by ID."""
        client = get_client(
            url=plane_url,
            api_key=api_key,
            workspace_slug=workspace_slug,
            verify=verify,
            config=config,
        )
        return client.retrieve_project(project_id=project_id)


def _build_advanced_search_filters(
    assignee_ids: list[str] | None = None,
    state_ids: list[str] | None = None,
    state_groups: list[str] | None = None,
    priorities: list[str] | None = None,
    label_ids: list[str] | None = None,
    type_ids: list[str] | None = None,
    cycle_ids: list[str] | None = None,
    module_ids: list[str] | None = None,
) -> dict[str, Any] | None:
    """Build an AND filter dict from flat filter params."""
    conditions = []
    if assignee_ids:
        conditions.append({"assignee_id__in": assignee_ids})
    if state_ids:
        conditions.append({"state_id__in": state_ids})
    if state_groups:
        conditions.append({"state_group__in": state_groups})
    if priorities:
        conditions.append({"priority__in": priorities})
    if label_ids:
        conditions.append({"label_id__in": label_ids})
    if type_ids:
        conditions.append({"type_id__in": type_ids})
    if cycle_ids:
        conditions.append({"cycle_id__in": cycle_ids})
    if module_ids:
        conditions.append({"module_id__in": module_ids})

    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"and": conditions}


def register_work_items_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def list_work_items(
        project_id: str | None = Field(description="UUID of the project", default=None),
        query: str | None = Field(description="Search query", default=None),
        assignee_ids: list[str] | None = None,
        state_ids: list[str] | None = None,
        state_groups: list[str] | None = None,
        priorities: list[str] | None = None,
        label_ids: list[str] | None = None,
        type_ids: list[str] | None = None,
        cycle_ids: list[str] | None = None,
        module_ids: list[str] | None = None,
        plane_url: str | None = Field(
            description="Base URL of Plane instance",
            default=os.environ.get("PLANE_URL", DEFAULT_PLANE_URL),
        ),
        api_key: str | None = Field(
            description="Plane API key",
            default=os.environ.get("PLANE_API_KEY", DEFAULT_PLANE_KEY),
        ),
        workspace_slug: str | None = Field(
            description="Plane workspace slug",
            default=os.environ.get("PLANE_WORKSPACE_SLUG", DEFAULT_PLANE_WORKSPACE),
        ),
        verify: bool | None = Field(
            description="Verify SSL certificate",
            default=True,
        ),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List work items in a project or search across workspace."""
        client = get_client(
            url=plane_url,
            api_key=api_key,
            workspace_slug=workspace_slug,
            verify=verify,
            config=config,
        )

        filters = _build_advanced_search_filters(
            assignee_ids=assignee_ids,
            state_ids=state_ids,
            state_groups=state_groups,
            priorities=priorities,
            label_ids=label_ids,
            type_ids=type_ids,
            cycle_ids=cycle_ids,
            module_ids=module_ids,
        )

        if filters or query:
            data = {"query": query, "filters": filters, "project_id": project_id}
            return client.advanced_search_work_items(data=data)

        if not project_id:
            return Response(
                response=None,
                data={"error": "project_id is required for listing without filters."},
            )

        return client.list_work_items(project_id=project_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def create_work_item(
        project_id: str = Field(description="UUID of the project"),
        name: str = Field(description="Name of the work item"),
        description_html: str | None = None,
        priority: str | None = None,
        state_id: str | None = None,
        assignee_ids: list[str] | None = None,
        label_ids: list[str] | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Create a new work item."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {
            "name": name,
            "description_html": description_html,
            "priority": priority,
            "state_id": state_id,
            "assignees": assignee_ids,
            "labels": label_ids,
        }
        return client.create_work_item(project_id=project_id, data=data)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def update_work_item(
        project_id: str = Field(description="UUID of the project"),
        work_item_id: str = Field(description="UUID of the work item"),
        name: str | None = None,
        description_html: str | None = None,
        priority: str | None = None,
        state_id: str | None = None,
        assignee_ids: list[str] | None = None,
        label_ids: list[str] | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Update a work item."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        if description_html:
            data["description_html"] = description_html
        if priority:
            data["priority"] = priority
        if state_id:
            data["state_id"] = state_id
        if assignee_ids:
            data["assignees"] = assignee_ids
        if label_ids:
            data["labels"] = label_ids
        return client.update_work_item(
            project_id=project_id, work_item_id=work_item_id, data=data
        )

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    async def delete_work_item(
        project_id: str = Field(description="UUID of the project"),
        work_item_id: str = Field(description="UUID of the work item"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Delete a work item."""
        if not await ctx_confirm_destructive(ctx, "delete work item"):
            return {"status": "cancelled", "message": "Operation cancelled by user"}
        await ctx_progress(ctx, 0, 100)
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.delete_work_item(project_id=project_id, work_item_id=work_item_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def search_work_items(
        query: str = Field(description="Search query"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Search work items across workspace."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.search_work_items(query=query)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def retrieve_work_item_by_identifier(
        project_identifier: str = Field(description="Project identifier (e.g. MP)"),
        issue_identifier: int = Field(description="Issue sequence number (e.g. 1)"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Retrieve a work item by project identifier and issue sequence number."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.retrieve_work_item_by_identifier(
            project_identifier=project_identifier, issue_identifier=issue_identifier
        )

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def retrieve_work_item(
        project_id: str = Field(description="UUID of the project"),
        work_item_id: str = Field(description="UUID of the work item"),
        plane_url: str | None = Field(
            description="Base URL of Plane instance",
            default=os.environ.get("PLANE_URL", DEFAULT_PLANE_URL),
        ),
        api_key: str | None = Field(
            description="Plane API key",
            default=os.environ.get("PLANE_API_KEY", DEFAULT_PLANE_KEY),
        ),
        workspace_slug: str | None = Field(
            description="Plane workspace slug",
            default=os.environ.get("PLANE_WORKSPACE_SLUG", DEFAULT_PLANE_WORKSPACE),
        ),
        verify: bool | None = Field(
            description="Verify SSL certificate",
            default=True,
        ),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Retrieve a work item by ID."""
        client = get_client(
            url=plane_url,
            api_key=api_key,
            workspace_slug=workspace_slug,
            verify=verify,
            config=config,
        )
        return client.retrieve_work_item(
            project_id=project_id, work_item_id=work_item_id
        )

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def list_work_item_activities(
        project_id: str = Field(description="UUID of the project"),
        work_item_id: str = Field(description="UUID of the work item"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List activities for a work item."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_work_item_activities(
            project_id=project_id, work_item_id=work_item_id
        )

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def list_work_item_comments(
        project_id: str = Field(description="UUID of the project"),
        work_item_id: str = Field(description="UUID of the work item"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List comments for a work item."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_work_item_comments(
            project_id=project_id, work_item_id=work_item_id
        )

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def create_work_item_comment(
        project_id: str = Field(description="UUID of the project"),
        work_item_id: str = Field(description="UUID of the work item"),
        comment_html: str = Field(description="Comment content in HTML"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Create a comment for a work item."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {"comment_html": comment_html}
        return client.create_work_item_comment(
            project_id=project_id, work_item_id=work_item_id, data=data
        )

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def list_work_item_links(
        project_id: str = Field(description="UUID of the project"),
        work_item_id: str = Field(description="UUID of the work item"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List links for a work item."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_work_item_links(
            project_id=project_id, work_item_id=work_item_id
        )

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def create_work_item_link(
        project_id: str = Field(description="UUID of the project"),
        work_item_id: str = Field(description="UUID of the work item"),
        url: str = Field(description="URL of the link"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Create a link for a work item."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {"url": url}
        return client.create_work_item_link(
            project_id=project_id, work_item_id=work_item_id, data=data
        )

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def list_work_item_relations(
        project_id: str = Field(description="UUID of the project"),
        work_item_id: str = Field(description="UUID of the work item"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List relations for a work item."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_work_item_relations(
            project_id=project_id, work_item_id=work_item_id
        )

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def list_work_item_types(
        project_id: str = Field(description="UUID of the project"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List work item types in a project."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_work_item_types(project_id=project_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def list_work_logs(
        project_id: str = Field(description="UUID of the project"),
        work_item_id: str = Field(description="UUID of the work item"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List work logs for a work item."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_work_logs(project_id=project_id, work_item_id=work_item_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"work_items"},
    )
    def create_work_log(
        project_id: str = Field(description="UUID of the project"),
        work_item_id: str = Field(description="UUID of the work item"),
        duration: int = Field(description="Duration in minutes"),
        description: str | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Create a work log for a work item."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {"duration": duration, "description": description}
        return client.create_work_log(
            project_id=project_id, work_item_id=work_item_id, data=data
        )


def register_cycles_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"cycles"},
    )
    def list_cycles(
        project_id: str = Field(description="UUID of the project"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List cycles in a project."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_cycles(project_id=project_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"cycles"},
    )
    def create_cycle(
        project_id: str = Field(description="UUID of the project"),
        name: str = Field(description="Cycle name"),
        owned_by: str = Field(description="UUID of the owner"),
        description: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Create a new cycle."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {
            "name": name,
            "owned_by": owned_by,
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
        }
        return client.create_cycle(project_id=project_id, data=data)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"cycles"},
    )
    def retrieve_cycle(
        project_id: str = Field(description="UUID of the project"),
        cycle_id: str = Field(description="UUID of the cycle"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Retrieve a cycle by ID."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.retrieve_cycle(project_id=project_id, cycle_id=cycle_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"cycles"},
    )
    def update_cycle(
        project_id: str = Field(description="UUID of the project"),
        cycle_id: str = Field(description="UUID of the cycle"),
        name: str | None = None,
        description: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        owned_by: str | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Update a cycle by ID."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if start_date:
            data["start_date"] = start_date
        if end_date:
            data["end_date"] = end_date
        if owned_by:
            data["owned_by"] = owned_by
        return client.update_cycle(project_id=project_id, cycle_id=cycle_id, data=data)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"cycles"},
    )
    async def delete_cycle(
        project_id: str = Field(description="UUID of the project"),
        cycle_id: str = Field(description="UUID of the cycle"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Delete a cycle by ID."""
        if not await ctx_confirm_destructive(ctx, "delete cycle"):
            return {"status": "cancelled", "message": "Operation cancelled by user"}
        await ctx_progress(ctx, 0, 100)
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.delete_cycle(project_id=project_id, cycle_id=cycle_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"cycles"},
    )
    def list_cycle_work_items(
        project_id: str = Field(description="UUID of the project"),
        cycle_id: str = Field(description="UUID of the cycle"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List work items in a cycle."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_cycle_work_items(project_id=project_id, cycle_id=cycle_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"cycles"},
    )
    def add_work_items_to_cycle(
        project_id: str = Field(description="UUID of the project"),
        cycle_id: str = Field(description="UUID of the cycle"),
        issue_ids: list[str] = Field(description="List of work item IDs"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Add work items to a cycle."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.add_work_items_to_cycle(
            project_id=project_id, cycle_id=cycle_id, issue_ids=issue_ids
        )


def register_epics_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"epics"},
    )
    def list_epics(
        project_id: str = Field(description="UUID of the project"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List epics in a project."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_epics(project_id=project_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"epics"},
    )
    def create_epic(
        project_id: str = Field(description="UUID of the project"),
        name: str = Field(description="Epic name"),
        priority: str | None = None,
        description: str | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Create a new epic."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {"name": name, "priority": priority, "description": description}
        return client.create_epic(project_id=project_id, data=data)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"epics"},
    )
    def retrieve_epic(
        project_id: str = Field(description="UUID of the project"),
        epic_id: str = Field(description="UUID of the epic"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Retrieve an epic by ID."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.retrieve_epic(project_id=project_id, epic_id=epic_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"epics"},
    )
    def update_epic(
        project_id: str = Field(description="UUID of the project"),
        epic_id: str = Field(description="UUID of the epic"),
        name: str | None = None,
        priority: str | None = None,
        description: str | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Update an epic by ID."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        if priority:
            data["priority"] = priority
        if description:
            data["description"] = description
        return client.update_epic(project_id=project_id, epic_id=epic_id, data=data)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"epics"},
    )
    async def delete_epic(
        project_id: str = Field(description="UUID of the project"),
        epic_id: str = Field(description="UUID of the epic"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Delete an epic by ID."""
        if not await ctx_confirm_destructive(ctx, "delete epic"):
            return {"status": "cancelled", "message": "Operation cancelled by user"}
        await ctx_progress(ctx, 0, 100)
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.delete_epic(project_id=project_id, epic_id=epic_id)


def register_milestones_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"milestones"},
    )
    def list_milestones(
        project_id: str = Field(description="UUID of the project"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List milestones in a project."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_milestones(project_id=project_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"milestones"},
    )
    def create_milestone(
        project_id: str = Field(description="UUID of the project"),
        title: str = Field(description="Milestone title"),
        target_date: str | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Create a new milestone."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {"title": title, "target_date": target_date}
        return client.create_milestone(project_id=project_id, data=data)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"milestones"},
    )
    def retrieve_milestone(
        project_id: str = Field(description="UUID of the project"),
        milestone_id: str = Field(description="UUID of the milestone"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Retrieve a milestone by ID."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.retrieve_milestone(
            project_id=project_id, milestone_id=milestone_id
        )

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"milestones"},
    )
    def update_milestone(
        project_id: str = Field(description="UUID of the project"),
        milestone_id: str = Field(description="UUID of the milestone"),
        title: str | None = None,
        target_date: str | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Update a milestone by ID."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data: dict[str, Any] = {}
        if title:
            data["title"] = title
        if target_date:
            data["target_date"] = target_date
        return client.update_milestone(
            project_id=project_id, milestone_id=milestone_id, data=data
        )

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"milestones"},
    )
    async def delete_milestone(
        project_id: str = Field(description="UUID of the project"),
        milestone_id: str = Field(description="UUID of the milestone"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Delete a milestone by ID."""
        if not await ctx_confirm_destructive(ctx, "delete milestone"):
            return {"status": "cancelled", "message": "Operation cancelled by user"}
        await ctx_progress(ctx, 0, 100)
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.delete_milestone(project_id=project_id, milestone_id=milestone_id)


def register_modules_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"modules"},
    )
    def list_modules(
        project_id: str = Field(description="UUID of the project"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List modules in a project."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_modules(project_id=project_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"modules"},
    )
    def create_module(
        project_id: str = Field(description="UUID of the project"),
        name: str = Field(description="Module name"),
        description: str | None = None,
        status: str | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Create a new module."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {"name": name, "description": description, "status": status}
        return client.create_module(project_id=project_id, data=data)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"modules"},
    )
    def retrieve_module(
        project_id: str = Field(description="UUID of the project"),
        module_id: str = Field(description="UUID of the module"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Retrieve a module by ID."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.retrieve_module(project_id=project_id, module_id=module_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"modules"},
    )
    def update_module(
        project_id: str = Field(description="UUID of the project"),
        module_id: str = Field(description="UUID of the module"),
        name: str | None = None,
        description: str | None = None,
        status: str | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Update a module by ID."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data: dict[str, Any] = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if status:
            data["status"] = status
        return client.update_module(
            project_id=project_id, module_id=module_id, data=data
        )

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"modules"},
    )
    async def delete_module(
        project_id: str = Field(description="UUID of the project"),
        module_id: str = Field(description="UUID of the module"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Delete a module by ID."""
        if not await ctx_confirm_destructive(ctx, "delete module"):
            return {"status": "cancelled", "message": "Operation cancelled by user"}
        await ctx_progress(ctx, 0, 100)
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.delete_module(project_id=project_id, module_id=module_id)


def register_states_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"states"},
    )
    def list_states(
        project_id: str = Field(description="UUID of the project"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List states in a project."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_states(project_id=project_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"states"},
    )
    def create_state(
        project_id: str = Field(description="UUID of the project"),
        name: str = Field(description="State name"),
        color: str = Field(description="Hex color code"),
        group: str | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Create a new state."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {"name": name, "color": color, "group": group}
        return client.create_state(project_id=project_id, data=data)


def register_users_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"users"},
    )
    def list_users(
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List users in the workspace."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_users()

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"users"},
    )
    def get_me(
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Get current user information."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.get_me()


def register_workspaces_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"workspaces"},
    )
    def get_workspace(
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Get current workspace details."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.get_workspace()

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"workspaces"},
    )
    def get_workspace_members(
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Get all members of the current workspace."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.get_workspace_members()

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"workspaces"},
    )
    def get_workspace_features(
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Get features of the current workspace."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.get_workspace_features()

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"workspaces"},
    )
    def update_workspace_features(
        project_grouping: bool | None = None,
        initiatives: bool | None = None,
        teams: bool | None = None,
        customers: bool | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Update features of the current workspace."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data: dict[str, Any] = {}
        if project_grouping is not None:
            data["project_grouping"] = project_grouping
        if initiatives is not None:
            data["initiatives"] = initiatives
        if teams is not None:
            data["teams"] = teams
        if customers is not None:
            data["customers"] = customers
        return client.update_workspace_features(data=data)


def register_initiative_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"initiatives"},
    )
    def list_initiatives(
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List all initiatives in the workspace."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_initiatives()

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"initiatives"},
    )
    def create_initiative(
        name: str = Field(description="Initiative name"),
        description: str | None = None,
        state: str | None = None,
        lead: str | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Create a new initiative."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {"name": name, "description": description, "state": state, "lead": lead}
        return client.create_initiative(data=data)


def register_intake_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"intake"},
    )
    def list_intake_work_items(
        project_id: str = Field(description="UUID of the project"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List all intake work items in a project."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_intake_work_items(project_id=project_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"intake"},
    )
    def create_intake_work_item(
        project_id: str = Field(description="UUID of the project"),
        name: str = Field(description="Work item name"),
        description: str | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Create a new intake work item."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {"name": name, "description": description}
        return client.create_intake_work_item(project_id=project_id, data=data)


def register_label_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"labels"},
    )
    def list_labels(
        project_id: str = Field(description="UUID of the project"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """List all labels in a project."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.list_labels(project_id=project_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"labels"},
    )
    def create_label(
        project_id: str = Field(description="UUID of the project"),
        name: str = Field(description="Label name"),
        color: str | None = None,
        description: str | None = None,
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Create a new label."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {"name": name, "color": color, "description": description}
        return client.create_label(project_id=project_id, data=data)


def register_page_tools(mcp: FastMCP):
    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"pages"},
    )
    def retrieve_project_page(
        project_id: str = Field(description="UUID of the project"),
        page_id: str = Field(description="UUID of the page"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Retrieve a project page by ID."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        return client.retrieve_project_page(project_id=project_id, page_id=page_id)

    @mcp.tool(
        exclude_args=["plane_url", "api_key", "workspace_slug", "verify"],
        tags={"pages"},
    )
    def create_project_page(
        project_id: str = Field(description="UUID of the project"),
        name: str = Field(description="Page name"),
        description_html: str = Field(description="Content in HTML"),
        plane_url: str | None = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: str | None = Field(description="API key", default=DEFAULT_PLANE_KEY),
        workspace_slug: str | None = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: bool | None = Field(description="Verify SSL certificate", default=True),
        ctx: Context = Field(
            description="MCP context for progress reporting", default=None
        ),
    ) -> Response:
        """Create a project page."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {"name": name, "description_html": description_html}
        return client.create_project_page(project_id=project_id, data=data)


def register_prompts(mcp: FastMCP):
    """Register Plane-specific prompts."""

    @mcp.prompt(
        name="plane-work-summary",
        description="Get a summary of current work in Plane",
    )
    def plane_work_summary() -> str:
        return "Review active cycles, high-priority issues, and recently updated documents in the Plane workspace."


def register_all_tools(mcp: FastMCP) -> list[str]:
    """Register all Plane tool categories correctly gated by environment variables."""
    registered_tags = []

    # Mapping of toggle env var to (registration_func, tag_name)
    tool_mappings = [
        ("PROJECTS_TOOL", (register_projects_tools, "projects")),
        ("WORK_ITEMS_TOOL", (register_work_items_tools, "work_items")),
        ("CYCLES_TOOL", (register_cycles_tools, "cycles")),
        ("EPICS_TOOL", (register_epics_tools, "epics")),
        ("INITIATIVE_TOOL", (register_initiative_tools, "initiative")),
        ("INTAKE_TOOL", (register_intake_tools, "intake")),
        ("LABEL_TOOL", (register_label_tools, "label")),
        ("PAGE_TOOL", (register_page_tools, "page")),
        ("MILESTONES_TOOL", (register_milestones_tools, "milestones")),
        ("MODULES_TOOL", (register_modules_tools, "modules")),
        ("STATES_TOOL", (register_states_tools, "states")),
        ("USERS_TOOL", (register_users_tools, "users")),
        ("WORKSPACES_TOOL", (register_workspaces_tools, "workspaces")),
    ]

    for env_key, (register_func, tag) in tool_mappings:
        if to_boolean(os.getenv(env_key, "True")):
            register_func(mcp)
            registered_tags.append(tag)

    return registered_tags


def get_mcp_instance() -> tuple[Any, Any, Any, Any]:
    """Create and return the Plane MCP instance."""
    load_dotenv(find_dotenv())

    args, mcp, middlewares = create_mcp_server(
        name="plane",
        version=__version__,
        instructions="Plane MCP Server",
    )

    registered_tags = register_all_tools(mcp)
    register_prompts(mcp)

    for mw in middlewares:
        mcp.add_middleware(mw)

    return mcp, args, middlewares, registered_tags


def mcp_server():
    """Run the Plane MCP server."""
    mcp, args, middlewares, registered_tags = get_mcp_instance()

    print(f"Plane Agent MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)
    print(f"  Auth: {args.auth_type}", file=sys.stderr)
    print(f"  Dynamic Tags Loaded: {registered_tags}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error(f"Invalid transport: {args.transport}")
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
