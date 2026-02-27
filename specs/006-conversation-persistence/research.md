# Research: Conversation Persistence for AI Chatbot

**Feature**: 006-conversation-persistence | **Date**: 2026-02-22

## Research Context

The Conversation and Message models were implemented in Spec 004 (AI Chatbot). Spec 006 formalizes the persistence requirements. This research focuses on gaps between the current implementation and the spec.

---

## Decision 1: Database Index Strategy

**Decision**: Add index on `conversation.user_id` and composite index on `message(conversation_id, created_at)`

**Rationale**: SC-002 requires conversation lookup by user in <100ms. SC-003 requires retrieving 50 messages from 500+ in <1s. Without indexes, these queries do full table scans which degrade as data grows.

**Alternatives considered**:
- No indexes (rely on FK-based implicit index) → Rejected: PostgreSQL does NOT auto-create indexes on FK columns; only PK and UNIQUE columns get auto-indexes. `conversation.user_id` has a unique constraint so it's already indexed. But `message.conversation_id` has no index.
- Single-column index on `message.conversation_id` only → Rejected: A composite index on (conversation_id, created_at) serves both the filter and the sort, making chronological message retrieval a single index scan.

**Note**: `conversation.user_id` already has a unique constraint which implicitly creates an index. No additional index needed there.

---

## Decision 2: Cascade Deletion Strategy

**Decision**: Configure SQLAlchemy relationship with `cascade="all, delete-orphan"` and database-level `ON DELETE CASCADE`

**Rationale**: FR-011 requires that when a conversation is deleted, all messages are automatically removed. Using both ORM-level and database-level cascade ensures data integrity regardless of how the deletion occurs (via ORM or raw SQL).

**Alternatives considered**:
- ORM-level only → Risky: If deletion happens via raw SQL or admin tool, messages would be orphaned
- Database-level only → Acceptable but ORM wouldn't know about cascades for session management
- Both levels → Chosen: Belt-and-suspenders approach for data integrity

---

## Decision 3: Role Validation

**Decision**: Keep string field with max_length=20 and add application-level validation in the chat service

**Rationale**: FR-015 requires roles limited to "user" and "assistant". The current implementation uses `max_length=20` which prevents arbitrary long strings but doesn't enforce specific values. Adding a database CHECK constraint would be the most robust approach, but SQLModel doesn't natively support CHECK constraints without raw SQL.

**Alternatives considered**:
- Python Enum type → Would require migration; SQLModel/SQLAlchemy handles Enum types but adds complexity
- Database CHECK constraint → Most robust but requires raw SQL migration
- Application-level validation only → Chosen: The chat service already only writes "user" and "assistant" roles; adding explicit validation in the model is a reasonable safeguard

---

## Decision 4: Content Non-Empty Validation

**Decision**: Add `min_length=1` to Message content field

**Rationale**: FR-009 requires non-empty content. The current implementation has `nullable=False` but no minimum length check. Adding `min_length=1` at the model level prevents empty strings.

**Alternatives considered**:
- Database-level NOT NULL + CHECK(length > 0) → More robust but requires raw SQL
- Application-level only → Already partially done (chat endpoint validates non-empty messages)
- Model-level min_length → Chosen: SQLModel/Pydantic validation catches empty strings before they reach the DB

---

## Decision 5: Pagination Verification

**Decision**: Existing pagination in chat_service.py is already compliant with FR-010

**Rationale**: The `get_chat_history()` function already accepts `limit` and `offset` parameters and uses them in the query. The `_load_message_history()` function uses `limit` for context window. Both return messages in chronological order.

**No changes needed** — just document and verify.
