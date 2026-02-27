# Research: MCP Server Tools for Task Management

**Feature**: 005-mcp-task-tools | **Date**: 2026-02-22

## Research Context

The MCP task tools were initially implemented as part of Spec 004 (AI Chatbot). Spec 005 formalizes the tool contracts as a standalone specification. This research focuses on the gap between the current implementation and the Spec-5 requirements.

---

## Decision 1: Tool Naming — `create_task` → `add_task`

**Decision**: Rename `create_task` to `add_task`

**Rationale**: Spec-5 explicitly defines `add_task` as the tool name (FR-001, FR-005). The name "add" is more natural for user-facing language ("add a task") vs the developer-oriented "create."

**Alternatives considered**:
- Keep `create_task` and update Spec-5 → Rejected: Spec is the source of truth; implementation aligns to spec
- Alias both names → Rejected: Constitution says no feature creep; one name per tool

**Impact**: Requires updating `task_tools.py` function name, `chat_service.py` imports, and agent tool registration.

---

## Decision 2: Dedicated `complete_task` Tool

**Decision**: Add a new `complete_task` tool that toggles task completion status

**Rationale**: Spec-5 defines `complete_task` as a separate tool (FR-001, FR-007) distinct from `update_task`. This provides clearer intent signaling for the AI agent — "complete this task" is a more natural command than "update task with completed=true."

**Alternatives considered**:
- Use `update_task` with `completed` parameter only → Rejected: Spec explicitly requires 5 distinct tools; `complete_task` provides toggle semantics
- Make `complete_task` only set to completed (no toggle) → Rejected: Spec-5 US3 scenario 3 explicitly says "toggles the task back to pending"

**Implementation**: New function wrapping a targeted update on the `completed` field with toggle logic.

---

## Decision 3: Retain `get_task` from Spec 004

**Decision**: Keep `get_task` in the codebase but document it as out of Spec-5 scope

**Rationale**: `get_task` was implemented in Spec 004 and is useful for the AI agent (e.g., looking up task details before updating). Spec-5 defines exactly 5 tools (FR-001) and `get_task` is not one of them, but removing it would break Spec 004 functionality.

**Alternatives considered**:
- Remove `get_task` → Rejected: Breaks existing chatbot functionality
- Add `get_task` to Spec-5 → Rejected: Spec is already approved; changes would require a new spec cycle

---

## Decision 4: Input Validation Strategy

**Decision**: Add explicit validation in tool functions before database operations

**Rationale**: The Task SQLModel already has field constraints (`min_length=1, max_length=200` for title, `max_length=1000` for description), but these raise database-level errors. Tools should validate inputs and return user-friendly error JSON per FR-010.

**Alternatives considered**:
- Rely solely on SQLModel validation → Rejected: Database errors are not user-friendly; tools should catch and format validation errors
- Use Pydantic model for tool input validation → Rejected: Over-engineering; simple if-checks are sufficient for 2 fields

---

## Decision 5: Response Format Alignment

**Decision**: Align all tool responses exactly to Spec-5 JSON contracts

**Rationale**: Current implementation closely matches the spec but has minor differences:
- `list_tasks` empty case already uses `"status": "empty"` ✓
- `update_task` already returns `changes` array ✓
- `delete_task` already returns `deleted_title` ✓
- Missing: `add_task` naming, `complete_task` response format

**No breaking changes** to existing response formats — only additions.

---

## Decision 6: Testing Approach

**Decision**: pytest with mocked AsyncSession for unit tests

**Rationale**: Tools are async functions that receive a `RunContextWrapper[UserContext]` with an injected session. By mocking the session, we can test tool logic in isolation without a database connection.

**Alternatives considered**:
- Integration tests with real Neon DB → Considered for later; unit tests come first per TDD
- Manual testing only → Rejected: Spec SC-001 requires all tools to be verifiable
