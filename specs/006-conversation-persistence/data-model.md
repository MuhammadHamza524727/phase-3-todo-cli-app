# Data Model: Conversation Persistence for AI Chatbot

**Feature**: 006-conversation-persistence | **Date**: 2026-02-22

## Overview

Two entities are formalized by this feature: Conversation and Message. Both already exist in `backend/src/models/conversation.py` from Spec 004. This document specifies the complete schema including indexes and constraints that need to be added.

## Entities

### Conversation

**Table**: `conversation`
**File**: `backend/src/models/conversation.py`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique conversation identifier |
| user_id | UUID | FK → user.id, UNIQUE, NOT NULL | Conversation owner (one per user) |
| created_at | datetime | auto-generated | When the conversation was created |
| updated_at | datetime | auto-generated | When the conversation was last active |

**Relationships**:
- `messages`: One-to-many → Message (cascade delete)
- `user_id` → `user.id` (many-to-one, implicit)

**Indexes**:
- PK index on `id` (automatic)
- Unique index on `user_id` (automatic from UNIQUE constraint)

**Constraints**:
- One conversation per user (UNIQUE on user_id)
- Cascade delete: deleting a conversation deletes all its messages

### Message

**Table**: `message`
**File**: `backend/src/models/conversation.py`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique message identifier |
| conversation_id | UUID | FK → conversation.id, NOT NULL, ON DELETE CASCADE | Parent conversation |
| role | string | NOT NULL, max 20 chars | Message sender: "user" or "assistant" |
| content | string(text) | NOT NULL, min 1 char | Message text content |
| created_at | datetime | auto-generated | When the message was sent |

**Relationships**:
- `conversation`: Many-to-one → Conversation

**Indexes**:
- PK index on `id` (automatic)
- Composite index on `(conversation_id, created_at)` — NEW, needed for FR-013/SC-003

**Constraints**:
- Foreign key to conversation with ON DELETE CASCADE
- Role limited to valid values ("user", "assistant")
- Content must not be empty (min_length=1)

### MessageRead (Read Schema)

**Purpose**: Read-only schema for API responses

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Message identifier |
| role | string | Message sender |
| content | string | Message text |
| created_at | datetime | Timestamp |

## Existing Entities (Reference)

### User (Spec 002)

**Table**: `user`
**Relationship**: Conversation.user_id → User.id

### Task (Spec 002)

**Table**: `task`
**Relationship**: No direct relationship to conversations or messages. Tasks are accessed via MCP tools during chat interactions.

## Entity Relationship Diagram (Text)

```
User (1) ──── (1) Conversation (1) ──── (N) Message
  │
  │
  └──── (N) Task (accessed via MCP tools, not via conversation)
```

## Changes Required

| Current State | Required Change | Spec Reference |
|---------------|-----------------|----------------|
| No composite index on message | Add index on (conversation_id, created_at) | FR-013, SC-003 |
| No cascade delete configured in ORM | Add cascade="all, delete-orphan" to relationship | FR-011 |
| No ON DELETE CASCADE on FK | Add ondelete="CASCADE" to conversation_id FK | FR-011 |
| No content min_length | Add min_length=1 to content field | FR-009 |
| Role not explicitly validated | Document valid values; optionally add validation | FR-015 |
