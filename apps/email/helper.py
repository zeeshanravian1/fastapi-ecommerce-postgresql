"""
    Email Pydantic Validators

    Description:
    - This module contains validators for email pydantic schemas.

"""

# Importing Python packages
from random import randint
from datetime import datetime, timedelta, timezone
from jose import jwt

# Importing FastAPI Packages

# Importing Project Files
from core import core_configuration
from .configuration import email_configuration
from .response_message import email_response_message
from .schema import EmailBaseSchema, EmailDataSchema, EmailSchema
from .send_email import send_email


# -----------------------------------------------------------------------------


async def generate_otp_code() -> str:
    """
    Generates 6 digit OTP code.

    Description:
    - This method is used to generate a 6 digit OTP.

    Parameter:
    - **None**

    Return:
    - **otp_code** (STR): 6 digit OTP code.

    """
    print("Calling generate_otp_code method")

    return str(randint(100000, 999999))


async def send_email_otp(record: EmailBaseSchema) -> dict:
    """
    Sends an email with OTP.

    Description:
    - This method is used to encode OTP code and send it to user via email.

    Parameters:
    Email details to be sent with following fields:
    - **subject** (STR): Subject of email. **(Required)**
    - **email_purpose** (STR): Purpose of email. **(Required)**
    - **user_name** (STR): Full name of user. **(Required)**
    - **email** (LIST): Email of user. **(Required)**

    Returns:
    - **detail** (DICT): Details of email sent.

    """

    # Generate OTP Code
    otp_code = await generate_otp_code()
    otp_expiry_time = datetime.now(tz=timezone.utc) + timedelta(
        minutes=email_configuration.OTP_CODE_EXPIRY_MINUTES
    )

    # Encode OTP Code
    encoded_jwt = jwt.encode(
        claims={
            "email": record.email,
            "token": otp_code,
            "exp": otp_expiry_time.timestamp(),
        },
        key=core_configuration.OTP_CODE_SECRET_KEY,
        algorithm=core_configuration.ALGORITHM,
    )

    url = "".join(
        [
            core_configuration.CLIENT_BASE_URL,
            "/",
            record.email_purpose.replace(" ", "-").lower(),
            "/",
            encoded_jwt,
        ]
    )

    # Send Email
    email_response = await send_email(
        email=EmailSchema(
            email=[record.email],
            subject=record.subject,
            body=EmailDataSchema(
                url=url,
                otp_code=otp_code,
                user_name=record.user_name,
                email_purpose=record.email_purpose,
                company_name=core_configuration.COMPANY_NAME,
                base_url=core_configuration.CLIENT_BASE_URL,
            ),
        )
    )

    if not email_response.get("success"):
        return {
            "success": False,
            "detail": email_response_message.EMAIL_SENT_FAILED,
        }

    return {
        "success": True,
        "detail": email_response_message.EMAIL_SENT,
        "otp_code": otp_code,
    }
