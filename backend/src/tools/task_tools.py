"""
MCP Tool definitions for task operations.
These tools are used by the OpenAI Agents SDK to perform task CRUD operations
on behalf of the authenticated user. User ID is injected via RunContext.
"""
import uuid
import json
from datetime import datetime
from typing import Optional
from agents import function_tool, RunContextWrapper
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.task import Task
from src.database.connection import get_session


def _validate_title(title: str) -> Optional[str]:
    """Validate task title. Returns error message or None if valid."""
    if not title or not title.strip():
        return "Title is required and must be between 1 and 200 characters."
    if len(title) > 200:
        return "Title must be between 1 and 200 characters."
    return None


def _validate_description(description: str) -> Optional[str]:
    """Validate task description. Returns error message or None if valid."""
    if description and len(description) > 1000:
        return "Description must not exceed 1000 characters."
    return None


class UserContext:
    """Context object injected into each MCP tool via RunContextWrapper.
    Carries the authenticated user_id (from JWT) and database session.
    Ensures all tool operations are scoped to the authenticated user (FR-002, FR-003).
    """
    def __init__(self, user_id: uuid.UUID, session: AsyncSession):
        self.user_id = user_id
        self.session = session


@function_tool
async def add_task(ctx: RunContextWrapper[UserContext], title: str, description: Optional[str] = None) -> str:
    """Add a new task to your task list. Use this when the user wants to create, add, or make a new task or todo item. Requires a title (1-200 characters). Optionally accepts a description (up to 1000 characters)."""
    # Input validation (FR-005, FR-010)
    title_error = _validate_title(title)
    if title_error:
        return json.dumps({"status": "error", "message": title_error})
    desc_error = _validate_description(description)
    if desc_error:
        return json.dumps({"status": "error", "message": desc_error})

    session = ctx.context.session
    user_id = ctx.context.user_id

    db_task = Task(
        title=title.strip(),
        description=description.strip() if description else "",
        completed=False,
        owner_user_id=user_id,
    )
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return json.dumps({
        "status": "success",
        "task_id": str(db_task.id),
        "title": db_task.title,
        "message": f"Task '{db_task.title}' created successfully."
    })


@function_tool
async def list_tasks(ctx: RunContextWrapper[UserContext], completed: Optional[bool] = None) -> str:
    """List all tasks in your task list. Use this when the user wants to see, view, or check their tasks. Optionally filter by completion status: set completed=true for completed tasks, completed=false for pending tasks, or omit for all tasks."""
    session = ctx.context.session
    user_id = ctx.context.user_id

    query = select(Task).where(Task.owner_user_id == user_id)
    if completed is not None:
        query = query.where(Task.completed == completed)
    query = query.order_by(Task.created_at.desc())

    result = await session.exec(query)
    tasks = result.all()

    if not tasks:
        filter_label = ""
        if completed is True:
            filter_label = " completed"
        elif completed is False:
            filter_label = " pending"
        return json.dumps({
            "status": "empty",
            "count": 0,
            "message": f"You don't have any{filter_label} tasks yet. Try saying 'Add a task to...'"
        })

    task_list = []
    for i, task in enumerate(tasks, 1):
        status = "completed" if task.completed else "pending"
        task_list.append({
            "index": i,
            "id": str(task.id),
            "title": task.title,
            "status": status,
            "description": task.description or "",
        })

    return json.dumps({
        "status": "success",
        "count": len(task_list),
        "tasks": task_list
    })


