"""
    Role Pydantic Schemas

    Description:
    - This module contains all role schemas used by API.

"""

# Importing Python Packages
from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

# Importing FastAPI Packages

# Importing Project Files
from apps.base import BaseReadSchema, BasePaginationReadSchema
from .configuration import role_configuration


# -----------------------------------------------------------------------------


class RoleBaseSchema(BaseModel):
    """
    Role Base Schema

    Description:
    - This schema is used to validate role base data passed to API.

    """

    role_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=role_configuration.ROLE,
    )
    role_description: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=role_configuration.ROLE_DESCRIPTION,
    )

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class RoleCreateSchema(RoleBaseSchema):
    """
    Role create Schema

    Description:
    - This schema is used to validate role creation data passed to API.

    """

    role_name: str = Field(
        min_length=1, max_length=2_55, example=role_configuration.ROLE
    )


class RoleReadSchema(RoleCreateSchema, BaseReadSchema):
    """
    Role Read Schema

    Description:
    - This schema is used to validate role data returned by API.

    """


class RolePaginationReadSchema(BasePaginationReadSchema):
    """
    Role Pagination Read Schema

    Description:
    - This schema is used to validate role pagination data returned by API.

    """

    records: list[RoleReadSchema]


class RoleUpdateSchema(RoleCreateSchema):
    """
    Role Update Schema

    Description:
    - This schema is used to validate role update data passed to API.

    """


class RolePartialUpdateSchema(RoleBaseSchema):
    """
    Role Update Schema

    Description:
    - This schema is used to validate role update data passed to API.

    """
