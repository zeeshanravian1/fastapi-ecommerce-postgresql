"""
    Organization Pydantic Schemas

    Description:
    - This module contains all organization schemas used by API.

"""

# Importing Python Packages
from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

# Importing FastAPI Packages

# Importing Project Files
from apps.base import BaseReadSchema, BasePaginationReadSchema
from .configuration import organization_configuration


# -----------------------------------------------------------------------------


class OrganizationBaseSchema(BaseModel):
    """
    Organization Base Schema

    Description:
    - This schema is used to validate organization base data passed to API.

    """

    organization_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=organization_configuration.ORGANIZATION,
    )
    organization_description: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=organization_configuration.ORGANIZATION_DESCRIPTION,
    )

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class OrganizationCreateSchema(OrganizationBaseSchema):
    """
    Organization create Schema

    Description:
    - This schema is used to validate organization creation data passed to API.

    """

    organization_name: str = Field(
        min_length=1,
        max_length=2_55,
        example=organization_configuration.ORGANIZATION,
    )


class OrganizationReadSchema(OrganizationCreateSchema, BaseReadSchema):
    """
    Organization Read Schema

    Description:
    - This schema is used to validate organization data returned by API.

    """


class OrganizationPaginationReadSchema(BasePaginationReadSchema):
    """
    Organization Pagination Read Schema

    Description:
    - This schema is used to validate organization pagination data returned
    from API.

    """

    records: list[OrganizationReadSchema]


class OrganizationUpdateSchema(OrganizationCreateSchema):
    """
    Organization Update Schema

    Description:
    - This schema is used to validate organization update data passed to API.

    """


class OrganizationPartialUpdateSchema(OrganizationBaseSchema):
    """
    Organization Update Schema

    Description:
    - This schema is used to validate organization update data passed to API.

    """
