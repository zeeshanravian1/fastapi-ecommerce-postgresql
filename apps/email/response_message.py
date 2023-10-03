"""
    Email Response Message Module

    Description:
    - This module is responsible for email response messages.

"""

# Importing Python Packages

# Importing FastAPI Packages

# Importing Project Files


# -----------------------------------------------------------------------------


class EmailResponseMessage:
    """
    Email Response Message Class

    Description:
    - This class is used to define email response messages.

    """

    EMAIL_SENT: str = "Email sent successfully at given email address"
    EMAIL_SENT_FAILED: str = "Email sending failed"
    INCORRECT_OTP_CODE: str = "Incorrect OTP code, please request a new one"
    USER_ALREADY_VERIFIED: str = "User already verified"
    EMAIL_VERIFIED: str = "Email verified successfully"


email_response_message = EmailResponseMessage()
