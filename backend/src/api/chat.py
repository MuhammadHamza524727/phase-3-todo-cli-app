"""
Chat API endpoints for the AI chatbot.
POST /api/chat — Send a message, receive AI response
GET /api/chat/history — Retrieve conversation history
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.connection import get_session
from src.models.user import User
from src.models.base_response import (
    ChatRequest,
    SuccessResponse,
    ErrorResponse,
    ChatResponseData,
    ChatHistoryData,
)
from src.middleware.jwt_auth import get_current_user
from src.services.chat_service import process_chat_message, get_chat_history

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=SuccessResponse[ChatResponseData])
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    Send a natural language message to the AI chatbot.
    The chatbot interprets the intent, executes task operations via MCP tools,
    and returns a conversational response.
    """
    try:
        result = await process_chat_message(
            user_id=current_user.id,
            message=request.message,
            session=session,
        )

        return SuccessResponse(
            data=ChatResponseData(
                response=result["response"],
                conversation_id=result["conversation_id"],
                tool_calls=result["tool_calls"],
            )
        )
    except Exception as e:
        logger.error(f"Chat processing error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The chatbot is temporarily unavailable. Please try again.",
        )


@router.get("/chat/history", response_model=SuccessResponse[ChatHistoryData])
async def chat_history(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    limit: int = Query(50, ge=1, le=100, description="Max messages to return"),
    offset: int = Query(0, ge=0, description="Messages to skip"),
):
    """
    Retrieve conversation history for the authenticated user.
    """
    result = await get_chat_history(
        user_id=current_user.id,
        session=session,
        limit=limit,
        offset=offset,
    )

    return SuccessResponse(
        data=ChatHistoryData(
            conversation_id=result["conversation_id"],
            messages=result["messages"],
            total=result["total"],
            limit=result["limit"],
            offset=result["offset"],
        )
    )
