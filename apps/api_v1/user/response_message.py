"""
    User Response Message Module

    Description:
    - This module is responsible for user response messages.

"""

# Importing Python Packages

# Importing FastAPI Packages

# Importing Project Files


# -----------------------------------------------------------------------------


class UserResponseMessage:
    """
    User Response Message Class

    Description:
    - This class is used to define user response messages.

    """

    USER_NOT_FOUND: str = "User not found"
    USER_DELETED: str = "User deleted successfully"

    PASSWORD_CHANGED: str = "Password changed successfully"
    INCORRECT_PASSWORD: str = "Incorrect password"
    PASSWORD_RESET: str = "Password reset successfully"


user_response_message = UserResponseMessage()
