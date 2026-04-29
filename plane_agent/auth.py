"""Authentication utility for Plane API."""

import logging
import os
from typing import Any

from agent_utilities.exceptions import AuthError, UnauthorizedError

from plane_agent.api_client import Api

logger = logging.getLogger(__name__)


def get_client(
    url: str | None = os.getenv("PLANE_BASE_URL", "https://api.plane.so"),
    api_key: str | None = os.getenv("PLANE_API_KEY", None),
    workspace_slug: str | None = os.getenv("PLANE_WORKSPACE_SLUG", None),
    verify: bool = True,
    config: Any | None = None,
) -> Api:
    """
    Initialize and return a Plane API client.

    Args:
        url: Plane API base URL.
        api_key: Plane API key.
        workspace_slug: Plane workspace slug.
        verify: Whether to verify SSL certificates.
        config: Optional configuration object.

    Returns:
        An instance of the Plane Api wrapper.
    """
    if not api_key:
        raise AuthError("PLANE_API_KEY is required")

    if not workspace_slug:
        raise AuthError("PLANE_WORKSPACE_SLUG is required")

    try:
        client = Api(
            url=url,
            api_key=api_key,
            workspace_slug=workspace_slug,
            verify=verify,
        )
        return client
    except (AuthError, UnauthorizedError) as e:
        logger.error(f"Failed to authenticate with Plane: {e}")
        raise RuntimeError(
            f"AUTHENTICATION ERROR: The Plane credentials provided are not valid for '{url}'. "
            f"Please check your PLANE_API_KEY and PLANE_WORKSPACE_SLUG environment variables. "
            f"Error details: {str(e)}"
        ) from e
