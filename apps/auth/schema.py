"""
    Authentication Pydantic Schemas

    Description:
    - This module contains all auth schemas used by API.

"""

# Importing Python Packages
from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

# Importing FastAPI Packages

# Importing Project Files
from core import TokenType
from apps.base.configuration import base_configuration
from apps.api_v1.organization.schema import (
    OrganizationCreateSchema,
    OrganizationReadSchema,
)
from apps.api_v1.user.schema import UserCreateSchema, UserReadSchema
from .configuration import auth_configuration


# -----------------------------------------------------------------------------


class RegisterAdminSchema(OrganizationCreateSchema, UserCreateSchema):
    """
    Register Admin Schema

    Description:
    - This schema is used to validate register admin data passed to API.

    """


class RegisterAdminReadSchema(OrganizationReadSchema, UserReadSchema):
    """
    Register Admin Read Schema

    Description:
    - This schema is used to validate register admin data returned by API.

    """


class LoginReadSchema(BaseModel):
    """
    Login Read Schema

    Description:
    - This schema is used to validate login data returned by API.

    """

    token_type: str = Field(example=auth_configuration.TOKEN_TYPE)
    access_token: str = Field(example=TokenType.ACCESS_TOKEN)
    refresh_token: str = Field(example=TokenType.REFRESH_TOKEN)
    role_id: int = Field(example=base_configuration.ID)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class RefreshToken(BaseModel):
    """
    Refresh Token Schema

    Description:
    - This schema is used to validate refresh token passed to API.

    """

    refresh_token: str = Field(example=TokenType.REFRESH_TOKEN)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class RefreshTokenReadSchema(BaseModel):
    """
    Refresh Token Read Schema

    Description:
    - This schema is used to validate refresh token data returned by API.

    """

    token_type: str = Field(example=auth_configuration.TOKEN_TYPE)
    access_token: str = Field(example=TokenType.ACCESS_TOKEN)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )
