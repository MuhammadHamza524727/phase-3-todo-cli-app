from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Union, Dict, Any
from datetime import datetime
import uuid


T = TypeVar('T')


class BaseResponse(BaseModel):
    success: bool
    timestamp: datetime = datetime.utcnow()


class SuccessResponse(BaseResponse, Generic[T]):
    success: bool = True
    data: T


class ErrorResponse(BaseResponse):
    success: bool = False
    error: Dict[str, Any]


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    completed: bool
    owner_user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    created_at: datetime
    updated_at: datetime
    is_active: bool


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ToolCallInfo(BaseModel):
    tool: str
    arguments: Dict[str, Any] = {}
    result: Optional[Dict[str, Any]] = None


class ChatResponseData(BaseModel):
    response: str
    conversation_id: uuid.UUID
    tool_calls: list[ToolCallInfo] = []


class ChatHistoryData(BaseModel):
    conversation_id: Optional[uuid.UUID] = None
    messages: list[Dict[str, Any]] = []
    total: int = 0
    limit: int = 50
    offset: int = 0