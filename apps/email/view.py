"""
    Email View Module

    Description:
    - This module is responsible for email views.

"""

# Importing Python Packages
from jose import jwt
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.dml import Update

# Importing FastAPI Packages

# Importing Project Files
from core import UserTokenStatus, TokenType, core_configuration, create_token
from apps.base import BaseView
from apps.auth.configuration import auth_configuration
from apps.api_v1.user.configuration import user_configuration
from apps.api_v1.user.response_message import user_response_message
from apps.api_v1.user.model import UserTable
from apps.api_v1.user.schema import UserCreateSchema, UserUpdateSchema
from .configuration import email_configuration
from .response_message import email_response_message
from .helper import send_email_otp
from .schema import (
    EmailVerifyRequestSchema,
    EmailBaseSchema,
    EmailVerifySchema,
    EmailVerifyReadSchema,
)


# -----------------------------------------------------------------------------


# Email class
class EmailView(
    BaseView[
        UserTable,
        UserCreateSchema,
        UserUpdateSchema,
    ]
):
    """
    Email View Class

    Description:
    - This class is responsible for email views.

    """

    def __init__(
        self,
        model: UserTable,
    ):
        """
        Email View Class Initialization

        Description:
        - This method is responsible for initializing class.

        Parameter:
        - **model** (UserTable): User Database Model.

        """

        super().__init__(model=model)

    async def email_verify_request(
        self, db_session: AsyncSession, record=EmailVerifyRequestSchema
    ) -> dict:
        """
        Email Verify Request

        Description:
        - This method is used to send email verification request to user.

        Parameters:
        - **email** (STR): Email of user to be verified. **(Required)**

        Returns:
        - **detail** (DICT): Details of email sent.

        """

        # Check if user exists
        result: UserTable = await super().read_by_value(
            db_session=db_session,
            column_name=user_configuration.USER_COLUMN_EMAIL,
            column_value=record.email,
        )

        if not result:
            return {"detail": user_response_message.USER_NOT_FOUND}

        # Check if user is verified
        if result.email_verified:
            return {"detail": email_response_message.USER_ALREADY_VERIFIED}

        # Send Email
        email_response = await send_email_otp(
            record=EmailBaseSchema(
                email=record.email,
                subject=email_configuration.EMAIL_VERIFY_SUBJECT,
                email_purpose=email_configuration.EMAIL_VERIFY_PURPOSE,
                user_name=f"{result.first_name} {result.last_name}",
            )
        )

        if not email_response.get("success"):
            return {"detail": email_response_message.EMAIL_SENT_FAILED}

        query: Update = (
            update(UserTable)
            .where(UserTable.id == result.id)
            .values(
                email_otp=email_response.get("otp_code"),
                token_status=UserTokenStatus.EMAIL_VERIFY,
            )
        )
        await db_session.execute(statement=query)
        await db_session.commit()

        return email_response

    async def email_verify(
        self, db_session: AsyncSession, record=EmailVerifySchema
    ) -> EmailVerifyReadSchema:
        """
        Email Verify

        Description:
        - This method is used to verify email of user.

        Parameters:
        - **db_session** (Session): Database session. **(Required)**
        - **token** (STR): Email verify token. **(Required)**

        Returns:
        Email verify data with following fields:
        - **detail** (STR): Email verified status.
        - **token_type** (STR): Token type.
        - **access_token** (STR): Access token.
        - **refresh_token** (STR): Refresh token.
        - **role_id** (INT): Role id.

        """

        # Decode OTP Code
        token_data = jwt.decode(
            token=record.token,
            key=core_configuration.OTP_CODE_SECRET_KEY,
            algorithms=[core_configuration.ALGORITHM],
        )

        # Check if user exists
        result: UserTable = await super().read_by_value(
            db_session=db_session,
            column_name=user_configuration.USER_COLUMN_EMAIL,
            column_value=token_data.get("email"),
        )

        if not result:
            return {"detail": user_response_message.USER_NOT_FOUND}

        # Check if user is verified
        if result.email_verified:
            return {"detail": email_response_message.USER_ALREADY_VERIFIED}

        # Check if OTP Code is valid
        if result.email_otp != token_data.get("token"):
            return {"detail": email_response_message.INCORRECT_OTP_CODE}

        data = {
            "id": result.id,
            "username": result.username,
            "email": result.email,
        }

        access_token: str = await create_token(
            data=data, token_type=TokenType.ACCESS_TOKEN
        )

        refresh_token: str = await create_token(
            data=data, token_type=TokenType.REFRESH_TOKEN
        )

        query: Update = (
            update(UserTable)
            .where(UserTable.id == result.id)
            .values(
                email_otp=None,
                email_verified=True,
                is_active=True,
                token_status=UserTokenStatus.LOGIN,
            )
        )
        await db_session.execute(statement=query)
        await db_session.commit()

        return EmailVerifyReadSchema(
            detail=email_response_message.EMAIL_VERIFIED,
            token_type=auth_configuration.TOKEN_TYPE,
            access_token=access_token,
            refresh_token=refresh_token,
            role_id=result.role_id,
        )


email_view = EmailView(model=UserTable)
