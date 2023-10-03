"""
    User Route Module

    Description:
    - This module is responsible for handling user routes.
    - It is used to create, get, update, delete user details.

"""

# Importing Python Packages
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

# Importing FastAPI Packages
from fastapi import APIRouter, Depends, Security, status
from fastapi.exceptions import HTTPException

# Importing Project Files
from database import get_session
from core import CurrentUserReadSchema, get_current_active_user
from apps.email.response_message import email_response_message
from apps.email.schema import EmailSentSchema
from .configuration import user_configuration
from .response_message import user_response_message
from .model import UserTable
from .schema import (
    UserCreateSchema,
    UserReadSchema,
    UserPaginationReadSchema,
    UserUpdateSchema,
    UserPartialUpdateSchema,
    PasswordChangeSchema,
    PasswordChangeReadSchema,
    PasswordResetRequestSchema,
    PasswordResetSchema,
    PasswordResetReadSchema,
)
from .view import user_view

# Router Object to Create Routes
router = APIRouter(prefix="/user", tags=["User"])


# -----------------------------------------------------------------------------


# Create a single user route
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single user",
    response_description="User created successfully",
)
async def create_user(
    record: UserCreateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> UserReadSchema:
    """
    Create a single user

    Description:
    - This route is used to create a single user.

    Parameter:
    User details to be created with following fields:
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

    Return:
    User details along with following information:
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
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """
    print("Calling create_user method")

    result: UserTable = await user_view.create(
        db_session=db_session, record=record
    )

    return UserReadSchema.model_validate(obj=result)


# Get a single user by id route
@router.get(
    path="/{user_id}/",
    status_code=status.HTTP_200_OK,
    summary="Get a single user by providing id",
    response_description="User details fetched successfully",
)
async def get_user_by_id(
    user_id: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> UserReadSchema:
    """
    Get a single user

    Description:
    - This route is used to get a single user by providing id.

    Parameter:
    - **user_id** (INT): ID of user to be fetched. **(Required)**

    Return:
    Get a single user with following information:
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
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """
    print("Calling get_user_by_id method")

    result: UserTable = await user_view.read_by_id(
        db_session=db_session, record_id=user_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    return UserReadSchema.model_validate(obj=result)


# Get a single user by username route
@router.get(
    path="/username/{username}/",
    status_code=status.HTTP_200_OK,
    summary="Get a single user by providing username",
    response_description="User details fetched successfully",
)
async def get_user_by_username(
    username: str,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> UserReadSchema:
    """
    Get a single user

    Description:
    - This route is used to get a single user by providing username.

    Parameter:
    - **username** (STR): Username of user to be fetched. **(Required)**

    Return:
    Get a single user with following information:
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
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """
    print("Calling get_user_by_username method")

    result: UserTable = await user_view.read_by_value(
        db_session=db_session,
        column_name=user_configuration.USER_COLUMN_USERNAME,
        column_value=username,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    return UserReadSchema.model_validate(obj=result)


# Get a single user by email route
@router.get(
    path="/email/{email}/",
    status_code=status.HTTP_200_OK,
    summary="Get a single user by providing email",
    response_description="User details fetched successfully",
)
async def get_user_by_email(
    email: EmailStr,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> UserReadSchema:
    """
    Get a single user

    Description:
    - This route is used to get a single user by providing email.

    Parameter:
    - **email** (STR): Email of user to be fetched. **(Required)**

    Return:
    Get a single user with following information:
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
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """
    print("Calling get_user_by_email method")

    result: UserTable = await user_view.read_by_value(
        db_session=db_session,
        column_name=user_configuration.USER_COLUMN_EMAIL,
        column_value=email,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    return UserReadSchema.model_validate(obj=result)


# Get all users route
@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Get all users",
    response_description="All users fetched successfully",
)
async def get_all_users(
    page: int | None = None,
    limit: int | None = None,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> UserPaginationReadSchema:
    """
    Get all users

    Description:
    - This route is used to get all users.

    Parameter:
    - **page** (INT): Page number to be fetched. **(Optional)**
    - **limit** (INT): Number of records to be fetched per page. **(Optional)**

    Return:
    Get all users with following information:
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
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """
    print("Calling get_all_users method")

    result: dict = await user_view.read_all(
        db_session=db_session, page=page, limit=limit
    )

    return UserPaginationReadSchema.model_validate(obj=result)


# Update a single user route
@router.put(
    path="/{user_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a single user by providing id",
    response_description="User updated successfully",
)
async def update_user(
    user_id: int,
    record: UserUpdateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> UserReadSchema:
    """
    Update a single user

    Description:
    - This route is used to update a single user by providing id.

    Parameter:
    - **user_id** (INT): ID of user to be updated. **(Required)**
    User details to be updated with following fields:
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
    - **is_active** (BOOL): Status of user. **(Required)**

    Return:
    User details along with following information:
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
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """
    print("Calling update_user method")

    result: UserTable = await user_view.update(
        db_session=db_session, record_id=user_id, record=record
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    return UserReadSchema.model_validate(obj=result)


# Partial update a single user route
@router.patch(
    path="/{user_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Partial update a single user by providing id",
    response_description="User updated successfully",
)
async def partial_update_user(
    user_id: int,
    record: UserPartialUpdateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> UserReadSchema:
    """
    Partial update a single user

    Description:
    - This route is used to partial update a single user by providing id.

    Parameter:
    - **user_id**: ID of user to be updated. (INT) **(Required)**
    User details to be updated with following fields:
    - **first_name** (STR): First name of user. **(Optional)**
    - **last_name** (STR): Last name of user. **(Optional)**
    - **contact** (STR): Contact number of user. **(Optional)**
    - **username** (STR): Username of user. **(Optional)**
    - **email** (STR): Email of user. **(Optional)**
    - **password** (STR): Password of user. **(Optional)**
    - **address** (STR): Address of user. **(Optional)**
    - **city** (STR): City of user. **(Optional)**
    - **state** (STR): State of user. **(Optional)**
    - **country** (STR): Country of user. **(Optional)**
    - **postal_code** (STR): Postal code of user. **(Optional)**
    - **role_id** (INT): Role ID of user. **(Optional)**
    - **is_active** (BOOL): Status of user. **(Optional)**

    Return:
    User details along with following information:
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
    - **created_at** (DATETIME): Datetime of user creation.
    - **updated_at** (DATETIME): Datetime of user updation.

    """
    print("Calling partial_update_user method")

    result: UserTable = await user_view.update(
        db_session=db_session, record_id=user_id, record=record
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    return UserReadSchema.model_validate(obj=result)


# Delete a single user route
@router.delete(
    path="/{user_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single user by providing id",
    response_description="User deleted successfully",
)
async def delete_user(
    user_id: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> None:
    """
    Delete a single user

    Description:
    - This route is used to delete a single user by providing id.

    Parameter:
    - **user_id** (INT): ID of user to be deleted. **(Required)**

    Return:
    - **None**

    """
    print("Calling delete_user method")

    result: UserTable = await user_view.delete(
        db_session=db_session, record_id=user_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )


# Change password of a single user route
@router.post(
    path="/change-password/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Change password of a single user",
    response_description="Password changed successfully",
)
async def password_change(
    record: PasswordChangeSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> PasswordChangeReadSchema:
    """
    Change password of a single user

    Description:
    - This route is used to change password of a single user.

    Parameter:
    - **old_password** (STR): Old password of user. **(Required)**
    - **new_password** (STR): New password of user. **(Required)**

    Return:
    - **detail** (STR): Password changed successfully.

    """
    print("Calling password_change method")

    result: UserTable = await user_view.password_change(
        db_session=db_session, record_id=current_user.id, record=record
    )

    if result.get("detail") == user_response_message.USER_NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    if result.get("detail") == user_response_message.INCORRECT_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=user_response_message.INCORRECT_PASSWORD,
        )

    return PasswordChangeReadSchema.model_validate(obj=result)


# Password reset request route
@router.post(
    path="/password-reset-request/",
    status_code=status.HTTP_200_OK,
    summary="Request password reset",
    response_description=email_response_message.EMAIL_SENT,
)
async def password_reset_request(
    record: PasswordResetRequestSchema,
    db_session: AsyncSession = Depends(get_session),
) -> EmailSentSchema:
    """
    Password Reset Request

    Description:
    - This route is used to request password reset.

    Parameter:
    Request password reset details with following fields:
    - **email** (STR): Email of user to be verified. **(Required)**

    Return:
    - **detail** (STR): Email sent successfully at given email address.

    """
    print("Calling password_reset_request method")

    result: dict = await user_view.password_reset_request(
        db_session=db_session, record=record
    )

    if result.get("detail") == user_response_message.USER_NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    if result.get("detail") == email_response_message.EMAIL_SENT_FAILED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=email_response_message.EMAIL_SENT_FAILED,
        )

    return EmailSentSchema.model_validate(obj=result)


# Password reset route
@router.post(
    path="/password-reset/",
    status_code=status.HTTP_200_OK,
    summary="Password reset",
    response_description=user_response_message.PASSWORD_RESET,
)
async def password_reset(
    record: PasswordResetSchema,
    db_session: AsyncSession = Depends(get_session),
) -> PasswordResetReadSchema:
    """
    Reset Password

    Description:
    - This route is used to reset password.

    Parameter:
    Reset password details with following fields:
    - **token** (STR): Password reset token. **(Required)**

    Return:
    - **detail** (STR): Reset password status.

    """
    print("Calling password_reset method")

    result: PasswordResetReadSchema = await user_view.password_reset(
        db_session=db_session, record=record
    )

    if not isinstance(result, PasswordResetReadSchema):
        if result.get("detail") == user_response_message.USER_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=user_response_message.USER_NOT_FOUND,
            )

        if result.get("detail") == email_response_message.INCORRECT_OTP_CODE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=email_response_message.INCORRECT_OTP_CODE,
            )

    return PasswordChangeReadSchema.model_validate(obj=result)
