#!/usr/bin/env python
import logging

import requests
import urllib3
from agent_utilities.core.exceptions import (
    AuthError,
    ParameterError,
    UnauthorizedError,
)

logger = logging.getLogger(__name__)


class BaseApiClient:
    def __init__(
        # CONCEPT:AU-ECO.mcp.fastmcp-middleware
        self,
        url: str | None,
        api_key: str,
        workspace_slug: str,
        verify: bool | None = True,
        proxies: dict | None = None,
        debug: bool = False,
    ):
        self.url = (url or "").rstrip("/")
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
            # The bare workspace-detail endpoint 401s even for a valid API key;
            # validate against a key-accessible endpoint that still proves the slug
            # (404 on a bad slug, 401 on a bad key). CONCEPT:AU-ECO.mcp.fastmcp-middleware
            url=f"{self.url}/workspaces/{self.workspace_slug}/projects/",
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

    def _delete(self, endpoint: str, json: dict | None = None) -> requests.Response:
        url = f"{self.url}/workspaces/{self.workspace_slug}{endpoint}"
        return self._session.delete(
            url,
            headers=self.headers,
            json=json,
            verify=self.verify,
            proxies=self.proxies,
        )
