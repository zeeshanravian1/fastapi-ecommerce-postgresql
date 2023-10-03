"""
    Organization Route Module

    Description:
    - This module is responsible for handling organization routes.
    - It is used to create, get, update, delete organization details.

"""

# Importing Python Packages
from sqlalchemy.ext.asyncio import AsyncSession

# Importing FastAPI Packages
from fastapi import APIRouter, Depends, Security, status
from fastapi.exceptions import HTTPException

# Importing Project Files
from database import get_session
from core import CurrentUserReadSchema, get_current_active_user
from .configuration import organization_configuration
from .response_message import organization_response_message
from .model import OrganizationTable
from .schema import (
    OrganizationCreateSchema,
    OrganizationReadSchema,
    OrganizationPaginationReadSchema,
    OrganizationUpdateSchema,
    OrganizationPartialUpdateSchema,
)
from .view import organization_view

# Router Object to Create Routes
router = APIRouter(prefix="/organization", tags=["Organization"])


# -----------------------------------------------------------------------------


# Create a single organization route
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single organization",
    response_description="Organization created successfully",
)
async def create_organization(
    record: OrganizationCreateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> OrganizationReadSchema:
    """
    Create a single organization.

    Description:
    - This route is used to create a single organization.

    Parameter:
    Organization details to be created with following fields:
    - **organization_name** (STR): Name of organization. **(Required)**
    - **organization_description** (STR): Description of organization.
    **(Optional)**

    Return:
    Organization details along with following information:
    - **id** (INT): Id of organization.
    - **organization_name** (STR): Name of organization.
    - **organization_description** (STR): Description of organization.
    - **created_at** (DATETIME): Datetime of organization creation.
    - **updated_at** (DATETIME): Datetime of organization updation.

    """
    print("Calling create_organization method")

    result: OrganizationTable = await organization_view.create(
        db_session=db_session, record=record
    )

    return OrganizationReadSchema.model_validate(obj=result)


# Get a single organization by id route
@router.get(
    path="/{organization_id}/",
    status_code=status.HTTP_200_OK,
    summary="Get a single organization by providing id",
    response_description="Organization details fetched successfully",
)
async def get_organization_by_id(
    organization_id: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> OrganizationReadSchema:
    """
    Get a single organization.

    Description:
    - This route is used to get a single organization by providing id.

    Parameter:
    - **organization_id** (INT): ID of organization to be fetched.
    **(Required)**

    Return:
    Get a single organization with following information:
    - **id** (INT): Id of organization.
    - **organization_name** (STR): Name of organization.
    - **organization_description** (STR): Description of organization.
    - **created_at** (DATETIME): Datetime of organization creation.
    - **updated_at** (DATETIME): Datetime of organization updation.

    """
    print("Calling get_organization_by_id method")

    result: OrganizationTable = await organization_view.read_by_id(
        db_session=db_session, record_id=organization_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=organization_response_message.ORGANIZATION_NOT_FOUND,
        )

    return OrganizationReadSchema.model_validate(obj=result)


# Get a single organization by name route
@router.get(
    path="/name/{organization_name}/",
    status_code=status.HTTP_200_OK,
    summary="Get a single organization by providing name",
    response_description="Organization details fetched successfully",
)
async def get_organization_by_name(
    organization_name: str,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> OrganizationReadSchema:
    """
    Get a single organization.

    Description:
    - This route is used to get a single organization by providing name.

    Parameter:
    - **organization_name** (STR): Name of organization to be fetched.
    **(Required)**

    Return:
    Get a single organization with following information:
    - **id** (INT): Id of organization.
    - **organization_name** (STR): Name of organization.
    - **organization_description** (STR): Description of organization.
    - **created_at** (DATETIME): Datetime of organization creation.
    - **updated_at** (DATETIME): Datetime of organization updation.

    """
    print("Calling get_organization_by_name method")

    result: OrganizationTable = await organization_view.read_by_value(
        db_session=db_session,
        column_name=organization_configuration.ORGANIZATION_COLUMN_NAME,
        column_value=organization_name,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=organization_response_message.ORGANIZATION_NOT_FOUND,
        )

    return OrganizationReadSchema.model_validate(obj=result)


# Get all organizations route
@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Get all organizations",
    response_description="All organizations fetched successfully",
)
async def get_all_organizations(
    page: int | None = None,
    limit: int | None = None,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> OrganizationPaginationReadSchema:
    """
    Get all organizations.

    Description:
    - This route is used to get all organizations.

    Parameter:
    - **page** (INT): Page number to be fetched. **(Optional)**
    - **limit** (INT): Number of records to be fetched per page. **(Optional)**

    Return:
    Get all organizations with following information:
    - **id** (INT): Id of organization.
    - **organization_name** (STR): Name of organization.
    - **organization_description** (STR): Description of organization.
    - **created_at** (DATETIME): Datetime of organization creation.
    - **updated_at** (DATETIME): Datetime of organization updation.

    """
    print("Calling get_all_organizations method")

    result: dict = await organization_view.read_all(
        db_session=db_session, page=page, limit=limit
    )

    return OrganizationPaginationReadSchema.model_validate(obj=result)


# Update a single organization route
@router.put(
    path="/{organization_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a single organization by providing id",
    response_description="Organization updated successfully",
)
async def update_organization(
    organization_id: int,
    record: OrganizationUpdateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> OrganizationReadSchema:
    """
    Update a single organization.

    Description:
    - This route is used to update a single organization by providing id.

    Parameter:
    - **organization_id** (INT): ID of organization to be updated.
    **(Required)**
    Organization details to be updated with following fields:
    - **organization_name** (STR): Name of organization. **(Required)**
    - **organization_description** (STR): Description of organization.
    **(Optional)**

    Return:
    Organization details along with following information:
    - **id** (INT): Id of organization.
    - **organization_name** (STR): Name of organization.
    - **organization_description** (STR): Description of organization.
    - **created_at** (DATETIME): Datetime of organization creation.
    - **updated_at** (DATETIME): Datetime of organization updation.

    """
    print("Calling update_organization method")

    result: OrganizationTable = await organization_view.update(
        db_session=db_session, record_id=organization_id, record=record
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=organization_response_message.ORGANIZATION_NOT_FOUND,
        )

    return OrganizationReadSchema.model_validate(obj=result)


# Partial update a single organization route
@router.patch(
    path="/{organization_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Partial update a single organization by providing id",
    response_description="Organization updated successfully",
)
async def partial_update_organization(
    organization_id: int,
    record: OrganizationPartialUpdateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> OrganizationReadSchema:
    """
    Partial update a single organization.

    Description:
    - This route is used to partial update a single organization by providing
    id.

    Parameter:
    - **organization_id**: ID of organization to be updated. (INT)
    **(Required)**
    Organization details to be updated with following fields:
    - **organization_name**: Name of organization. (STR) **(Optional)**
    - **organization_description**: Description of organization. (STR)
    **(Optional)**

    Return:
    Organization details along with following information:
    - **id** (INT): Id of organization.
    - **organization_name** (STR): Name of organization.
    - **organization_description** (STR): Description of organization.
    - **created_at** (DATETIME): Datetime of organization creation.
    - **updated_at** (DATETIME): Datetime of organization updation.

    """
    print("Calling partial_update_organization method")

    result: OrganizationTable = await organization_view.update(
        db_session=db_session, record_id=organization_id, record=record
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=organization_response_message.ORGANIZATION_NOT_FOUND,
        )

    return OrganizationReadSchema.model_validate(obj=result)


# Delete a single organization route
@router.delete(
    path="/{organization_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single organization by providing id",
    response_description="Organization deleted successfully",
)
async def delete_organization(
    organization_id: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> None:
    """
    Delete a single organization.

    Description:
    - This route is used to delete a single organization by providing id.

    Parameter:
    - **organization_id** (INT): ID of organization to be deleted.
    **(Required)**

    Return:
    - **None**

    """
    print("Calling delete_organization method")

    result: OrganizationTable = await organization_view.delete(
        db_session=db_session, record_id=organization_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=organization_response_message.ORGANIZATION_NOT_FOUND,
        )
