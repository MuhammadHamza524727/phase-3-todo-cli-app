# Data Model: AI Chatbot for Natural Language Task Management

**Feature**: 004-ai-chatbot | **Date**: 2026-02-21

## New Entities

### Conversation

Represents a chat session between a user and the AI assistant.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique conversation identifier |
| user_id | UUID | FK → User.id, UNIQUE | Owner of the conversation (one per user) |
| created_at | datetime | auto-set UTC | When conversation was started |
| updated_at | datetime | auto-set UTC | Last message timestamp |

**Relationships**:
- Belongs to one User (via user_id)
- Has many Messages (via conversation_id)

**Validation Rules**:
- user_id must reference an existing, active user
- Only one conversation per user (UNIQUE constraint on user_id)

### Message

Represents a single turn in a conversation (user input or assistant response).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique message identifier |
| conversation_id | UUID | FK → Conversation.id | Parent conversation |
| role | string | enum: "user", "assistant" | Who sent this message |
| content | text | required, non-empty | Message content |
| created_at | datetime | auto-set UTC | When message was sent |

**Relationships**:
- Belongs to one Conversation (via conversation_id)

**Validation Rules**:
- role must be either "user" or "assistant"
- content must not be empty
- Messages are ordered by created_at ASC within a conversation

## Existing Entities (Referenced, Not Modified)

### User (from Spec 002)

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | PK |
| email | string | Unique identifier |
| name | string | Display name |
| password_hash | string | Bcrypt hashed password |
| is_active | bool | Account status |
| created_at | datetime | Registration date |
| updated_at | datetime | Last update |

### Task (from Spec 002)

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | PK |
| title | string | Task title (1-200 chars) |
| description | string? | Optional description (max 1000 chars) |
| completed | bool | Completion status |
| owner_user_id | UUID | FK → User.id |
| due_date | datetime? | Optional due date |
| created_at | datetime | Creation date |
| updated_at | datetime | Last update |

## Entity Relationship Diagram

```
┌──────────┐     1:1      ┌──────────────┐     1:N      ┌──────────┐
│   User   │─────────────▶│ Conversation │─────────────▶│ Message  │
│          │              │              │              │          │
│ id (PK)  │              │ id (PK)      │              │ id (PK)  │
│ email    │              │ user_id (FK) │              │ conv_id  │
│ name     │              │ created_at   │              │ role     │
│ ...      │              │ updated_at   │              │ content  │
└──────────┘              └──────────────┘              │ created  │
     │                                                  └──────────┘
     │  1:N
     ▼
┌──────────┐
│   Task   │
│          │
│ id (PK)  │
│ title    │
│ ...      │
│ owner_id │
└──────────┘
```

## State Transitions

### Conversation Lifecycle

```
[No Conversation] → First message → [Active Conversation]
[Active Conversation] → New message → [Active Conversation] (updated_at refreshed)
```

No delete or archive states in initial implementation.

### Message Lifecycle

Messages are immutable once created. No update or delete operations.

```
[Created] → Persisted → [Permanent]
```
