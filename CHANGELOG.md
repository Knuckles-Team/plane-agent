# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.18] - 2026-11-12

### Removed
- The thirteen action-routed tools (`plane_projects`, `plane_work_items`, `plane_cycles`, `plane_epics`, `plane_milestones`, `plane_modules`, `plane_states`, `plane_users`, `plane_workspaces`, `plane_initiatives`, `plane_intake`, `plane_labels`, `plane_pages`). Every action they routed to is already a typed per-operation tool (`plane_list_projects`, `plane_create_work_item`, ...), so callers switch to the typed name. The best-effort ingest that rode on the action-routed `list_*` calls is gone; the `plane_ingest_*` tools remain.

### Changed
- Read contracts and the source mapping name the typed list tools; the `Workspace` class extends the core `Collection` class; skills and docs describe the typed tools.

## [2.3.17] - 2026-11-06

### Changed
- Surface backfill: 16 business tool-use contracts and one per remaining tool, operator and two business-role prompts, three API area skills, task skills rewritten for the typed tools, scion-sdk 0.9

## [2.3.16] - 2026-10-30

### Changed
- Require `scion-sdk>=0.6.4,<0.7.0`; `uv.lock` relocked.

## [2.3.14] - 2026-10-27

### Added
- Add the Plane rapid-delivery development skill, Pages spec dashboard wiring,
  and focused publication contract tests.

## [2.3.12] - 2026-10-24

### Added
- Owner and assignee edges on the ingest sources (SDK 0.5.5 `EdgeSpec`): project to project lead, work item to
  assignees and to its project, with the `Person` record type (CONN-PLANE-AGENT-CONNECTOR-CONTENT-R005).

## [2.3.11] - 2026-10-24

### Changed
- Central connector migration: requires `agent-connector-sdk>=0.5.2`; server bootstrap, version, containers, ontology artifacts, security scaffold and pre-commit config are provided centrally.

## [Unreleased]

### Added
-

### Changed
-

### Fixed
-

## [0.1.45] - 2026-04-29

### Added
- Initial release
