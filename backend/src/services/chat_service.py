"""
Chat service: orchestrates the AI agent for natural language task management.
Handles conversation persistence, agent creation, and message processing.
Stateless — conversation context is reconstructed from DB on each request.
"""
import uuid
import json
import logging
import os
from datetime import datetime
from typing import Optional

from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.tracing import set_tracing_disabled
from openai import AsyncOpenAI

set_tracing_disabled(True)
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models.conversation import Conversation, Message
from src.models.base_response import ToolCallInfo
from src.database.connection import engine
from src.tools.task_tools import (
    add_task,
    list_tasks,
    complete_task,
    get_task,
    update_task,
    delete_task,
    UserContext,
)

logger = logging.getLogger(__name__)

llm_client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

SYSTEM_INSTRUCTIONS = """You are a helpful task management assistant. You help users manage their to-do tasks through natural language conversation.

Your capabilities:
- Add new tasks (when users say things like "add a task", "create a task", "I need to...")
- List tasks (when users say "show my tasks", "list tasks", "what are my tasks?")
- Complete tasks (when users say "mark X as done", "complete X", "finish X" — use the complete_task tool)
- Update tasks (when users say "rename X", "change X", "update the description of X" — use the update_task tool)
- Delete tasks (when users say "delete X", "remove X")

Important rules:
1. Always use the provided tools to perform task operations. Never make up task data.
2. When a user wants to complete, update, or delete a task, first call list_tasks to find the matching task by name, then use the task's ID for the operation.
3. If the user's request is ambiguous (e.g., "complete the task" when they have multiple tasks), list their tasks and ask them to specify which one.
4. After every successful operation, confirm what was done with specific details (task title, new status, etc.).
5. If a task is not found, say so clearly and suggest alternatives.
6. For non-task-related messages (greetings, questions about weather, etc.), respond politely and remind the user what you can help with.
7. Be concise but friendly in your responses.
"""


async def _get_or_create_conversation(user_id: uuid.UUID) -> uuid.UUID:
    """Get the user's conversation ID or create a new one. Returns conversation ID."""
    async with AsyncSession(engine) as session:
        query = select(Conversation).where(Conversation.user_id == user_id)
        result = await session.execute(query)
        conversation = result.scalars().first()

        if not conversation:
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)

        return conversation.id


async def _load_message_history(conversation_id: uuid.UUID, limit: int = 50) -> list[dict]:
    """Load recent messages for the conversation in chronological order."""
    async with AsyncSession(engine) as session:
        query = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(query)
        messages = list(reversed(result.scalars().all()))

        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]


async def _persist_message(conversation_id: uuid.UUID, role: str, content: str) -> Message:
    """Save a message to the database."""
    async with AsyncSession(engine) as session:
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        session.add(msg)
        await session.commit()
        await session.refresh(msg)
        return msg


async def process_chat_message(
    user_id: uuid.UUID,
    message: str,
    session: AsyncSession,
) -> dict:
    """
    Process a user's chat message through the AI agent.
    Returns dict with response, conversation_id, and tool_calls.
    """
    # 1. Get or create conversation
    conversation_id = await _get_or_create_conversation(user_id)

    # 2. Load message history
    history = await _load_message_history(conversation_id)

    # 3. Persist user message
    await _persist_message(conversation_id, "user", message)

    # 4. Build messages for the agent
    agent_messages = history + [{"role": "user", "content": message}]

    # 5. Create agent with MCP tools (using Gemini via OpenAI-compatible endpoint)
    agent = Agent(
        name="TaskBot",
        instructions=SYSTEM_INSTRUCTIONS,
        tools=[add_task, list_tasks, complete_task, get_task, update_task, delete_task],
        model=OpenAIChatCompletionsModel(
            model="llama-3.1-8b-instant",
            openai_client=llm_client,
        ),
    )

    # 6. Create context with user_id for tools
    user_context = UserContext(user_id=user_id)

    # 7. Run the agent
    try:
        result = await Runner.run(
            agent,
            input=agent_messages,
            context=user_context,
        )
        response_text = result.final_output or "I'm sorry, I couldn't process that request."

        # 8. Extract tool calls from the run result
        tool_calls_info = []
        if hasattr(result, 'raw_responses'):
            for raw in result.raw_responses:
                if hasattr(raw, 'output'):
                    for item in raw.output:
                        if hasattr(item, 'type') and item.type == 'function_call':
                            tool_call = ToolCallInfo(
                                tool=item.name if hasattr(item, 'name') else "unknown",
                                arguments=json.loads(item.arguments) if hasattr(item, 'arguments') else {},
                            )
                            tool_calls_info.append(tool_call)

    except Exception as e:
        logger.error(f"Agent execution failed: {e}", exc_info=True)
        response_text = "I'm sorry, I encountered an error processing your request. Please try again."
        tool_calls_info = []

    # 9. Persist assistant response
    await _persist_message(conversation_id, "assistant", response_text)

    # 10. Update conversation timestamp
    async with AsyncSession(engine) as s:
        query = select(Conversation).where(Conversation.id == conversation_id)
        result = await s.execute(query)
        conv = result.scalars().first()
        if conv:
            conv.updated_at = datetime.utcnow()
            await s.commit()

    return {
        "response": response_text,
        "conversation_id": conversation_id,
        "tool_calls": [tc.model_dump() for tc in tool_calls_info],
    }


async def get_chat_history(
    user_id: uuid.UUID,
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> dict:
    """
    Retrieve conversation history for the user.
    Returns dict with conversation_id, messages, total, limit, offset.
    """
    # Find user's conversation
    query = select(Conversation).where(Conversation.user_id == user_id)
    result = await session.execute(query)
    conversation = result.scalars().first()

    if not conversation:
        return {
            "conversation_id": None,
            "messages": [],
            "total": 0,
            "limit": limit,
            "offset": offset,
        }

    # Count total messages
    count_query = select(Message).where(Message.conversation_id == conversation.id)
    count_result = await session.execute(count_query)
    all_messages = count_result.scalars().all()
    total = len(all_messages)

    # Get paginated messages in chronological order
    msg_query = (
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.asc())
        .offset(offset)
        .limit(limit)
    )
    msg_result = await session.execute(msg_query)
    messages = msg_result.scalars().all()

    return {
        "conversation_id": conversation.id,
        "messages": [
            {
                "id": str(msg.id),
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            }
            for msg in messages
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    }
