"""Pydantic models for Plane API."""

from typing import Optional, Any, Dict
from pydantic import BaseModel, Field


class Response(BaseModel):
    """Standard wrapper for API responses."""

    response: Any
    data: Any


class ProjectModel(BaseModel):
    """Input model for project operations."""

    project_id: Optional[str] = None
    name: Optional[str] = None
    identifier: Optional[str] = None
    description: Optional[str] = None
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)


class WorkItemModel(BaseModel):
    """Input model for work item operations."""

    project_id: Optional[str] = None
    work_item_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    state: Optional[str] = None
    api_parameters: Optional[Dict] = Field(description="API Parameters", default=None)


                                                       
class Project(BaseModel):
    id: str
    name: str = ""
    identifier: str = ""
    description: Optional[str] = None
    workspace: Optional[str] = None


class WorkItem(BaseModel):
    id: str
    name: str = ""
    project: Optional[str] = None
    state: Optional[str] = None
    priority: Optional[str] = None
    description: Optional[str] = None
