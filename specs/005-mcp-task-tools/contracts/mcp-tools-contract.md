# MCP Tool Contracts: Task Management

**Feature**: 005-mcp-task-tools | **Date**: 2026-02-22

## Overview

This document defines the exact Input/Output JSON contracts for all 5 MCP tools. Each tool is an async Python function decorated with `@function_tool` from the OpenAI Agents SDK. All tools receive a `RunContextWrapper[UserContext]` as the first parameter (injected by the framework, not by the AI agent).

---

## Tool 1: `add_task`

**Purpose**: Create a new task for the authenticated user.

**Docstring**: "Add a new task to your task list. Use this when the user wants to create, add, or make a new task or todo item. Requires a title (1-200 characters). Optionally accepts a description (up to 1000 characters)."

### Input Parameters

| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| title | string | Yes | 1-200 characters | Task title |
| description | string | No | Max 1000 characters, default "" | Task description |

### Output: Success

```json
{
  "status": "success",
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "Buy groceries",
  "message": "Task 'Buy groceries' created successfully."
}
```

### Output: Error (validation)

```json
{
  "status": "error",
  "message": "Title is required and must be between 1 and 200 characters."
}
```

---

## Tool 2: `list_tasks`

**Purpose**: List the authenticated user's tasks with optional status filter.

**Docstring**: "List all tasks in your task list. Use this when the user wants to see, view, or check their tasks. Optionally filter by completion status: set completed=true for completed tasks, completed=false for pending tasks, or omit for all tasks."

### Input Parameters

| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| completed | boolean | No | true/false/omit | Filter by completion status |

### Output: Success (with tasks)

```json
{
  "status": "success",
  "count": 3,
  "tasks": [
    {
      "index": 1,
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "title": "Buy groceries",
      "status": "pending",
      "description": "Milk, eggs, bread"
    },
    {
      "index": 2,
      "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "title": "Clean house",
      "status": "completed",
      "description": ""
    },
    {
      "index": 3,
      "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
      "title": "Read book",
      "status": "pending",
      "description": ""
    }
  ]
}
```

### Output: Empty

```json
{
  "status": "empty",
  "count": 0,
  "message": "You don't have any tasks yet. Try saying 'Add a task to...'"
}
```

---

## Tool 3: `complete_task`

**Purpose**: Toggle a task's completion status (pending ↔ completed).

**Docstring**: "Mark a task as completed or toggle it back to pending. Use this when the user says they finished, completed, or done with a task, or when they want to un-complete a task. Requires the task ID."

### Input Parameters

| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| task_id | string | Yes | Valid UUID format | ID of the task to toggle |

### Output: Success

```json
{
  "status": "success",
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "Buy groceries",
  "completed": true,
  "message": "Task 'Buy groceries' marked as completed."
}
```

### Output: Success (toggled back to pending)

```json
{
  "status": "success",
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "Buy groceries",
  "completed": false,
  "message": "Task 'Buy groceries' marked as pending."
}
```

### Output: Error (not found)

```json
{
  "status": "error",
  "message": "Task not found."
}
```

### Output: Error (invalid ID)

```json
{
  "status": "error",
  "message": "Invalid task ID: not-a-uuid"
}
```

---

## Tool 4: `update_task`

**Purpose**: Update one or more fields of an existing task.

**Docstring**: "Update an existing task's details. Use this when the user wants to change, modify, rename, or edit a task. You can update the title, description, or completion status. Requires the task ID and at least one field to change."

### Input Parameters

| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| task_id | string | Yes | Valid UUID format | ID of the task to update |
| title | string | No | 1-200 characters | New title |
| description | string | No | Max 1000 characters | New description |
| completed | boolean | No | true/false | New completion status |

### Output: Success

```json
{
  "status": "success",
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "Buy organic groceries",
  "changes": [
    "title changed from 'Buy groceries' to 'Buy organic groceries'",
    "description updated"
  ],
  "message": "Task 'Buy organic groceries' updated: title changed from 'Buy groceries' to 'Buy organic groceries', description updated."
}
```

### Output: Success (no changes)

```json
{
  "status": "success",
  "message": "No changes were needed.",
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### Output: Error (not found)

```json
{
  "status": "error",
  "message": "Task not found."
}
```

---

## Tool 5: `delete_task`

**Purpose**: Permanently remove a task.

**Docstring**: "Delete a task from your task list. Use this when the user wants to remove, delete, or get rid of a task. This action is permanent. Requires the task ID."

### Input Parameters

| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| task_id | string | Yes | Valid UUID format | ID of the task to delete |

### Output: Success

```json
{
  "status": "success",
  "deleted_title": "Buy groceries",
  "message": "Task 'Buy groceries' has been deleted."
}
```

### Output: Error (not found)

```json
{
  "status": "error",
  "message": "Task not found."
}
```

### Output: Error (invalid ID)

```json
{
  "status": "error",
  "message": "Invalid task ID: not-a-uuid"
}
```

---

## Common Error Patterns

All tools return errors in this format:

```json
{
  "status": "error",
  "message": "<descriptive error message>"
}
```

### Error Categories

| Error | Trigger | Message Example |
|-------|---------|-----------------|
| Missing required field | Empty title for `add_task` | "Title is required and must be between 1 and 200 characters." |
| Invalid UUID | Non-UUID string for task_id | "Invalid task ID: {value}" |
| Task not found | ID doesn't exist or belongs to another user | "Task not found." |
| Title too long | Title > 200 characters | "Title must be between 1 and 200 characters." |
| Description too long | Description > 1000 characters | "Description must not exceed 1000 characters." |
| Service failure | Database unavailable | "Service temporarily unavailable. Please try again." |
