#!/usr/bin/env python
from typing import Any

from agent_utilities.core.decorators import require_auth

from plane_agent.api.api_client_base import BaseApiClient
from plane_agent.plane_models import Response


class Api(BaseApiClient):
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
        # CONCEPT:ECO-4.1
        """Get current workspace details."""
        response = self._session.get(
            url=f"{self.url}/workspaces/{self.workspace_slug}/",
            headers=self.headers,
            verify=self.verify,
            proxies=self.proxies,
        )
        response.raise_for_status()
        return Response(response=response, data=response.json())
