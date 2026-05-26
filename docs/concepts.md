# Concept Registry — plane-agent

> **Prefix**: `CONCEPT:PLANE-*`
> **Version**: 0.14.0
> **Bridge**: [`CONCEPT:ECO-4.0`](../../agent-utilities/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:PLANE-001` | Cycles Operations | MCP tool domain `cycles` — Action-routed dynamic tool registration |
| `CONCEPT:PLANE-002` | Epics Operations | MCP tool domain `epics` — Action-routed dynamic tool registration |
| `CONCEPT:PLANE-003` | Initiatives Operations | MCP tool domain `initiatives` — Action-routed dynamic tool registration |
| `CONCEPT:PLANE-004` | Intake Operations | MCP tool domain `intake` — Action-routed dynamic tool registration |
| `CONCEPT:PLANE-005` | Labels Operations | MCP tool domain `labels` — Action-routed dynamic tool registration |
| `CONCEPT:PLANE-006` | Milestones Operations | MCP tool domain `milestones` — Action-routed dynamic tool registration |
| `CONCEPT:PLANE-007` | Modules Operations | MCP tool domain `modules` — Action-routed dynamic tool registration |
| `CONCEPT:PLANE-008` | Pages Operations | MCP tool domain `pages` — Action-routed dynamic tool registration |
| `CONCEPT:PLANE-009` | Projects Operations | MCP tool domain `projects` — Action-routed dynamic tool registration |
| `CONCEPT:PLANE-010` | States Operations | MCP tool domain `states` — Action-routed dynamic tool registration |
| `CONCEPT:PLANE-011` | Users Operations | MCP tool domain `users` — Action-routed dynamic tool registration |
| `CONCEPT:PLANE-012` | Work Items Operations | MCP tool domain `work_items` — Action-routed dynamic tool registration |
| `CONCEPT:PLANE-013` | Workspaces Operations | MCP tool domain `workspaces` — Action-routed dynamic tool registration |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:ECO-4.0` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:ORCH-1.2` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:OS-5.1` | Prompt Injection Defense | agent-utilities |
| `CONCEPT:OS-5.2` | Cognitive Scheduler | agent-utilities |
| `CONCEPT:OS-5.3` | Guardrail Engine | agent-utilities |
| `CONCEPT:OS-5.4` | Audit Logging | agent-utilities |
| `CONCEPT:KG-2.0` | Knowledge Graph Core | agent-utilities |

## Synergy with agent-utilities

This project integrates with `agent-utilities` via `CONCEPT:ECO-4.0` (Unified Toolkit Ingestion). The `plane_agent` MCP server registers its tools with the agent-utilities FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all PLANE-* concepts.
