#!/usr/bin/python
# coding: utf-8
import sys
import json
import os
import argparse
import logging
import uvicorn
import httpx
from contextlib import asynccontextmanager
from typing import Optional, Any

from pydantic_ai import Agent, ModelSettings, RunContext
from pydantic_ai.mcp import (
    load_mcp_servers,
    MCPServerStreamableHTTP,
    MCPServerSSE,
)
from pydantic_ai_skills import SkillsToolset
from fasta2a import Skill
from plane_agent.utils import (
    to_boolean,
    to_integer,
    to_float,
    to_list,
    to_dict,
    get_mcp_config_path,
    get_skills_path,
    load_skills_from_directory,
    create_model,
    prune_large_messages,
)

from fastapi import FastAPI, Request
from starlette.responses import Response, StreamingResponse
from pydantic import ValidationError
from pydantic_ai.ui import SSE_CONTENT_TYPE
from pydantic_ai.ui.ag_ui import AGUIAdapter

__version__ = "0.1.4"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logging.getLogger("pydantic_ai").setLevel(logging.INFO)
logging.getLogger("fastmcp").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(os.getenv("PORT", "9000"))
DEFAULT_DEBUG = to_boolean(os.getenv("DEBUG", "False"))
DEFAULT_PROVIDER = os.getenv("PROVIDER", "openai")
DEFAULT_MODEL_ID = os.getenv("MODEL_ID", "qwen/qwen3-coder-next")
DEFAULT_LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://host.docker.internal:1234/v1")
DEFAULT_LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")
DEFAULT_MCP_URL = os.getenv("MCP_URL", None)
DEFAULT_MCP_CONFIG = os.getenv("MCP_CONFIG", get_mcp_config_path())
DEFAULT_CUSTOM_SKILLS_DIRECTORY = os.getenv("CUSTOM_SKILLS_DIRECTORY", None)
DEFAULT_ENABLE_WEB_UI = to_boolean(os.getenv("ENABLE_WEB_UI", "False"))
DEFAULT_SSL_VERIFY = to_boolean(os.getenv("SSL_VERIFY", "True"))

DEFAULT_MAX_TOKENS = to_integer(os.getenv("MAX_TOKENS", "16384"))
DEFAULT_TEMPERATURE = to_float(os.getenv("TEMPERATURE", "0.7"))
DEFAULT_TOP_P = to_float(os.getenv("TOP_P", "1.0"))
DEFAULT_TIMEOUT = to_float(os.getenv("TIMEOUT", "32400.0"))
DEFAULT_TOOL_TIMEOUT = to_float(os.getenv("TOOL_TIMEOUT", "32400.0"))
DEFAULT_PARALLEL_TOOL_CALLS = to_boolean(os.getenv("PARALLEL_TOOL_CALLS", "True"))
DEFAULT_SEED = to_integer(os.getenv("SEED", None))
DEFAULT_PRESENCE_PENALTY = to_float(os.getenv("PRESENCE_PENALTY", "0.0"))
DEFAULT_FREQUENCY_PENALTY = to_float(os.getenv("FREQUENCY_PENALTY", "0.0"))
DEFAULT_LOGIT_BIAS = to_dict(os.getenv("LOGIT_BIAS", None))
DEFAULT_STOP_SEQUENCES = to_list(os.getenv("STOP_SEQUENCES", None))
DEFAULT_EXTRA_HEADERS = to_dict(os.getenv("EXTRA_HEADERS", None))
DEFAULT_EXTRA_BODY = to_dict(os.getenv("EXTRA_BODY", None))

AGENT_NAME = "Plane Agent"
AGENT_DESCRIPTION = "A manager for the Plane Platform, orchestrating specialized agents for different domains."

SUPERVISOR_SYSTEM_PROMPT = os.environ.get(
    "SUPERVISOR_SYSTEM_PROMPT",
    default=(
        "You are the Plane Supervisor Agent, an expert orchestrator for project management tasks in Plane.\n"
        "Your primary goal is to analyze user requests, classify them into relevant domains, and delegate to specialized child agents.\n"
        "Domains include:\n"
        "- Projects: Management of projects\n"
        "- Work Items: Core items, comments, links, types, properties, relations, activities\n"
        "- Cycles: Time-boxed iteration management\n"
        "- Modules: Functional grouping of work items\n"
        "- Pages: Wiki/Documentation pages\n"
        "- Intake: Intake process for new issues\n"
        "- Users: User information\n"
        "- States: Workflow states\n"
        "- Labels: Tagging and classification\n"
        "- Initiatives: High-level goals\n"
        "- Workspaces: Workspace configuration\n"
        "- Work Logs: Time tracking\n\n"
        "Step-by-step reasoning: 1. Parse the request. 2. Map to 1-3 domains. 3. Delegate to child agents using `assign_task_to_[domain]_agent`. 4. Synthesize results.\n"
        "Guardrails: Never perform actions directly—always delegate. If unsure, ask for clarification."
    ),
)


