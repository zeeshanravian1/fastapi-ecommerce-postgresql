"""
    Authentication Response Message Module

    Description:
    - This module is responsible for auth response messages.

"""

# Importing Python Packages

# Importing FastAPI Packages

# Importing Project Files


# -----------------------------------------------------------------------------


class AuthResponseMessage:
    """
    Auth Response Message Class

    Description:
    - This class is used to define auth response messages.

    """

    USER_NOT_FOUND: str = "User not found"
    INCORRECT_PASSWORD: str = "Incorrect password"
    USER_LOGGED_OUT: str = "User logged out successfully"
    ORGANIZATION_ALREADY_EXISTS: str = "Organization already exists"
    USERNAME_ALREADY_EXISTS: str = "Username already exists"
    EMAIL_ALREADY_EXISTS: str = "Email already exists"


auth_response_message = AuthResponseMessage()
