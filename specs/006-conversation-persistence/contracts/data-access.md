# Data Access Contracts: Conversation Persistence

**Feature**: 006-conversation-persistence | **Date**: 2026-02-22

## Overview

This document defines the data access patterns for conversations and messages. These are internal service-layer operations (not REST endpoints) used by the chat service to persist and retrieve conversation data.

---

## Operation 1: Get or Create Conversation

**Purpose**: Retrieve the user's existing conversation, or create one if it doesn't exist.

**Input**: user_id (UUID)

**Behavior**:
1. Query conversation table WHERE user_id = :user_id
2. If found → return existing conversation
3. If not found → create new conversation with user_id, return it

**Output**: Conversation object (id, user_id, created_at, updated_at)

**Performance**: <100ms (SC-002) — uses unique index on user_id

---

## Operation 2: Persist Message

**Purpose**: Store a single message in the conversation.

**Input**: conversation_id (UUID), role (string: "user" | "assistant"), content (string, non-empty)

**Validation**:
- content must not be empty (FR-009)
- role must be "user" or "assistant" (FR-015)

**Output**: Message object (id, conversation_id, role, content, created_at)

**Performance**: Single INSERT, <50ms expected

---

## Operation 3: Load Message History (Full)

**Purpose**: Retrieve recent messages for AI agent context reconstruction.

**Input**: conversation_id (UUID), limit (int, default 50)

**Behavior**:
1. Query messages WHERE conversation_id = :conversation_id
2. ORDER BY created_at DESC (get most recent)
3. LIMIT :limit
4. Reverse result for chronological order

**Output**: List of {role, content} dictionaries

**Performance**: <1s for 50 messages from 500+ (SC-003) — uses composite index on (conversation_id, created_at)

---

## Operation 4: Get Chat History (Paginated)

**Purpose**: Retrieve paginated message history for frontend display.

**Input**: user_id (UUID), limit (int, default 50), offset (int, default 0)

**Behavior**:
1. Find conversation WHERE user_id = :user_id
2. If no conversation → return empty result
3. Count total messages WHERE conversation_id = :conversation_id
4. Query messages WHERE conversation_id = :conversation_id ORDER BY created_at ASC OFFSET :offset LIMIT :limit

**Output**:
```json
{
  "conversation_id": "uuid",
  "messages": [
    {"id": "uuid", "role": "user", "content": "...", "created_at": "ISO8601"},
    {"id": "uuid", "role": "assistant", "content": "...", "created_at": "ISO8601"}
  ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

**Performance**: <1s (SC-003) — uses composite index

---

## Operation 5: Delete Conversation (Cascade)

**Purpose**: Remove a conversation and all its messages.

**Input**: conversation_id (UUID)

**Behavior**:
1. DELETE FROM conversation WHERE id = :conversation_id
2. All associated messages are automatically deleted via CASCADE

**Output**: Confirmation of deletion

**Performance**: Cascade DELETE, <500ms expected for conversation with 500 messages

---

## Index Requirements

| Table | Index | Columns | Type | Purpose |
|-------|-------|---------|------|---------|
| conversation | pk_conversation | id | Primary Key (auto) | Unique lookup |
| conversation | uq_conversation_user_id | user_id | Unique (auto) | Fast user lookup (SC-002) |
| message | pk_message | id | Primary Key (auto) | Unique lookup |
| message | ix_message_conv_created | conversation_id, created_at | Composite B-tree | Fast chronological retrieval (SC-003) |
