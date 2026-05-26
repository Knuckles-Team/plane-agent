#!/usr/bin/env python
from typing import Any

from agent_utilities.core.decorators import require_auth

from plane_agent.api.api_client_base import BaseApiClient
from plane_agent.plane_models import Response


class Api(BaseApiClient):
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
