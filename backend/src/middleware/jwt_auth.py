# from fastapi import HTTPException, Depends, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemySession
# from src.database.connection import get_session
# from src.models.user import User
# from sqlalchemy.future import select
# import os
# from datetime import datetime, timezone, timedelta
# from typing import Optional
# import uuid
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from dotenv import load_dotenv

# load_dotenv()

# security = HTTPBearer()
# SECRET_KEY = os.getenv("JWT_SECRET", "your-default-secret-key-change-in-production")
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


# # Create a global context for password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password: str) -> str:
#     # Bcrypt has a password length limit of 72 bytes, so truncate if necessary
#     truncated_password = password[:72] if len(password) > 72 else password
#     return pwd_context.hash(truncated_password)


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     """
#     Create a new access token with the provided data
#     """
#     to_encode = data.copy()

#     # Add expiration if not provided
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         # Default to 30 minutes
#         expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
#     session: AsyncSession = Depends(get_session)
# ) -> User:
#     """
#     Get the current user from the JWT token in the Authorization header
#     """
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: str = payload.get("sub")

#         if user_id is None:
#             raise credentials_exception

#         # Convert user_id to UUID if it's a string
#         try:
#             user_id_uuid = uuid.UUID(user_id)
#         except ValueError:
#             raise credentials_exception

#     except JWTError:
#         raise credentials_exception

#     # Query for the user
#     statement = select(User).where(User.id == user_id_uuid)
#     result = await session.execute(statement)
#     user = result.scalar_one_or_none()

#     if user is None:
#         raise credentials_exception

#     if not user.is_active:
#         raise HTTPException(status_code=401, detail="Inactive user")

#     return user


# def verify_token(token: str) -> Optional[dict]:
#     """
#     Verify a JWT token and return the payload if valid
#     """
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         return None




from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.database.connection import get_session
from src.models.user import User
import os
from datetime import datetime, timezone, timedelta
from typing import Optional
import uuid
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET", "your-default-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    truncated = plain_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(truncated, hashed_password)

def get_password_hash(password: str) -> str:
    truncated = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(truncated)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc) + expires_delta
        if expires_delta
        else datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception

        user_id_uuid = uuid.UUID(user_id)

    except Exception:
        raise credentials_exception

    result = await session.exec(
        select(User).where(User.id == user_id_uuid)
    )
    user = result.first()

    if not user:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")

    return user


def verify_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
