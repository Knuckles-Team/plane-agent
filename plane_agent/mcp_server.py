#!/usr/bin/python
import warnings

from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from fastmcp.utilities.logging import get_logger
from pydantic import Field

# Filter RequestsDependencyWarning early to prevent log spam
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        from requests.exceptions import RequestsDependencyWarning

        warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    except ImportError:
        pass

warnings.filterwarnings("ignore", message=".*urllib3.*or chardet.*")
warnings.filterwarnings("ignore", message=".*urllib3.*or charset_normalizer.*")

import logging
from typing import Any

from scion_sdk.mcp.concurrency import run_blocking

from plane_agent.auth import get_client

logger = get_logger(name="plane-agent")
logger.setLevel(logging.INFO)


def _kg_records(result: Any, key: str = "results") -> list[dict[str, Any]]:
    """Normalize a client Response/list into a list of plain record dicts."""
    data = getattr(result, "data", result)
    if isinstance(data, dict):
        data = data.get(key, data.get("data", data))
    records = data if isinstance(data, list) else [data]
    out: list[dict[str, Any]] = []
    for r in records:
        if r is None:
            continue
        out.append(r.model_dump() if hasattr(r, "model_dump") else r)
    return [r for r in out if isinstance(r, dict)]


def register_kg_tools(mcp: FastMCP):
    """Register the Plane to epistemic-graph ingest tools (one tool per record kind).

    Each tool lists records via the Plane API, then pushes them as typed nodes + links
    via the fast engine client (best-effort: ``{"ingested": null}`` with no engine).
    CONCEPT:AU-KG.ingest.enterprise-source-extractor.
    """

    @mcp.tool(
        name="plane_ingest_projects",
        tags={"kg"},
        annotations={"readOnlyHint": False, "idempotentHint": True},
    )
    async def plane_ingest_projects(
        per_page: int | None = Field(default=None, description="Page size"),
        cursor: str | None = Field(default=None, description="Pagination cursor"),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Ingest Plane projects as :SoftwareProject nodes (+ :Workspace / :inWorkspace)."""
        from plane_agent import kg_ingest

        if ctx:
            await ctx.info("Executing tool...")
        kwargs = {
            k: v for k, v in {"per_page": per_page, "cursor": cursor}.items() if v
        }
        result = await run_blocking(client.list_projects, **kwargs)
        records = _kg_records(result)
        ingested = await kg_ingest.ingest_projects(
            records, workspace_slug=getattr(client, "workspace_slug", None)
        )
        return {"listed": len(records), "ingested": ingested}

    @mcp.tool(
        name="plane_ingest_work_items",
        tags={"kg"},
        annotations={"readOnlyHint": False, "idempotentHint": True},
    )
    async def plane_ingest_work_items(
        project_id: str = Field(description="Project whose work items are ingested"),
        per_page: int | None = Field(default=None, description="Page size"),
        cursor: str | None = Field(default=None, description="Pagination cursor"),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Ingest a project's work items as :Issue nodes (+ :belongsToProject / :assignedTo / :hasState / :inCycle)."""
        from plane_agent import kg_ingest

        if ctx:
            await ctx.info("Executing tool...")
        kwargs = {
            k: v for k, v in {"per_page": per_page, "cursor": cursor}.items() if v
        }
        result = await run_blocking(client.list_work_items, project_id, **kwargs)
        records = _kg_records(result)
        ingested = await kg_ingest.ingest_work_items(records, project_id=project_id)
        return {"listed": len(records), "ingested": ingested}

    @mcp.tool(
        name="plane_ingest_cycles",
        tags={"kg"},
        annotations={"readOnlyHint": False, "idempotentHint": True},
    )
    async def plane_ingest_cycles(
        project_id: str = Field(description="Project whose cycles are ingested"),
        per_page: int | None = Field(default=None, description="Page size"),
        cursor: str | None = Field(default=None, description="Pagination cursor"),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Ingest a project's cycles as :Cycle nodes (+ :belongsToProject)."""
        from plane_agent import kg_ingest

        if ctx:
            await ctx.info("Executing tool...")
        kwargs = {
            k: v for k, v in {"per_page": per_page, "cursor": cursor}.items() if v
        }
        result = await run_blocking(client.list_cycles, project_id, **kwargs)
        records = _kg_records(result)
        ingested = await kg_ingest.ingest_cycles(records, project_id=project_id)
        return {"listed": len(records), "ingested": ingested}

    return None
