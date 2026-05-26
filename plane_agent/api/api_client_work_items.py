#!/usr/bin/env python
from typing import Any

from agent_utilities.core.decorators import require_auth

from plane_agent.api.api_client_base import BaseApiClient
from plane_agent.plane_models import Response, WorkItem


class Api(BaseApiClient):
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
    def list_work_item_activities(
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        work_item_id: str,
        **kwargs,
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
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        work_item_id: str,
        **kwargs,
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
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        work_item_id: str,
        comment_id: str,
        data: dict[str, Any],
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
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        work_item_id: str,
        **kwargs,
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
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        work_item_id: str,
        link_id: str,
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
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        type_id: str,
        **kwargs,
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
        # CONCEPT:ECO-4.1
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
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        work_item_id: str,
        related_issue: str,
    ) -> Response:
        """Remove a relation from a work item."""

        response = self._delete(
            f"/projects/{project_id}/issues/{work_item_id}/relations/",
            json={"related_issue": related_issue},
        )
        response.raise_for_status()
        return Response(response=response, data={"status": "removed"})

    @require_auth
    def list_work_item_types(self, project_id: str) -> Response:
        """List work item types in a project."""
        response = self._get(f"/projects/{project_id}/work-item-types/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def create_work_item_type(self, project_id: str, data: dict[str, Any]) -> Response:
        """Create a new work item type."""
        response = self._post(f"/projects/{project_id}/types/", data=data)
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
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        work_item_id: str,
        work_log_id: str,
        data: dict[str, Any],
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
    def get_project_worklog_summary(self, project_id: str) -> Response:
        """Get work log summary for a project."""
        response = self._get(f"/projects/{project_id}/worklog-summary/")
        response.raise_for_status()
        return Response(response=response, data=response.json())
