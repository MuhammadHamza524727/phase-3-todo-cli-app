"""
Tool functions for task operations.
Plain async functions called directly by chat_service with user_id injected.
"""
import uuid
import json
from datetime import datetime
from typing import Optional
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.task import Task
from src.database.connection import engine


async def add_task_fn(user_id: uuid.UUID, title: str, description: str = "", **kwargs) -> str:
    """Add a new task."""
    if not title or not title.strip() or len(title) > 200:
        return json.dumps({"status": "error", "message": "Title must be between 1 and 200 characters."})

    async with AsyncSession(engine) as session:
        db_task = Task(
            title=title.strip(),
            description=description.strip() if description else None,
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


async def list_tasks_fn(user_id: uuid.UUID, **kwargs) -> str:
    """List all tasks."""
    async with AsyncSession(engine) as session:
        query = select(Task).where(Task.owner_user_id == user_id).order_by(Task.created_at.desc())
        result = await session.execute(query)
        tasks = result.scalars().all()

        if not tasks:
            return json.dumps({
                "status": "empty",
                "count": 0,
                "message": "You don't have any tasks yet."
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


async def complete_task_fn(user_id: uuid.UUID, task_id: str, **kwargs) -> str:
    """Toggle task completion."""
    try:
        tid = uuid.UUID(task_id)
    except ValueError:
        return json.dumps({"status": "error", "message": f"Invalid task ID: {task_id}"})

    async with AsyncSession(engine) as session:
        query = select(Task).where(and_(Task.id == tid, Task.owner_user_id == user_id))
        result = await session.execute(query)
        task = result.scalars().first()

        if not task:
            return json.dumps({"status": "error", "message": "Task not found."})

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


async def get_task_fn(user_id: uuid.UUID, task_id: str, **kwargs) -> str:
    """Get a single task."""
    try:
        tid = uuid.UUID(task_id)
    except ValueError:
        return json.dumps({"status": "error", "message": f"Invalid task ID: {task_id}"})

    async with AsyncSession(engine) as session:
        query = select(Task).where(and_(Task.id == tid, Task.owner_user_id == user_id))
        result = await session.execute(query)
        task = result.scalars().first()

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


async def update_task_fn(
    user_id: uuid.UUID,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    **kwargs,
) -> str:
    """Update a task."""
    try:
        tid = uuid.UUID(task_id)
    except ValueError:
        return json.dumps({"status": "error", "message": f"Invalid task ID: {task_id}"})

    async with AsyncSession(engine) as session:
        query = select(Task).where(and_(Task.id == tid, Task.owner_user_id == user_id))
        result = await session.execute(query)
        task = result.scalars().first()

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


async def delete_task_fn(user_id: uuid.UUID, task_id: str, **kwargs) -> str:
    """Delete a task."""
    try:
        tid = uuid.UUID(task_id)
    except ValueError:
        return json.dumps({"status": "error", "message": f"Invalid task ID: {task_id}"})

    async with AsyncSession(engine) as session:
        query = select(Task).where(and_(Task.id == tid, Task.owner_user_id == user_id))
        result = await session.execute(query)
        task = result.scalars().first()

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
