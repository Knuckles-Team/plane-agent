#!/usr/bin/env python
from typing import Any

from agent_utilities.core.decorators import require_auth

from plane_agent.api.api_client_base import BaseApiClient
from plane_agent.plane_models import Project, Response


class Api(BaseApiClient):
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
    def delete_project(self, project_id: str) -> Response:
        """Delete a project by ID."""
        response = self._delete(f"/projects/{project_id}/")
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

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
    def list_labels(self, project_id: str, **kwargs) -> Response:
        """List all labels in a project."""
        response = self._get(f"/projects/{project_id}/labels/", params=kwargs)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def create_label(self, project_id: str, data: dict[str, Any]) -> Response:
        """Create a new label."""
        response = self._post(f"/projects/{project_id}/labels/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def retrieve_project_page(self, project_id: str, page_id: str) -> Response:
        """Retrieve a project page by ID."""
        response = self._get(f"/projects/{project_id}/pages/{page_id}/")
        response.raise_for_status()
        return Response(response=response, data=response.json())

    @require_auth
    def create_project_page(self, project_id: str, data: dict[str, Any]) -> Response:
        """Create a new project page."""
        response = self._post(f"/projects/{project_id}/pages/", data=data)
        response.raise_for_status()
        return Response(response=response, data=response.json())
