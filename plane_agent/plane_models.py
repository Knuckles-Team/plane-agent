"""Pydantic models for Plane API."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Response(BaseModel):
    """Standard wrapper for API responses."""

    response: Any
    data: Any


class ProjectModel(BaseModel):
    """Input model for project operations."""

    project_id: str | None = None
    name: str | None = None
    identifier: str | None = None
    description: str | None = None
    api_parameters: dict | None = Field(description="API Parameters", default=None)


class WorkItemModel(BaseModel):
    """Input model for work item operations."""

    project_id: str | None = None
    work_item_id: str | None = None
    name: str | None = None
    description: str | None = None
    priority: str | None = None
    state: str | None = None
    api_parameters: dict | None = Field(description="API Parameters", default=None)


class Project(BaseModel):
    id: str
    name: str = ""
    identifier: str = ""
    description: str | None = None
    workspace: str | None = None


class WorkItem(BaseModel):
    # Preserve the full Plane work-item record: the KG ingestion connector and any
    # downstream consumer need ``updated_at`` (delta watermark), ``sequence_id``,
    # ``description_html`` and ``assignees``, which a fixed projection would drop.
    model_config = ConfigDict(extra="allow")

    id: str
    name: str = ""
    project: str | None = None
    state: str | None = None
    priority: str | None = None
    description: str | None = None
    description_html: str | None = None
    sequence_id: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    assignees: list[Any] | None = None
