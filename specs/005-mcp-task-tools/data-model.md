# Data Model: MCP Server Tools for Task Management

**Feature**: 005-mcp-task-tools | **Date**: 2026-02-22

## Overview

No new entities are introduced by this feature. All MCP tools operate on the existing Task entity defined in Spec 002 (Backend API & Data Persistence). This document serves as a reference to the existing data model.

## Existing Entities (Reference)

### Task (Spec 002)

**Table**: `task`
**File**: `backend/src/models/task.py`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique task identifier |
| title | string | 1-200 chars, required | Task title |
| description | string | max 1000 chars, optional | Task description |
| completed | boolean | default: false | Completion status |
| owner_user_id | UUID | FK → user.id, required | Task owner (data isolation) |
| due_date | datetime | optional | Task due date |
| created_at | datetime | auto-generated | Creation timestamp |
| updated_at | datetime | auto-generated | Last update timestamp |

### Relationships

- `Task.owner_user_id` → `User.id` (many-to-one)
- All tool operations filter by `owner_user_id` to enforce user data isolation

## Tool-to-Entity Mapping

| MCP Tool | Operation | Fields Used |
|----------|-----------|-------------|
| `add_task` | INSERT | title (required), description (optional) → auto-sets completed=false, owner_user_id from context |
| `list_tasks` | SELECT | id, title, completed, description; optional filter on completed |
| `complete_task` | UPDATE | completed (toggle true↔false), updated_at |
| `update_task` | UPDATE | title (optional), description (optional), completed (optional), updated_at |
| `delete_task` | DELETE | Identified by id; validated by owner_user_id |

## User Context (Injected)

The `UserContext` class carries authenticated user identity into each tool:

| Field | Type | Source |
|-------|------|--------|
| user_id | UUID | Extracted from JWT by chat service |
| session | AsyncSession | Database session from connection pool |

UserContext is NOT a database entity — it is a runtime context object injected via `RunContextWrapper[UserContext]`.

## Schema Changes

**None required.** FR-013 and SC-010 explicitly state no new tables or schema changes.
