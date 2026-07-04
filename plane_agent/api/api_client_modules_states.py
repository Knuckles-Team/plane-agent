#!/usr/bin/env python
from typing import Any

from agent_utilities.core.decorators import require_auth

from plane_agent.api.api_client_base import BaseApiClient
from plane_agent.plane_models import Response


class Api(BaseApiClient):
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
        # CONCEPT:AU-ECO.mcp.fastmcp-middleware
        self,
        project_id: str,
        module_id: str,
        issue_ids: list[str],
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
        # CONCEPT:AU-ECO.mcp.fastmcp-middleware
        self,
        project_id: str,
        module_id: str,
        **kwargs,
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
