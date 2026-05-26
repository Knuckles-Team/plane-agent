#!/usr/bin/env python
from typing import Any

from agent_utilities.core.decorators import require_auth

from plane_agent.api.api_client_base import BaseApiClient
from plane_agent.plane_models import Response


class Api(BaseApiClient):
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
