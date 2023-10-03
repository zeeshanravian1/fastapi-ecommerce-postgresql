"""
    Email Configuration Module

    Description:
    - This module is responsible for email configuration.

"""

# Importing Python Packages

# Importing FastAPI Packages

# Importing Project Files
from core import core_configuration


# -----------------------------------------------------------------------------


class EmailConfiguration:
    """
    Email Settings Class

    Description:
    - This class is used to define email configurations.

    """

    EMAIL_TEMPLATE_FOLDER: str = "static/email"
    EMAIL_TEMPLATE_FILE: str = "email.html"

    OTP_CODE: str = "123456"
    OTP_CODE_EXPIRY_MINUTES: int = 5
    EMAIL: str = "test@email.com"
    EMAIL_VERIFY_SUBJECT: str = f"Welcome to {core_configuration.COMPANY_NAME}"
    EMAIL_VERIFY_PURPOSE: str = "Verify Email"
    EMAIL_PASSWORD_RESET_SUBJECT: str = "Reset Password Request"
    EMAIL_PASSWORD_RESET_PURPOSE: str = "Reset Password"


email_configuration = EmailConfiguration()
