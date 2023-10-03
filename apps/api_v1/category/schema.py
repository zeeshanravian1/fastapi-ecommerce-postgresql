"""
    Category Pydantic Schemas

    Description:
    - This module contains all category schemas used by API.

"""

# Importing Python Packages
from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

# Importing FastAPI Packages

# Importing Project Files
from apps.base import BaseReadSchema, BasePaginationReadSchema
from .configuration import category_configuration


# -----------------------------------------------------------------------------


class CategoryBaseSchema(BaseModel):
    """
    Category Base Schema

    Description:
    - This schema is used to validate category base data passed to API.

    """

    category_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=category_configuration.CATEGORY,
    )
    category_description: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=category_configuration.CATEGORY_DESCRIPTION,
    )

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class CategoryCreateSchema(CategoryBaseSchema):
    """
    Category create Schema

    Description:
    - This schema is used to validate category creation data passed to API.

    """

    category_name: str = Field(
        min_length=1, max_length=2_55, example=category_configuration.CATEGORY
    )


class CategoryReadSchema(CategoryCreateSchema, BaseReadSchema):
    """
    Category Read Schema

    Description:
    - This schema is used to validate category data returned by API.

    """


class CategoryPaginationReadSchema(BasePaginationReadSchema):
    """
    Category Pagination Read Schema

    Description:
    - This schema is used to validate category pagination data returned by API.

    """

    records: list[CategoryReadSchema]


class CategoryUpdateSchema(CategoryCreateSchema):
    """
    Category Update Schema

    Description:
    - This schema is used to validate category update data passed to API.

    """


class CategoryPartialUpdateSchema(CategoryBaseSchema):
    """
    Category Update Schema

    Description:
    - This schema is used to validate category update data passed to API.

    """
