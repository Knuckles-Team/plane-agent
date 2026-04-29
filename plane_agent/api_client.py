"""Plane API wrapper implementation."""

import logging
from typing import Any, TypeVar

import requests
import urllib3
from agent_utilities.decorators import require_auth
from agent_utilities.exceptions import (
    AuthError,
    ParameterError,
    UnauthorizedError,
)

from plane_agent.plane_models import Project, Response, WorkItem

logger = logging.getLogger(__name__)

T = TypeVar("T")


class Api:
    """Plane API client wrapper."""

    def __init__(
        self,
        url: str,
        api_key: str,
        workspace_slug: str,
        verify: bool = True,
        proxies: dict | None = None,
        debug: bool = False,
    ):
        self.url = url.rstrip("/")
        if "/api/v1" not in self.url:
            self.url = f"{self.url}/api/v1"

        self.api_key = api_key
        self.workspace_slug = workspace_slug
        self.verify = verify
        self.proxies = proxies
        self.debug = debug

        self._session = requests.Session()
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }

        if not self.verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self._validate_auth()

    def _validate_auth(self):
        """Verify the API key and workspace slug are valid."""
        response = self._session.get(
            url=f"{self.url}/workspaces/{self.workspace_slug}/",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        if response.status_code in (401, 403):
            raise AuthError if response.status_code == 401 else UnauthorizedError
        elif response.status_code == 404:
            raise ParameterError(f"Workspace slug '{self.workspace_slug}' not found.")
        response.raise_for_status()

    def _get(self, endpoint: str, params: dict | None = None) -> requests.Response:
        url = f"{self.url}/workspaces/{self.workspace_slug}{endpoint}"
        return self._session.get(
            url,
            headers=self.headers,
            params=params,
            verify=self.verify,
            proxies=self.proxies,
        )

    def _post(self, endpoint: str, data: dict | None = None) -> requests.Response:
        url = f"{self.url}/workspaces/{self.workspace_slug}{endpoint}"
        return self._session.post(
            url,
            headers=self.headers,
            json=data,
            verify=self.verify,
            proxies=self.proxies,
        )

    def _patch(self, endpoint: str, data: dict | None = None) -> requests.Response:
        url = f"{self.url}/workspaces/{self.workspace_slug}{endpoint}"
        return self._session.patch(
            url,
            headers=self.headers,
            json=data,
            verify=self.verify,
            proxies=self.proxies,
        )

    def _delete(self, endpoint: str) -> requests.Response:
        url = f"{self.url}/workspaces/{self.workspace_slug}{endpoint}"
        return self._session.delete(
            url, headers=self.headers, verify=self.verify, proxies=self.proxies
        )

    @require_auth
    def list_projects(self, **kwargs) -> Response:
        """List all projects in the workspace."""
        response = self._get("/projects/", params=kwargs)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", data) if isinstance(data, dict) else data
        parsed_data = [Project(**item) for item in results]
        return Response(response=response, data=parsed_data)

    @require_auth
    def retrieve_project(self, project_id: str) -> Response:
        """Retrieve a project by ID."""
        response = self._get(f"/projects/{project_id}/")
        response.raise_for_status()
        parsed_data = Project(**response.json())
        return Response(response=response, data=parsed_data)

    @require_auth
    def list_work_items(self, project_id: str, **kwargs) -> Response:
        """List work items in a project."""
        response = self._get(f"/projects/{project_id}/work-items/", params=kwargs)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        parsed_data = [WorkItem(**item) for item in results]
        return Response(response=response, data=parsed_data)

    @require_auth
    def retrieve_work_item(self, project_id: str, work_item_id: str) -> Response:
        """Retrieve a work item by ID."""
        response = self._get(f"/projects/{project_id}/work-items/{work_item_id}/")
        response.raise_for_status()
        parsed_data = WorkItem(**response.json())
        return Response(response=response, data=parsed_data)

    @require_auth
    def list_cycles(self, project_id: str, **kwargs) -> Response:
        """List all cycles in a project."""
        response = self._get(f"/projects/{project_id}/cycles/", params=kwargs)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def create_cycle(self, project_id: str, data: dict[str, Any]) -> Response:
        """Create a new cycle."""
        response = self._post(f"/projects/{project_id}/cycles/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def retrieve_cycle(self, project_id: str, cycle_id: str) -> Response:
        """Retrieve a cycle by ID."""
        response = self._get(f"/projects/{project_id}/cycles/{cycle_id}/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def update_cycle(
        self, project_id: str, cycle_id: str, data: dict[str, Any]
    ) -> Response:
        """Update a cycle by ID."""
        response = self._patch(f"/projects/{project_id}/cycles/{cycle_id}/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def delete_project(self, project_id: str) -> Response:
        """Delete a project by ID."""
        response = self._delete(f"/projects/{project_id}/")
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

    @require_auth
    def get_project_worklog_summary(self, project_id: str) -> Response:
        """Get work log summary for a project."""
        response = self._get(f"/projects/{project_id}/worklog-summary/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def get_project_members(self, project_id: str, **kwargs) -> Response:
        """Get all members of a project."""
        response = self._get(f"/projects/{project_id}/members/", params=kwargs)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def get_project_features(self, project_id: str) -> Response:
        """Get features of a project."""
        response = self._get(f"/projects/{project_id}/")
        response.raise_for_status()
        data = response.json()
        return Response(response=response, data=data.get("features", {}))

    @require_auth
    def update_project_features(
        self, project_id: str, data: dict[str, Any]
    ) -> Response:
        """Update features of a project."""
        response = self._patch(f"/projects/{project_id}/", data={"features": data})
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def list_archived_cycles(self, project_id: str, **kwargs) -> Response:
        """List archived cycles in a project."""
        response = self._get(f"/projects/{project_id}/archived-cycles/", params=kwargs)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def add_work_items_to_cycle(
        self, project_id: str, cycle_id: str, issue_ids: list[str]
    ) -> Response:
        """Add work items to a cycle."""
        response = self._post(
            f"/projects/{project_id}/cycles/{cycle_id}/cycle-issues/",
            data={"issues": issue_ids},
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def remove_work_item_from_cycle(
        self, project_id: str, cycle_id: str, work_item_id: str
    ) -> Response:
        """Remove a work item from a cycle."""
        response = self._delete(
            f"/projects/{project_id}/cycles/{cycle_id}/cycle-issues/{work_item_id}/"
        )
        response.raise_for_status()
        return Response(response=response, data={"status": "removed"})

    @require_auth
    def list_cycle_work_items(
        self, project_id: str, cycle_id: str, **kwargs
    ) -> Response:
        """List work items in a cycle."""
        response = self._get(
            f"/projects/{project_id}/cycles/{cycle_id}/cycle-issues/", params=kwargs
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def transfer_cycle_work_items(
        self, project_id: str, cycle_id: str, new_cycle_id: str
    ) -> Response:
        """Transfer work items from one cycle to another."""
        response = self._post(
            f"/projects/{project_id}/cycles/{cycle_id}/transfer-issues/",
            data={"new_cycle_id": new_cycle_id},
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def list_epics(self, project_id: str, **kwargs) -> Response:
        """List all epics in a project."""
        response = self._get(f"/projects/{project_id}/epics/", params=kwargs)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def create_epic(self, project_id: str, data: dict[str, Any]) -> Response:
        """Create a new epic (technically a work item with epic type)."""

        if "type_id" not in data:
            types_res = self.list_work_item_types(project_id)
            epic_type = next((t for t in types_res.data if t.get("is_epic")), None)
            if not epic_type:
                raise ParameterError(
                    "No work item type with is_epic=True found in the project"
                )
            data["type_id"] = epic_type["id"]

        response = self._post(f"/projects/{project_id}/work-items/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def retrieve_epic(self, project_id: str, epic_id: str) -> Response:
        """Retrieve an epic by ID."""
        response = self._get(f"/projects/{project_id}/epics/{epic_id}/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def update_epic(
        self, project_id: str, epic_id: str, data: dict[str, Any]
    ) -> Response:
        """Update an epic by ID."""
        response = self._patch(
            f"/projects/{project_id}/work-items/{epic_id}/", data=data
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def delete_epic(self, project_id: str, epic_id: str) -> Response:
        """Delete an epic by ID."""
        response = self._delete(f"/projects/{project_id}/work-items/{epic_id}/")
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

    @require_auth
    def list_work_item_types(self, project_id: str) -> Response:
        """List work item types in a project."""
        response = self._get(f"/projects/{project_id}/work-item-types/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def list_initiatives(self, **kwargs) -> Response:
        """List all initiatives in the workspace."""
        response = self._get("/initiatives/", params=kwargs)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def create_initiative(self, data: dict[str, Any]) -> Response:
        """Create a new initiative in the workspace."""
        response = self._post("/initiatives/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def retrieve_initiative(self, initiative_id: str) -> Response:
        """Retrieve an initiative by ID."""
        response = self._get(f"/initiatives/{initiative_id}/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def update_initiative(self, initiative_id: str, data: dict[str, Any]) -> Response:
        """Update an initiative by ID."""
        response = self._patch(f"/initiatives/{initiative_id}/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def delete_initiative(self, initiative_id: str) -> Response:
        """Delete an initiative by ID."""
        response = self._delete(f"/initiatives/{initiative_id}/")
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

    @require_auth
    def list_intake_work_items(self, project_id: str, **kwargs) -> Response:
        """List all intake work items in a project."""
        response = self._get(f"/projects/{project_id}/intake/", params=kwargs)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def create_intake_work_item(
        self, project_id: str, data: dict[str, Any]
    ) -> Response:
        """Create a new intake work item in a project."""
        response = self._post(f"/projects/{project_id}/intake/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def list_work_item_activities(
        self, project_id: str, work_item_id: str, **kwargs
    ) -> Response:
        """List activities for a work item."""
        response = self._get(
            f"/projects/{project_id}/issues/{work_item_id}/history/", params=kwargs
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def retrieve_work_item_activity(
        self, project_id: str, work_item_id: str, activity_id: str
    ) -> Response:
        """Retrieve a specific activity for a work item."""
        response = self._get(
            f"/projects/{project_id}/issues/{work_item_id}/history/{activity_id}/"
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def list_work_item_comments(
        self, project_id: str, work_item_id: str, **kwargs
    ) -> Response:
        """List comments for a work item."""
        response = self._get(
            f"/projects/{project_id}/issues/{work_item_id}/comments/", params=kwargs
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def create_work_item_comment(
        self, project_id: str, work_item_id: str, data: dict[str, Any]
    ) -> Response:
        """Create a comment for a work item."""
        response = self._post(
            f"/projects/{project_id}/issues/{work_item_id}/comments/", data=data
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def retrieve_work_item_comment(
        self, project_id: str, work_item_id: str, comment_id: str
    ) -> Response:
        """Retrieve a specific comment for a work item."""
        response = self._get(
            f"/projects/{project_id}/issues/{work_item_id}/comments/{comment_id}/"
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def update_work_item_comment(
        self, project_id: str, work_item_id: str, comment_id: str, data: dict[str, Any]
    ) -> Response:
        """Update a comment for a work item."""
        response = self._patch(
            f"/projects/{project_id}/issues/{work_item_id}/comments/{comment_id}/",
            data=data,
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def delete_work_item_comment(
        self, project_id: str, work_item_id: str, comment_id: str
    ) -> Response:
        """Delete a comment for a work item."""
        response = self._delete(
            f"/projects/{project_id}/issues/{work_item_id}/comments/{comment_id}/"
        )
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

    @require_auth
    def list_work_item_links(
        self, project_id: str, work_item_id: str, **kwargs
    ) -> Response:
        """List links for a work item."""
        response = self._get(
            f"/projects/{project_id}/issues/{work_item_id}/links/", params=kwargs
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def create_work_item_link(
        self, project_id: str, work_item_id: str, data: dict[str, Any]
    ) -> Response:
        """Create a link for a work item."""
        response = self._post(
            f"/projects/{project_id}/issues/{work_item_id}/links/", data=data
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def retrieve_work_item_link(
        self, project_id: str, work_item_id: str, link_id: str
    ) -> Response:
        """Retrieve a specific link for a work item."""

        response = self._get(
            f"/projects/{project_id}/issues/{work_item_id}/links/{link_id}/"
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def update_work_item_link(
        self, project_id: str, work_item_id: str, link_id: str, data: dict[str, Any]
    ) -> Response:
        """Update a link for a work item."""
        response = self._patch(
            f"/projects/{project_id}/issues/{work_item_id}/links/{link_id}/", data=data
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def delete_work_item_link(
        self, project_id: str, work_item_id: str, link_id: str
    ) -> Response:
        """Delete a link for a work item."""
        response = self._delete(
            f"/projects/{project_id}/issues/{work_item_id}/links/{link_id}/"
        )
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

    @require_auth
    def list_work_item_properties(
        self, project_id: str, type_id: str, **kwargs
    ) -> Response:
        """List work item properties for a work item type."""
        response = self._get(
            f"/projects/{project_id}/types/{type_id}/attributes/", params=kwargs
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def create_work_item_property(
        self, project_id: str, type_id: str, data: dict[str, Any]
    ) -> Response:
        """Create a new work item property."""
        response = self._post(
            f"/projects/{project_id}/types/{type_id}/attributes/", data=data
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def retrieve_work_item_property(
        self, project_id: str, type_id: str, work_item_property_id: str
    ) -> Response:
        """Retrieve a work item property by ID."""
        response = self._get(
            f"/projects/{project_id}/types/{type_id}/attributes/{work_item_property_id}/"
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def update_work_item_property(
        self,
        project_id: str,
        type_id: str,
        work_item_property_id: str,
        data: dict[str, Any],
    ) -> Response:
        """Update a work item property by ID."""
        response = self._patch(
            f"/projects/{project_id}/types/{type_id}/attributes/{work_item_property_id}/",
            data=data,
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def delete_work_item_property(
        self, project_id: str, type_id: str, work_item_property_id: str
    ) -> Response:
        """Delete a work item property by ID."""
        response = self._delete(
            f"/projects/{project_id}/types/{type_id}/attributes/{work_item_property_id}/"
        )
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

    @require_auth
    def list_work_item_relations(self, project_id: str, work_item_id: str) -> Response:
        """List relations for a work item."""
        response = self._get(f"/projects/{project_id}/issues/{work_item_id}/relations/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def create_work_item_relation(
        self, project_id: str, work_item_id: str, data: dict[str, Any]
    ) -> Response:
        """Create relations for a work item."""
        response = self._post(
            f"/projects/{project_id}/issues/{work_item_id}/relations/", data=data
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def remove_work_item_relation(
        self, project_id: str, work_item_id: str, related_issue: str
    ) -> Response:
        """Remove a relation from a work item."""

        response = self._delete(
            f"/projects/{project_id}/issues/{work_item_id}/relations/",
            json={"related_issue": related_issue},
        )
        response.raise_for_status()
        return Response(response=response, data={"status": "removed"})

    @require_auth
    def create_work_item_type(self, project_id: str, data: dict[str, Any]) -> Response:
        """Create a new work item type."""
        response = self._post(f"/projects/{project_id}/types/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def create_work_item(self, project_id: str, data: dict[str, Any]) -> Response:
        """Create a new work item."""
        response = self._post(f"/projects/{project_id}/issues/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def retrieve_work_item_by_identifier(
        self, project_identifier: str, issue_identifier: int
    ) -> Response:
        """Retrieve a work item by project identifier and issue sequence number."""
        response = self._get(
            f"/projects/{project_identifier}/issues/{issue_identifier}/"
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def update_work_item(
        self, project_id: str, work_item_id: str, data: dict[str, Any]
    ) -> Response:
        """Update a work item by ID."""
        response = self._patch(
            f"/projects/{project_id}/issues/{work_item_id}/", data=data
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def delete_work_item(self, project_id: str, work_item_id: str) -> Response:
        """Delete a work item by ID."""
        response = self._delete(f"/projects/{project_id}/issues/{work_item_id}/")
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

    @require_auth
    def search_work_items(self, query: str, **kwargs) -> Response:
        """Search work items across a workspace."""
        response = self._get("/search-issues/", params={"query": query, **kwargs})
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def advanced_search_work_items(self, data: dict[str, Any]) -> Response:
        """Advanced search for work items."""
        response = self._post("/advanced-search/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def update_work_item_type(
        self, project_id: str, work_item_type_id: str, data: dict[str, Any]
    ) -> Response:
        """Update a work item type by ID."""
        response = self._patch(
            f"/projects/{project_id}/types/{work_item_type_id}/", data=data
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def delete_work_item_type(
        self, project_id: str, work_item_type_id: str
    ) -> Response:
        """Delete a work item type by ID."""
        response = self._delete(f"/projects/{project_id}/types/{work_item_type_id}/")
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

    @require_auth
    def list_work_logs(self, project_id: str, work_item_id: str, **kwargs) -> Response:
        """List work logs for a work item."""
        response = self._get(
            f"/projects/{project_id}/issues/{work_item_id}/worklogs/", params=kwargs
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def create_work_log(
        self, project_id: str, work_item_id: str, data: dict[str, Any]
    ) -> Response:
        """Create a work log for a work item."""
        response = self._post(
            f"/projects/{project_id}/issues/{work_item_id}/worklogs/", data=data
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def update_work_log(
        self, project_id: str, work_item_id: str, work_log_id: str, data: dict[str, Any]
    ) -> Response:
        """Update a work log for a work item."""
        response = self._patch(
            f"/projects/{project_id}/issues/{work_item_id}/worklogs/{work_log_id}/",
            data=data,
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def delete_work_log(
        self, project_id: str, work_item_id: str, work_log_id: str
    ) -> Response:
        """Delete a work log for a work item."""
        response = self._delete(
            f"/projects/{project_id}/issues/{work_item_id}/worklogs/{work_log_id}/"
        )
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

    @require_auth
    def get_workspace_members(self) -> Response:
        """Get all members of the current workspace."""
        response = self._get("/members/")
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def get_workspace_features(self) -> Response:
        """Get features of the current workspace."""
        response = self._get("/")
        response.raise_for_status()
        data = response.json()
        return Response(response=response, data=data.get("features", {}))

    @require_auth
    def update_workspace_features(self, data: dict[str, Any]) -> Response:
        """Update features of the current workspace."""
        response = self._patch("/", data={"features": data})
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def retrieve_intake_work_item(self, project_id: str, work_item_id: str) -> Response:
        """Retrieve an intake work item by work item ID."""
        response = self._get(f"/projects/{project_id}/intake/{work_item_id}/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def update_intake_work_item(
        self, project_id: str, work_item_id: str, data: dict[str, Any]
    ) -> Response:
        """Update an intake work item by work item ID."""
        response = self._patch(
            f"/projects/{project_id}/intake/{work_item_id}/", data=data
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    def delete_intake_work_item(self, project_id: str, work_item_id: str) -> Response:
        """Delete an intake work item by work item ID."""
        response = self._delete(f"/projects/{project_id}/intake/{work_item_id}/")
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

    @require_auth
    def list_milestones(self, project_id: str, **kwargs) -> Response:
        """List all milestones in a project."""
        response = self._get(f"/projects/{project_id}/milestones/", params=kwargs)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def create_milestone(self, project_id: str, data: dict[str, Any]) -> Response:
        """Create a new milestone."""
        response = self._post(f"/projects/{project_id}/milestones/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def retrieve_milestone(self, project_id: str, milestone_id: str) -> Response:
        """Retrieve a milestone by ID."""
        response = self._get(f"/projects/{project_id}/milestones/{milestone_id}/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def update_milestone(
        self, project_id: str, milestone_id: str, data: dict[str, Any]
    ) -> Response:
        """Update a milestone by ID."""
        response = self._patch(
            f"/projects/{project_id}/milestones/{milestone_id}/", data=data
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def delete_milestone(self, project_id: str, milestone_id: str) -> Response:
        """Delete a milestone by ID."""
        response = self._delete(f"/projects/{project_id}/milestones/{milestone_id}/")
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

    @require_auth
    def add_work_items_to_milestone(
        self, project_id: str, milestone_id: str, issue_ids: list[str]
    ) -> Response:
        """Add work items to a milestone."""
        response = self._post(
            f"/projects/{project_id}/milestones/{milestone_id}/milestone-issues/",
            data={"issues": issue_ids},
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def remove_work_items_from_milestone(
        self, project_id: str, milestone_id: str, issue_ids: list[str]
    ) -> Response:
        """Remove work items from a milestone."""

        response = self._post(
            f"/projects/{project_id}/milestones/{milestone_id}/milestone-issues/remove/",
            data={"issues": issue_ids},
        )
        response.raise_for_status()
        return Response(response=response, data={"status": "removed"})

    @require_auth
    def list_milestone_work_items(
        self, project_id: str, milestone_id: str, **kwargs
    ) -> Response:
        """List work items in a milestone."""
        response = self._get(
            f"/projects/{project_id}/milestones/{milestone_id}/milestone-issues/",
            params=kwargs,
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def list_modules(self, project_id: str, **kwargs) -> Response:
        """List all modules in a project."""
        response = self._get(f"/projects/{project_id}/modules/", params=kwargs)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def create_module(self, project_id: str, data: dict[str, Any]) -> Response:
        """Create a new module."""
        response = self._post(f"/projects/{project_id}/modules/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def retrieve_module(self, project_id: str, module_id: str) -> Response:
        """Retrieve a module by ID."""
        response = self._get(f"/projects/{project_id}/modules/{module_id}/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def update_module(
        self, project_id: str, module_id: str, data: dict[str, Any]
    ) -> Response:
        """Update a module by ID."""
        response = self._patch(
            f"/projects/{project_id}/modules/{module_id}/", data=data
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def delete_module(self, project_id: str, module_id: str) -> Response:
        """Delete a module by ID."""
        response = self._delete(f"/projects/{project_id}/modules/{module_id}/")
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

    @require_auth
    def list_archived_modules(self, project_id: str, **kwargs) -> Response:
        """List archived modules in a project."""
        response = self._get(f"/projects/{project_id}/archived-modules/", params=kwargs)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def add_work_items_to_module(
        self, project_id: str, module_id: str, issue_ids: list[str]
    ) -> Response:
        """Add work items to a module."""
        response = self._post(
            f"/projects/{project_id}/modules/{module_id}/module-issues/",
            data={"issues": issue_ids},
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def remove_work_item_from_module(
        self, project_id: str, module_id: str, work_item_id: str
    ) -> Response:
        """Remove a work item from a module."""
        response = self._delete(
            f"/projects/{project_id}/modules/{module_id}/module-issues/{work_item_id}/"
        )
        response.raise_for_status()
        return Response(response=response, data={"status": "removed"})

    @require_auth
    def list_module_work_items(
        self, project_id: str, module_id: str, **kwargs
    ) -> Response:
        """List work items in a module."""
        response = self._get(
            f"/projects/{project_id}/modules/{module_id}/module-issues/", params=kwargs
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def archive_module(self, project_id: str, module_id: str) -> Response:
        """Archive a module."""
        response = self._post(f"/projects/{project_id}/modules/{module_id}/archive/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def unarchive_module(self, project_id: str, module_id: str) -> Response:
        """Unarchive a module."""
        response = self._post(f"/projects/{project_id}/modules/{module_id}/unarchive/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def list_states(self, project_id: str, **kwargs) -> Response:
        """List all states in a project."""
        response = self._get(f"/projects/{project_id}/states/", params=kwargs)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def create_state(self, project_id: str, data: dict[str, Any]) -> Response:
        """Create a new state."""
        response = self._post(f"/projects/{project_id}/states/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def retrieve_state(self, project_id: str, state_id: str) -> Response:
        """Retrieve a state by ID."""
        response = self._get(f"/projects/{project_id}/states/{state_id}/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def update_state(
        self, project_id: str, state_id: str, data: dict[str, Any]
    ) -> Response:
        """Update a state by ID."""
        response = self._patch(f"/projects/{project_id}/states/{state_id}/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def delete_state(self, project_id: str, state_id: str) -> Response:
        """Delete a state by ID."""
        response = self._delete(f"/projects/{project_id}/states/{state_id}/")
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

    @require_auth
    def list_users(self, **kwargs) -> Response:
        """List all users in the workspace."""
        response = self._get("/users/", params=kwargs)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", data) if isinstance(data, dict) else data
        return Response(response=response, data=results)

    @require_auth
    def get_me(self) -> Response:
        """Get current user information."""
        response = self._get("/users/me/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def get_workspace(self) -> Response:
        """Get current workspace details."""
        response = self._session.get(
            url=f"{self.url}/workspaces/{self.workspace_slug}/",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())
