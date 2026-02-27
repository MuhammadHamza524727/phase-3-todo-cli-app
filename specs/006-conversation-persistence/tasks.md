# Tasks: Conversation Persistence for AI Chatbot

**Input**: Design documents from `/specs/006-conversation-persistence/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/data-access.md

**Tests**: Not explicitly requested — verification tasks included in Polish phase.

**Organization**: Tasks are grouped by user story. Since Conversation and Message models already exist from Spec 004, tasks focus on aligning the implementation with Spec-6 requirements (indexes, cascade deletion, validation).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Review current state and prepare for alignment changes

- [x] T001 Review current Conversation and Message models in backend/src/models/conversation.py and document current field definitions, constraints, and relationships
- [x] T002 Review current chat_service.py data access patterns in backend/src/services/chat_service.py and verify which Spec-6 operations are already implemented

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No foundational changes needed — models already exist. This phase is a no-op.

**Checkpoint**: Models exist from Spec 004 — user story work can begin

---

## Phase 3: User Story 1 — System Persists Chat Conversations (Priority: P1) 🎯 MVP

**Goal**: Ensure Conversation model has correct constraints: unique user_id, timestamps, proper FK

**Independent Test**: Authenticate a user, trigger a chat, verify conversation record exists with correct user association and timestamps

### Implementation for User Story 1

- [x] T003 [US1] Verify Conversation model has `user_id` with `unique=True` and `nullable=False` constraints in backend/src/models/conversation.py — already present, document confirmation
- [x] T004 [US1] Verify Conversation model has `created_at` and `updated_at` fields with `default_factory=datetime.utcnow` in backend/src/models/conversation.py — already present, document confirmation
- [x] T005 [US1] Verify `_get_or_create_conversation` function in backend/src/services/chat_service.py correctly retrieves existing conversation or creates new one — handles unique constraint

**Checkpoint**: Conversation persistence is confirmed working per Spec-6 FR-001 through FR-004

---

## Phase 4: User Story 2 — System Stores Chat Messages (Priority: P1)

**Goal**: Ensure Message model enforces non-empty content and valid roles, with proper FK to Conversation

**Independent Test**: Send multiple messages, verify each is stored with correct role, content, conversation link, and timestamp

### Implementation for User Story 2

- [x] T006 [US2] Add `min_length=1` validation to Message `content` field in backend/src/models/conversation.py to enforce FR-009 (non-empty content)
- [x] T007 [US2] Add role validation — document that Message `role` field is limited to "user" and "assistant" (FR-015); optionally add a validator or comment in backend/src/models/conversation.py
- [x] T008 [US2] Add `ondelete="CASCADE"` to Message `conversation_id` foreign key field in backend/src/models/conversation.py to enable database-level cascade deletion (FR-011 prerequisite)
- [x] T009 [US2] Verify `_persist_message` function in backend/src/services/chat_service.py correctly creates messages with role, content, and conversation_id

**Checkpoint**: Message storage enforces content validation and role constraints per Spec-6 FR-005 through FR-009

---

## Phase 5: User Story 3 — System Supports Fast Message Retrieval (Priority: P2)

**Goal**: Add composite index on message(conversation_id, created_at) for efficient chronological retrieval

**Independent Test**: Create 100+ messages, retrieve them with pagination, verify query performance and correct ordering

### Implementation for User Story 3

- [x] T010 [US3] Add composite index on `(conversation_id, created_at)` to Message model in backend/src/models/conversation.py using SQLModel `__table_args__` with `Index("ix_message_conv_created", "conversation_id", "created_at")`
- [x] T011 [US3] Verify `_load_message_history` function in backend/src/services/chat_service.py orders messages by `created_at` and uses `limit` parameter for context window loading
- [x] T012 [US3] Verify `get_chat_history` function in backend/src/services/chat_service.py supports `limit` and `offset` parameters for paginated retrieval (FR-010) and orders by `created_at ASC`

**Checkpoint**: Message retrieval is indexed and supports pagination per Spec-6 FR-010, FR-013, SC-003

---

## Phase 6: User Story 4 — Cascade Deletion (Priority: P2)

**Goal**: Configure cascade deletion so removing a conversation automatically removes all its messages

**Independent Test**: Create a conversation with messages, delete the conversation, verify all messages are gone

### Implementation for User Story 4

- [x] T013 [US4] Update Conversation `messages` relationship in backend/src/models/conversation.py to include `cascade_delete=True` (SQLModel) or `sa_relationship_kwargs={"cascade": "all, delete-orphan"}` for ORM-level cascade
- [x] T014 [US4] Verify that the combination of DB-level `ondelete="CASCADE"` (T008) and ORM-level cascade (T013) ensures complete message cleanup when a conversation is deleted

**Checkpoint**: Cascade deletion works at both DB and ORM level per Spec-6 FR-011, SC-005

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Verification, testing, and compatibility checks

- [x] T015 [P] Create unit test file backend/tests/unit/test_conversation_model.py with tests for: content min_length validation, role validation, cascade deletion behavior, unique user_id constraint
- [x] T016 [P] Verify all conversation operations in backend/src/services/chat_service.py are scoped to authenticated user — no cross-user access (SC-004)
- [x] T017 [P] Verify existing User model in backend/src/models/user.py is unchanged — no regressions from Spec-6 changes (FR-014)
- [x] T018 [P] Verify existing Task model in backend/src/models/task.py is unchanged — no regressions from Spec-6 changes (FR-014)
- [x] T019 Run quickstart.md verification checklist against conversation and message models

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: N/A — no foundational work needed
- **US1 (Phase 3)**: Depends on Phase 1 — verification only
- **US2 (Phase 4)**: Depends on Phase 1 — model modifications
- **US3 (Phase 5)**: Depends on US2 (index added to same file)
- **US4 (Phase 6)**: Depends on US2 (T008 provides DB-level cascade)
- **Polish (Phase 7)**: Depends on ALL user stories complete

### User Story Dependencies

- **US1 (Conversations)**: Independent — verification only
- **US2 (Messages)**: Independent — model modifications
- **US3 (Fast Retrieval)**: Depends on US2 (same file modifications)
- **US4 (Cascade Deletion)**: Depends on US2 (T008 adds ondelete)

### Within Each User Story

- All tasks in US1 are verification (sequential, same file)
- US2 tasks are sequential (same file: `conversation.py`)
- US3 tasks: index first, then service verification
- US4 tasks: relationship update depends on T008

### Parallel Opportunities

- US1 and US2 can run in parallel (US1 is verification-only, US2 modifies different aspects)
- T015, T016, T017, T018 in Polish phase can run in parallel (different files/concerns)

---

## Parallel Example: Polish Phase

```bash
# These can run in parallel (different files/concerns):
Task T015: "Create unit tests in backend/tests/unit/test_conversation_model.py"
Task T016: "Verify user scoping in backend/src/services/chat_service.py"
Task T017: "Verify User model unchanged in backend/src/models/user.py"
Task T018: "Verify Task model unchanged in backend/src/models/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 3: US1 — verify conversation persistence (T003-T005)
3. Complete Phase 4: US2 — add content/role validation + cascade FK (T006-T009)
4. **STOP and VALIDATE**: Test message creation and validation
5. Proceed to US3 + US4 for performance and cascade

### Incremental Delivery

1. Setup → Verify current state
2. US1 (Conversations) → Confirm persistence works
3. US2 (Messages) → Add validation + cascade FK → Core data integrity
4. US3 (Fast Retrieval) → Add composite index → Performance
5. US4 (Cascade Deletion) → Add ORM cascade → Data integrity
6. Polish → Tests, verification, compatibility checks

---

## Notes

- Most tasks modify `backend/src/models/conversation.py` — execute sequentially to avoid conflicts
- US1 is purely verification (no code changes expected) — confirms existing implementation
- The main code changes are in US2 (validation, cascade FK) and US3 (index) and US4 (relationship cascade)
- Total: 19 tasks across 7 phases
- US1: 3 tasks | US2: 4 tasks | US3: 3 tasks | US4: 2 tasks | Polish: 5 tasks
