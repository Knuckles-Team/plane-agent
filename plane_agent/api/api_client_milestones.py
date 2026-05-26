#!/usr/bin/env python
from typing import Any

from agent_utilities.core.decorators import require_auth

from plane_agent.api.api_client_base import BaseApiClient
from plane_agent.plane_models import Response


class Api(BaseApiClient):
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
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        milestone_id: str,
        issue_ids: list[str],
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
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        milestone_id: str,
        issue_ids: list[str],
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
        # CONCEPT:ECO-4.1
        self,
        project_id: str,
        milestone_id: str,
        **kwargs,
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
