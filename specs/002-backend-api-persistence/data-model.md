# Data Model: Backend API & Data Persistence (Spec 2)

**Feature**: Backend API & Data Persistence (Spec 2)
**Date**: 2026-01-23
**Phase**: Phase 1 - Data Modeling

## Overview

This document defines the data models for the Backend API & Data Persistence feature, focusing on the Task entity with proper relationships and validation rules for user ownership.

## Entity: Task

**Description**: Represents a user's todo task with title, description, completion status, and ownership information

**Fields**:
- `id` (UUID): Unique identifier for the task (Primary Key)
- `title` (String): Title of the task (Required, Max 200 characters)
- `description` (String): Optional detailed description of the task (Optional, Max 1000 characters)
- `completed` (Boolean): Whether the task is completed (Default: False)
- `owner_user_id` (UUID): Foreign key linking to the task owner (Required, References User.id)
- `created_at` (DateTime): Timestamp when task was created (Auto-generated)
- `updated_at` (DateTime): Timestamp when task was last updated (Auto-generated)
- `due_date` (DateTime): Optional deadline for the task (Optional)

**Validation Rules**:
- Title must not be empty
- Title length must be between 1 and 200 characters
- Description length must not exceed 1000 characters
- owner_user_id must reference an existing User record
- Due date cannot be in the past (optional validation)

**Relationships**:
- Many-to-One: A Task belongs to one User (via owner_user_id foreign key)

## Entity: User (Reference)

**Description**: Represents an authenticated user identified by a unique ID extracted from the JWT token

**Fields** (referenced for relationship):
- `id` (UUID): Unique identifier for the user (Primary Key)
- `email` (String): User's email address (Unique, Required)
- `created_at` (DateTime): Timestamp when user account was created
- `updated_at` (DateTime): Timestamp when user record was last updated

**Relationships**:
- One-to-Many: A User has many Tasks

## State Transitions

### Task Completion States
- **Pending**: `completed = False`
- **Completed**: `completed = True`

**Transitions**:
- Pending → Completed: When user marks task as complete
- Completed → Pending: When user unmarks task as complete

## Indexes

**Task Table**:
- Primary Index: `id` (UUID)
- Foreign Key Index: `owner_user_id` (UUID) - critical for user isolation queries
- Regular Index: `created_at` (DateTime)
- Regular Index: `completed` (Boolean) - for filtering completed/pending tasks

## Constraints

### Data Integrity
- Foreign Key Constraint: `task.owner_user_id` must reference existing `user.id`
- Not Null Constraints: All required fields (id, title, owner_user_id)
- Unique Constraint: Not applicable for tasks

### Business Logic
- A task can only be accessed by its owner (enforced by application logic)
- Users cannot access other users' tasks (enforced by JWT validation and owner_user_id matching)

## Sample Data Structure

```python
# Task model example
{
  "id": "f0e9d8c7-b6a5-4321-fedc-ba9876543210",
  "title": "Complete project proposal",
  "description": "Finish the proposal document and submit to manager",
  "completed": False,
  "owner_user_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "created_at": "2026-01-23T10:00:00Z",
  "updated_at": "2026-01-23T10:00:00Z",
  "due_date": "2026-01-30T17:00:00Z"
}
```

## Security Considerations

1. **Data Isolation**: The `owner_user_id` foreign key is critical for enforcing user data isolation
2. **Access Control**: All queries must be filtered by the authenticated user's ID
3. **Audit Trail**: Created/updated timestamps provide basic audit capability

## Future Extensibility

The model supports future enhancements:
- Adding categories/tags to tasks (new Category table with many-to-many relationship)
- Task priorities (new priority field)
- Subtasks (parent_task_id field)
- Sharing capabilities (though not in current scope)