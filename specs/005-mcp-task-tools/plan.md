# Implementation Plan: MCP Server Tools for Task Management

**Branch**: `005-mcp-task-tools` | **Date**: 2026-02-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-mcp-task-tools/spec.md`

## Summary

Formalize and align the existing MCP task tools (implemented in Spec 004) with the Spec-5 contract. The tools already exist in `backend/src/tools/task_tools.py` but require adjustments: rename `create_task` → `add_task`, add a dedicated `complete_task` tool (toggle behavior), validate input constraints (title 1-200 chars, description max 1000 chars), and ensure all JSON responses match the exact Spec-5 contract format. The `get_task` tool (not in Spec-5) is retained as it was part of Spec 004 but is not part of this spec's scope.

## Technical Context

**Language/Version**: Python 3.11 (Backend)
**Primary Dependencies**: FastAPI, OpenAI Agents SDK (`openai-agents`), SQLModel, asyncpg
**Storage**: Neon Serverless PostgreSQL (existing Task table from Spec 002 — no schema changes)
**Testing**: pytest + pytest-asyncio (unit tests for each tool)
**Target Platform**: Web (backend deployed to Hugging Face Spaces)
**Project Type**: Web application (monorepo: frontend/ + backend/)
**Performance Goals**: Each tool completes within 2 seconds (SC-004, SC-005)
**Constraints**: Stateless operations, user data isolation via UserContext, all ops scoped to authenticated user, no new tables
**Scale/Scope**: Up to 100 tasks per user, single-user context per tool invocation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Evidence |
|------|--------|----------|
| Spec-Driven Development | PASS | Spec 005 created and approved before planning |
| Security-First Design | PASS | All tools enforce user data isolation via UserContext; no cross-user access |
| Deterministic Behavior | PASS | All task ops routed through MCP tools; JSON contracts are deterministic |
| Separation of Concerns | PASS | Tools are isolated in `src/tools/`; called only by chat service |
| Zero Manual Coding | PASS | All implementation via Claude Code |
| JWT-Based Authentication | PASS | User context injected by chat service after JWT verification |
| Stateless Server Design | PASS | Each tool invocation is independent; no shared state |
| MCP-Driven Task Operations | PASS | All 5 tools defined as `@function_tool` decorated functions |

## Project Structure

### Documentation (this feature)

```text
specs/005-mcp-task-tools/
├── plan.md              # This file
├── research.md          # Phase 0: Gap analysis between existing code and spec
├── data-model.md        # Phase 1: Task entity reference (no new entities)
├── quickstart.md        # Phase 1: Testing guide for MCP tools
├── contracts/           # Phase 1: Tool JSON contracts
│   └── mcp-tools-contract.md  # Input/Output JSON for all 5 tools
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── tools/
│   │   ├── __init__.py          # Existing — update exports
│   │   └── task_tools.py        # Existing — MODIFY: rename create_task→add_task, add complete_task, add input validation
│   └── services/
│       └── chat_service.py      # Existing — MODIFY: update tool imports (add_task, complete_task)
└── tests/
    └── test_mcp_tools.py        # NEW: Unit tests for all 5 MCP tools
```

**Structure Decision**: Modify existing files only. The tools already exist from Spec 004. This spec formalizes the contract and aligns the implementation. No new directories or models needed.

## Complexity Tracking

No constitution violations. All gates pass.

---

## Phase 0: Research Decisions

See [research.md](./research.md) for detailed analysis.

### Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Tool naming | Rename `create_task` → `add_task` | Spec-5 defines `add_task`; aligns with user-facing language |
| Toggle completion | Add dedicated `complete_task` tool | Spec-5 requires a separate tool for clearer agent intent; toggles completed↔pending |
| `get_task` retention | Keep but out of Spec-5 scope | Spec 004 defined it; useful for agent; no spec conflict |
| Input validation | Add title/description length validation in tools | Spec FR-005/FR-010 require validation; existing Task model has constraints but tools should validate before DB |
| Response format alignment | Match exact JSON structure from Spec-5 contracts | Current implementation is close but needs minor adjustments (e.g., `complete_task` response) |
| Test approach | pytest with mocked AsyncSession | Tools are pure functions with injected context; easily testable |

## Phase 1: Design

### Data Model

See [data-model.md](./data-model.md) for entity reference.

**No new entities**. All tools operate on the existing Task entity from Spec 002.

### Tool Contracts

See [contracts/mcp-tools-contract.md](./contracts/mcp-tools-contract.md) for full tool contracts.

### Gap Analysis: Current Implementation vs Spec-5

| Spec-5 Requirement | Current Status | Action Required |
|---------------------|----------------|-----------------|
| `add_task` tool | Exists as `create_task` | Rename function and update docstring |
| `list_tasks` tool | Exists and matches | Minor: verify empty response uses `"status": "empty"` |
| `complete_task` tool | Does not exist | Create new tool: toggle completed status |
| `update_task` tool | Exists and matches | Verify changes list format matches spec |
| `delete_task` tool | Exists and matches | Already matches spec contract |
| Title validation (1-200 chars) | Handled by SQLModel field | Add explicit tool-level validation with error message |
| Description validation (max 1000) | Handled by SQLModel field | Add explicit tool-level validation with error message |
| FR-014 descriptive docstrings | Partial | Update docstrings to be more descriptive for agent use |

### Developer Quickstart

See [quickstart.md](./quickstart.md) for setup and testing instructions.
