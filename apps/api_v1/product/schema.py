"""
    Product Pydantic Schemas

    Description:
    - This module contains all product schemas used by API.

"""

# Importing Python Packages
from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

# Importing FastAPI Packages

# Importing Project Files
from apps.base import BaseReadSchema, BasePaginationReadSchema
from .configuration import product_configuration


# -----------------------------------------------------------------------------


class ProductBaseSchema(BaseModel):
    """
    Product Base Schema

    Description:
    - This schema is used to validate product base data passed to API.

    """

    product_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_55,
        example=product_configuration.PRODUCT_NAME,
    )
    price: float | None = Field(
        default=None, gt=0, example=product_configuration.PRICE
    )
    quantity: int | None = Field(
        default=None, ge=0, example=product_configuration.QUANTITY
    )
    is_available: bool | None = Field(
        default=None, example=product_configuration.IS_AVAILABLE
    )
    low_stock_threshold: int | None = Field(
        default=None,
        ge=0,
        example=product_configuration.LOW_STOCK_THRESHOLD,
    )
    category_id: int | None = Field(
        default=None, gt=0, example=product_configuration.CATEGORY_ID
    )

    # Settings Configuration
    model_config = SettingsConfigDict(
        str_strip_whitespace=True, from_attributes=True
    )


class ProductCreateSchema(ProductBaseSchema):
    """
    Product create Schema

    Description:
    - This schema is used to validate product creation data passed to API.

    """

    product_name: str = Field(
        min_length=1,
        max_length=2_55,
        example=product_configuration.PRODUCT_NAME,
    )
    price: float = Field(gt=0, example=product_configuration.PRICE)
    quantity: int = Field(gt=0, example=product_configuration.QUANTITY)
    category_id: int = Field(gt=0, example=product_configuration.CATEGORY_ID)


class ProductReadSchema(ProductCreateSchema, BaseReadSchema):
    """
    Product Read Schema

    Description:
    - This schema is used to validate product data returned by API.

    """


class ProductPaginationReadSchema(BasePaginationReadSchema):
    """
    Product Pagination Read Schema

    Description:
    - This schema is used to validate product pagination data returned by API.

    """

    records: list[ProductReadSchema]


class ProductUpdateSchema(ProductCreateSchema):
    """
    Product Update Schema

    Description:
    - This schema is used to validate product update data passed to API.

    """


class ProductPartialUpdateSchema(ProductBaseSchema):
    """
    Product Update Schema

    Description:
    - This schema is used to validate product update data passed to API.

    """