AGENTS_CONFIG = {
    "projects": {
        "prompt": "You are the Plane Projects Agent. Manage projects, members, features, and summaries.",
        "name": "Plane_Projects_Agent",
    },
    "work_items": {
        "prompt": "You are the Plane Work Items Agent. Create, update, list, and search work items.",
        "name": "Plane_Work_Items_Agent",
    },
    "cycles": {
        "prompt": "You are the Plane Cycles Agent. Manage cycles and their work items.",
        "name": "Plane_Cycles_Agent",
    },
    "modules": {
        "prompt": "You are the Plane Modules Agent. Manage modules and their work items.",
        "name": "Plane_Modules_Agent",
    },
    "pages": {
        "prompt": "You are the Plane Pages Agent. Manage project and workspace pages.",
        "name": "Plane_Pages_Agent",
    },
    "users": {
        "prompt": "You are the Plane Users Agent. Retrieve user information.",
        "name": "Plane_Users_Agent",
    },
    "states": {
        "prompt": "You are the Plane States Agent. Manage workflow states.",
        "name": "Plane_States_Agent",
    },
    "labels": {
        "prompt": "You are the Plane Labels Agent. Manage labels.",
        "name": "Plane_Labels_Agent",
    },
    "work_item_types": {
        "prompt": "You are the Plane Work Item Types Agent. Manage different types of work items.",
        "name": "Plane_Work_Item_Types_Agent",
    },
    "work_item_comments": {
        "prompt": "You are the Plane Work Item Comments Agent. Manage comments on work items.",
        "name": "Plane_Work_Item_Comments_Agent",
    },
    "work_item_links": {
        "prompt": "You are the Plane Work Item Links Agent. Manage links between work items.",
        "name": "Plane_Work_Item_Links_Agent",
    },
    "work_item_properties": {
        "prompt": "You are the Plane Work Item Properties Agent. Manage custom properties.",
        "name": "Plane_Work_Item_Properties_Agent",
    },
    "work_item_activities": {
        "prompt": "You are the Plane Work Item Activities Agent. Retrieve activity logs.",
        "name": "Plane_Work_Item_Activities_Agent",
    },
    "work_logs": {
        "prompt": "You are the Plane Work Logs Agent. Manage work logs and time tracking.",
        "name": "Plane_Work_Logs_Agent",
    },
    "initiatives": {
        "prompt": "You are the Plane Initiatives Agent. Manage initiatives.",
        "name": "Plane_Initiatives_Agent",
    },
    "intake": {
        "prompt": "You are the Plane Intake Agent. Manage intake work items.",
        "name": "Plane_Intake_Agent",
    },
    "workspaces": {
        "prompt": "You are the Plane Workspaces Agent. Manage workspace details and members.",
        "name": "Plane_Workspaces_Agent",
    },
    "work_item_relations": {
        "prompt": "You are the Plane Work Item Relations Agent. Manage relations (blocking, etc.) between items.",
        "name": "Plane_Work_Item_Relations_Agent",
    },
}


