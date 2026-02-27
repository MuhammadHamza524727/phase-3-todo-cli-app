# Quickstart: MCP Server Tools for Task Management

**Feature**: 005-mcp-task-tools | **Date**: 2026-02-22

## Prerequisites

- Python 3.11+
- Backend dependencies installed: `pip install -r backend/requirements.txt`
- Environment variables configured in `backend/.env`:
  - `DATABASE_URL` — Neon PostgreSQL connection string
  - `OPENAI_API_KEY` — OpenAI API key
  - `SECRET_KEY` — JWT signing secret

## File Structure

```text
backend/src/tools/
├── __init__.py          # Exports all tool functions
└── task_tools.py        # 5 MCP tool definitions + UserContext class
```

## Tool Registration

Tools are registered with the OpenAI Agent in `backend/src/services/chat_service.py`:

```python
from src.tools.task_tools import add_task, list_tasks, complete_task, update_task, delete_task

agent = Agent(
    name="TaskBot",
    instructions=SYSTEM_INSTRUCTIONS,
    tools=[add_task, list_tasks, complete_task, update_task, delete_task]
)
```

## Testing Individual Tools

### Run Unit Tests

```bash
cd backend
pytest tests/test_mcp_tools.py -v
```

### Manual Testing via Chat Endpoint

Start the backend server:

```bash
cd backend
uvicorn main:app --reload
```

Send chat messages that trigger each tool:

```bash
# Create a task (triggers add_task)
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'

# List tasks (triggers list_tasks)
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me my tasks"}'

# Complete a task (triggers complete_task)
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Mark the groceries task as done"}'

# Update a task (triggers update_task)
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Rename the groceries task to Buy organic groceries"}'

# Delete a task (triggers delete_task)
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Delete the groceries task"}'
```

## Verification Checklist

- [ ] `add_task` creates a task and returns success JSON with task_id and title
- [ ] `list_tasks` returns all user tasks with index, id, title, status, description
- [ ] `list_tasks` with `completed=true` returns only completed tasks
- [ ] `list_tasks` returns `"status": "empty"` when user has no tasks
- [ ] `complete_task` toggles a pending task to completed
- [ ] `complete_task` toggles a completed task back to pending
- [ ] `update_task` changes title and lists specific changes made
- [ ] `update_task` with no changes returns "No changes were needed"
- [ ] `delete_task` removes task and returns deleted title
- [ ] All tools return `"Task not found."` for invalid/other-user task IDs
- [ ] All tools return validation errors for invalid inputs (empty title, bad UUID)
- [ ] No tool can access another user's tasks
