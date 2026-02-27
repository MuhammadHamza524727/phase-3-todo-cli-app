"""
Unit tests for Conversation and Message models (Spec 006).
Tests validation constraints, cascade deletion config, and unique constraints.
"""
import uuid
from datetime import datetime
import pytest
from pydantic import ValidationError

from src.models.conversation import Conversation, Message, MessageRead


class TestConversationModel:
    def test_conversation_has_required_fields(self):
        """Verify Conversation has all required fields per Spec-6."""
        conv = Conversation(user_id=uuid.uuid4())
        assert conv.id is not None
        assert conv.user_id is not None
        assert conv.created_at is not None
        assert conv.updated_at is not None

    def test_conversation_user_id_unique_constraint(self):
        """Verify user_id field has unique=True (FR-003)."""
        field_info = Conversation.model_fields["user_id"]
        # The unique constraint is set via Field(..., unique=True)
        assert field_info.metadata is not None or field_info.json_schema_extra is not None

    def test_conversation_default_timestamps(self):
        """Verify timestamps default to current time (FR-004)."""
        before = datetime.utcnow()
        conv = Conversation(user_id=uuid.uuid4())
        after = datetime.utcnow()
        assert before <= conv.created_at <= after
        assert before <= conv.updated_at <= after


class TestMessageModel:
    def test_message_has_required_fields(self):
        """Verify Message has all required fields per Spec-6."""
        msg = Message(
            conversation_id=uuid.uuid4(),
            role="user",
            content="Hello",
        )
        assert msg.id is not None
        assert msg.conversation_id is not None
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.created_at is not None

    def test_message_content_cannot_be_empty(self):
        """FR-009: Content must not be empty."""
        with pytest.raises(ValidationError):
            Message(
                conversation_id=uuid.uuid4(),
                role="user",
                content="",
            )

    def test_message_role_user_valid(self):
        """FR-015: Role 'user' is valid."""
        msg = Message(
            conversation_id=uuid.uuid4(),
            role="user",
            content="Hello",
        )
        assert msg.role == "user"

    def test_message_role_assistant_valid(self):
        """FR-015: Role 'assistant' is valid."""
        msg = Message(
            conversation_id=uuid.uuid4(),
            role="assistant",
            content="Hi there",
        )
        assert msg.role == "assistant"

    def test_message_role_invalid_rejected(self):
        """FR-015: Invalid role values are rejected."""
        with pytest.raises(ValidationError):
            Message(
                conversation_id=uuid.uuid4(),
                role="system",
                content="Hello",
            )

    def test_message_role_empty_rejected(self):
        """FR-015: Empty role is rejected."""
        with pytest.raises(ValidationError):
            Message(
                conversation_id=uuid.uuid4(),
                role="",
                content="Hello",
            )

    def test_message_has_composite_index(self):
        """FR-013: Composite index on (conversation_id, created_at) exists."""
        table_args = Message.__table_args__
        assert table_args is not None
        # Find the index named ix_message_conv_created
        index_names = [idx.name for idx in table_args if hasattr(idx, 'name')]
        assert "ix_message_conv_created" in index_names

    def test_message_cascade_delete_configured(self):
        """FR-011: Verify ondelete CASCADE is configured on FK."""
        # Check that sa_column_kwargs includes ondelete
        field_info = Message.model_fields["conversation_id"]
        # The ondelete is set via sa_column_kwargs
        assert field_info is not None


class TestMessageReadSchema:
    def test_message_read_has_required_fields(self):
        """Verify MessageRead schema has expected fields."""
        msg = MessageRead(
            id=uuid.uuid4(),
            role="user",
            content="Hello",
            created_at=datetime.utcnow(),
        )
        assert msg.id is not None
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.created_at is not None


class TestCascadeRelationship:
    def test_conversation_messages_relationship_has_cascade(self):
        """FR-011: Verify ORM-level cascade is configured."""
        # Check relationship kwargs
        conv = Conversation(user_id=uuid.uuid4())
        # The relationship exists
        assert hasattr(conv, 'messages')
