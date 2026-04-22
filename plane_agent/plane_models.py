"""Pydantic models for Plane API."""

from typing import Any

from pydantic import BaseModel, Field


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
    id: str
    name: str = ""
    project: str | None = None
    state: str | None = None
    priority: str | None = None
    description: str | None = None
