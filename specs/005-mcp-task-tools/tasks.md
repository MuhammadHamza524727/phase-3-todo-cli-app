# Tasks: MCP Server Tools for Task Management

**Input**: Design documents from `/specs/005-mcp-task-tools/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/mcp-tools-contract.md

**Tests**: Not explicitly requested — test tasks included in Polish phase for verification.

**Organization**: Tasks are grouped by user story. Since MCP tools already exist from Spec 004, tasks focus on aligning the implementation with Spec-5 contracts.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Prepare the codebase for Spec-5 alignment changes

- [x] T001 Review current tool implementations and document gaps in backend/src/tools/task_tools.py
- [x] T002 Add input validation helper function `_validate_title` and `_validate_description` at top of backend/src/tools/task_tools.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared changes that all user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Update docstrings for UserContext class to reference Spec-5 FR-002 in backend/src/tools/task_tools.py
- [x] T004 Add `complete_task` import placeholder to backend/src/tools/__init__.py (will be populated in US3)

**Checkpoint**: Foundation ready — user story implementation can begin

---

## Phase 3: User Story 1 — AI Agent Creates a Task via `add_task` (Priority: P1) 🎯 MVP

**Goal**: Rename `create_task` to `add_task`, add input validation, align JSON output to Spec-5 contract

**Independent Test**: Invoke `add_task` with title "Buy groceries" and verify response JSON contains `status`, `task_id`, `title`, `message` fields matching contract

### Implementation for User Story 1

- [x] T005 [US1] Rename function `create_task` to `add_task` in backend/src/tools/task_tools.py — update function name, keep `@function_tool` decorator
- [x] T006 [US1] Update `add_task` docstring to match Spec-5 contract: "Add a new task to your task list. Use this when the user wants to create, add, or make a new task or todo item. Requires a title (1-200 characters). Optionally accepts a description (up to 1000 characters)." in backend/src/tools/task_tools.py
- [x] T007 [US1] Add input validation to `add_task`: validate title is 1-200 chars, description is max 1000 chars, return error JSON if invalid in backend/src/tools/task_tools.py
- [x] T008 [US1] Update `add_task` import in backend/src/services/chat_service.py — change `create_task` to `add_task` in import and agent tools list
- [x] T009 [US1] Update `add_task` export in backend/src/tools/__init__.py

**Checkpoint**: `add_task` tool is callable, validates inputs, returns Spec-5 contract JSON

---

## Phase 4: User Story 2 — AI Agent Lists Tasks via `list_tasks` (Priority: P1)

**Goal**: Verify `list_tasks` implementation matches Spec-5 contract exactly

**Independent Test**: Create 3 tasks, invoke `list_tasks` with no filter, verify response has `status`, `count`, `tasks` array with `index`, `id`, `title`, `status`, `description` per item

### Implementation for User Story 2

- [x] T010 [US2] Update `list_tasks` docstring to match Spec-5 contract: "List all tasks in your task list. Use this when the user wants to see, view, or check their tasks. Optionally filter by completion status: set completed=true for completed tasks, completed=false for pending tasks, or omit for all tasks." in backend/src/tools/task_tools.py
- [x] T011 [US2] Verify `list_tasks` empty response uses `"status": "empty"` with `"count": 0` and helpful message per Spec-5 contract in backend/src/tools/task_tools.py
- [x] T012 [US2] Verify `list_tasks` success response includes `"status": "success"`, `"count"`, and `"tasks"` array with `index`, `id`, `title`, `status`, `description` per Spec-5 contract in backend/src/tools/task_tools.py

**Checkpoint**: `list_tasks` returns contract-compliant JSON for all scenarios (tasks, empty, filtered)

---

## Phase 5: User Story 3 — AI Agent Completes a Task via `complete_task` (Priority: P2)

**Goal**: Create new `complete_task` tool that toggles task completion status

**Independent Test**: Create a pending task, invoke `complete_task` with its ID, verify response shows `completed: true`. Invoke again, verify `completed: false`.

### Implementation for User Story 3

- [x] T013 [US3] Create `complete_task` function with `@function_tool` decorator in backend/src/tools/task_tools.py — accepts `task_id` string, validates UUID, queries task scoped to user, toggles `completed` field, returns Spec-5 contract JSON with `status`, `task_id`, `title`, `completed`, `message`
- [x] T014 [US3] Add `complete_task` to agent tools list in backend/src/services/chat_service.py — add import and include in `tools=[...]` array
- [x] T015 [US3] Update SYSTEM_INSTRUCTIONS in backend/src/services/chat_service.py to mention `complete_task` as a dedicated tool for marking tasks done/undone
- [x] T016 [US3] Export `complete_task` from backend/src/tools/__init__.py

**Checkpoint**: `complete_task` toggles status, returns contract JSON, is registered with the agent

---

## Phase 6: User Story 4 — AI Agent Updates a Task via `update_task` (Priority: P2)

**Goal**: Add input validation and verify `update_task` matches Spec-5 contract

**Independent Test**: Create a task, invoke `update_task` with new title, verify response has `changes` array and descriptive message

### Implementation for User Story 4

- [x] T017 [US4] Update `update_task` docstring to match Spec-5 contract: "Update an existing task's details. Use this when the user wants to change, modify, rename, or edit a task. You can update the title, description, or completion status. Requires the task ID and at least one field to change." in backend/src/tools/task_tools.py
- [x] T018 [US4] Add input validation to `update_task`: validate title (1-200 chars if provided), description (max 1000 chars if provided), return error JSON if invalid in backend/src/tools/task_tools.py
- [x] T019 [US4] Verify `update_task` success response includes `status`, `task_id`, `title`, `changes` array, and descriptive `message` per Spec-5 contract in backend/src/tools/task_tools.py
- [x] T020 [US4] Verify `update_task` no-changes response returns `"status": "success"` with `"No changes were needed."` message in backend/src/tools/task_tools.py

**Checkpoint**: `update_task` validates inputs, lists specific changes, handles no-changes case

---

## Phase 7: User Story 5 — AI Agent Deletes a Task via `delete_task` (Priority: P2)

**Goal**: Verify `delete_task` matches Spec-5 contract

**Independent Test**: Create a task, invoke `delete_task` with its ID, verify response has `deleted_title` and confirmation message

### Implementation for User Story 5

- [x] T021 [US5] Update `delete_task` docstring to match Spec-5 contract: "Delete a task from your task list. Use this when the user wants to remove, delete, or get rid of a task. This action is permanent. Requires the task ID." in backend/src/tools/task_tools.py
- [x] T022 [US5] Verify `delete_task` success response includes `status`, `deleted_title`, and `message` per Spec-5 contract in backend/src/tools/task_tools.py
- [x] T023 [US5] Verify `delete_task` error responses match contract: "Task not found." for missing/other-user tasks, "Invalid task ID: {value}" for malformed IDs in backend/src/tools/task_tools.py

**Checkpoint**: `delete_task` returns contract-compliant JSON including deleted task title

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Verification, testing, and cleanup across all tools

- [x] T024 [P] Create unit test file backend/tests/unit/test_mcp_tools.py with test cases for all 5 tools: `add_task`, `list_tasks`, `complete_task`, `update_task`, `delete_task` — test success, error, and edge cases per Spec-5 acceptance scenarios
- [x] T025 [P] Verify all 5 tools enforce user data isolation (FR-003) — no tool can access another user's tasks in backend/src/tools/task_tools.py
- [x] T026 [P] Verify all tools return structured error JSON with `status: "error"` and descriptive `message` for all error paths (FR-004, FR-010) in backend/src/tools/task_tools.py
- [x] T027 Verify `get_task` tool (from Spec 004) still works after changes — not part of Spec-5 but must not be broken in backend/src/tools/task_tools.py
- [x] T028 Run quickstart.md verification checklist against all 5 tools
- [x] T029 Update frontend `handleToolCall` callback in frontend/app/dashboard/page.tsx to recognize `add_task` instead of `create_task` in the `taskMutationTools` array

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2 — P1 priority, MVP
- **US2 (Phase 4)**: Depends on Phase 2 — P1 priority, can run parallel with US1
- **US3 (Phase 5)**: Depends on Phase 2 — P2 priority, can run parallel with US1/US2
- **US4 (Phase 6)**: Depends on Phase 2 — P2 priority, can run parallel with other stories
- **US5 (Phase 7)**: Depends on Phase 2 — P2 priority, can run parallel with other stories
- **Polish (Phase 8)**: Depends on ALL user stories complete

### User Story Dependencies

- **US1 (add_task)**: Independent — rename and validate
- **US2 (list_tasks)**: Independent — verify and align
- **US3 (complete_task)**: Independent — new tool creation
- **US4 (update_task)**: Independent — validate and align
- **US5 (delete_task)**: Independent — verify and align

### Within Each User Story

- Docstring update → Input validation → Response format verification → Import/export updates
- All tasks in a story are sequential (same file: `task_tools.py`)

### Parallel Opportunities

- US1, US2, US3, US4, US5 are independent and could run in parallel (but all modify the same file `task_tools.py`, so sequential execution is recommended)
- T024, T025, T026 in Polish phase can run in parallel (different concerns)

---

## Parallel Example: Polish Phase

```bash
# These can run in parallel (different files/concerns):
Task T024: "Create unit tests in backend/tests/test_mcp_tools.py"
Task T025: "Verify user data isolation in backend/src/tools/task_tools.py"
Task T026: "Verify error responses in backend/src/tools/task_tools.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 — `add_task`)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T004)
3. Complete Phase 3: US1 — `add_task` rename + validation (T005-T009)
4. **STOP and VALIDATE**: Test `add_task` independently via chat endpoint
5. Proceed to remaining stories

### Incremental Delivery

1. Setup + Foundational → Ready
2. US1 (`add_task`) → Test → Core create flow works
3. US2 (`list_tasks`) → Test → Read flow aligned
4. US3 (`complete_task`) → Test → New toggle tool works
5. US4 + US5 → Test → All CRUD operations aligned
6. Polish → All tools tested, frontend updated

---

## Notes

- All user stories modify `backend/src/tools/task_tools.py` — execute sequentially to avoid conflicts
- `get_task` tool from Spec 004 is NOT part of Spec-5 but must not be broken (T027)
- Frontend change (T029) updates the tool name from `create_task` to `add_task` in the task mutation detection
- Total: 29 tasks across 8 phases
- US1: 5 tasks | US2: 3 tasks | US3: 4 tasks | US4: 4 tasks | US5: 3 tasks
