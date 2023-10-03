"""
    User View Module

    Description:
    - This module is responsible for user views.

"""

# Importing Python Packages
from passlib.hash import pbkdf2_sha256
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from sqlalchemy.sql.dml import Update

# Importing FastAPI Packages

# Importing Project Files
from core import UserTokenStatus, core_configuration
from apps.base import BaseView
from apps.email.configuration import email_configuration
from apps.email.response_message import email_response_message
from apps.email.helper import send_email_otp
from apps.email.schema import EmailBaseSchema
from .configuration import user_configuration
from .response_message import user_response_message
from .model import UserTable
from .schema import (
    UserCreateSchema,
    UserUpdateSchema,
    PasswordChangeSchema,
    PasswordResetRequestSchema,
    PasswordResetSchema,
    PasswordResetReadSchema,
)


# -----------------------------------------------------------------------------


# User class
class UserView(
    BaseView[
        UserTable,
        UserCreateSchema,
        UserUpdateSchema,
    ]
):
    """
    User View Class

    Description:
    - This class is responsible for user views.

    """

    def __init__(
        self,
        model: UserTable,
    ):
        """
        User View Class Initialization

        Description:
        - This method is responsible for initializing class.

        Parameter:
        - **model** (UserTable): User Database Model.

        """

        super().__init__(model=model)

    async def create(
        self, db_session: AsyncSession, record: UserCreateSchema
    ) -> UserTable:
        """
        Create User

        Description:
        - This method is responsible for creating a user.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record** (UserCreateSchema): User create schema. **(Required)**

        Return:
        - **record** (UserTable): UserTable object.

        """

        record.password = pbkdf2_sha256.hash(record.password)

        return await super().create(db_session=db_session, record=record)

    async def password_change(
        self,
        db_session: AsyncSession,
        record_id: int,
        record: PasswordChangeSchema,
    ) -> dict:
        """
        Change Password

        Description:
        - This method is responsible for changing user password.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record_id** (INT): Id of user. **(Required)**
        - **record** (PasswordChangeSchema): Password change schema.
        **(Required)**

        Return:
        - **detail** (STR): Password changed successfully.

        """

        result = await super().read_by_id(
            db_session=db_session, record_id=record_id
        )

        if not result:
            return {"detail": user_response_message.USER_NOT_FOUND}

        if not pbkdf2_sha256.verify(record.old_password, result.password):
            return {"detail": user_response_message.INCORRECT_PASSWORD}

        query: Update = (
            update(self.model)
            .where(self.model.id == record_id)
            .values(password=pbkdf2_sha256.hash(record.new_password))
        )
        await db_session.execute(statement=query)
        await db_session.commit()

        return {"detail": user_response_message.PASSWORD_CHANGED}

    async def password_reset_request(
        self,
        db_session: AsyncSession,
        record: PasswordResetRequestSchema,
    ) -> dict:
        """
        Password Reset Request

        Description:
        - This method is used to request password reset.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record** (PasswordResetRequestSchema): Password reset request
        schema. **(Required)**

        Return:
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

        # Send Email
        email_response = await send_email_otp(
            record=EmailBaseSchema(
                email=record.email,
                subject=email_configuration.EMAIL_PASSWORD_RESET_SUBJECT,
                email_purpose=email_configuration.EMAIL_PASSWORD_RESET_PURPOSE,
                user_name=f"{result.first_name} {result.last_name}",
            )
        )

        if not email_response.get("success"):
            return {"detail": email_response_message.EMAIL_SENT_FAILED}

        query: Update = (
            update(UserTable)
            .where(UserTable.id == result.id)
            .values(
                password_otp=email_response.get("otp_code"),
                token_status=UserTokenStatus.PASSWORD_RESET,
            )
        )
        await db_session.execute(statement=query)
        await db_session.commit()

        return email_response

    async def password_reset(
        self,
        db_session: AsyncSession,
        record: PasswordResetSchema,
    ) -> PasswordResetReadSchema:
        """
        Password Reset

        Description:
        - This method is used to reset password.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **token** (STR): Password reset token. **(Required)**

        Return:
        - **detail** (STR): Password changed status.

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

        # Check if OTP Code is valid
        if result.password_otp != token_data.get("otp_code"):
            return {"detail": email_response_message.INCORRECT_OTP_CODE}

        query: Update = (
            update(UserTable)
            .where(UserTable.id == result.id)
            .values(
                password_otp=None,
                token_status=UserTokenStatus.LOGIN,
            )
        )
        await db_session.execute(statement=query)
        await db_session.commit()

        return PasswordResetReadSchema(
            detail=user_response_message.PASSWORD_RESET,
        )


user_view = UserView(model=UserTable)
