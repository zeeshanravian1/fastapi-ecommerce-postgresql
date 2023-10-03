"""
    Authentication Route Module

    Description:
    - This module is responsible for handling auth routes.
    - It is used to login, refresh token, logout user.

"""

# Importing Python Packages
from sqlalchemy.ext.asyncio import AsyncSession

# Importing FastAPI Packages
from fastapi import APIRouter, Depends, Security, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

# Importing Project Files
from database import get_session
from core import CurrentUserReadSchema, get_current_active_user
from apps.email.response_message import email_response_message
from .response_message import auth_response_message
from .schema import (
    RegisterAdminSchema,
    RegisterAdminReadSchema,
    LoginReadSchema,
    RefreshToken,
    RefreshTokenReadSchema,
)
from .view import auth_view


# Router Object to Create Routes
router = APIRouter(prefix="/auth", tags=["Authentication"])


# -----------------------------------------------------------------------------


# Create a single admin user route
@router.post(
    path="/register/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single admin user",
    response_description="Admin user created successfully",
)
async def register_admin_user(
    record: RegisterAdminSchema,
    db_session: AsyncSession = Depends(get_session),
) -> RegisterAdminReadSchema:
    """
    Register a single admin user.

    Description:
    - This method is used to create a single admin user for an organization.

    Parameter:
    Admin user details to be created with following fields:
    - **first_name** (STR): First name of user. **(Required)**
    - **last_name** (STR): Last name of user. **(Required)**
    - **contact** (STR): Contact number of user. **(Optional)**
    - **username** (STR): Username of user. **(Required)**
    - **email** (STR): Email of user. **(Required)**
    - **password** (STR): Password of user. **(Required)**
    - **address** (STR): Address of user. **(Optional)**
    - **city** (STR): City of user. **(Optional)**
    - **state** (STR): State of user. **(Optional)**
    - **country** (STR): Country of user. **(Optional)**
    - **postal_code** (STR): Postal code of user. **(Optional)**
    - **role_id** (INT): Role ID of user. **(Required)**
    - **organization_name** (STR): Name of organization. **(Required)**
    - **organization_description** (STR): Description of organization.
    **(Optional)**

    Return:
    Admin user details along with following information:
    - **id** (INT): Id of user.
    - **first_name** (STR): First name of user.
    - **last_name** (STR): Last name of user.
    - **contact** (STR): Contact number of user.
    - **username** (STR): Username of user.
    - **email** (STR): Email of user.
    - **address** (STR): Address of user.
    - **city** (STR): City of user.
    - **state** (STR): State of user.
    - **country** (STR): Country of user.
    - **postal_code** (STR): Postal code of user.
    - **role_id** (INT): Role ID of user.
    - **is_active** (BOOL): Status of user.
    - **token_status** (STR): Token status of user.
    - **organization_name** (STR): Name of organization.
    - **organization_description** (STR): Description of organization.
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """
    print("Calling register_admin_user method")

    result = await auth_view.register_admin_user(
        db_session=db_session, record=record
    )

    if not isinstance(result, RegisterAdminReadSchema):
        if (
            result.get("detail")
            == auth_response_message.ORGANIZATION_ALREADY_EXISTS
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=auth_response_message.ORGANIZATION_ALREADY_EXISTS,
            )

        if (
            result.get("detail")
            == auth_response_message.USERNAME_ALREADY_EXISTS
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=auth_response_message.USERNAME_ALREADY_EXISTS,
            )

        if result.get("detail") == auth_response_message.EMAIL_ALREADY_EXISTS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=auth_response_message.EMAIL_ALREADY_EXISTS,
            )

        if result.get("detail") == email_response_message.EMAIL_SENT_FAILED:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=email_response_message.EMAIL_SENT_FAILED,
            )

    return RegisterAdminReadSchema.model_validate(obj=result)


# Login route
@router.post(
    path="/login/",
    status_code=status.HTTP_200_OK,
    summary="Perform Authentication",
    response_description="User logged in successfully",
)
async def login(
    db_session: AsyncSession = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> LoginReadSchema:
    """
    Login.

    Description:
    - This route is used to login user.

    Parameter:
    - **email or username** (STR): Email or username of user. **(Required)**
    - **password** (STR): Password of user. **(Required)**

    Return:
    - **token_type** (STR): Token type of user.
    - **access_token** (STR): Access token of user.
    - **refresh_token** (STR): Refresh token of user.
    - **role_id** (INT): Role ID of user.

    """
    print("Calling login method")

    result = await auth_view.login(db_session=db_session, form_data=form_data)

    if not isinstance(result, LoginReadSchema):
        if result.get("detail") == auth_response_message.USER_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=auth_response_message.USER_NOT_FOUND,
            )

        if result.get("detail") == auth_response_message.INCORRECT_PASSWORD:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response_message.INCORRECT_PASSWORD,
            )

    return LoginReadSchema.model_validate(obj=result)


# Refresh token route
@router.post(
    path="/refresh/",
    status_code=status.HTTP_200_OK,
    summary="Refreshes Authentication Token",
    response_description="Token refreshed successfully",
)
async def refresh_token(
    record: RefreshToken, db_session: AsyncSession = Depends(get_session)
) -> RefreshTokenReadSchema:
    """
    Refresh Token.

    Description:
    - This route is used to refresh token.

    Parameter:
    - **record** (STR): Refresh token of user. **(Required)**

    Return:
    - **token_type** (STR): Token type of user.
    - **access_token** (STR): Access token of user.

    """
    print("Calling refresh_token method")

    result = await auth_view.refresh_token(
        db_session=db_session, record=record
    )

    if not isinstance(result, RefreshTokenReadSchema):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=auth_response_message.USER_NOT_FOUND,
        )

    return RefreshTokenReadSchema.model_validate(obj=result)


# Logout route
@router.post(
    path="/logout/",
    status_code=status.HTTP_200_OK,
    summary="Perform Logout",
    response_description="User logged out successfully",
)
async def logout(
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> dict:
    """
    Logout.

    Description:
    - This route is used to logout user.

    Parameter:
    - **None**

    Return:
    - **detail** (STR): User logged out successfully.

    """
    print("Calling logout method")

    result = await auth_view.logout(
        db_session=db_session, user_id=current_user.id
    )

    if result.get("detail") == auth_response_message.USER_NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=auth_response_message.USER_NOT_FOUND,
        )

    return {"detail": auth_response_message.USER_LOGGED_OUT}
