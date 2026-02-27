"""
Unit tests for MCP task tools (Spec 005).
Tests all 5 tools: add_task, list_tasks, complete_task, update_task, delete_task.
Uses mocked AsyncSession and RunContextWrapper to test tool logic in isolation.
"""
import json
import uuid
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from src.tools.task_tools import (
    add_task,
    list_tasks,
    complete_task,
    update_task,
    delete_task,
    UserContext,
    _validate_title,
    _validate_description,
)


# ---- Helpers ----

def make_ctx(user_id=None, session=None):
    """Create a mock RunContextWrapper[UserContext]."""
    if user_id is None:
        user_id = uuid.uuid4()
    if session is None:
        session = AsyncMock()
    ctx = MagicMock()
    ctx.context = UserContext(user_id=user_id, session=session)
    return ctx


def make_task(user_id, title="Test task", description=None, completed=False, task_id=None):
    """Create a mock Task object."""
    task = MagicMock()
    task.id = task_id or uuid.uuid4()
    task.title = title
    task.description = description
    task.completed = completed
    task.owner_user_id = user_id
    task.created_at = datetime(2026, 1, 1, 12, 0, 0)
    task.updated_at = datetime(2026, 1, 1, 12, 0, 0)
    return task


# ---- Validation Tests ----

class TestValidation:
    def test_validate_title_valid(self):
        assert _validate_title("Buy groceries") is None

    def test_validate_title_empty(self):
        assert _validate_title("") is not None

    def test_validate_title_whitespace(self):
        assert _validate_title("   ") is not None

    def test_validate_title_too_long(self):
        assert _validate_title("x" * 201) is not None

    def test_validate_title_max_length(self):
        assert _validate_title("x" * 200) is None

    def test_validate_description_valid(self):
        assert _validate_description("Some description") is None

    def test_validate_description_empty(self):
        assert _validate_description("") is None

    def test_validate_description_too_long(self):
        assert _validate_description("x" * 1001) is not None

    def test_validate_description_max_length(self):
        assert _validate_description("x" * 1000) is None


# ---- add_task Tests ----

class TestAddTask:
    @pytest.mark.asyncio
    async def test_add_task_success(self):
        session = AsyncMock()
        user_id = uuid.uuid4()
        ctx = make_ctx(user_id=user_id, session=session)

        task_id = uuid.uuid4()
        session.refresh = AsyncMock(side_effect=lambda t: setattr(t, 'id', task_id))

        result = json.loads(await add_task.on_invoke_tool(ctx, json.dumps({"title": "Buy groceries"})))
        assert result["status"] == "success"
        assert result["title"] == "Buy groceries"
        assert "message" in result

    @pytest.mark.asyncio
    async def test_add_task_empty_title(self):
        ctx = make_ctx()
        result = json.loads(await add_task.on_invoke_tool(ctx, json.dumps({"title": ""})))
        assert result["status"] == "error"
        assert "Title" in result["message"]

    @pytest.mark.asyncio
    async def test_add_task_title_too_long(self):
        ctx = make_ctx()
        result = json.loads(await add_task.on_invoke_tool(ctx, json.dumps({"title": "x" * 201})))
        assert result["status"] == "error"

    @pytest.mark.asyncio
    async def test_add_task_description_too_long(self):
        ctx = make_ctx()
        result = json.loads(await add_task.on_invoke_tool(ctx, json.dumps({"title": "Valid", "description": "x" * 1001})))
        assert result["status"] == "error"
        assert "Description" in result["message"]


# ---- list_tasks Tests ----

