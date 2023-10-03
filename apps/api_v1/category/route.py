"""
    Category Route Module

    Description:
    - This module is responsible for handling category routes.
    - It is used to create, get, update, delete category details.

"""

# Importing Python Packages
from sqlalchemy.ext.asyncio import AsyncSession

# Importing FastAPI Packages
from fastapi import APIRouter, Depends, Security, status
from fastapi.exceptions import HTTPException

# Importing Project Files
from database.session import get_session
from core import CurrentUserReadSchema, get_current_active_user
from .configuration import category_configuration
from .response_message import category_response_message
from .model import CategoryTable
from .schema import (
    CategoryCreateSchema,
    CategoryReadSchema,
    CategoryPaginationReadSchema,
    CategoryUpdateSchema,
    CategoryPartialUpdateSchema,
)
from .view import category_view

# Router Object to Create Routes
router = APIRouter(prefix="/category", tags=["Category"])


# -----------------------------------------------------------------------------


# Create a single category route
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single category",
    response_description="Category created successfully",
)
async def create_category(
    record: CategoryCreateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> CategoryReadSchema:
    """
    Create a single category

    Description:
    - This route is used to create a single category.

    Parameter:
    Category details to be created with following fields:
    - **category_name** (STR): Name of category. **(Required)**
    - **category_description** (STR): Description of category. **(Optional)**

    Return:
    Category details along with following information:
    - **id** (INT): Id of category.
    - **category_name** (STR): Name of category.
    - **category_description** (STR): Description of ategory.
    - **created_at** (DATETIME): Datetime of category creation.
    - **updated_at** (DATETIME): Datetime of category updation.

    """
    print("Calling create_category method")

    result: CategoryTable = await category_view.create(
        db_session=db_session, record=record
    )

    return CategoryReadSchema.model_validate(obj=result)


# Get a single category by id route
@router.get(
    path="/{category_id}/",
    status_code=status.HTTP_200_OK,
    summary="Get a single category by providing id",
    response_description="Category details fetched successfully",
)
async def get_category_by_id(
    category_id: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> CategoryReadSchema:
    """
    Get a single category

    Description:
    - This route is used to get a single category by providing id.

    Parameter:
    - **category_id** (INT): ID of category to be fetched. **(Required)**

    Return:
    Get a single category with following information:
    - **id** (INT): Id of category.
    - **category_name** (STR): Name of category.
    - **category_description** (STR): Description of category.
    - **created_at** (DATETIME): Datetime of category creation.
    - **updated_at** (DATETIME): Datetime of category updation.

    """
    print("Calling get_category_by_id method")

    result: CategoryTable = await category_view.read_by_id(
        db_session=db_session, record_id=category_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=category_response_message.CATEGORY_NOT_FOUND,
        )

    return CategoryReadSchema.model_validate(obj=result)


# Get a single category by name route
@router.get(
    path="/name/{category_name}/",
    status_code=status.HTTP_200_OK,
    summary="Get a single category by providing name",
    response_description="Category details fetched successfully",
)
async def get_category_by_name(
    category_name: str,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> CategoryReadSchema:
    """
    Get a single category

    Description:
    - This route is used to get a single category by providing name.

    Parameter:
    - **category_name** (STR): Name of category to be fetched. **(Required)**

    Return:
    Get a single category with following information:
    - **id** (INT): Id of category.
    - **category_name** (STR): Name of category.
    - **category_description** (STR): Description of category.
    - **created_at** (DATETIME): Datetime of category creation.
    - **updated_at** (DATETIME): Datetime of category updation.

    """
    print("Calling get_category_by_name method")

    result: CategoryTable = await category_view.read_by_value(
        db_session=db_session,
        column_name=category_configuration.CATEGORY_COLUMN_NAME,
        column_value=category_name,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=category_response_message.CATEGORY_NOT_FOUND,
        )

    return CategoryReadSchema.model_validate(obj=result)


# Get all categories route
@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Get all categories",
    response_description="All categories fetched successfully",
)
async def get_all_categories(
    page: int | None = None,
    limit: int | None = None,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> CategoryPaginationReadSchema:
    """
    Get all categories

    Description:
    - This route is used to get all categories.

    Parameter:
    - **page** (INT): Page number to be fetched. **(Optional)**
    - **limit** (INT): Number of records to be fetched per page. **(Optional)**

    Return:
    Get all categories with following information:
    - **id** (INT): Id of category.
    - **category_name** (STR): Name of category.
    - **category_description** (STR): Description of category.
    - **created_at** (DATETIME): Datetime of category creation.
    - **updated_at** (DATETIME): Datetime of category updation.

    """
    print("Calling get_all_categories method")

    result: dict = await category_view.read_all(
        db_session=db_session, page=page, limit=limit
    )

    return CategoryPaginationReadSchema.model_validate(obj=result)


# Update a single category route
@router.put(
    path="/{category_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a single category by providing id",
    response_description="Category updated successfully",
)
async def update_category(
    category_id: int,
    record: CategoryUpdateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> CategoryReadSchema:
    """
    Update a single category

    Description:
    - This route is used to update a single category by providing id.

    Parameter:
    - **category_id** (INT): ID of category to be updated. **(Required)**
    Category details to be updated with following fields:
    - **category_name** (STR): Name of category. **(Required)**
    - **category_description** (STR): Description of category. **(Optional)**

    Return:
    Category details along with following information:
    - **id** (INT): Id of category.
    - **category_name** (STR): Name of category.
    - **category_description** (STR): Description of category.
    - **created_at** (DATETIME): Datetime of category creation.
    - **updated_at** (DATETIME): Datetime of category updation.

    """
    print("Calling update_category method")

    result: CategoryTable = await category_view.update(
        db_session=db_session, record_id=category_id, record=record
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=category_response_message.CATEGORY_NOT_FOUND,
        )

    return CategoryReadSchema.model_validate(obj=result)


# Partial update a single category route
@router.patch(
    path="/{category_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Partial update a single category by providing id",
    response_description="Category updated successfully",
)
async def partial_update_category(
    category_id: int,
    record: CategoryPartialUpdateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> CategoryReadSchema:
    """
    Partial update a single category

    Description:
    - This route is used to partial update a single category by providing id.

    Parameter:
    - **category_id** (INT): ID of category to be updated. **(Required)**
    Category details to be updated with following fields:
    - **category_name** (STR): Name of category. **(Optional)**
    - **category_description** (STR): Description of category. **(Optional)**

    Return:
    Category details along with following information:
    - **id** (INT): Id of category.
    - **category_name** (STR): Name of category.
    - **category_description** (STR): Description of category.
    - **created_at** (DATETIME): Datetime of category creation.
    - **updated_at** (DATETIME): Datetime of category updation.

    """
    print("Calling partial_update_category method")

    result: CategoryTable = await category_view.update(
        db_session=db_session, record_id=category_id, record=record
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=category_response_message.CATEGORY_NOT_FOUND,
        )

    return CategoryReadSchema.model_validate(obj=result)


# Delete a single category route
@router.delete(
    path="/{category_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single category by providing id",
    response_description="Category deleted successfully",
)
async def delete_category(
    category_id: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> None:
    """
    Delete a single category

    Description:
    - This route is used to delete a single category by providing id.

    Parameter:
    - **category_id** (INT): ID of category to be deleted. **(Required)**

    Return:
    - **None**

    """
    print("Calling delete_category method")

    result: CategoryTable = await category_view.delete(
        db_session=db_session, record_id=category_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=category_response_message.CATEGORY_NOT_FOUND,
        )
