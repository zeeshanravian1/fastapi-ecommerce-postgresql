"""
    User Pydantic Schemas

    Description:
    - This module contains all user schemas used by API.

"""

# Importing Python Packages
from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_settings import SettingsConfigDict

# Importing FastAPI Packages

# Importing Project Files
from core import UserTokenStatus
from apps.base import BaseReadSchema, BasePaginationReadSchema
from .configuration import user_configuration
from .response_message import user_response_message
from .helper import (
    names_validator,
    contact_validator,
    username_validator,
    lowercase_email,
    password_validator,
)


# -----------------------------------------------------------------------------


class UserBaseSchema(BaseModel):
    """
    User Base Schema

    Description:
    - This schema is used to validate user base data passed to API.

    """

    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=user_configuration.FIRST_NAME,
    )
    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=user_configuration.LAST_NAME,
    )
    contact: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=user_configuration.CONTACT,
    )
    username: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=user_configuration.USERNAME,
    )
    email: EmailStr | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=user_configuration.EMAIL,
    )
    address: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=user_configuration.ADDRESS,
    )
    city: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=user_configuration.CITY,
    )
    state: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=user_configuration.STATE,
    )
    country: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=user_configuration.COUNTRY,
    )
    postal_code: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=user_configuration.POSTAL_CODE,
    )
    role_id: int | None = Field(
        default=None,
        ge=1,
        example=user_configuration.ROLE_ID,
    )

    # Custom Validators
    first_name_validator = field_validator("first_name")(names_validator)
    last_name_validator = field_validator("last_name")(names_validator)
    contact_validator = field_validator("contact")(contact_validator)
    username_validator = field_validator("username")(username_validator)
    email_validator = field_validator("email")(lowercase_email)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class UserCreateSchema(UserBaseSchema):
    """
    User create Schema

    Description:
    - This schema is used to validate user creation data passed to API.

    """

    first_name: str = Field(
        min_length=1,
        max_length=2_55,
        example=user_configuration.FIRST_NAME,
    )
    last_name: str = Field(
        min_length=1,
        max_length=2_55,
        example=user_configuration.LAST_NAME,
    )
    username: str = Field(
        min_length=1,
        max_length=2_55,
        example=user_configuration.USERNAME,
    )
    email: EmailStr = Field(
        min_length=1,
        max_length=2_55,
        example=user_configuration.EMAIL,
    )
    password: str = Field(
        min_length=8,
        max_length=1_00,
        example=user_configuration.PASSWORD,
    )
    role_id: int = Field(
        ge=1,
        example=user_configuration.ROLE_ID,
    )

    # Custom Validators
    password_validator = field_validator("password")(password_validator)


class UserReadSchema(UserBaseSchema, BaseReadSchema):
    """
    User Read Schema

    Description:
    - This schema is used to validate user data returned by API.

    """

    is_active: bool = Field(example=user_configuration.IS_ACTIVE)
    token_status: UserTokenStatus = Field(example=UserTokenStatus.LOGOUT)


class UserPaginationReadSchema(BasePaginationReadSchema):
    """
    User Pagination Read Schema

    Description:
    - This schema is used to validate user pagination data returned by API.

    """

    records: list[UserReadSchema]


class UserUpdateSchema(UserBaseSchema):
    """
    User Update Schema

    Description:
    - This schema is used to validate user update data passed to API.

    """

    first_name: str = Field(
        min_length=1,
        max_length=2_55,
        example=user_configuration.FIRST_NAME,
    )
    last_name: str = Field(
        min_length=1,
        max_length=2_55,
        example=user_configuration.LAST_NAME,
    )
    username: str = Field(
        min_length=1,
        max_length=2_55,
        example=user_configuration.USERNAME,
    )
    email: EmailStr = Field(
        min_length=1,
        max_length=2_55,
        example=user_configuration.EMAIL,
    )
    role_id: int = Field(
        ge=1,
        example=user_configuration.ROLE_ID,
    )
    is_active: bool = Field(example=user_configuration.IS_ACTIVE)


class UserPartialUpdateSchema(UserBaseSchema):
    """
    User Update Schema

    Description:
    - This schema is used to validate user update data passed to API.

    """

    is_active: bool | None = Field(
        default=None, example=user_configuration.IS_ACTIVE
    )


class PasswordChangeSchema(BaseModel):
    """
    Change Password Schema

    Description:
    - This schema is used to validate change password data passed to API.

    """

    old_password: str = Field(
        min_length=8, max_length=1_00, example=user_configuration.PASSWORD
    )
    new_password: str = Field(
        min_length=8, max_length=1_00, example=user_configuration.PASSWORD
    )

    # Custom Validators
    old_password_validator = field_validator("old_password")(
        password_validator
    )
    new_password_validator = field_validator("new_password")(
        password_validator
    )

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class PasswordChangeReadSchema(BaseModel):
    """
    Change Password Read Schema

    Description:
    - This schema is used to validate change password data returned by API.

    """

    detail: str = Field(example=user_response_message.PASSWORD_CHANGED)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class PasswordResetRequestSchema(BaseModel):
    """
    Password Reset Request Schema

    Description:
    - This schema is used to validate password reset request data passed to
    API.

    """

    email: EmailStr = Field(
        min_length=1,
        max_length=2_55,
        example=user_configuration.EMAIL,
    )

    # Custom Validators
    email_validator = field_validator("email")(lowercase_email)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class PasswordResetSchema(BaseModel):
    """
    Password Reset Schema

    Description:
    - This schema is used to validate password reset data passed to API.

    """

    token: str = Field(example=user_configuration.OTP_CODE)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class PasswordResetReadSchema(BaseModel):
    """
    Password Reset Read Schema

    Description:
    - This schema is used to validate password reset data returned by API.

    """

    detail: str = Field(example=user_response_message.PASSWORD_RESET)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )
