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

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
import os
import sys
from typing import Any

from agent_utilities.base_utilities import to_boolean
from agent_utilities.mcp_utilities import create_mcp_server
from dotenv import find_dotenv, load_dotenv
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field
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
        project_id: str | None = Field(default=None, description="project id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage projects operations.

        Actions:
          - 'list_projects': List all projects in the workspace.
          - 'retrieve_project': Retrieve a project by ID.
        """
        kwargs: dict[str, Any]
        if action == "list_projects":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_projects(**kwargs)
        if action == "retrieve_project":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.retrieve_project(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_projects', 'retrieve_project"
        )


def register_work_items_tools(mcp: FastMCP):
    @mcp.tool(tags={"work_items"})
    async def plane_work_items(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_work_items', 'create_work_item', 'update_work_item', 'delete_work_item', 'search_work_items', 'retrieve_work_item_by_identifier', 'retrieve_work_item', 'list_work_item_activities', 'list_work_item_comments', 'create_work_item_comment', 'list_work_item_links', 'create_work_item_link', 'list_work_item_relations', 'list_work_item_types', 'list_work_logs', 'create_work_log'"
        ),
        project_id: str | None = Field(default=None, description="project id"),
        work_item_id: str | None = Field(default=None, description="work item id"),
        data: dict[str, Any] | None = Field(default=None, description="data"),
        project_identifier: str | None = Field(
            default=None, description="project identifier"
        ),
        issue_identifier: int | None = Field(
            default=None, description="issue identifier"
        ),
        query: str | None = Field(default=None, description="query"),
        client=Depends(get_client),
    ) -> dict:
        """Manage work items operations.

        Actions:
          - 'list_work_items': List work items in a project.
          - 'create_work_item': Create a new work item.
          - 'update_work_item': Update a work item by ID.
          - 'delete_work_item': Delete a work item by ID.
          - 'search_work_items': Search work items across a workspace.
          - 'retrieve_work_item_by_identifier': Retrieve a work item by project identifier and issue sequence number.
          - 'retrieve_work_item': Retrieve a work item by ID.
          - 'list_work_item_activities': List activities for a work item.
          - 'list_work_item_comments': List comments for a work item.
          - 'create_work_item_comment': Create a comment for a work item.
          - 'list_work_item_links': List links for a work item.
          - 'create_work_item_link': Create a link for a work item.
          - 'list_work_item_relations': List relations for a work item.
          - 'list_work_item_types': List work item types in a project.
          - 'list_work_logs': List work logs for a work item.
          - 'create_work_log': Create a work log for a work item.
        """
        kwargs: dict[str, Any]
        if action == "list_work_items":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_work_items(**kwargs)
        if action == "create_work_item":
            kwargs = {"project_id": project_id, "data": data}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_work_item(**kwargs)
        if action == "update_work_item":
            kwargs = {
                "project_id": project_id,
                "work_item_id": work_item_id,
                "data": data,  # type: ignore
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_work_item(**kwargs)
        if action == "delete_work_item":
            kwargs = {
                "project_id": project_id,
                "work_item_id": work_item_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_work_item(**kwargs)
        if action == "search_work_items":
            kwargs = {"query": query}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.search_work_items(**kwargs)
        if action == "retrieve_work_item_by_identifier":
            kwargs = {
                "project_identifier": project_identifier,
                "issue_identifier": issue_identifier,  # type: ignore
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.retrieve_work_item_by_identifier(**kwargs)
        if action == "retrieve_work_item":
            kwargs = {
                "project_id": project_id,
                "work_item_id": work_item_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.retrieve_work_item(**kwargs)
        if action == "list_work_item_activities":
            kwargs = {
                "project_id": project_id,
                "work_item_id": work_item_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_work_item_activities(**kwargs)
        if action == "list_work_item_comments":
            kwargs = {
                "project_id": project_id,
                "work_item_id": work_item_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_work_item_comments(**kwargs)
        if action == "create_work_item_comment":
            kwargs = {
                "project_id": project_id,
                "work_item_id": work_item_id,
                "data": data,  # type: ignore
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_work_item_comment(**kwargs)
        if action == "list_work_item_links":
            kwargs = {
                "project_id": project_id,
                "work_item_id": work_item_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_work_item_links(**kwargs)
        if action == "create_work_item_link":
            kwargs = {
                "project_id": project_id,
                "work_item_id": work_item_id,
                "data": data,  # type: ignore
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_work_item_link(**kwargs)
        if action == "list_work_item_relations":
            kwargs = {
                "project_id": project_id,
                "work_item_id": work_item_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_work_item_relations(**kwargs)
        if action == "list_work_item_types":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_work_item_types(**kwargs)
        if action == "list_work_logs":
            kwargs = {
                "project_id": project_id,
                "work_item_id": work_item_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_work_logs(**kwargs)
        if action == "create_work_log":
            kwargs = {
                "project_id": project_id,
                "work_item_id": work_item_id,
                "data": data,  # type: ignore
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_work_log(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_work_items', 'create_work_item', 'update_work_item', 'delete_work_item', 'search_work_items', 'retrieve_work_item_by_identifier', 'retrieve_work_item', 'list_work_item_activities', 'list_work_item_comments', 'create_work_item_comment', 'list_work_item_links', 'create_work_item_link', 'list_work_item_relations', 'list_work_item_types', 'list_work_logs', 'create_work_log"
        )


def register_cycles_tools(mcp: FastMCP):
    @mcp.tool(tags={"cycles"})
    async def plane_cycles(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_cycles', 'create_cycle', 'retrieve_cycle', 'update_cycle', 'delete_cycle', 'list_cycle_work_items', 'add_work_items_to_cycle'"
        ),
        project_id: str | None = Field(default=None, description="project id"),
        data: dict[str, Any] | None = Field(default=None, description="data"),
        cycle_id: str | None = Field(default=None, description="cycle id"),
        issue_ids: list[str] | None = Field(default=None, description="issue ids"),
        client=Depends(get_client),
    ) -> dict:
        """Manage cycles operations.

        Actions:
          - 'list_cycles': List all cycles in a project.
          - 'create_cycle': Create a new cycle.
          - 'retrieve_cycle': Retrieve a cycle by ID.
          - 'update_cycle': Update a cycle by ID.
          - 'delete_cycle': Call delete_cycle
          - 'list_cycle_work_items': List work items in a cycle.
          - 'add_work_items_to_cycle': Add work items to a cycle.
        """
        kwargs: dict[str, Any]
        if action == "list_cycles":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_cycles(**kwargs)
        if action == "create_cycle":
            kwargs = {"project_id": project_id, "data": data}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_cycle(**kwargs)
        if action == "retrieve_cycle":
            kwargs = {"project_id": project_id, "cycle_id": cycle_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.retrieve_cycle(**kwargs)
        if action == "update_cycle":
            kwargs = {
                "project_id": project_id,
                "cycle_id": cycle_id,
                "data": data,
            }  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_cycle(**kwargs)
        if action == "delete_cycle":
            kwargs = {"project_id": project_id, "cycle_id": cycle_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_cycle(**kwargs)
        if action == "list_cycle_work_items":
            kwargs = {"project_id": project_id, "cycle_id": cycle_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_cycle_work_items(**kwargs)
        if action == "add_work_items_to_cycle":
            kwargs = {
                "project_id": project_id,
                "cycle_id": cycle_id,
                "issue_ids": issue_ids,  # type: ignore
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.add_work_items_to_cycle(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_cycles', 'create_cycle', 'retrieve_cycle', 'update_cycle', 'delete_cycle', 'list_cycle_work_items', 'add_work_items_to_cycle"
        )


def register_epics_tools(mcp: FastMCP):
    @mcp.tool(tags={"epics"})
    async def plane_epics(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_epics', 'create_epic', 'retrieve_epic', 'update_epic', 'delete_epic'"
        ),
        project_id: str | None = Field(default=None, description="project id"),
        data: dict[str, Any] | None = Field(default=None, description="data"),
        epic_id: str | None = Field(default=None, description="epic id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage epics operations.

        Actions:
          - 'list_epics': List all epics in a project.
          - 'create_epic': Create a new epic (technically a work item with epic type).
          - 'retrieve_epic': Retrieve an epic by ID.
          - 'update_epic': Update an epic by ID.
          - 'delete_epic': Delete an epic by ID.
        """
        kwargs: dict[str, Any]
        if action == "list_epics":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_epics(**kwargs)
        if action == "create_epic":
            kwargs = {"project_id": project_id, "data": data}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_epic(**kwargs)
        if action == "retrieve_epic":
            kwargs = {"project_id": project_id, "epic_id": epic_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.retrieve_epic(**kwargs)
        if action == "update_epic":
            kwargs = {
                "project_id": project_id,
                "epic_id": epic_id,
                "data": data,
            }  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_epic(**kwargs)
        if action == "delete_epic":
            kwargs = {"project_id": project_id, "epic_id": epic_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_epic(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_epics', 'create_epic', 'retrieve_epic', 'update_epic', 'delete_epic"
        )


def register_milestones_tools(mcp: FastMCP):
    @mcp.tool(tags={"milestones"})
    async def plane_milestones(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_milestones', 'create_milestone', 'retrieve_milestone', 'update_milestone', 'delete_milestone'"
        ),
        project_id: str | None = Field(default=None, description="project id"),
        data: dict[str, Any] | None = Field(default=None, description="data"),
        milestone_id: str | None = Field(default=None, description="milestone id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage milestones operations.

        Actions:
          - 'list_milestones': List all milestones in a project.
          - 'create_milestone': Create a new milestone.
          - 'retrieve_milestone': Retrieve a milestone by ID.
          - 'update_milestone': Update a milestone by ID.
          - 'delete_milestone': Delete a milestone by ID.
        """
        kwargs: dict[str, Any]
        if action == "list_milestones":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_milestones(**kwargs)
        if action == "create_milestone":
            kwargs = {"project_id": project_id, "data": data}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_milestone(**kwargs)
        if action == "retrieve_milestone":
            kwargs = {
                "project_id": project_id,
                "milestone_id": milestone_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.retrieve_milestone(**kwargs)
        if action == "update_milestone":
            kwargs = {
                "project_id": project_id,
                "milestone_id": milestone_id,
                "data": data,  # type: ignore
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_milestone(**kwargs)
        if action == "delete_milestone":
            kwargs = {
                "project_id": project_id,
                "milestone_id": milestone_id,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_milestone(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_milestones', 'create_milestone', 'retrieve_milestone', 'update_milestone', 'delete_milestone"
        )


def register_modules_tools(mcp: FastMCP):
    @mcp.tool(tags={"modules"})
    async def plane_modules(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_modules', 'create_module', 'retrieve_module', 'update_module', 'delete_module'"
        ),
        project_id: str | None = Field(default=None, description="project id"),
        data: dict[str, Any] | None = Field(default=None, description="data"),
        module_id: str | None = Field(default=None, description="module id"),
        client=Depends(get_client),
    ) -> dict:
        """Manage modules operations.

        Actions:
          - 'list_modules': List all modules in a project.
          - 'create_module': Create a new module.
          - 'retrieve_module': Retrieve a module by ID.
          - 'update_module': Update a module by ID.
          - 'delete_module': Delete a module by ID.
        """
        kwargs: dict[str, Any]
        if action == "list_modules":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_modules(**kwargs)
        if action == "create_module":
            kwargs = {"project_id": project_id, "data": data}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_module(**kwargs)
        if action == "retrieve_module":
            kwargs = {"project_id": project_id, "module_id": module_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.retrieve_module(**kwargs)
        if action == "update_module":
            kwargs = {
                "project_id": project_id,
                "module_id": module_id,
                "data": data,
            }  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_module(**kwargs)
        if action == "delete_module":
            kwargs = {"project_id": project_id, "module_id": module_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.delete_module(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_modules', 'create_module', 'retrieve_module', 'update_module', 'delete_module"
        )


def register_states_tools(mcp: FastMCP):
    @mcp.tool(tags={"states"})
    async def plane_states(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_states', 'create_state'"
        ),
        project_id: str | None = Field(default=None, description="project id"),
        data: dict[str, Any] | None = Field(default=None, description="data"),
        client=Depends(get_client),
    ) -> dict:
        """Manage states operations.

        Actions:
          - 'list_states': List all states in a project.
          - 'create_state': Create a new state.
        """
        kwargs: dict[str, Any]
        if action == "list_states":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_states(**kwargs)
        if action == "create_state":
            kwargs = {"project_id": project_id, "data": data}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_state(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_states', 'create_state"
        )


def register_users_tools(mcp: FastMCP):
    @mcp.tool(tags={"users"})
    async def plane_users(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_users', 'get_me'"
        ),
        client=Depends(get_client),
    ) -> dict:
        """Manage users operations.

        Actions:
          - 'list_users': List all users in the workspace.
          - 'get_me': Get current user information.
        """
        kwargs: dict[str, Any]
        if action == "list_users":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_users(**kwargs)
        if action == "get_me":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_me(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_users', 'get_me"
        )


def register_workspaces_tools(mcp: FastMCP):
    @mcp.tool(tags={"workspaces"})
    async def plane_workspaces(
        action: str = Field(
            description="Action to perform. Must be one of: 'get_workspace', 'get_workspace_members', 'get_workspace_features', 'update_workspace_features'"
        ),
        data: dict[str, Any] | None = Field(default=None, description="data"),
        client=Depends(get_client),
    ) -> dict:
        """Manage workspaces operations.

        Actions:
          - 'get_workspace': Get current workspace details.
          - 'get_workspace_members': Get all members of the current workspace.
          - 'get_workspace_features': Get features of the current workspace.
          - 'update_workspace_features': Update features of the current workspace.
        """
        kwargs: dict[str, Any]
        if action == "get_workspace":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_workspace(**kwargs)
        if action == "get_workspace_members":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_workspace_members(**kwargs)
        if action == "get_workspace_features":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.get_workspace_features(**kwargs)
        if action == "update_workspace_features":
            kwargs = {"data": data}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.update_workspace_features(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: get_workspace', 'get_workspace_members', 'get_workspace_features', 'update_workspace_features"
        )


def register_initiatives_tools(mcp: FastMCP):
    @mcp.tool(tags={"initiatives"})
    async def plane_initiatives(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_initiatives', 'create_initiative'"
        ),
        data: dict[str, Any] | None = Field(default=None, description="data"),
        client=Depends(get_client),
    ) -> dict:
        """Manage initiatives operations.

        Actions:
          - 'list_initiatives': List all initiatives in the workspace.
          - 'create_initiative': Create a new initiative in the workspace.
        """
        kwargs: dict[str, Any]
        if action == "list_initiatives":
            kwargs = {}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_initiatives(**kwargs)
        if action == "create_initiative":
            kwargs = {"data": data}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_initiative(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_initiatives', 'create_initiative"
        )


def register_intake_tools(mcp: FastMCP):
    @mcp.tool(tags={"intake"})
    async def plane_intake(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_intake_work_items', 'create_intake_work_item'"
        ),
        project_id: str | None = Field(default=None, description="project id"),
        data: dict[str, Any] | None = Field(default=None, description="data"),
        client=Depends(get_client),
    ) -> dict:
        """Manage intake operations.

        Actions:
          - 'list_intake_work_items': List all intake work items in a project.
          - 'create_intake_work_item': Create a new intake work item in a project.
        """
        kwargs: dict[str, Any]
        if action == "list_intake_work_items":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_intake_work_items(**kwargs)
        if action == "create_intake_work_item":
            kwargs = {"project_id": project_id, "data": data}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_intake_work_item(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_intake_work_items', 'create_intake_work_item"
        )


def register_labels_tools(mcp: FastMCP):
    @mcp.tool(tags={"labels"})
    async def plane_labels(
        action: str = Field(
            description="Action to perform. Must be one of: 'list_labels', 'create_label'"
        ),
        project_id: str | None = Field(default=None, description="project id"),
        data: dict[str, Any] | None = Field(default=None, description="data"),
        client=Depends(get_client),
    ) -> dict:
        """Manage labels operations.

        Actions:
          - 'list_labels': List all labels in a project.
          - 'create_label': Create a new label.
        """
        kwargs: dict[str, Any]
        if action == "list_labels":
            kwargs = {"project_id": project_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.list_labels(**kwargs)
        if action == "create_label":
            kwargs = {"project_id": project_id, "data": data}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_label(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: list_labels', 'create_label"
        )


def register_pages_tools(mcp: FastMCP):
    @mcp.tool(tags={"pages"})
    async def plane_pages(
        action: str = Field(
            description="Action to perform. Must be one of: 'retrieve_project_page', 'create_project_page'"
        ),
        project_id: str | None = Field(default=None, description="project id"),
        page_id: str | None = Field(default=None, description="page id"),
        data: dict[str, Any] | None = Field(default=None, description="data"),
        client=Depends(get_client),
    ) -> dict:
        """Manage pages operations.

        Actions:
          - 'retrieve_project_page': Retrieve a project page by ID.
          - 'create_project_page': Create a new project page.
        """
        kwargs: dict[str, Any]
        if action == "retrieve_project_page":
            kwargs = {"project_id": project_id, "page_id": page_id}
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.retrieve_project_page(**kwargs)
        if action == "create_project_page":
            kwargs = {"project_id": project_id, "data": data}  # type: ignore
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            return client.create_project_page(**kwargs)
        raise ValueError(
            f"Unknown action: {action}. Must be one of: retrieve_project_page', 'create_project_page"
        )


def get_mcp_instance() -> tuple[Any, ...]:
    """Initialize and return the MCP instance."""
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
