"""
    Core Configuration Module

    Description:
    - This module is responsible for core configuration and read values from
    environment file.

"""

# Importing Python Packages
from enum import Enum
import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict

# Importing FastAPI Packages

# Importing Project Files

# -----------------------------------------------------------------------------


class CoreConfiguration(BaseSettings):
    """
    Core Settings Class

    Description:
    - This class is used to load core configurations from .env file.

    """

    # Database Configuration

    DATABASE: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_SCHEMA: str

    @property
    def DATABASE_URL(self):  # pylint: disable=C0103
        """
        Database URL

        Description:
        - This property is used to generate database URL.

        """
        return "".join(
            [
                self.DATABASE,
                "://",
                self.DB_USER,
                ":",
                self.DB_PASSWORD,
                "@",
                self.DB_HOST,
                ":",
                str(self.DB_PORT),
                "/",
                self.DB_NAME,
            ]
        )

    # Project Configuration

    CORS_ALLOW_ORIGINS: str
    CORS_ALLOW_METHODS: str
    CORS_ALLOW_HEADERS: str

    PROJECT_TITLE: str = "Ecommerce Assessment APIs Project"
    PROJECT_DESCRIPTION: str = (
        "Ecommerce Assessment APIs Project Documentation"
    )

    VERSION: str = "1.0.0"

    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # JWT Configuration

    ACCESS_TOKEN_SECRET_KEY: str = secrets.token_urlsafe(32)
    REFRESH_TOKEN_SECRET_KEY: str = secrets.token_urlsafe(32)
    OTP_CODE_SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Super Admin Configuration

    SUPERUSER_FIRST_NAME: str
    SUPERUSER_LAST_NAME: str
    SUPERUSER_CONTACT: str
    SUPERUSER_USERNAME: str
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: str
    SUPERUSER_ADDRESS: str
    SUPERUSER_CITY: str
    SUPERUSER_STATE: str
    SUPERUSER_COUNTRY: str
    SUPERUSER_POSTAL_CODE: str
    SUPERUSER_ROLE: str
    SUPERUSER_ROLE_DESCRIPTION: str

    # Email Configuration

    EMAIL_HOST: str
    EMAIL_PORT: str
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    EMAIL_FROM_NAME: str

    # OpenAI Configuration

    OPENAI_API_KEY: str
    MODEL_NAME: str = "gpt-3.5-turbo-16k"

    # Client Configuration

    CLIENT_BASE_URL: str
    COMPANY_NAME: str

    # Settings Configuration
    model_config = SettingsConfigDict(env_file=".env")


class UserTokenStatus(str, Enum):
    """
    User Token Status Enum

    Description:
    - This enum is used to define user token status.

    """

    LOGIN: str = "login"
    LOGOUT: str = "logout"
    EMAIL_VERIFY: str = "email_verify"
    PASSWORD_RESET: str = "password_reset"


class TokenType(str, Enum):
    """
    Token Type Enum

    Description:
    - This enum is used to define token type.

    """

    ACCESS_TOKEN: str = "access_token"
    REFRESH_TOKEN: str = "refresh_token"


core_configuration = CoreConfiguration()
