# API Contract: Chat Endpoint

**Feature**: 004-ai-chatbot | **Date**: 2026-02-21

## POST /api/chat

Send a natural language message to the AI chatbot. The chatbot interprets the intent, executes task operations via MCP tools, and returns a conversational response.

### Authentication

Required. Bearer JWT token in Authorization header.

### Request

**Headers**:
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Body**:
```json
{
  "message": "string (required, non-empty, max 2000 chars)"
}
```

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| message | string | Yes | 1-2000 chars | User's natural language message |

### Response

**Success (200 OK)**:
```json
{
  "success": true,
  "data": {
    "response": "I've created a task 'Buy groceries' for you.",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "tool_calls": [
      {
        "tool": "create_task",
        "arguments": {
          "title": "Buy groceries"
        },
        "result": {
          "id": "660e8400-e29b-41d4-a716-446655440001",
          "title": "Buy groceries",
          "completed": false
        }
      }
    ]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| response | string | AI assistant's natural language response |
| conversation_id | UUID | Conversation identifier (created or existing) |
| tool_calls | array | List of MCP tools invoked (may be empty for conversational responses) |
| tool_calls[].tool | string | Tool name (create_task, list_tasks, get_task, update_task, delete_task) |
| tool_calls[].arguments | object | Arguments passed to the tool |
| tool_calls[].result | object | Tool execution result |

### Error Responses

**401 Unauthorized** — Missing or invalid JWT:
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired authentication token"
  }
}
```

**400 Bad Request** — Empty or invalid message:
```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Message cannot be empty"
  }
}
```

**500 Internal Server Error** — AI service failure:
```json
{
  "success": false,
  "error": {
    "code": "AI_SERVICE_ERROR",
    "message": "The chatbot is temporarily unavailable. Please try again."
  }
}
```

### Example Interactions

**Create a task**:
```
Request:  {"message": "Add a task to buy groceries"}
Response: {"response": "I've created a task 'Buy groceries' for you.", ...}
```

**List tasks**:
```
Request:  {"message": "Show my tasks"}
Response: {"response": "Here are your tasks:\n1. Buy groceries (pending)\n2. Review PR (completed)", ...}
```

**Complete a task**:
```
Request:  {"message": "Mark buy groceries as done"}
Response: {"response": "Done! I've marked 'Buy groceries' as completed.", ...}
```

**Delete a task**:
```
Request:  {"message": "Delete the task buy groceries"}
Response: {"response": "I've deleted the task 'Buy groceries'.", ...}
```

**Update a task**:
```
Request:  {"message": "Rename 'Buy groceries' to 'Buy organic groceries'"}
Response: {"response": "I've updated the task title to 'Buy organic groceries'.", ...}
```

**Ambiguous reference**:
```
Request:  {"message": "Complete the task"}
Response: {"response": "I found multiple tasks. Which one do you want to complete?\n1. Buy groceries\n2. Review PR", ...}
```

**Non-task message**:
```
Request:  {"message": "What's the weather?"}
Response: {"response": "I can help you manage your tasks! Try saying 'show my tasks' or 'add a task to...'", ...}
```

---

## GET /api/chat/history

Retrieve conversation history for the authenticated user.

### Authentication

Required. Bearer JWT token in Authorization header.

### Request

**Headers**:
```
Authorization: Bearer <jwt-token>
```

**Query Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| limit | integer | No | 50 | Max messages to return (1-100) |
| offset | integer | No | 0 | Messages to skip |

### Response

**Success (200 OK)**:
```json
{
  "success": true,
  "data": {
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "messages": [
      {
        "id": "770e8400-e29b-41d4-a716-446655440002",
        "role": "user",
        "content": "Show my tasks",
        "created_at": "2026-02-21T10:30:00Z"
      },
      {
        "id": "880e8400-e29b-41d4-a716-446655440003",
        "role": "assistant",
        "content": "Here are your tasks:\n1. Buy groceries (pending)",
        "created_at": "2026-02-21T10:30:02Z"
      }
    ],
    "total": 24,
    "limit": 50,
    "offset": 0
  }
}
```

**204 No Content** — No conversation exists yet (first-time user).