def create_agent(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = DEFAULT_LLM_BASE_URL,
    api_key: Optional[str] = DEFAULT_LLM_API_KEY,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    custom_skills_directory: Optional[str] = DEFAULT_CUSTOM_SKILLS_DIRECTORY,
    ssl_verify: bool = DEFAULT_SSL_VERIFY,
) -> Agent:
    """
    Factory function that creates:
    - Specialized sub-agents (workers) for Plane domains
    - An orchestrator agent (supervisor) that delegates to them

    Returns the orchestrator agent, ready to run.
    """
    logger.info("Initializing Multi-Agent System for Plane...")

    agent_toolsets = []
    if mcp_url:
        if "sse" in mcp_url.lower():
            server = MCPServerSSE(
                mcp_url,
                http_client=httpx.AsyncClient(
                    verify=ssl_verify, timeout=DEFAULT_TIMEOUT
                ),
            )
        else:
            server = MCPServerStreamableHTTP(
                mcp_url,
                http_client=httpx.AsyncClient(
                    verify=ssl_verify, timeout=DEFAULT_TIMEOUT
                ),
            )
        agent_toolsets.append(server)
        logger.info(f"Connected to MCP Server: {mcp_url}")
    elif mcp_config:
        mcp_toolset = load_mcp_servers(mcp_config)
        for server in mcp_toolset:
            if hasattr(server, "http_client"):
                server.http_client = httpx.AsyncClient(
                    verify=ssl_verify, timeout=DEFAULT_TIMEOUT
                )
        agent_toolsets.extend(mcp_toolset)
        logger.info(f"Connected to MCP Config JSON: {mcp_toolset}")

    model = create_model(
        provider=provider,
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        ssl_verify=ssl_verify,
        timeout=DEFAULT_TIMEOUT,
    )
    settings = ModelSettings(
        max_tokens=DEFAULT_MAX_TOKENS,
        temperature=DEFAULT_TEMPERATURE,
        top_p=DEFAULT_TOP_P,
        timeout=DEFAULT_TIMEOUT,
        parallel_tool_calls=DEFAULT_PARALLEL_TOOL_CALLS,
        seed=DEFAULT_SEED,
        presence_penalty=DEFAULT_PRESENCE_PENALTY,
        frequency_penalty=DEFAULT_FREQUENCY_PENALTY,
        logit_bias=DEFAULT_LOGIT_BIAS,
        stop_sequences=DEFAULT_STOP_SEQUENCES,
        extra_headers=DEFAULT_EXTRA_HEADERS,
        extra_body=DEFAULT_EXTRA_BODY,
    )

    child_agents = {}
    supervisor_skills = []
    supervisor_skills_directories = [get_skills_path()]

    from plane_agent.utils import tool_in_tag

    for tag, config in AGENTS_CONFIG.items():
        tag_toolsets = []

        # Filter tools for this tag
        for ts in agent_toolsets:

            def filter_func(ctx, tool_def, t=tag):
                return tool_in_tag(tool_def, t)

            if hasattr(ts, "filtered"):
                filtered_ts = ts.filtered(filter_func)
                tag_toolsets.append(filtered_ts)
            else:
                # If toolset doesn't support filtered(), we might be passing all tools
                # But pydantic_ai MCPServers usually support it or we rely on the agent to handle it?
                # Actually, MCPServer doesn't have filtered by default unless wrapped.
                # But since we are using pydantic-ai, we might need to rely on the agent seeing all tools
                # but only being told about the ones relevant?
                # No, we want to restrict tools.
                # If ts is MCPServerStdio, it inherits from AbstractToolset which might not have filtered.
                # Wait, AbstractToolset HAS filtered. Checked code in pydantic_ai/toolsets/abstract.py (implied).
                # Only check if available.
                try:
                    filtered_ts = ts.filtered(filter_func)
                    tag_toolsets.append(filtered_ts)
                except Exception:
                    # Fallback if filtering not supported, but ideally it should be.
                    # We'll rely on system prompt if filtering fails, but let's assume it works.
                    pass

        skill_dir_name = f"plane-{tag.replace('_', '-')}"
        child_skills_directories = []

        # Check custom skills directory
        if custom_skills_directory:
            skill_dir_path = os.path.join(custom_skills_directory, skill_dir_name)
            if os.path.exists(skill_dir_path):
                child_skills_directories.append(skill_dir_path)

        # Check default skills directory
        default_skill_path = os.path.join(get_skills_path(), skill_dir_name)
        if os.path.exists(default_skill_path):
            child_skills_directories.append(default_skill_path)

        if child_skills_directories:
            ts = SkillsToolset(directories=child_skills_directories)
            tag_toolsets.append(ts)
            logger.info(
                f"Loaded specialized skills for {tag} from {child_skills_directories}"
            )

        # Log available tools for debug
        # (Simplified logging compared to servicenow to save space)

        agent = Agent(
            model=model,
            system_prompt=config["prompt"],
            name=config["name"],
            toolsets=tag_toolsets,
            tool_timeout=DEFAULT_TOOL_TIMEOUT,
            model_settings=settings,
        )
        child_agents[tag] = agent

    if custom_skills_directory:
        supervisor_skills_directories.append(custom_skills_directory)

    # Load Supervisor Skills (generic ones if any, plus delegation tools)
    supervisor_skills.append(SkillsToolset(directories=supervisor_skills_directories))
    logger.info(f"Loaded supervisor skills from: {supervisor_skills_directories}")

    supervisor = Agent(
        name=AGENT_NAME,
        system_prompt=SUPERVISOR_SYSTEM_PROMPT,
        model=model,
        model_settings=settings,
        toolsets=supervisor_skills,
        deps_type=Any,
    )

    # Delegation Tools
    # Note: We must define these dynamically or repetitively because Python decorators need the function.
    # We can use a loop to generate them, but binding is tricky.
    # It's better to be explicit for clarity despite verbosity, matching servicenow example.

    @supervisor.tool
    async def assign_task_to_projects_agent(ctx: RunContext[Any], task: str) -> str:
        """Assigns a task to the Projects agent."""
        logger.info(f"Assigning to Projects: {task}")
        result = await child_agents["projects"].run(
            task, usage=ctx.usage, deps=ctx.deps
        )
        return result.output

    @supervisor.tool
    async def assign_task_to_work_items_agent(ctx: RunContext[Any], task: str) -> str:
        """Assigns a task to the Work Items agent."""
        logger.info(f"Assigning to Work Items: {task}")
        result = await child_agents["work_items"].run(
            task, usage=ctx.usage, deps=ctx.deps
        )
        return result.output

    @supervisor.tool
    async def assign_task_to_cycles_agent(ctx: RunContext[Any], task: str) -> str:
        """Assigns a task to the Cycles agent."""
        logger.info(f"Assigning to Cycles: {task}")
        result = await child_agents["cycles"].run(task, usage=ctx.usage, deps=ctx.deps)
        return result.output

    @supervisor.tool
    async def assign_task_to_modules_agent(ctx: RunContext[Any], task: str) -> str:
        """Assigns a task to the Modules agent."""
        logger.info(f"Assigning to Modules: {task}")
        result = await child_agents["modules"].run(task, usage=ctx.usage, deps=ctx.deps)
        return result.output

    @supervisor.tool
    async def assign_task_to_pages_agent(ctx: RunContext[Any], task: str) -> str:
        """Assigns a task to the Pages agent."""
        logger.info(f"Assigning to Pages: {task}")
        result = await child_agents["pages"].run(task, usage=ctx.usage, deps=ctx.deps)
        return result.output

    @supervisor.tool
    async def assign_task_to_users_agent(ctx: RunContext[Any], task: str) -> str:
        """Assigns a task to the Users agent."""
        logger.info(f"Assigning to Users: {task}")
        result = await child_agents["users"].run(task, usage=ctx.usage, deps=ctx.deps)
        return result.output

    @supervisor.tool
    async def assign_task_to_states_agent(ctx: RunContext[Any], task: str) -> str:
        """Assigns a task to the States agent."""
        logger.info(f"Assigning to States: {task}")
        result = await child_agents["states"].run(task, usage=ctx.usage, deps=ctx.deps)
        return result.output

    @supervisor.tool
    async def assign_task_to_labels_agent(ctx: RunContext[Any], task: str) -> str:
        """Assigns a task to the Labels agent."""
        logger.info(f"Assigning to Labels: {task}")
        result = await child_agents["labels"].run(task, usage=ctx.usage, deps=ctx.deps)
        return result.output

    @supervisor.tool
    async def assign_task_to_work_item_types_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assigns a task to the Work Item Types agent."""
        logger.info(f"Assigning to Work Item Types: {task}")
        result = await child_agents["work_item_types"].run(
            task, usage=ctx.usage, deps=ctx.deps
        )
        return result.output

    @supervisor.tool
    async def assign_task_to_work_item_comments_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assigns a task to the Work Item Comments agent."""
        logger.info(f"Assigning to Work Item Comments: {task}")
        result = await child_agents["work_item_comments"].run(
            task, usage=ctx.usage, deps=ctx.deps
        )
        return result.output

    @supervisor.tool
    async def assign_task_to_work_item_links_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assigns a task to the Work Item Links agent."""
        logger.info(f"Assigning to Work Item Links: {task}")
        result = await child_agents["work_item_links"].run(
            task, usage=ctx.usage, deps=ctx.deps
        )
        return result.output

    @supervisor.tool
    async def assign_task_to_work_item_properties_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assigns a task to the Work Item Properties agent."""
        logger.info(f"Assigning to Work Item Properties: {task}")
        result = await child_agents["work_item_properties"].run(
            task, usage=ctx.usage, deps=ctx.deps
        )
        return result.output

    @supervisor.tool
    async def assign_task_to_work_item_activities_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assigns a task to the Work Item Activities agent."""
        logger.info(f"Assigning to Work Item Activities: {task}")
        result = await child_agents["work_item_activities"].run(
            task, usage=ctx.usage, deps=ctx.deps
        )
        return result.output

    @supervisor.tool
    async def assign_task_to_work_logs_agent(ctx: RunContext[Any], task: str) -> str:
        """Assigns a task to the Work Logs agent."""
        logger.info(f"Assigning to Work Logs: {task}")
        result = await child_agents["work_logs"].run(
            task, usage=ctx.usage, deps=ctx.deps
        )
        return result.output

    @supervisor.tool
    async def assign_task_to_initiatives_agent(ctx: RunContext[Any], task: str) -> str:
        """Assigns a task to the Initiatives agent."""
        logger.info(f"Assigning to Initiatives: {task}")
        result = await child_agents["initiatives"].run(
            task, usage=ctx.usage, deps=ctx.deps
        )
        return result.output

    @supervisor.tool
    async def assign_task_to_intake_agent(ctx: RunContext[Any], task: str) -> str:
        """Assigns a task to the Intake agent."""
        logger.info(f"Assigning to Intake: {task}")
        result = await child_agents["intake"].run(task, usage=ctx.usage, deps=ctx.deps)
        return result.output

    @supervisor.tool
    async def assign_task_to_workspaces_agent(ctx: RunContext[Any], task: str) -> str:
        """Assigns a task to the Workspaces agent."""
        logger.info(f"Assigning to Workspaces: {task}")
        result = await child_agents["workspaces"].run(
            task, usage=ctx.usage, deps=ctx.deps
        )
        return result.output

    @supervisor.tool
    async def assign_task_to_work_item_relations_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assigns a task to the Work Item Relations agent."""
        logger.info(f"Assigning to Work Item Relations: {task}")
        result = await child_agents["work_item_relations"].run(
            task, usage=ctx.usage, deps=ctx.deps
        )
        return result.output

    return supervisor


