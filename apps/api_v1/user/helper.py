"""
    User Pydantic Validators

    Description:
    - This module contains validators for user pydantic schemas.

"""

# Importing Python packages
import re

# Importing FastAPI packages

# Importing from project files


# -----------------------------------------------------------------------------


def names_validator(name: str) -> str:
    """
    Name Validator

    Description:
    - This method is used to validate name data passed to API.

    Parameter:
    - **name** (STR): Name to be validated. **(Required)**

    Return:
    - **name** (STR): Validated name with capitalized.

    """
    print("Calling names_validator method")

    if not name:
        return name

    if not re.search(r"^[a-zA-Z]*$", name):
        raise ValueError("Only alphabets are allowed")

    return name.capitalize()


def contact_validator(contact: str) -> str:
    """
    Contact Number Validator

    Description:
    - This method is used to validate contact number passed to API.

    Parameter:
    - **contact** (STR): Contact to be validated. **(Required)**

    Return:
    - **contact** (STR): Validated contact.

    """
    print("Calling contact_validator method")

    if not contact:
        return contact

    if not re.search(
        r"\d{3}[-. ]\d{3}[-. ]\d{4}|"
        r"\(\d{2,3}\)[-. ]\d{3,4}[-. ]\d{4}|"
        r"\+\d{1,2}[-. ]\(\d{3}\)[-. ]\d{3}[-. ]\d{4}|"
        r"\+\d{1,2}\(\d{3}\)[-. ]\d{3}[-. ]\d{4}|"
        r"\+\d{1,2}[-. ]\d{3}[-. ]\d{3}[-. ]\d{4}|\+\d{1,2}\d{10}",
        contact,
    ):
        raise ValueError("Contact number should be in proper format")

    return contact


def username_validator(username: str) -> str:
    """
    Username Validator

    Description:
    - This method is used to validate username data passed to API.

    Parameter:
    - **username** (STR): Username to be validated. **(Required)**

    Return:
    - **username** (STR): Validated username with lowered.

    """
    print("Calling username_validator method")

    if not re.search(r"^[a-zA-Z0-9_.-]+$", username):
        raise ValueError(
            "Username can only contain alphabets, numbers, underscore, dot "
            "and hyphen"
        )

    return username.lower()


def lowercase_email(email: str) -> str:
    """
    Lowercase Email

    Description:
    - This method is used to lowercase email passed to API.

    Parameter:
    - **email** (STR): Email to be lowercased. **(Required)**

    Return:
    - **email** (STR): Lowercased email.

    """
    print("Calling lowercase_email method")

    return email.lower()


def password_validator(password: str) -> str:
    """
    Password Validator

    Description:
    - This method is used to validate password data passed to API.

    Parameter:
    - **password** (STR): Password to be validated. **(Required)**

    Return:
    - **password** (STR): Validated password.

    """
    print("Calling password_validator method")

    if not re.search(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#^()_+-/])"
        r"[A-Za-z\d@$!%*?&#^()_+-/]{8,}$",
        password,
    ):
        raise ValueError(
            "Password should contain at least one uppercase, "
            "one lowercase and one special character"
        )

    return password
