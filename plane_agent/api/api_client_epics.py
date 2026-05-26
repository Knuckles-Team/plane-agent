#!/usr/bin/env python
from typing import Any, cast

from agent_utilities.core.decorators import require_auth
from agent_utilities.core.exceptions import ParameterError

from plane_agent.api.api_client_base import BaseApiClient
from plane_agent.plane_models import Response


class Api(BaseApiClient):
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
        # CONCEPT:ECO-4.1
        """Create a new epic (technically a work item with epic type)."""

        if "type_id" not in data:
            types_res = cast(Any, self).list_work_item_types(project_id)
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
