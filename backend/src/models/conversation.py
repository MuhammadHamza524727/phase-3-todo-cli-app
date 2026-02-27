from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy import types as sa_types
from pydantic import field_validator
from datetime import datetime
import uuid
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Conversation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", unique=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Message(SQLModel, table=True):
    __table_args__ = (
        Index("ix_message_conv_created", "conversation_id", "created_at"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(
        foreign_key="conversation.id",
        nullable=False,
    )
    role: str = Field(nullable=False, max_length=20)  # FR-015: only "user" or "assistant"
    content: str = Field(nullable=False)

    @field_validator("role")
    @classmethod
    def role_must_be_valid(cls, v: str) -> str:
        if v not in ("user", "assistant"):
            raise ValueError("role must be 'user' or 'assistant'")
        return v

    @field_validator("content")
    @classmethod
    def content_must_not_be_empty(cls, v: str) -> str:
        if not v:
            raise ValueError("content must not be empty")
        return v
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: Optional[Conversation] = Relationship(back_populates="messages")


class MessageRead(SQLModel):
    id: uuid.UUID
    role: str
    content: str
    created_at: datetime
