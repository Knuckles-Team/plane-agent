# Verification Checklist: Code Enhancement: plane-agent

## Functional Requirements Verification
- [ ] **FR-001**: 2 functions exceed 200 lines (actionable refactoring targets): register_work_items_tools (514L), register_cycles_tools (207L)
- [ ] **FR-002**: Monolithic: mcp_server.py (1816L) — 2 functions with high complexity (worst: register_work_items_tools at 514L, CC=11); Low cohesion: 23 distinct concepts in one file
- [ ] **FR-003**: Needs attention: api_client.py (1064L) — God class: Api (107 methods) — consider mixins/composition
- [ ] **FR-004**: Low test-to-source ratio: 0.27
- [ ] **FR-005**: Test suite lacks intent diversity (only one type)
- [ ] **FR-006**: 37 potential doc-test drift items
- [ ] **FR-007**: README.md missing sections: overview
- [ ] **FR-008**: 1 broken internal links in README.md
- [ ] **FR-009**: README missing: Has a clear project description (>50 chars)
- [ ] **FR-010**: README missing: Has a Table of Contents
- [ ] **FR-011**: README missing: Has architecture overview or diagram
- [ ] **FR-012**: README missing: References /docs directory material
- [ ] **FR-013**: SRP: 2 modules exceed 500 lines (god modules)
- [ ] **FR-014**: SRP: 1 classes have >15 methods
- [ ] **FR-015**: No discernible layer architecture (no domain/service/adapter separation)
- [ ] **FR-016**: Low traceability ratio: 0% concepts fully traced
- [ ] **FR-017**: 3 test functions missing concept markers
- [ ] **FR-018**: 96 significant functions (>10 lines) missing concept markers in docstrings
- [ ] **FR-019**: Total lint findings: 0 (high/error: 0, medium/warning: 0, low: 0)
- [ ] **FR-020**: 2 hook(s) may be outdated: ruff-pre-commit, uv-pre-commit
- [ ] **FR-021**: 2 rogue/throwaway scripts detected (fix_*, validate_*, patch_*, etc.): scripts/validate_agent.py, scripts/validate_a2a_agent.py
- [ ] **FR-022**: CHANGELOG.md exists but could not be parsed — check format compliance
- [ ] **FR-023**: No changelog entries within the last 30 days
- [ ] **FR-024**: keepachangelog not installed — pip install 'universal-skills[code-enhancer]'
- [ ] **FR-025**: Only 23% of env vars documented in README.md
- [ ] **FR-026**: Undocumented env vars: ALLOWED_CLIENT_REDIRECT_URIS, AUTH_TYPE, EUNOMIA_POLICY_FILE, EUNOMIA_REMOTE_URL, EUNOMIA_TYPE, FASTMCP_SERVER_AUTH, FASTMCP_SERVER_AUTH_JWT_ALGORITHM, FASTMCP_SERVER_AUTH_JWT_AUDIENCE, FASTMCP_SERVER_AUTH_JWT_ISSUER, FASTMCP_SERVER_AUTH_JWT_JWKS_URI
- [ ] **FR-027**: 8 Python env vars not in .env.example: DEFAULT_AGENT_NAME, LLM_API_KEY, LLM_BASE_URL, MCP_URL, MODEL_ID

## User Stories / Acceptance Criteria
- [ ] As a **developer**, I want to **address Project Analysis findings (grade: C, score: 74)**, so that **improve project project analysis from C to at least B (80+)**.
- [ ] As a **developer**, I want to **address Codebase Optimization findings (grade: C, score: 77)**, so that **improve project codebase optimization from C to at least B (80+)**.
- [ ] As a **developer**, I want to **address Test Coverage findings (grade: D, score: 60)**, so that **improve project test coverage from D to at least B (80+)**.
- [ ] As a **developer**, I want to **address Architecture & Design Patterns findings (grade: C, score: 70)**, so that **improve project architecture & design patterns from C to at least B (80+)**.
- [ ] As a **developer**, I want to **address Concept Traceability findings (grade: F, score: 44)**, so that **improve project concept traceability from F to at least B (80+)**.
- [ ] As a **developer**, I want to **address Changelog Audit findings (grade: C, score: 75)**, so that **improve project changelog audit from C to at least B (80+)**.
- [ ] As a **developer**, I want to **address Environment Variables findings (grade: D, score: 60)**, so that **improve project environment variables from D to at least B (80+)**.

## Success Criteria
- [ ] Overall GPA: 2.82 → 3.0
- [ ] Domains at B or above: 10 → 17
- [ ] Actionable findings: 27 → 0

## Technical Quality Gates
- [x] Pre-commit linting (Ruff check/format) passed
- [x] Repository standards checked and verified
- [x] Zero deprecated / local absolute `file:///` URLs

## Review & Acceptance
- **Overall Verification Score**: 0%
- **Final Review Status**: **Needs Revision**
