#!/usr/bin/env python
from typing import Any

from agent_utilities.core.decorators import require_auth

from plane_agent.api.api_client_base import BaseApiClient
from plane_agent.plane_models import Response


class Api(BaseApiClient):
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
    def delete_cycle(self, project_id: str, cycle_id: str) -> Response:
        """Delete a cycle by ID."""
        response = self._delete(f"/projects/{project_id}/cycles/{cycle_id}/")
        response.raise_for_status()
        return Response(response=response, data={"status": "deleted"})

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
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        cycle_id: str,
        issue_ids: list[str],
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
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        cycle_id: str,
        **kwargs,
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
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        cycle_id: str,
        new_cycle_id: str,
    ) -> Response:
        """Transfer work items from one cycle to another."""
        response = self._post(
            f"/projects/{project_id}/cycles/{cycle_id}/transfer-issues/",
            data={"new_cycle_id": new_cycle_id},
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())
