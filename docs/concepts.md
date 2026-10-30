# Concept Registry — plane-agent

> **Prefix**: `CONCEPT:PLANE-*`
> **Version**: 0.14.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://github.com/Knuckles-Team/scion-sdk/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:PN-OS.governance.plane` | Cycles Operations | MCP tool domain `cycles` — Action-routed dynamic tool registration |
| `CONCEPT:PN-OS.governance.plane-2` | Epics Operations | MCP tool domain `epics` — Action-routed dynamic tool registration |
| `CONCEPT:PN-OS.governance.plane-3` | Initiatives Operations | MCP tool domain `initiatives` — Action-routed dynamic tool registration |
| `CONCEPT:PN-OS.governance.plane-4` | Intake Operations | MCP tool domain `intake` — Action-routed dynamic tool registration |
| `CONCEPT:PN-OS.governance.plane-5` | Labels Operations | MCP tool domain `labels` — Action-routed dynamic tool registration |
| `CONCEPT:PN-OS.governance.plane-6` | Milestones Operations | MCP tool domain `milestones` — Action-routed dynamic tool registration |
| `CONCEPT:PN-OS.governance.plane-7` | Modules Operations | MCP tool domain `modules` — Action-routed dynamic tool registration |
| `CONCEPT:PN-OS.governance.plane-8` | Pages Operations | MCP tool domain `pages` — Action-routed dynamic tool registration |
| `CONCEPT:PN-OS.governance.plane-9` | Projects Operations | MCP tool domain `projects` — Action-routed dynamic tool registration |
| `CONCEPT:PN-OS.governance.plane-10` | States Operations | MCP tool domain `states` — Action-routed dynamic tool registration |
| `CONCEPT:PN-OS.governance.plane-11` | Users Operations | MCP tool domain `users` — Action-routed dynamic tool registration |
| `CONCEPT:PN-OS.governance.plane-12` | Work Items Operations | MCP tool domain `work_items` — Action-routed dynamic tool registration |
| `CONCEPT:PN-OS.governance.plane-13` | Workspaces Operations | MCP tool domain `workspaces` — Action-routed dynamic tool registration |

## Cross-Project References (from scion-sdk)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | scion-sdk |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | scion-sdk |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | scion-sdk |
| `CONCEPT:AU-OS.state.cognitive-scheduler-preemption` | Cognitive Scheduler | scion-sdk |
| `CONCEPT:AU-OS.governance.reactive-multi-axis-budget` | Guardrail Engine | scion-sdk |
| `CONCEPT:AU-OS.governance.wasm-micro-agent-sandbox` | Audit Logging | scion-sdk |
| `CONCEPT:AU-KG.query.object-graph-mapper` | Knowledge Graph Core | scion-sdk |

## Synergy with scion-sdk

This project integrates with `scion-sdk` via `CONCEPT:AU-ECO.messaging.native-backend-abstraction` (Unified Toolkit Ingestion). The `plane_agent` MCP server registers its tools with the scion-sdk FastMCP middleware, enabling automatic discovery, telemetry, and Knowledge Graph ingestion of all PLANE-* concepts.
