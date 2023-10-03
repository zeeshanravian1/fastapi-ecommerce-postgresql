"""
    Token, Scopes, and Security

    Description:
    - This module is used to create a token for user and get current user.

"""

# Importing Python packages
import logging
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql.selectable import Select


# Importing FastAPI packages
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer

# Importing from project files
from database.session import get_session
from core import UserTokenStatus, core_configuration
from apps.api_v1.user.model import UserTable
from .configuration import TokenType
from .schema import CurrentUserReadSchema


security_logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


async def create_token(data: dict, token_type: TokenType) -> str:
    """
    Create token

    Description:
    - This function is used to create access token and refresh token.

    Parameter:
    - **data** (JSON): Data to be encoded in token. **(Required)**
    - **token_type** (TokenType): Type of token to be created. **(Required)**
        - **Allowed values:** "access_token", "refresh_token"

    Return:
    - **token** (STR): Created token.

    """
    print("Calling create_token method")

    to_encode: dict = data.copy()

    expire_minutes: int = (
        core_configuration.ACCESS_TOKEN_EXPIRE_MINUTES
        if token_type == TokenType.ACCESS_TOKEN
        else core_configuration.REFRESH_TOKEN_EXPIRE_MINUTES
    )

    secret_key: str = (
        core_configuration.ACCESS_TOKEN_SECRET_KEY
        if token_type == TokenType.ACCESS_TOKEN
        else core_configuration.REFRESH_TOKEN_SECRET_KEY
    )

    expire: datetime = datetime.now(tz=timezone.utc) + timedelta(
        minutes=expire_minutes
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        claims=to_encode,
        key=secret_key,
        algorithm=core_configuration.ALGORITHM,
    )


async def get_current_user(
    db_session: AsyncSession = Depends(get_session),
    access_token: str = Depends(oauth2_scheme),
) -> CurrentUserReadSchema:
    """
    Get current user.

    Description:
    - This function is used to get current user.

    Parameter:
    - **db_session** (AsyncSession): Database session. **(Required)**
    - **token** (STR): Encoded token to get current user. **(Required)**

    Return:
    - **user** (CurrentUserReadSchema): User details.

    """
    print("Calling get_current_user method")

    authenticate_value: str = "Bearer"

    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload: dict[str, any] = jwt.decode(
            token=access_token,
            key=core_configuration.ACCESS_TOKEN_SECRET_KEY,
            algorithms=[core_configuration.ALGORITHM],
        )

        user_id: str = payload.get("id")
        user_name: str = payload.get("username")
        user_email: str = payload.get("email")

        if user_name is None or user_email is None:
            raise credentials_exception

    except (JWTError, ValidationError) as err:
        raise credentials_exception from err

    except Exception as err:
        security_logger.exception(msg=err)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while getting current user",
        ) from err

    query: Select = select(UserTable).where(UserTable.id == user_id)
    result: ChunkedIteratorResult = await db_session.execute(statement=query)
    user_data: UserTable = result.scalars().first()

    if not user_data:
        raise credentials_exception

    if user_data.token_status == UserTokenStatus.LOGOUT:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User has been logged out",
            headers={"WWW-Authenticate": authenticate_value},
        )

    current_user: dict = {
        "id": user_data.id,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "contact": user_data.contact,
        "username": user_data.username,
        "email": user_data.email,
        "address": user_data.address,
        "city": user_data.city,
        "state": user_data.state,
        "country": user_data.country,
        "postal_code": user_data.postal_code,
        "role_id": user_data.role_id,
        "role_name": user_data.user_role.role_name,
        "is_active": user_data.is_active,
        "token_status": user_data.token_status,
        "created_at": user_data.created_at,
        "updated_at": user_data.updated_at,
    }

    if user_data.user_role.role_name == core_configuration.SUPERUSER_ROLE:
        return CurrentUserReadSchema.model_validate(obj=current_user)

    return CurrentUserReadSchema(
        **current_user,
        organization_id=user_data.organization_id,
        organization_name=user_data.user_organization.organization_name
    )


async def get_current_active_user(
    current_user: CurrentUserReadSchema = Security(get_current_user),
) -> CurrentUserReadSchema:
    """
    Get current active user.

    Description:
    - This function is used to get current active user.

    Parameter:
    - **current_user** (CurrentUserReadSchema): Current user details.
    **(Required)**

    Return:
    - **user** (CurrentUserReadSchema): User details.

    """
    print("Calling get_current_active_user method")

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return CurrentUserReadSchema.model_validate(obj=current_user)
