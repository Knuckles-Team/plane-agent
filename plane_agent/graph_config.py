"""Plane graph configuration — tag prompts and env var mappings.

This is the only file needed to enable graph mode for this agent.
Provides TAG_PROMPTS and TAG_ENV_VARS for create_graph_agent_server().
"""

# ── Tag → System Prompt Mapping ──────────────────────────────────────
TAG_PROMPTS: dict[str, str] = {
    "projects": (
        "You are a Plane Projects specialist. Help users manage and interact with Projects functionality using the available tools."
    ),
    "work_items": (
        "You are a Plane Work Items specialist. Help users manage and interact with Work Items functionality using the available tools."
    ),
    "cycles": (
        "You are a Plane Cycles specialist. Help users manage and interact with Cycles functionality using the available tools."
    ),
    "epics": (
        "You are a Plane Epics specialist. Help users manage and interact with Epics functionality using the available tools."
    ),
    "initiatives": (
        "You are a Plane Initiatives specialist. Help users manage and interact with Initiatives functionality using the available tools."
    ),
    "intake": (
        "You are a Plane Intake specialist. Help users manage and interact with Intake functionality using the available tools."
    ),
    "labels": (
        "You are a Plane Labels specialist. Help users manage and interact with Labels functionality using the available tools."
    ),
    "pages": (
        "You are a Plane Pages specialist. Help users manage and interact with Pages functionality using the available tools."
    ),
    "milestones": (
        "You are a Plane Milestones specialist. Help users manage and interact with Milestones functionality using the available tools."
    ),
    "modules": (
        "You are a Plane Modules specialist. Help users manage and interact with Modules functionality using the available tools."
    ),
    "states": (
        "You are a Plane States specialist. Help users manage and interact with States functionality using the available tools."
    ),
    "users": (
        "You are a Plane Users specialist. Help users manage and interact with Users functionality using the available tools."
    ),
    "workspaces": (
        "You are a Plane Workspaces specialist. Help users manage and interact with Workspaces functionality using the available tools."
    ),
}


# ── Tag → Environment Variable Mapping ────────────────────────────────
TAG_ENV_VARS: dict[str, str] = {
    "projects": "PROJECTSTOOL",
    "work_items": "WORK_ITEMSTOOL",
    "cycles": "CYCLESTOOL",
    "epics": "EPICSTOOL",
    "initiatives": "INITIATIVESTOOL",
    "intake": "INTAKETOOL",
    "labels": "LABELSTOOL",
    "pages": "PAGESTOOL",
    "milestones": "MILESTONESTOOL",
    "modules": "MODULESTOOL",
    "states": "STATESTOOL",
    "users": "USERSTOOL",
    "workspaces": "WORKSPACESTOOL",
}