def create_agent_server(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = DEFAULT_LLM_BASE_URL,
    api_key: Optional[str] = DEFAULT_LLM_API_KEY,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    custom_skills_directory: Optional[str] = DEFAULT_CUSTOM_SKILLS_DIRECTORY,
    debug: Optional[bool] = DEFAULT_DEBUG,
    host: Optional[str] = DEFAULT_HOST,
    port: Optional[int] = DEFAULT_PORT,
    enable_web_ui: bool = DEFAULT_ENABLE_WEB_UI,
    ssl_verify: bool = DEFAULT_SSL_VERIFY,
):
    print(
        f"Starting {AGENT_NAME}:"
        f"\tprovider={provider}"
        f"\tmodel={model_id}"
        f"\tbase_url={base_url}"
        f"\tmcp={mcp_url} | {mcp_config}"
        f"\tssl_verify={ssl_verify}"
    )
    agent = create_agent(
        provider=provider,
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        mcp_url=mcp_url,
        mcp_config=mcp_config,
        custom_skills_directory=custom_skills_directory,
        ssl_verify=ssl_verify,
    )

    # Always load default skills

    skills = load_skills_from_directory(get_skills_path())

    logger.info(f"Loaded {len(skills)} default skills from {get_skills_path()}")

    # Load custom skills if provided

    if custom_skills_directory and os.path.exists(custom_skills_directory):

        custom_skills = load_skills_from_directory(custom_skills_directory)

        skills.extend(custom_skills)

        logger.info(
            f"Loaded {len(custom_skills)} custom skills from {custom_skills_directory}"
        )

    if not skills:

        skills = [
            Skill(
                id="plane_agent",
                name="Plane Agent",
                description="General access to Plane tools",
                tags=["plane"],
                input_modes=["text"],
                output_modes=["text"],
            )
        ]

    a2a_app = agent.to_a2a(
        name=AGENT_NAME,
        description=AGENT_DESCRIPTION,
        version=__version__,
        skills=skills,
        debug=debug,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if hasattr(a2a_app, "router") and hasattr(a2a_app.router, "lifespan_context"):
            async with a2a_app.router.lifespan_context(a2a_app):
                yield
        else:
            yield

    app = FastAPI(
        title=f"{AGENT_NAME} - A2A + AG-UI Server",
        description=AGENT_DESCRIPTION,
        debug=debug,
        lifespan=lifespan,
    )

    @app.get("/health")
    async def health_check():
        return {"status": "OK"}

    app.mount("/a2a", a2a_app)

    @app.post("/ag-ui")
    async def ag_ui_endpoint(request: Request) -> Response:
        accept = request.headers.get("accept", SSE_CONTENT_TYPE)
        try:
            run_input = AGUIAdapter.build_run_input(await request.body())
        except ValidationError as e:
            return Response(
                content=json.dumps(e.json()),
                media_type="application/json",
                status_code=422,
            )

        if hasattr(run_input, "messages"):
            run_input.messages = prune_large_messages(run_input.messages)

        adapter = AGUIAdapter(agent=agent, run_input=run_input, accept=accept)
        event_stream = adapter.run_stream()
        sse_stream = adapter.encode_stream(event_stream)

        return StreamingResponse(
            sse_stream,
            media_type=accept,
        )

    if enable_web_ui:
        web_ui = agent.to_web(instructions=SUPERVISOR_SYSTEM_PROMPT)
        app.mount("/", web_ui)
        logger.info(
            "Starting server on %s:%s (A2A at /a2a, AG-UI at /ag-ui, Web UI: %s)",
            host,
            port,
            "Enabled at /" if enable_web_ui else "Disabled",
        )

    uvicorn.run(
        app,
        host=host,
        port=port,
        timeout_keep_alive=1800,
        timeout_graceful_shutdown=60,
        log_level="debug" if debug else "info",
    )


def agent_server():
    print(f"{AGENT_NAME} v{__version__}")
    parser = argparse.ArgumentParser(
        add_help=False, description=f"Run the {AGENT_NAME} A2A + AG-UI Server"
    )
    parser.add_argument(
        "--host", default=DEFAULT_HOST, help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="Port to bind the server to"
    )
    parser.add_argument(
        "--debug", action="store_true", default=DEFAULT_DEBUG, help="Debug mode"
    )
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    parser.add_argument(
        "--provider",
        default=DEFAULT_PROVIDER,
        choices=[
            "openai",
            "anthropic",
            "google",
            "huggingface",
            "groq",
            "mistral",
            "ollama",
        ],
        help="LLM Provider",
    )
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID, help="LLM Model ID")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_LLM_BASE_URL,
        help="LLM Base URL (for OpenAI compatible providers)",
    )
    parser.add_argument("--api-key", default=DEFAULT_LLM_API_KEY, help="LLM API Key")
    parser.add_argument("--mcp-url", default=DEFAULT_MCP_URL, help="MCP Server URL")
    parser.add_argument(
        "--mcp-config", default=DEFAULT_MCP_CONFIG, help="MCP Server Config"
    )
    parser.add_argument(
        "--custom-skills-directory",
        default=DEFAULT_CUSTOM_SKILLS_DIRECTORY,
        help="Directory containing additional custom agent skills",
    )

    parser.add_argument(
        "--web",
        action="store_true",
        default=DEFAULT_ENABLE_WEB_UI,
        help="Enable Pydantic AI Web UI",
    )

    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable SSL verification for LLM requests (Use with caution)",
    )

    parser.add_argument("--help", action="store_true", help="Show usage")

    args = parser.parse_args()

    if hasattr(args, "help") and args.help:

        parser.print_help()

        sys.exit(0)

    if args.debug:
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
            force=True,
        )
        logging.getLogger("pydantic_ai").setLevel(logging.DEBUG)
        logging.getLogger("fastmcp").setLevel(logging.DEBUG)
        logging.getLogger("httpcore").setLevel(logging.DEBUG)
        logging.getLogger("httpx").setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    create_agent_server(
        provider=args.provider,
        model_id=args.model_id,
        base_url=args.base_url,
        api_key=args.api_key,
        mcp_url=args.mcp_url,
        mcp_config=args.mcp_config,
        custom_skills_directory=args.custom_skills_directory,
        debug=args.debug,
        host=args.host,
        port=args.port,
        enable_web_ui=args.web,
        ssl_verify=not args.insecure,
    )


if __name__ == "__main__":
    agent_server()