@function_tool
async def complete_task(ctx: RunContextWrapper[UserContext], task_id: str) -> str:
    """Mark a task as completed or toggle it back to pending. Use this when the user says they finished, completed, or done with a task, or when they want to un-complete a task. Requires the task ID."""
    session = ctx.context.session
    user_id = ctx.context.user_id

    try:
        tid = uuid.UUID(task_id)
    except ValueError:
        return json.dumps({"status": "error", "message": f"Invalid task ID: {task_id}"})

    query = select(Task).where(and_(Task.id == tid, Task.owner_user_id == user_id))
    result = await session.exec(query)
    task = result.first()

    if not task:
        return json.dumps({"status": "error", "message": "Task not found."})

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(task)

    status_label = "completed" if task.completed else "pending"
    return json.dumps({
        "status": "success",
        "task_id": str(task.id),
        "title": task.title,
        "completed": task.completed,
        "message": f"Task '{task.title}' marked as {status_label}."
    })


@function_tool
async def get_task(ctx: RunContextWrapper[UserContext], task_id: str) -> str:
    """Get details of a specific task by its ID. Use this to look up a single task."""
    session = ctx.context.session
    user_id = ctx.context.user_id

    try:
        tid = uuid.UUID(task_id)
    except ValueError:
        return json.dumps({"status": "error", "message": f"Invalid task ID: {task_id}"})

    query = select(Task).where(and_(Task.id == tid, Task.owner_user_id == user_id))
    result = await session.exec(query)
    task = result.first()

    if not task:
        return json.dumps({"status": "error", "message": "Task not found."})

    return json.dumps({
        "status": "success",
        "task": {
            "id": str(task.id),
            "title": task.title,
            "description": task.description or "",
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
        }
    })


@function_tool
async def update_task(
    ctx: RunContextWrapper[UserContext],
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
) -> str:
    """Update an existing task's details. Use this when the user wants to change, modify, rename, or edit a task. You can update the title, description, or completion status. Requires the task ID and at least one field to change."""
    # Input validation (FR-010)
    if title is not None:
        title_error = _validate_title(title)
        if title_error:
            return json.dumps({"status": "error", "message": title_error})
    if description is not None:
        desc_error = _validate_description(description)
        if desc_error:
            return json.dumps({"status": "error", "message": desc_error})

    session = ctx.context.session
    user_id = ctx.context.user_id

    try:
        tid = uuid.UUID(task_id)
    except ValueError:
        return json.dumps({"status": "error", "message": f"Invalid task ID: {task_id}"})

    query = select(Task).where(and_(Task.id == tid, Task.owner_user_id == user_id))
    result = await session.exec(query)
    task = result.first()

    if not task:
        return json.dumps({"status": "error", "message": "Task not found."})

    changes = []
    if title is not None and title != task.title:
        old_title = task.title
        task.title = title
        changes.append(f"title changed from '{old_title}' to '{title}'")
    if description is not None:
        task.description = description
        changes.append("description updated")
    if completed is not None and completed != task.completed:
        task.completed = completed
        status_str = "completed" if completed else "pending"
        changes.append(f"marked as {status_str}")

    if not changes:
        return json.dumps({"status": "success", "message": "No changes were needed.", "task_id": str(task.id)})

    task.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(task)

    return json.dumps({
        "status": "success",
        "task_id": str(task.id),
        "title": task.title,
        "changes": changes,
        "message": f"Task '{task.title}' updated: {', '.join(changes)}."
    })


@function_tool
async def delete_task(ctx: RunContextWrapper[UserContext], task_id: str) -> str:
    """Delete a task from your task list. Use this when the user wants to remove, delete, or get rid of a task. This action is permanent. Requires the task ID."""
    session = ctx.context.session
    user_id = ctx.context.user_id

    try:
        tid = uuid.UUID(task_id)
    except ValueError:
        return json.dumps({"status": "error", "message": f"Invalid task ID: {task_id}"})

    query = select(Task).where(and_(Task.id == tid, Task.owner_user_id == user_id))
    result = await session.exec(query)
    task = result.first()

    if not task:
        return json.dumps({"status": "error", "message": "Task not found."})

    deleted_title = task.title
    await session.delete(task)
    await session.commit()

    return json.dumps({
        "status": "success",
        "deleted_title": deleted_title,
        "message": f"Task '{deleted_title}' has been deleted."
    })
