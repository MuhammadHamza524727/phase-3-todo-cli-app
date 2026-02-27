from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime
import uuid
from src.database.connection import get_session
from src.models.task import Task, TaskRead, TaskCreate, TaskUpdate, TaskPatch
from src.models.user import User
from src.middleware.jwt_auth import get_current_user
from src.models.base_response import SuccessResponse, ErrorResponse, TaskResponse

router = APIRouter()


@router.get("/tasks", response_model=List[TaskRead])
async def get_tasks(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    limit: int = Query(50, ge=1, le=100, description="Number of tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip"),
    completed: Optional[bool] = Query(None, description="Filter by completion status")
) -> List[TaskRead]:
    """
    Retrieve the authenticated user's tasks with optional filtering and pagination.
    """
    # Build the query with user isolation
    query = select(Task).where(Task.owner_user_id == current_user.id)

    # Add optional filtering for completed status
    if completed is not None:
        query = query.where(Task.completed == completed)

    # Add pagination
    query = query.offset(offset).limit(limit).order_by(Task.created_at.desc())

    result = await session.exec(query)
    tasks = [row[0] if isinstance(row, tuple) else row for row in result.all()]

    return tasks


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> TaskRead:
    """
    Create a new task for the authenticated user.
    """
    # Ensure the task is associated with the current user
    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        owner_user_id=current_user.id,  # Enforce user ownership
        due_date=task_create.due_date
    )

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return db_task


@router.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> TaskRead:
    """
    Retrieve a specific task by ID, ensuring it belongs to the current user.
    """
    # Query for the task that belongs to the current user
    query = select(Task).where(
        and_(Task.id == task_id, Task.owner_user_id == current_user.id)
    )
    result = await session.exec(query)
    task = result.first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to current user"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: uuid.UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> TaskRead:
    """
    Update a specific task by ID, ensuring it belongs to the current user.
    """
    # Query for the task that belongs to the current user
    query = select(Task).where(
        and_(Task.id == task_id, Task.owner_user_id == current_user.id)
    )
    result = await session.exec(query)
    db_task = result.first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to current user"
        )

    # Update the task with provided fields
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, field, value)

    # Update the updated_at timestamp
    db_task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(db_task)

    return db_task


@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
async def update_task_completion(
    task_id: uuid.UUID,
    task_patch: TaskPatch,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> TaskRead:
    """
    Toggle task completion status, ensuring it belongs to the current user.
    """
    # Query for the task that belongs to the current user
    query = select(Task).where(
        and_(Task.id == task_id, Task.owner_user_id == current_user.id)
    )
    result = await session.exec(query)
    db_task = result.first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to current user"
        )

    # Update the completion status if provided
    if task_patch.completed is not None:
        db_task.completed = task_patch.completed

    # Update the updated_at timestamp
    db_task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(db_task)

    return db_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
) -> None:
    """
    Delete a specific task by ID, ensuring it belongs to the current user.
    """
    # Query for the task that belongs to the current user
    query = select(Task).where(
        and_(Task.id == task_id, Task.owner_user_id == current_user.id)
    )
    result = await session.exec(query)
    db_task = result.first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or does not belong to current user"
        )

    await session.delete(db_task)
    await session.commit()

    # Return 204 No Content