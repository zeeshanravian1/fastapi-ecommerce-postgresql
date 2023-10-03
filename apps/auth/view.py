"""
    Authentication View Module

    Description:
    - This module is responsible for auth views.

"""

# Importing Python Packages
from jose import jwt
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.dml import Update, Delete

# Importing FastAPI Packages
from fastapi.security import OAuth2PasswordRequestForm

# Importing Project Files
from core import UserTokenStatus, TokenType, core_configuration, create_token
from apps.base import BaseView
from apps.email.configuration import email_configuration
from apps.email.response_message import email_response_message
from apps.email.helper import send_email_otp
from apps.email.schema import EmailBaseSchema
from apps.api_v1.organization.model import OrganizationTable
from apps.api_v1.user.model import UserTable
from apps.api_v1.user.schema import UserCreateSchema, UserUpdateSchema
from .configuration import auth_configuration
from .response_message import auth_response_message
from .schema import (
    RegisterAdminSchema,
    RegisterAdminReadSchema,
    LoginReadSchema,
    RefreshToken,
    RefreshTokenReadSchema,
)


# -----------------------------------------------------------------------------


# Authentication class
class AuthView(
    BaseView[
        UserTable,
        UserCreateSchema,
        UserUpdateSchema,
    ]
):
    """
    Authentication View Class

    Description:
    - This class is responsible for auth views.

    """

    def __init__(
        self,
        model: UserTable,
    ):
        """
        Authentication View Class Initialization

        Description:
        - This method is responsible for initializing class.

        Parameter:
        - **model** (UserTable): User Database Model.

        """

        super().__init__(model=model)

    async def register_admin_user(
        self, db_session: AsyncSession, record=RegisterAdminSchema
    ) -> RegisterAdminReadSchema:
        """
        Register a single admin user.

        Description:
        - This method is used to create a single admin user for an
        organization.

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

        # Verify if organization or Admin already created
        query: Select = select(OrganizationTable).where(
            OrganizationTable.organization_name == record.organization_name
        )
        result: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )
        organization_data: UserTable = result.scalars().first()

        if organization_data:
            return {
                "detail": auth_response_message.ORGANIZATION_ALREADY_EXISTS
            }

        query: Select = select(UserTable).where(
            or_(
                UserTable.username == record.username,
                UserTable.email == record.email,
            )
        )
        result: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )
        user_data: UserTable = result.scalars().first()

        if user_data:
            if user_data.username == record.username:
                return {
                    "detail": auth_response_message.USERNAME_ALREADY_EXISTS
                }

            if user_data.email == record.email:
                return {"detail": auth_response_message.EMAIL_ALREADY_EXISTS}

        # Create Organization
        organization_record: OrganizationTable = OrganizationTable(
            organization_name=record.organization_name,
            organization_description=record.organization_description,
        )
        db_session.add(instance=organization_record)
        await db_session.commit()
        await db_session.refresh(instance=organization_record)

        email_otp_response = await send_email_otp(
            record=EmailBaseSchema(
                subject=email_configuration.EMAIL_VERIFY_SUBJECT,
                email_purpose=email_configuration.EMAIL_VERIFY_PURPOSE,
                user_name=f"{record.first_name} {record.last_name}",
                email=record.email,
            )
        )

        if not email_otp_response.get("success"):
            query: Delete = delete(OrganizationTable).where(
                OrganizationTable.id == organization_record.id
            )
            await db_session.execute(statement=query)
            await db_session.commit()

            return {
                "detail": email_response_message.EMAIL_SENT_FAILED,
            }

        # Create Admin User
        user_record: UserTable = UserTable(
            first_name=record.first_name,
            last_name=record.last_name,
            contact=record.contact,
            username=record.username,
            email=record.email,
            password=pbkdf2_sha256.hash(record.password),
            address=record.address,
            city=record.city,
            state=record.state,
            country=record.country,
            postal_code=record.postal_code,
            email_otp=email_otp_response.get("otp_code"),
            role_id=record.role_id,
            organization_id=organization_record.id,
        )

        db_session.add(instance=user_record)
        await db_session.commit()
        await db_session.refresh(instance=user_record)

        return RegisterAdminReadSchema(
            id=user_record.id,
            first_name=user_record.first_name,
            last_name=user_record.last_name,
            contact=user_record.contact,
            username=user_record.username,
            email=user_record.email,
            address=user_record.address,
            city=user_record.city,
            state=user_record.state,
            country=user_record.country,
            postal_code=user_record.postal_code,
            role_id=user_record.role_id,
            is_active=user_record.is_active,
            token_status=user_record.token_status,
            organization_name=organization_record.organization_name,
            organization_description=organization_record.organization_description,
            created_at=user_record.created_at,
            updated_at=user_record.updated_at,
        )

    async def login(
        self, db_session: AsyncSession, form_data: OAuth2PasswordRequestForm
    ) -> LoginReadSchema:
        """
        Login.

        Description:
        - This method is responsible for login user.

        Parameter:
        - **email or username** (STR): Email or username of user.
        **(Required)**
        - **password** (STR): Password of user. **(Required)**

        Return:
        - **token_type** (STR): Token type of user.
        - **access_token** (STR): Access token of user.
        - **refresh_token** (STR): Refresh token of user.

        """

        form_data.username = form_data.username.lower()

        query: Select = select(UserTable).where(
            or_(
                UserTable.username == form_data.username,
                UserTable.email == form_data.username,
            )
        )
        result: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )
        user_data: UserTable = result.scalars().first()

        if not user_data:
            return {"detail": auth_response_message.USER_NOT_FOUND}

        if not pbkdf2_sha256.verify(form_data.password, user_data.password):
            return {"detail": auth_response_message.INCORRECT_PASSWORD}

        data = {
            "id": user_data.id,
            "username": user_data.username,
            "email": user_data.email,
        }

        access_token: str = await create_token(
            data=data, token_type=TokenType.ACCESS_TOKEN
        )

        refresh_token: str = await create_token(
            data=data, token_type=TokenType.REFRESH_TOKEN
        )

        query: Update = (
            update(UserTable)
            .where(UserTable.id == user_data.id)
            .values(token_status=UserTokenStatus.LOGIN)
        )
        await db_session.execute(statement=query)
        await db_session.commit()

        return LoginReadSchema(
            token_type=auth_configuration.TOKEN_TYPE,
            access_token=access_token,
            refresh_token=refresh_token,
            role_id=user_data.role_id,
        )

    async def refresh_token(
        self, db_session: AsyncSession, record: RefreshToken
    ) -> RefreshTokenReadSchema:
        """
        Refresh Token.

        Description:
        - This method is responsible for refresh token.

        Parameter:
        - **record** (STR): Refresh token of user. **(Required)**

        Return:
        - **token_type** (STR): Token type of user.
        - **access_token** (STR): Access token of user.

        """

        data = jwt.decode(
            token=record.refresh_token,
            key=core_configuration.REFRESH_TOKEN_SECRET_KEY,
            algorithms=[core_configuration.ALGORITHM],
        )

        result = await super().read_by_id(
            db_session=db_session, record_id=data.get("id")
        )

        if not result:
            return {"detail": auth_response_message.USER_NOT_FOUND}

        return RefreshTokenReadSchema(
            token_type=TokenType.ACCESS_TOKEN,
            access_token=await create_token(
                data=data, token_type=TokenType.ACCESS_TOKEN
            ),
        )

    async def logout(self, db_session: AsyncSession, user_id: int) -> dict:
        """
        Logout.

        Description:
        - This method is responsible for logout user.

        Parameter:
        - **user_id** (INT): ID of user. **(Required)**

        Return:
        - **detail** (STR): User logged out successfully.

        """

        result = await super().read_by_id(
            db_session=db_session, record_id=user_id
        )

        if not result:
            return {"detail": auth_response_message.USER_NOT_FOUND}

        query: Update = (
            update(UserTable)
            .where(UserTable.id == user_id)
            .values(token_status=UserTokenStatus.LOGOUT)
        )
        await db_session.execute(statement=query)
        await db_session.commit()

        return {"detail": auth_response_message.USER_LOGGED_OUT}


auth_view = AuthView(model=UserTable)
