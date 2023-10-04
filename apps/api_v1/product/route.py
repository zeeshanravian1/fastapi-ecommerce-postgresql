"""
    Product Route Module

    Description:
    - This module is responsible for handling product routes.
    - It is used to create, get, update, delete product details.

"""

# Importing Python Packages
from sqlalchemy.ext.asyncio import AsyncSession

# Importing FastAPI Packages
from fastapi import APIRouter, Depends, Security, status
from fastapi.exceptions import HTTPException

# Importing Project Files
from database.session import get_session
from core import CurrentUserReadSchema, get_current_active_user
from .configuration import product_configuration
from .response_message import product_response_message
from .model import ProductTable
from .schema import (
    ProductCreateSchema,
    ProductReadSchema,
    ProductPaginationReadSchema,
    ProductUpdateSchema,
    ProductPartialUpdateSchema,
)
from .view import product_view

# Router Object to Create Routes
router = APIRouter(prefix="/product", tags=["Product"])


# -----------------------------------------------------------------------------


# Create a single product route
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single product",
    response_description="Product created successfully",
)
async def create_product(
    record: ProductCreateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> ProductReadSchema:
    """
    Create a single product

    Description:
    - This route is used to create a single product.

    Parameter:
    Product details to be created with following fields:
    - **product_name** (STR): Name of product. **(Required)**
    - **price** (FLOAT): Price of product. **(Required)**
    - **quantity** (INT): Quantity of product. **(Required)**
    - **is_available** (BOOL): Availability of product. **(Optional)**
    - **low_stock_threshold** (INT): Low stock threshold of product.
    **(Optional)**
    - **category_id** (INT): Category ID of product. **(Required)**

    Return:
    Product details along with following information:
    - **id** (INT): Id of product.
    - **product_name** (STR): Name of product.
    - **price** (FLOAT): Price of product.
    - **quantity** (INT): Quantity of product.
    - **is_available** (BOOL): Availability of product.
    - **low_stock_threshold** (INT): Low stock threshold of product.
    - **category_id** (INT): Category ID of product.
    - **created_at** (DATETIME): Datetime of product creation.
    - **updated_at** (DATETIME): Datetime of product updation.

    """
    print("Calling create_product method")

    result: ProductTable = await product_view.create(
        db_session=db_session, record=record
    )

    return ProductReadSchema.model_validate(obj=result)


# Get a single product by id route
@router.get(
    path="/{product_id}/",
    status_code=status.HTTP_200_OK,
    summary="Get a single product by providing id",
    response_description="Product details fetched successfully",
)
async def get_product_by_id(
    product_id: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> ProductReadSchema:
    """
    Get a single product

    Description:
    - This route is used to get a single product by providing id.

    Parameter:
    - **product_id** (INT): ID of product to be fetched. **(Required)**

    Return:
    Get a single product with following information:
    - **id** (INT): Id of product.
    - **product_name** (STR): Name of product.
    - **price** (FLOAT): Price of product.
    - **quantity** (INT): Quantity of product.
    - **is_available** (BOOL): Availability of product.
    - **low_stock_threshold** (INT): Low stock threshold of product.
    - **category_id** (INT): Category ID of product.
    - **created_at** (DATETIME): Datetime of product creation.
    - **updated_at** (DATETIME): Datetime of product updation.

    """
    print("Calling get_product_by_id method")

    result: ProductTable = await product_view.read_by_id(
        db_session=db_session, record_id=product_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=product_response_message.PRODUCT_NOT_FOUND,
        )

    return ProductReadSchema.model_validate(obj=result)


# Get a single product by name route
@router.get(
    path="/name/{product_name}/",
    status_code=status.HTTP_200_OK,
    summary="Get a single product by providing name",
    response_description="Product details fetched successfully",
)
async def get_product_by_name(
    product_name: str,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> ProductReadSchema:
    """
    Get a single product

    Description:
    - This route is used to get a single product by providing name.

    Parameter:
    - **product_name** (STR): Name of product to be fetched. **(Required)**

    Return:
    Get a single product with following information:
    - **id** (INT): Id of product.
    - **product_name** (STR): Name of product.
    - **price** (FLOAT): Price of product.
    - **quantity** (INT): Quantity of product.
    - **is_available** (BOOL): Availability of product.
    - **low_stock_threshold** (INT): Low stock threshold of product.
    - **category_id** (INT): Category ID of product.
    - **created_at** (DATETIME): Datetime of product creation.
    - **updated_at** (DATETIME): Datetime of product updation.

    """
    print("Calling get_product_by_name method")

    result: ProductTable = await product_view.read_by_value(
        db_session=db_session,
        column_name=product_configuration.PRODUCT_COLUMN_NAME,
        column_value=product_name,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=product_response_message.PRODUCT_NOT_FOUND,
        )

    return ProductReadSchema.model_validate(obj=result)


# Get all products by category id route
@router.get(
    path="/category/{category_id}/",
    status_code=status.HTTP_200_OK,
    summary="Get all products by providing category id",
    response_description="All products fetched successfully",
)
async def get_all_products_by_category_id(
    category_id: int,
    page: int | None = None,
    limit: int | None = None,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> ProductPaginationReadSchema:
    """
    Get all products

    Description:
    - This route is used to get all products by providing category id.

    Parameter:
    - **category_id** (INT): Category ID of product to be fetched.
    **(Required)**
    - **page** (INT): Page number to be fetched. **(Optional)**
    - **limit** (INT): Number of records to be fetched per page. **(Optional)**

    Return:
    Get all products with following information:
    - **id** (INT): Id of product.
    - **product_name** (STR): Name of product.
    - **price** (FLOAT): Price of product.
    - **quantity** (INT): Quantity of product.
    - **is_available** (BOOL): Availability of product.
    - **low_stock_threshold** (INT): Low stock threshold of product.
    - **category_id** (INT): Category ID of product.
    - **created_at** (DATETIME): Datetime of product creation.
    - **updated_at** (DATETIME): Datetime of product updation.

    """
    print("Calling get_all_products_by_category_id method")

    result: dict = await product_view.read_all_by_category_id(
        db_session=db_session, category_id=category_id, page=page, limit=limit
    )

    return ProductPaginationReadSchema.model_validate(obj=result)


# Update a single product route
@router.put(
    path="/{product_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a single product by providing id",
    response_description="Product updated successfully",
)
async def update_product(
    product_id: int,
    record: ProductUpdateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> ProductReadSchema:
    """
    Update a single product

    Description:
    - This route is used to update a single product by providing id.

    Parameter:
    - **product_id** (INT): ID of product to be updated. **(Required)**
    Product details to be updated with following fields:
    - **product_name** (STR): Name of product. **(Required)**
    - **price** (FLOAT): Price of product. **(Required)**
    - **quantity** (INT): Quantity of product. **(Required)**
    - **is_available** (BOOL): Availability of product. **(Optional)**
    - **low_stock_threshold** (INT): Low stock threshold of product.
    **(Optional)**
    - **category_id** (INT): Category ID of product. **(Required)**

    Return:
    Product details along with following information:
    - **id** (INT): Id of product.
    - **product_name** (STR): Name of product.
    - **price** (FLOAT): Price of product.
    - **quantity** (INT): Quantity of product.
    - **is_available** (BOOL): Availability of product.
    - **low_stock_threshold** (INT): Low stock threshold of product.
    - **category_id** (INT): Category ID of product.
    - **created_at** (DATETIME): Datetime of product creation.
    - **updated_at** (DATETIME): Datetime of product updation.

    """
    print("Calling update_product method")

    result: ProductTable = await product_view.update(
        db_session=db_session, record_id=product_id, record=record
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=product_response_message.PRODUCT_NOT_FOUND,
        )

    return ProductReadSchema.model_validate(obj=result)


# Partial update a single product route
@router.patch(
    path="/{product_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Partial update a single product by providing id",
    response_description="Product updated successfully",
)
async def partial_update_product(
    product_id: int,
    record: ProductPartialUpdateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> ProductReadSchema:
    """
    Partial update a single product

    Description:
    - This route is used to partial update a single product by providing id.

    Parameter:
    - **product_id** (INT): ID of product to be updated. **(Required)**
    Product details to be updated with following fields:
    - **product_name** (STR): Name of product. **(Optional)**
    - **price** (FLOAT): Price of product. **(Optional)**
    - **quantity** (INT): Quantity of product. **(Optional)**
    - **is_available** (BOOL): Availability of product. **(Optional)**
    - **low_stock_threshold** (INT): Low stock threshold of product.
    **(Optional)**
    - **category_id** (INT): Category ID of product. **(Optional)**

    Return:
    product details along with following information:
    - **id** (INT): Id of product.
    - **product_name** (STR): Name of product.
    - **price** (FLOAT): Price of product.
    - **quantity** (INT): Quantity of product.
    - **is_available** (BOOL): Availability of product.
    - **low_stock_threshold** (INT): Low stock threshold of product.
    - **category_id** (INT): Category ID of product.
    - **created_at** (DATETIME): Datetime of product creation.
    - **updated_at** (DATETIME): Datetime of product updation.

    """
    print("Calling partial_update_product method")

    result: ProductTable = await product_view.update(
        db_session=db_session, record_id=product_id, record=record
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=product_response_message.PRODUCT_NOT_FOUND,
        )

    return ProductReadSchema.model_validate(obj=result)


# Delete a single product route
@router.delete(
    path="/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single product by providing id",
    response_description="Product deleted successfully",
)
async def delete_product(
    product_id: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> None:
    """
    Delete a single product

    Description:
    - This route is used to delete a single product by providing id.

    Parameter:
    - **product_id** (INT): ID of product to be deleted. **(Required)**

    Return:
    - **None**

    """
    print("Calling delete_product method")

    result: ProductTable = await product_view.delete(
        db_session=db_session, record_id=product_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=product_response_message.PRODUCT_NOT_FOUND,
        )
