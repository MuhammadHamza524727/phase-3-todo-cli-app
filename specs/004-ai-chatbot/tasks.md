# Tasks: AI Chatbot for Natural Language Task Management

**Input**: Design documents from `/specs/004-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/chat-api.md

**Tests**: Not explicitly requested. Test tasks are omitted.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add dependencies and environment configuration for AI chatbot feature

- [x] T001 Add `openai-agents` dependency to `backend/requirements.txt`
- [x] T002 [P] Add `OPENAI_API_KEY` placeholder to `backend/.env.example` and document in `backend/.env`
- [x] T003 [P] Create `backend/src/tools/` directory with `__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database models, response schemas, and MCP tools that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create Conversation and Message SQLModel models in `backend/src/models/conversation.py` per data-model.md (Conversation: id UUID PK, user_id UUID FK→User unique, created_at, updated_at; Message: id UUID PK, conversation_id UUID FK→Conversation, role enum user/assistant, content text, created_at)
- [x] T005 [P] Add ChatRequest and ChatResponse Pydantic schemas to `backend/src/models/base_response.py` (ChatRequest: message str 1-2000 chars; ChatResponse: success bool, data with response str, conversation_id UUID, tool_calls list)
- [x] T006 [P] Add ChatMessage, ChatResponse, and ToolCall TypeScript interfaces to `frontend/types/index.ts` (ChatMessage: id, role, content, created_at; ChatResponse: response, conversation_id, tool_calls; ToolCall: tool, arguments, result)
- [x] T007 Implement `create_task` MCP tool function in `backend/src/tools/task_tools.py` using `@function_tool` decorator — accepts title and optional description, creates task via SQLModel query scoped to context user_id, returns confirmation string with task title
- [x] T008 Implement `list_tasks` MCP tool function in `backend/src/tools/task_tools.py` — accepts optional completed filter, queries tasks scoped to context user_id, returns formatted task list string
- [x] T009 Implement `get_task` MCP tool function in `backend/src/tools/task_tools.py` — accepts task_id, queries single task scoped to context user_id, returns task details or "not found" error
- [x] T010 Implement `update_task` MCP tool function in `backend/src/tools/task_tools.py` — accepts task_id and optional title/description/completed fields, updates task scoped to context user_id, returns confirmation string
- [x] T011 Implement `delete_task` MCP tool function in `backend/src/tools/task_tools.py` — accepts task_id, deletes task scoped to context user_id, returns confirmation string with deleted task title
- [x] T012 Implement `chat_service.py` in `backend/src/services/chat_service.py` — create `process_chat_message(user_id, message, db_session)` function that: loads/creates conversation from DB, loads message history, creates OpenAI Agent with task tools and system instructions, runs agent with conversation context, persists user message and assistant response to DB, returns ChatResponse with response text, conversation_id, and tool_calls
- [x] T013 Create chat API router in `backend/src/api/chat.py` with two endpoints: POST `/api/chat` (accepts ChatRequest body, requires JWT via get_current_user dependency, calls chat_service.process_chat_message, returns ChatResponse) and GET `/api/chat/history` (requires JWT, accepts limit/offset query params, returns paginated message history for user's conversation)
- [x] T014 Register chat router in `backend/main.py` — import chat_router from `src.api.chat` and include with prefix="/api"

**Checkpoint**: Backend chat infrastructure ready — all MCP tools defined, agent service wired, endpoints live. Frontend types defined.

---

## Phase 3: User Story 1 — Natural Language Task Creation (Priority: P1) MVP

**Goal**: User sends "Add a task to buy groceries" in chat and receives confirmation with task details

**Independent Test**: Send a create-task message via the chat interface, verify task appears in task list and confirmation message displayed

### Implementation for User Story 1

- [x] T015 [P] [US1] Create chat API service in `frontend/services/chat.ts` — implement `sendMessage(message: string): Promise<ChatResponse>` using existing apiClient with POST to `/api/chat`, and `getChatHistory(limit?, offset?): Promise<ChatMessage[]>` with GET to `/api/chat/history`
- [x] T016 [P] [US1] Create ChatMessage component in `frontend/components/chat/ChatMessage.tsx` — renders a single message bubble with role-based styling (user messages right-aligned purple, assistant messages left-aligned white/gray), displays content text and timestamp, uses existing Tailwind design system (glass morphism, purple theme)
- [x] T017 [P] [US1] Create ChatInput component in `frontend/components/chat/ChatInput.tsx` — text input with send button, loading state (disable input + show spinner while waiting for response), handles Enter key to send, validates non-empty message before sending
- [x] T018 [US1] Create ChatInterface component in `frontend/components/chat/ChatInterface.tsx` — container with scrollable message list and ChatInput at bottom, manages messages state array, calls sendMessage from chat service on submit, appends user message immediately and assistant response on completion, shows loading indicator while waiting, auto-scrolls to latest message
- [x] T019 [US1] Integrate chat panel into dashboard page in `frontend/app/dashboard/page.tsx` — add a toggle button (chat icon) to show/hide a collapsible side panel containing ChatInterface, desktop: side panel (right side, ~400px width), mobile: full-screen overlay, panel visible state managed via useState

**Checkpoint**: User can open chat on dashboard, type "Add a task to buy groceries", see confirmation, and verify task in task list.

---

## Phase 4: User Story 2 — Listing and Querying Tasks (Priority: P1)

**Goal**: User sends "Show my tasks" and sees a formatted list of their tasks in the chat

**Independent Test**: Create several tasks via UI, then ask chatbot "Show my tasks" and verify all tasks are listed with titles and statuses

### Implementation for User Story 2

- [x] T020 [US2] Verify `list_tasks` tool in `backend/src/tools/task_tools.py` formats output as readable numbered list with title and completion status (e.g., "1. Buy groceries (pending)\n2. Review PR (completed)") — update format if needed
- [x] T021 [US2] Verify agent system instructions in `backend/src/services/chat_service.py` include guidance for list intents — agent should call list_tasks tool when user asks "Show my tasks", "List all tasks", "What are my tasks?", and format empty results as "You don't have any tasks yet. Try saying 'Add a task to...'"

**Checkpoint**: User can ask "Show my tasks" / "List completed tasks" and see formatted results.

---

## Phase 5: User Story 3 — Completing and Updating Tasks (Priority: P2)

**Goal**: User sends "Mark buy groceries as done" or "Update task title" and receives confirmation

**Independent Test**: Create a task, ask chatbot to mark it complete, verify status change in task list and confirmation in chat

### Implementation for User Story 3

- [x] T022 [US3] Verify `update_task` tool in `backend/src/tools/task_tools.py` handles title updates and returns confirmation with old and new values — update confirmation format if needed
- [x] T023 [US3] Verify agent system instructions in `backend/src/services/chat_service.py` handle ambiguous task references — when user says "Complete the task" but multiple tasks exist, agent should call list_tasks first and ask user to clarify which task they mean
- [x] T024 [US3] Verify `get_task` and `update_task` tools return clear "Task not found" error string when task_id doesn't exist or doesn't belong to user — agent should relay this as a user-friendly message

**Checkpoint**: User can complete, update tasks via chat with confirmation. Ambiguous references prompt clarification.

---

## Phase 6: User Story 4 — Deleting Tasks (Priority: P2)

**Goal**: User sends "Delete the task 'Old task'" and receives confirmation with deleted task title

**Independent Test**: Create a task, ask chatbot to delete it, verify task removed from list and confirmation shows specific task name

### Implementation for User Story 4

- [x] T025 [US4] Verify `delete_task` tool in `backend/src/tools/task_tools.py` returns confirmation string including the deleted task's title (not just "task deleted") — update if needed
- [x] T026 [US4] Verify agent system instructions in `backend/src/services/chat_service.py` handle delete intents — agent should identify task by name/description from user message, call list_tasks if needed to find matching task, then call delete_task with correct task_id

**Checkpoint**: User can delete tasks via chat with specific confirmation. Non-existent task references show clear error.

---

## Phase 7: User Story 5 — Conversation Persistence Across Sessions (Priority: P3)

**Goal**: User returns to chat and sees previous conversation history loaded from database

**Independent Test**: Have a conversation, refresh page, verify previous messages are displayed in order

### Implementation for User Story 5

- [x] T027 [US5] Load conversation history on chat mount in `frontend/components/chat/ChatInterface.tsx` — call getChatHistory() from chat service in useEffect on component mount, populate messages state with loaded history, show loading spinner while fetching, handle empty history (first-time user)
- [x] T028 [US5] Verify GET `/api/chat/history` endpoint in `backend/src/api/chat.py` returns messages in chronological order (created_at ASC) with correct pagination (limit/offset), returns 200 with empty messages array if no conversation exists

**Checkpoint**: User can close browser, return to dashboard, and see previous chat history loaded.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, edge cases, and UX improvements across all stories

- [x] T029 [P] Add error handling in `frontend/components/chat/ChatInterface.tsx` — handle network errors (show "Failed to send message. Please try again." with retry option), handle 401 responses (redirect to login via auth context), handle 500 responses (show "Chatbot temporarily unavailable")
- [x] T030 [P] Add empty message validation in `frontend/components/chat/ChatInput.tsx` — prevent sending empty or whitespace-only messages, trim message before sending
- [x] T031 [P] Add non-task message handling in agent system instructions in `backend/src/services/chat_service.py` — agent should respond to greetings conversationally and redirect unrelated questions (e.g., "What's the weather?") with "I can help you manage your tasks! Try saying 'show my tasks' or 'add a task to...'"
- [x] T032 Handle JWT expiration during chat session in `frontend/components/chat/ChatInterface.tsx` — detect 401 from chat API, clear messages state, show "Session expired" message, redirect to login page
- [x] T033 Add CORS configuration for chat endpoints in `backend/main.py` — verify existing CORS middleware covers the new `/api/chat` and `/api/chat/history` routes (should work automatically since CORS is configured at app level)
- [x] T034 Refresh task list after chat operations in `frontend/app/dashboard/page.tsx` — when chat panel is open and a tool_call is returned in the chat response (create_task, update_task, delete_task), trigger a re-fetch of the task list to keep dashboard in sync

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Phase 2 — delivers MVP
- **User Story 2 (Phase 4)**: Depends on Phase 2 — can run in parallel with US1
- **User Story 3 (Phase 5)**: Depends on Phase 2 — can run in parallel with US1/US2
- **User Story 4 (Phase 6)**: Depends on Phase 2 — can run in parallel with US1/US2/US3
- **User Story 5 (Phase 7)**: Depends on Phase 3 (needs ChatInterface component)
- **Polish (Phase 8)**: Depends on Phase 3 minimum

### User Story Dependencies

- **US1 (Task Creation)**: After Foundational — builds ChatInterface, ChatMessage, ChatInput, chat service, dashboard integration
- **US2 (List Tasks)**: After Foundational — only needs tool formatting and agent instruction verification
- **US3 (Complete/Update)**: After Foundational — only needs tool verification and agent instruction tuning
- **US4 (Delete Tasks)**: After Foundational — only needs tool verification and agent instruction tuning
- **US5 (Conversation Persistence)**: After US1 — needs ChatInterface component to add history loading

### Within Phase 2 (Foundational)

```
T004 (models) ──┐
T005 (schemas)  ─┤──→ T007-T011 (tools, depend on models) ──→ T012 (chat service, depends on tools) ──→ T013 (router) ──→ T014 (register)
T006 (FE types) ─┘
```

### Parallel Opportunities

- T001, T002, T003 — all setup tasks in parallel
- T004, T005, T006 — models and types in parallel (different files, different codebases)
- T007, T008, T009, T010, T011 — all 5 tool functions can be written in parallel (same file but independent functions)
- T015, T016, T17 — frontend service and UI components in parallel (different files)
- T020/T021, T022/T023/T024, T025/T026 — US2, US3, US4 can all proceed in parallel after foundational
- T029, T030, T031 — polish tasks in parallel (different files)

---

## Parallel Example: Foundational Phase

```bash
# Batch 1 — Models and types (parallel):
Task T004: "Create Conversation + Message models in backend/src/models/conversation.py"
Task T005: "Add ChatRequest/ChatResponse schemas in backend/src/models/base_response.py"
Task T006: "Add chat TypeScript interfaces in frontend/types/index.ts"

# Batch 2 — Tools (sequential after models, but tools can be parallel with each other):
Task T007: "Implement create_task tool in backend/src/tools/task_tools.py"
Task T008: "Implement list_tasks tool in backend/src/tools/task_tools.py"
Task T009: "Implement get_task tool in backend/src/tools/task_tools.py"
Task T010: "Implement update_task tool in backend/src/tools/task_tools.py"
Task T011: "Implement delete_task tool in backend/src/tools/task_tools.py"

# Batch 3 — Service (after tools):
Task T012: "Implement chat_service.py in backend/src/services/chat_service.py"

# Batch 4 — Router + registration (sequential):
Task T013: "Create chat router in backend/src/api/chat.py"
Task T014: "Register chat router in backend/main.py"
```

## Parallel Example: User Story 1

```bash
# Batch 1 — Frontend components (parallel):
Task T015: "Create chat API service in frontend/services/chat.ts"
Task T016: "Create ChatMessage component in frontend/components/chat/ChatMessage.tsx"
Task T017: "Create ChatInput component in frontend/components/chat/ChatInput.tsx"

# Batch 2 — Integration (after batch 1):
Task T018: "Create ChatInterface container in frontend/components/chat/ChatInterface.tsx"

# Batch 3 — Dashboard integration (after batch 2):
Task T019: "Integrate chat panel into frontend/app/dashboard/page.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T014)
3. Complete Phase 3: User Story 1 (T015-T019)
4. **STOP and VALIDATE**: Send "Add a task to buy groceries" in chat, verify task created and confirmation shown
5. Deploy/demo if ready — chatbot creates tasks via natural language

### Incremental Delivery

1. Setup + Foundational → Backend chat infrastructure live
2. Add US1 (Create) → MVP! User can create tasks via chat
3. Add US2 (List) → User can also view tasks via chat
4. Add US3 (Complete/Update) → Full task lifecycle via chat
5. Add US4 (Delete) → Complete CRUD via chat
6. Add US5 (Persistence) → Conversation survives browser refresh
7. Polish → Error handling, edge cases, task list sync

---

## Notes

- All backend tools operate on the same file (`task_tools.py`) but are independent functions
- Chat service is the heaviest task (T012) — it orchestrates agent creation, conversation management, and message persistence
- Frontend chat components are lightweight (~40-100 lines each) using existing Tailwind design system
- US2-US4 are primarily verification/tuning tasks — the core logic is built in the foundational tools and chat service
- Task list sync (T034) is critical UX — without it, users won't see tasks created via chat until they refresh
