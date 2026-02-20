# """
# Authentication Service Module

# This module provides authentication-related business logic and utility functions
# that can be reused across different API endpoints.
# """

# from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlalchemy.future import select
# from src.models.user import User, UserCreate
# from src.middleware.jwt_auth import get_password_hash, verify_password
# from fastapi import HTTPException, status
# from typing import Optional
# import uuid


# async def authenticate_user(session: AsyncSession, email: str, password: str) -> User:
#     """
#     Authenticate a user by email and password

#     Args:
#         session: Database session
#         email: User's email address
#         password: Plain text password to verify

#     Returns:
#         User object if authentication successful, raises HTTPException otherwise
#     """
#     result = await session.execute(select(User).where(User.email == email))
#     user = result.scalar_one_or_none()

#     if not user or not verify_password(password, user.password_hash):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password"
#         )

#     if not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Inactive user"
#         )

#     return user


# async def create_new_user(session: AsyncSession, user_create: UserCreate) -> User:
#     """
#     Create a new user with the provided details

#     Args:
#         session: Database session
#         user_create: User creation request object containing user details

#     Returns:
#         Created User object

#     Raises:
#         HTTPException: If email is already registered
#     """
#     # Check if user already exists
#     existing_user = await session.execute(
#         select(User).where(User.email == user_create.email)
#     )
#     if existing_user.scalar_one_or_none():
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="Email already registered"
#         )

#     # Validate password confirmation
#     if user_create.password != user_create.password_confirm:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Passwords do not match"
#         )

#     # Hash the password
#     hashed_password = get_password_hash(user_create.password)

#     # Create new user
#     db_user = User(
#         email=user_create.email,
#         name=user_create.name,
#         password_hash=hashed_password
#     )

#     session.add(db_user)
#     await session.commit()
#     await session.refresh(db_user)

#     return db_user


# async def get_user_by_id(session: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
#     """
#     Retrieve a user by their ID

#     Args:
#         session: Database session
#         user_id: UUID of the user to retrieve

#     Returns:
#         User object if found, None otherwise
#     """
#     result = await session.execute(
#         select(User).where(User.id == user_id)
#     )
#     return result.scalar_one_or_none()


# async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
#     """
#     Retrieve a user by their email

#     Args:
#         session: Database session
#         email: Email of the user to retrieve

#     Returns:
#         User object if found, None otherwise
#     """
#     result = await session.execute(
#         select(User).where(User.email == email)
#     )
#     return result.scalar_one_or_none()




from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.models.user import User, UserCreate
from src.middleware.jwt_auth import get_password_hash, verify_password
from fastapi import HTTPException, status
from typing import Optional
import uuid
import logging

logger = logging.getLogger(__name__)


async def authenticate_user(session: AsyncSession, email: str, password: str) -> User:
    result = await session.exec(
        select(User).where(User.email == email)
    )
    user = result.first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )

    return user


async def create_new_user(session: AsyncSession, user_create: UserCreate) -> User:
    try:
        logger.info(f"Creating new user with email: {user_create.email}")
        
        result = await session.exec(
            select(User).where(User.email == user_create.email)
        )
        existing_user = result.first()

        if existing_user:
            logger.warning(f"Email already registered: {user_create.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        if user_create.password != user_create.password_confirm:
            logger.warning(f"Password mismatch for email: {user_create.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )

        logger.info("Hashing password...")
        hashed_password = get_password_hash(user_create.password)

        logger.info("Creating user object...")
        db_user = User(
            email=user_create.email,
            name=user_create.name,
            password_hash=hashed_password,
            is_active=True
        )

        logger.info("Adding user to session...")
        session.add(db_user)
        
        logger.info("Committing transaction...")
        await session.commit()
        
        logger.info("Refreshing user object...")
        await session.refresh(db_user)

        logger.info(f"User created successfully with ID: {db_user.id}")
        return db_user
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}", exc_info=True)
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


async def get_user_by_id(session: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
    result = await session.exec(
        select(User).where(User.id == user_id)
    )
    return result.first()


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    result = await session.exec(
        select(User).where(User.email == email)
    )
    return result.first()
