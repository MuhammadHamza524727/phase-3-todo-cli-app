from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemySession
from src.database.connection import get_session
from src.models.user import User, UserCreate, UserRead
from src.middleware.jwt_auth import create_access_token, get_password_hash, get_current_user
from src.services.auth_service import authenticate_user, create_new_user
from typing import Dict, Any
import uuid
from pydantic import BaseModel
import logging
import traceback

logger = logging.getLogger(__name__)

router = APIRouter()


class LoginData(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    user: Dict[str, Any]
    token: str


@router.post("/register", response_model=AuthResponse)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        logger.info(f"Registration attempt for email: {user.email}")
        
        # Check if passwords match
        if user.password != user.password_confirm:
            logger.warning(f"Password mismatch for email: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )

        # Use the authentication service to create the user
        db_user = await create_new_user(session, user)
        logger.info(f"User created successfully: {db_user.id}")

        # Create access token
        access_token = create_access_token(data={"sub": str(db_user.id)})

        # Convert user to dict for response
        user_dict = {
            "id": str(db_user.id),
            "email": db_user.email,
            "name": db_user.name,
            "created_at": db_user.created_at.isoformat() if db_user.created_at else None,
            "updated_at": db_user.updated_at.isoformat() if db_user.updated_at else None,
            "is_active": db_user.is_active
        }

        return AuthResponse(user=user_dict, token=access_token)

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=AuthResponse)
async def login(login_data: LoginData, session: AsyncSession = Depends(get_session)):
    # Use the authentication service to authenticate the user
    # This function will raise appropriate exceptions if authentication fails
    user = await authenticate_user(session, login_data.email, login_data.password)

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    # Convert user to dict for response
    user_dict = {
        "id": str(user.id),
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        "is_active": user.is_active
    }

    return AuthResponse(user=user_dict, token=access_token)


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """Get the current authenticated user's profile"""
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "name": current_user.name,
    }