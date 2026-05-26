#!/usr/bin/env python

from plane_agent.api.api_client_cycles import Api as CyclesApi
from plane_agent.api.api_client_epics import Api as EpicsApi
from plane_agent.api.api_client_initiatives import Api as InitiativesApi
from plane_agent.api.api_client_intake import Api as IntakeApi
from plane_agent.api.api_client_milestones import Api as MilestonesApi
from plane_agent.api.api_client_modules_states import Api as ModulesStatesApi
from plane_agent.api.api_client_projects import Api as ProjectsApi
from plane_agent.api.api_client_work_items import Api as WorkItemsApi
from plane_agent.api.api_client_workspace import Api as WorkspaceApi


class Api(
    ProjectsApi,
    CyclesApi,
    EpicsApi,
    InitiativesApi,
    IntakeApi,
    WorkItemsApi,
    MilestonesApi,
    ModulesStatesApi,
    WorkspaceApi,
):
    """Unified Api client for Plane, composed of domain-specific sub-clients."""

    pass
