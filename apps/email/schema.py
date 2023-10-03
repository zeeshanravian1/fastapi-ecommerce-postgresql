"""
    Email Pydantic Schemas

    Description:
    - This module contains all email schemas used by API.

"""

# Importing Python Packages
from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic_settings import SettingsConfigDict

# Importing FastAPI Packages

# Importing Project Files
from core import core_configuration
from apps.auth.schema import LoginReadSchema
from apps.api_v1.user.configuration import user_configuration
from apps.api_v1.user.helper import lowercase_email
from .configuration import email_configuration
from .response_message import email_response_message


# -----------------------------------------------------------------------------


class EmailVerifyRequestSchema(BaseModel):
    """
    Email Verify Request Schema

    Description:
    - This schema is used to validate email verify request data passed to API.

    """

    email: EmailStr = Field(example=email_configuration.EMAIL)

    # Custom Validators
    lowercase_email = field_validator("email")(lowercase_email)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class EmailSentSchema(BaseModel):
    """
    Email Sent Schema

    Description:
    - This schema is used to validate email sent data returned by API.

    """

    detail: str = Field(example=email_response_message.EMAIL_SENT)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class EmailVerifySchema(BaseModel):
    """
    Email Verify Schema

    Description:
    - This schema is used to validate email verify token passed to API.

    """

    token: str = Field(example=email_configuration.OTP_CODE)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class EmailVerifyReadSchema(LoginReadSchema):
    """
    Email Verify Read Schema

    Description:
    - This schema is used to validate email verify data returned by API.

    """

    detail: str = Field(example=email_response_message.EMAIL_VERIFIED)


class EmailBaseSchema(BaseModel):
    """
    Email Base Schema

    Description:
    - This schema is used to validate base email data passed to send email.

    """

    subject: str = Field(example=email_configuration.EMAIL_VERIFY_SUBJECT)
    email_purpose: str = Field(
        example=email_configuration.EMAIL_VERIFY_PURPOSE
    )
    user_name: str = Field(example=user_configuration.FULL_NAME)
    email: EmailStr = Field(example=email_configuration.EMAIL)

    # Custom Validators
    email_validator = field_validator("email")(lowercase_email)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class EmailDataSchema(BaseModel):
    """
    Email Data Schema

    Description:
    - This schema is used to validate email data passed to send email.

    """

    url: str = Field(example=core_configuration.CLIENT_BASE_URL)
    otp_code: str = Field(
        min_length=6, max_length=6, example=email_configuration.OTP_CODE
    )
    user_name: str = Field(example=user_configuration.FULL_NAME)
    email_purpose: str = Field(
        example=email_configuration.EMAIL_VERIFY_PURPOSE
    )
    company_name: str = Field(example=core_configuration.COMPANY_NAME)
    base_url: str = Field(example=core_configuration.CLIENT_BASE_URL)

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class EmailSchema(BaseModel):
    """
    Email Schema

    Description:
    - This schema is used to validate email data passed to send email.

    """

    email: list[EmailStr] = Field(example=email_configuration.EMAIL)
    subject: str = Field(example=email_configuration.EMAIL_VERIFY_SUBJECT)
    body: EmailDataSchema

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )
