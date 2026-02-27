# Quickstart: Conversation Persistence

**Feature**: 006-conversation-persistence | **Date**: 2026-02-22

## Prerequisites

- Python 3.11+
- Backend dependencies installed: `pip install -r backend/requirements.txt`
- Environment variables configured in `backend/.env`:
  - `DATABASE_URL` — Neon PostgreSQL connection string
  - `SECRET_KEY` — JWT signing secret

## File Structure

```text
backend/src/models/
└── conversation.py      # Conversation + Message SQLModel models
```

## Verification Checklist

### Schema Verification

- [ ] Conversation table exists with columns: id (UUID PK), user_id (UUID FK UNIQUE), created_at, updated_at
- [ ] Message table exists with columns: id (UUID PK), conversation_id (UUID FK), role (varchar 20), content (text), created_at
- [ ] Unique constraint on conversation.user_id enforced
- [ ] Foreign key from message.conversation_id → conversation.id with ON DELETE CASCADE
- [ ] Composite index on message(conversation_id, created_at) exists

### Data Integrity Verification

- [ ] Creating two conversations for the same user fails (unique violation)
- [ ] Creating a message with empty content fails (validation error)
- [ ] Creating a message with role other than "user"/"assistant" is caught by validation
- [ ] Deleting a conversation automatically deletes all associated messages
- [ ] Deleting user A's conversation does not affect user B's data

### Query Performance Verification

- [ ] Looking up a conversation by user_id uses the unique index (EXPLAIN shows Index Scan)
- [ ] Retrieving messages ordered by created_at uses the composite index (EXPLAIN shows Index Scan)
- [ ] Paginated query with OFFSET/LIMIT returns correct subset of messages

### Integration Verification

- [ ] Chat endpoint creates conversation on first message
- [ ] Chat endpoint retrieves existing conversation on subsequent messages
- [ ] Chat history endpoint returns paginated messages in chronological order
- [ ] All conversation operations are scoped to the authenticated user

## Manual Testing via SQL

```sql
-- Verify indexes exist
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'message';
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'conversation';

-- Verify cascade deletion
-- 1. Create test conversation and messages
-- 2. DELETE FROM conversation WHERE id = '<test_id>';
-- 3. SELECT count(*) FROM message WHERE conversation_id = '<test_id>'; -- should be 0

-- Verify unique constraint
-- 1. INSERT INTO conversation (id, user_id) VALUES (gen_random_uuid(), '<user_id>');
-- 2. INSERT INTO conversation (id, user_id) VALUES (gen_random_uuid(), '<user_id>'); -- should fail
```
