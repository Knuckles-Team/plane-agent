"""Authentication utility for Plane API."""

import logging

from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)

from plane_agent.api_client import Api

logger = logging.getLogger(__name__)


def get_client(
    url: str | None = None,
    api_key: str | None = None,
    workspace_slug: str | None = None,
    tls_profile: ResolvedTLSProfile | None = None,
) -> Api:
    """
    Initialize and return a Plane API client.

    CONCEPT:AU-ECO.mcp.fastmcp-middleware

    Args:
        url: Plane API base URL.
        api_key: Plane API key.
        workspace_slug: Plane workspace slug.
        tls_profile: Resolved mandatory-verification transport policy.

    Returns:
        An instance of the Plane Api wrapper.
    """
    url = url or setting("PLANE_BASE_URL", "https://api.plane.so")
    api_key = api_key or setting("PLANE_API_KEY", None)
    workspace_slug = workspace_slug or setting("PLANE_WORKSPACE_SLUG", None)
    profile = tls_profile or resolve_configured_tls_profile(
        "plane",
        profile_name=setting("PLANE_TLS_PROFILE", "") or None,
        profile_ref=setting("PLANE_TLS_PROFILE_REF", "") or None,
    )

    if not api_key:
        raise AuthError("PLANE_API_KEY is required")

    if not workspace_slug:
        raise AuthError("PLANE_WORKSPACE_SLUG is required")

    try:
        client = Api(
            url=url,
            api_key=api_key,
            workspace_slug=workspace_slug,
            tls_profile=profile,
        )
        return client
    except (AuthError, UnauthorizedError) as e:
        logger.error("Operation failed: error_type=%s", type(e).__name__)
        raise RuntimeError(
            "AUTHENTICATION ERROR: The configured credentials were rejected. "
            f"Please check your PLANE_API_KEY and PLANE_WORKSPACE_SLUG environment variables. "
            f"Error details: {type(e).__name__}"
        ) from e
