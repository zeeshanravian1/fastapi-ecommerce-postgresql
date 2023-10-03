"""
    Email Route Module

    Description:
    - This module is responsible for handling email routes.
    - It is used to email verify request, email verify token request details.

"""

# Importing Python Packages
from sqlalchemy.ext.asyncio import AsyncSession

# Importing FastAPI Packages
from fastapi import APIRouter, Depends, HTTPException, status

# Importing Project Files
from database import get_session
from apps.api_v1.user.response_message import user_response_message
from .response_message import email_response_message
from .schema import (
    EmailVerifyRequestSchema,
    EmailSentSchema,
    EmailVerifySchema,
    EmailVerifyReadSchema,
)
from .view import email_view

# Router Object to Create Routes
router = APIRouter(prefix="/email", tags=["Email"])


# -----------------------------------------------------------------------------


# Email verify request route
@router.post(
    path="/verify-request/",
    status_code=status.HTTP_200_OK,
    summary="Request Verify Email",
    response_description=email_response_message.EMAIL_SENT,
)
async def email_verify_request(
    record: EmailVerifyRequestSchema,
    db_session: AsyncSession = Depends(get_session),
) -> EmailSentSchema:
    """
    Email Verify Request

    Description:
    - This route is used to request email verification.

    Parameter:
    Request email verification details with following fields:
    - **email** (STR): Email of user to be verified. **(Required)**

    Return:
    - **detail** (STR): Email sent successfully at given email address.

    """
    print("Calling email_verify_request method")

    result: dict = await email_view.email_verify_request(
        db_session=db_session, record=record
    )

    if result.get("detail") == user_response_message.USER_NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=user_response_message.USER_NOT_FOUND,
        )

    if result.get("detail") == email_response_message.USER_ALREADY_VERIFIED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=email_response_message.USER_ALREADY_VERIFIED,
        )

    if result.get("detail") == email_response_message.EMAIL_SENT_FAILED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=email_response_message.EMAIL_SENT_FAILED,
        )

    return EmailSentSchema.model_validate(obj=result)


# Email verify route
@router.post(
    path="/verify/",
    status_code=status.HTTP_200_OK,
    summary="Verify email",
    response_description=email_response_message.EMAIL_VERIFIED,
)
async def email_verify(
    record: EmailVerifySchema,
    db_session: AsyncSession = Depends(get_session),
) -> EmailVerifyReadSchema:
    """
    Email Verify

    Description:
    - This route is used to verify email.

    Parameter:
    Email verify details with following fields:
    - **token** (STR): Email verify token. **(Required)**

    Return:
    - **detail** (STR): Email verified status.
    - **token_type** (STR): Token type.
    - **access_token** (STR): Access token.
    - **refresh_token** (STR): Refresh token.
    - **role_id** (INT): Role id.

    """
    print("Calling email_verify method")

    result: EmailVerifyReadSchema = await email_view.email_verify(
        db_session=db_session, record=record
    )

    if not isinstance(result, EmailVerifyReadSchema):
        if result.get("detail") == user_response_message.USER_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=user_response_message.USER_NOT_FOUND,
            )

        if (
            result.get("detail")
            == email_response_message.USER_ALREADY_VERIFIED
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=email_response_message.USER_ALREADY_VERIFIED,
            )

        if result.get("detail") == email_response_message.INCORRECT_OTP_CODE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=email_response_message.INCORRECT_OTP_CODE,
            )

    return EmailVerifyReadSchema.model_validate(obj=result)
