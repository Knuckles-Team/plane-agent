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

import os
import sys
import logging
from typing import Optional, List, Dict, Any

from pydantic import Field
from fastmcp import FastMCP
from fastmcp.utilities.logging import get_logger
from plane_agent.plane_models import Response
from agent_utilities.mcp_utilities import (
    config,
)
from plane_agent.auth import get_client

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
        plane_url: Optional[str] = Field(
            description="Base URL of Plane instance",
            default=os.environ.get("PLANE_URL", DEFAULT_PLANE_URL),
        ),
        api_key: Optional[str] = Field(
            description="Plane API key",
            default=os.environ.get("PLANE_API_KEY", DEFAULT_PLANE_KEY),
        ),
        workspace_slug: Optional[str] = Field(
            description="Plane workspace slug",
            default=os.environ.get("PLANE_WORKSPACE_SLUG", DEFAULT_PLANE_WORKSPACE),
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=True,
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
        plane_url: Optional[str] = Field(
            description="Base URL of Plane instance",
            default=os.environ.get("PLANE_URL", DEFAULT_PLANE_URL),
        ),
        api_key: Optional[str] = Field(
            description="Plane API key",
            default=os.environ.get("PLANE_API_KEY", DEFAULT_PLANE_KEY),
        ),
        workspace_slug: Optional[str] = Field(
            description="Plane workspace slug",
            default=os.environ.get("PLANE_WORKSPACE_SLUG", DEFAULT_PLANE_WORKSPACE),
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=True,
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
    assignee_ids: Optional[List[str]] = None,
    state_ids: Optional[List[str]] = None,
    state_groups: Optional[List[str]] = None,
    priorities: Optional[List[str]] = None,
    label_ids: Optional[List[str]] = None,
    type_ids: Optional[List[str]] = None,
    cycle_ids: Optional[List[str]] = None,
    module_ids: Optional[List[str]] = None,
) -> Optional[Dict[str, Any]]:
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
        project_id: Optional[str] = Field(
            description="UUID of the project", default=None
        ),
        query: Optional[str] = Field(description="Search query", default=None),
        assignee_ids: Optional[List[str]] = None,
        state_ids: Optional[List[str]] = None,
        state_groups: Optional[List[str]] = None,
        priorities: Optional[List[str]] = None,
        label_ids: Optional[List[str]] = None,
        type_ids: Optional[List[str]] = None,
        cycle_ids: Optional[List[str]] = None,
        module_ids: Optional[List[str]] = None,
        plane_url: Optional[str] = Field(
            description="Base URL of Plane instance",
            default=os.environ.get("PLANE_URL", DEFAULT_PLANE_URL),
        ),
        api_key: Optional[str] = Field(
            description="Plane API key",
            default=os.environ.get("PLANE_API_KEY", DEFAULT_PLANE_KEY),
        ),
        workspace_slug: Optional[str] = Field(
            description="Plane workspace slug",
            default=os.environ.get("PLANE_WORKSPACE_SLUG", DEFAULT_PLANE_WORKSPACE),
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=True,
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
        description_html: Optional[str] = None,
        priority: Optional[str] = None,
        state_id: Optional[str] = None,
        assignee_ids: Optional[List[str]] = None,
        label_ids: Optional[List[str]] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        name: Optional[str] = None,
        description_html: Optional[str] = None,
        priority: Optional[str] = None,
        state_id: Optional[str] = None,
        assignee_ids: Optional[List[str]] = None,
        label_ids: Optional[List[str]] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
        ),
    ) -> Response:
        """Update a work item."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {}
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
    def delete_work_item(
        project_id: str = Field(description="UUID of the project"),
        work_item_id: str = Field(description="UUID of the work item"),
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
        ),
    ) -> Response:
        """Delete a work item."""
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL of Plane instance",
            default=os.environ.get("PLANE_URL", DEFAULT_PLANE_URL),
        ),
        api_key: Optional[str] = Field(
            description="Plane API key",
            default=os.environ.get("PLANE_API_KEY", DEFAULT_PLANE_KEY),
        ),
        workspace_slug: Optional[str] = Field(
            description="Plane workspace slug",
            default=os.environ.get("PLANE_WORKSPACE_SLUG", DEFAULT_PLANE_WORKSPACE),
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate",
            default=True,
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        description: Optional[str] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        description: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        name: Optional[str] = None,
        description: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        owned_by: Optional[str] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
        ),
    ) -> Response:
        """Update a cycle by ID."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {}
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
    def delete_cycle(
        project_id: str = Field(description="UUID of the project"),
        cycle_id: str = Field(description="UUID of the cycle"),
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
        ),
    ) -> Response:
        """Delete a cycle by ID."""
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        issue_ids: List[str] = Field(description="List of work item IDs"),
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        priority: Optional[str] = None,
        description: Optional[str] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        name: Optional[str] = None,
        priority: Optional[str] = None,
        description: Optional[str] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
        ),
    ) -> Response:
        """Update an epic by ID."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {}
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
    def delete_epic(
        project_id: str = Field(description="UUID of the project"),
        epic_id: str = Field(description="UUID of the epic"),
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
        ),
    ) -> Response:
        """Delete an epic by ID."""
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        target_date: Optional[str] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        title: Optional[str] = None,
        target_date: Optional[str] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
        ),
    ) -> Response:
        """Update a milestone by ID."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {}
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
    def delete_milestone(
        project_id: str = Field(description="UUID of the project"),
        milestone_id: str = Field(description="UUID of the milestone"),
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
        ),
    ) -> Response:
        """Delete a milestone by ID."""
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        description: Optional[str] = None,
        status: Optional[str] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
        ),
    ) -> Response:
        """Update a module by ID."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {}
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
    def delete_module(
        project_id: str = Field(description="UUID of the project"),
        module_id: str = Field(description="UUID of the module"),
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
        ),
    ) -> Response:
        """Delete a module by ID."""
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        group: Optional[str] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        project_grouping: Optional[bool] = None,
        initiatives: Optional[bool] = None,
        teams: Optional[bool] = None,
        customers: Optional[bool] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
        ),
    ) -> Response:
        """Update features of the current workspace."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {}
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        description: Optional[str] = None,
        state: Optional[str] = None,
        lead: Optional[str] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        description: Optional[str] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        color: Optional[str] = None,
        description: Optional[str] = None,
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
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
        plane_url: Optional[str] = Field(
            description="Base URL", default=DEFAULT_PLANE_URL
        ),
        api_key: Optional[str] = Field(
            description="API key", default=DEFAULT_PLANE_KEY
        ),
        workspace_slug: Optional[str] = Field(
            description="Workspace slug", default=DEFAULT_PLANE_WORKSPACE
        ),
        verify: Optional[bool] = Field(
            description="Verify SSL certificate", default=True
        ),
    ) -> Response:
        """Create a project page."""
        client = get_client(
            url=plane_url, api_key=api_key, workspace_slug=workspace_slug, verify=verify
        )
        data = {"name": name, "description_html": description_html}
        return client.create_project_page(project_id=project_id, data=data)


def get_mcp_instance() -> FastMCP:
    """Create and return the Plane MCP instance."""
    mcp = FastMCP("Plane MCP Server", version=__version__)

    register_projects_tools(mcp)
    register_work_items_tools(mcp)
    register_cycles_tools(mcp)
    register_epics_tools(mcp)
    register_initiative_tools(mcp)
    register_intake_tools(mcp)
    register_label_tools(mcp)
    register_page_tools(mcp)
    register_milestones_tools(mcp)
    register_modules_tools(mcp)
    register_states_tools(mcp)
    register_users_tools(mcp)
    register_workspaces_tools(mcp)

    return mcp


def mcp_server():
    mcp = get_mcp_instance()
    mcp.run()


def main():
    mcp_server()


if __name__ == "__main__":
    mcp_server()