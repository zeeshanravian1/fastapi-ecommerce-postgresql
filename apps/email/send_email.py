"""
    Send Email Module

    Description:
    - This module is used to send email to user.

"""

# Importing Python packages

# Importing FastAPI packages
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

# Importing from project files
from core import core_configuration
from .configuration import email_configuration
from .response_message import email_response_message
from .schema import EmailSchema


# -----------------------------------------------------------------------------


# Email Configuration
email_config = ConnectionConfig(
    MAIL_USERNAME=core_configuration.EMAIL_USERNAME,
    MAIL_PASSWORD=core_configuration.EMAIL_PASSWORD,
    MAIL_FROM=core_configuration.EMAIL_FROM,
    MAIL_PORT=core_configuration.EMAIL_PORT,
    MAIL_SERVER=core_configuration.EMAIL_HOST,
    MAIL_FROM_NAME=core_configuration.EMAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=email_configuration.EMAIL_TEMPLATE_FOLDER,
)


# Sending OTP Code
async def send_email(email: EmailSchema) -> dict:
    """
    Sends an OTP code to user email.

    Description:
    - This method is used to send an OTP code to user email.

    Parameter:
    - **email** (EmailBaseSchema): Email data to be sent. **(Required)**

    Return:
    - **detail** (JSON): Email sent status.

    """
    print("Calling send_email method")

    message = MessageSchema(
        subject=email.subject,
        recipients=email.email,
        template_body=email.body.model_dump(),
        subtype=MessageType.html,
    )

    fastapi_mail = FastMail(email_config)
    await fastapi_mail.send_message(
        message=message, template_name=email_configuration.EMAIL_TEMPLATE_FILE
    )

    return {"success": True, "detail": email_response_message.EMAIL_SENT}