class TestListTasks:
    @pytest.mark.asyncio
    async def test_list_tasks_empty(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.all.return_value = []
        session.exec = AsyncMock(return_value=mock_result)
        ctx = make_ctx(session=session)

        result = json.loads(await list_tasks.on_invoke_tool(ctx, json.dumps({})))
        assert result["status"] == "empty"
        assert result["count"] == 0

    @pytest.mark.asyncio
    async def test_list_tasks_with_tasks(self):
        user_id = uuid.uuid4()
        session = AsyncMock()
        tasks = [
            make_task(user_id, "Task 1", completed=False),
            make_task(user_id, "Task 2", completed=True),
        ]
        mock_result = MagicMock()
        mock_result.all.return_value = tasks
        session.exec = AsyncMock(return_value=mock_result)
        ctx = make_ctx(user_id=user_id, session=session)

        result = json.loads(await list_tasks.on_invoke_tool(ctx, json.dumps({})))
        assert result["status"] == "success"
        assert result["count"] == 2
        assert len(result["tasks"]) == 2
        assert result["tasks"][0]["index"] == 1
        assert "id" in result["tasks"][0]
        assert "title" in result["tasks"][0]
        assert "status" in result["tasks"][0]
        assert "description" in result["tasks"][0]


# ---- complete_task Tests ----

class TestCompleteTask:
    @pytest.mark.asyncio
    async def test_complete_task_toggle_to_completed(self):
        user_id = uuid.uuid4()
        session = AsyncMock()
        task = make_task(user_id, "Buy groceries", completed=False)
        mock_result = MagicMock()
        mock_result.first.return_value = task
        session.exec = AsyncMock(return_value=mock_result)
        ctx = make_ctx(user_id=user_id, session=session)

        result = json.loads(await complete_task.on_invoke_tool(ctx, json.dumps({"task_id": str(task.id)})))
        assert result["status"] == "success"
        assert result["completed"] is True
        assert "completed" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_complete_task_toggle_to_pending(self):
        user_id = uuid.uuid4()
        session = AsyncMock()
        task = make_task(user_id, "Buy groceries", completed=True)
        mock_result = MagicMock()
        mock_result.first.return_value = task
        session.exec = AsyncMock(return_value=mock_result)
        ctx = make_ctx(user_id=user_id, session=session)

        result = json.loads(await complete_task.on_invoke_tool(ctx, json.dumps({"task_id": str(task.id)})))
        assert result["status"] == "success"
        assert result["completed"] is False
        assert "pending" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_complete_task_not_found(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.first.return_value = None
        session.exec = AsyncMock(return_value=mock_result)
        ctx = make_ctx(session=session)

        result = json.loads(await complete_task.on_invoke_tool(ctx, json.dumps({"task_id": str(uuid.uuid4())})))
        assert result["status"] == "error"
        assert result["message"] == "Task not found."

    @pytest.mark.asyncio
    async def test_complete_task_invalid_id(self):
        ctx = make_ctx()
        result = json.loads(await complete_task.on_invoke_tool(ctx, json.dumps({"task_id": "not-a-uuid"})))
        assert result["status"] == "error"
        assert "Invalid task ID" in result["message"]


# ---- update_task Tests ----

class TestUpdateTask:
    @pytest.mark.asyncio
    async def test_update_task_title(self):
        user_id = uuid.uuid4()
        session = AsyncMock()
        task = make_task(user_id, "Old title")
        mock_result = MagicMock()
        mock_result.first.return_value = task
        session.exec = AsyncMock(return_value=mock_result)
        ctx = make_ctx(user_id=user_id, session=session)

        result = json.loads(await update_task.on_invoke_tool(ctx, json.dumps({"task_id": str(task.id), "title": "New title"})))
        assert result["status"] == "success"
        assert "changes" in result
        assert any("title" in c for c in result["changes"])

    @pytest.mark.asyncio
    async def test_update_task_no_changes(self):
        user_id = uuid.uuid4()
        session = AsyncMock()
        task = make_task(user_id, "Same title")
        mock_result = MagicMock()
        mock_result.first.return_value = task
        session.exec = AsyncMock(return_value=mock_result)
        ctx = make_ctx(user_id=user_id, session=session)

        result = json.loads(await update_task.on_invoke_tool(ctx, json.dumps({"task_id": str(task.id), "title": "Same title"})))
        assert result["status"] == "success"
        assert "No changes" in result["message"]

    @pytest.mark.asyncio
    async def test_update_task_validation_title_too_long(self):
        ctx = make_ctx()
        result = json.loads(await update_task.on_invoke_tool(ctx, json.dumps({"task_id": str(uuid.uuid4()), "title": "x" * 201})))
        assert result["status"] == "error"

    @pytest.mark.asyncio
    async def test_update_task_not_found(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.first.return_value = None
        session.exec = AsyncMock(return_value=mock_result)
        ctx = make_ctx(session=session)

        result = json.loads(await update_task.on_invoke_tool(ctx, json.dumps({"task_id": str(uuid.uuid4()), "title": "New"})))
        assert result["status"] == "error"
        assert result["message"] == "Task not found."


# ---- delete_task Tests ----

class TestDeleteTask:
    @pytest.mark.asyncio
    async def test_delete_task_success(self):
        user_id = uuid.uuid4()
        session = AsyncMock()
        task = make_task(user_id, "Buy groceries")
        mock_result = MagicMock()
        mock_result.first.return_value = task
        session.exec = AsyncMock(return_value=mock_result)
        ctx = make_ctx(user_id=user_id, session=session)

        result = json.loads(await delete_task.on_invoke_tool(ctx, json.dumps({"task_id": str(task.id)})))
        assert result["status"] == "success"
        assert result["deleted_title"] == "Buy groceries"
        assert "deleted" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self):
        session = AsyncMock()
        mock_result = MagicMock()
        mock_result.first.return_value = None
        session.exec = AsyncMock(return_value=mock_result)
        ctx = make_ctx(session=session)

        result = json.loads(await delete_task.on_invoke_tool(ctx, json.dumps({"task_id": str(uuid.uuid4())})))
        assert result["status"] == "error"
        assert result["message"] == "Task not found."

    @pytest.mark.asyncio
    async def test_delete_task_invalid_id(self):
        ctx = make_ctx()
        result = json.loads(await delete_task.on_invoke_tool(ctx, json.dumps({"task_id": "bad-id"})))
        assert result["status"] == "error"
        assert "Invalid task ID" in result["message"]
