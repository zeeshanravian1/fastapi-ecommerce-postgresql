"""
    Role Route Module

    Description:
    - This module is responsible for handling role routes.
    - It is used to create, get, update, delete role details.

"""

# Importing Python Packages
from sqlalchemy.ext.asyncio import AsyncSession

# Importing FastAPI Packages
from fastapi import APIRouter, Depends, Security, status
from fastapi.exceptions import HTTPException

# Importing Project Files
from database.session import get_session
from core import CurrentUserReadSchema, get_current_active_user
from .configuration import role_configuration
from .response_message import role_response_message
from .model import RoleTable
from .schema import (
    RoleCreateSchema,
    RoleReadSchema,
    RolePaginationReadSchema,
    RoleUpdateSchema,
    RolePartialUpdateSchema,
)
from .view import role_view

# Router Object to Create Routes
router = APIRouter(prefix="/role", tags=["Role"])


# -----------------------------------------------------------------------------


# Create a single role route
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a single role",
    response_description="Role created successfully",
)
async def create_role(
    record: RoleCreateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> RoleReadSchema:
    """
    Create a single role

    Description:
    - This route is used to create a single role.

    Parameter:
    Role details to be created with following fields:
    - **role_name** (STR): Name of role. **(Required)**
    - **role_description** (STR): Description of role. **(Optional)**

    Return:
    Role details along with following information:
    - **id** (INT): Id of role.
    - **role_name** (STR): Name of role.
    - **role_description** (STR): Description of role.
    - **created_at** (DATETIME): Datetime of role creation.
    - **updated_at** (DATETIME): Datetime of role updation.

    """
    print("Calling create_role method")

    result: RoleTable = await role_view.create(
        db_session=db_session, record=record
    )

    return RoleReadSchema.model_validate(obj=result)


# Get a single role by id route
@router.get(
    path="/{role_id}/",
    status_code=status.HTTP_200_OK,
    summary="Get a single role by providing id",
    response_description="Role details fetched successfully",
)
async def get_role_by_id(
    role_id: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> RoleReadSchema:
    """
    Get a single role

    Description:
    - This route is used to get a single role by providing id.

    Parameter:
    - **role_id** (INT): ID of role to be fetched. **(Required)**

    Return:
    Get a single role with following information:
    - **id** (INT): Id of role.
    - **role_name** (STR): Name of role.
    - **role_description** (STR): Description of role.
    - **created_at** (DATETIME): Datetime of role creation.
    - **updated_at** (DATETIME): Datetime of role updation.

    """
    print("Calling get_role_by_id method")

    result: RoleTable = await role_view.read_by_id(
        db_session=db_session, record_id=role_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=role_response_message.ROLE_NOT_FOUND,
        )

    return RoleReadSchema.model_validate(obj=result)


# Get a single role by name route
@router.get(
    path="/name/{role_name}/",
    status_code=status.HTTP_200_OK,
    summary="Get a single role by providing name",
    response_description="Role details fetched successfully",
)
async def get_role_by_name(
    role_name: str,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> RoleReadSchema:
    """
    Get a single role

    Description:
    - This route is used to get a single role by providing name.

    Parameter:
    - **role_name** (STR): Name of role to be fetched. **(Required)**

    Return:
    Get a single role with following information:
    - **id** (INT): Id of role.
    - **role_name** (STR): Name of role.
    - **role_description** (STR): Description of role.
    - **created_at** (DATETIME): Datetime of role creation.
    - **updated_at** (DATETIME): Datetime of role updation.

    """
    print("Calling get_role_by_name method")

    result: RoleTable = await role_view.read_by_value(
        db_session=db_session,
        column_name=role_configuration.ROLE_COLUMN_NAME,
        column_value=role_name,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=role_response_message.ROLE_NOT_FOUND,
        )

    return RoleReadSchema.model_validate(obj=result)


# Get all roles route
@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    summary="Get all roles",
    response_description="All roles fetched successfully",
)
async def get_all_roles(
    page: int | None = None,
    limit: int | None = None,
    db_session: AsyncSession = Depends(get_session),
) -> RolePaginationReadSchema:
    """
    Get all roles

    Description:
    - This route is used to get all roles.

    Parameter:
    - **page** (INT): Page number to be fetched. **(Optional)**
    - **limit** (INT): Number of records to be fetched per page. **(Optional)**

    Return:
    Get all roles with following information:
    - **id** (INT): Id of role.
    - **role_name** (STR): Name of role.
    - **role_description** (STR): Description of role.
    - **created_at** (DATETIME): Datetime of role creation.
    - **updated_at** (DATETIME): Datetime of role updation.

    """
    print("Calling get_all_roles method")

    result: dict = await role_view.read_all(
        db_session=db_session, page=page, limit=limit
    )

    return RolePaginationReadSchema.model_validate(obj=result)


# Update a single role route
@router.put(
    path="/{role_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a single role by providing id",
    response_description="Role updated successfully",
)
async def update_role(
    role_id: int,
    record: RoleUpdateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> RoleReadSchema:
    """
    Update a single role

    Description:
    - This route is used to update a single role by providing id.

    Parameter:
    - **role_id** (INT): ID of role to be updated. **(Required)**
    Role details to be updated with following fields:
    - **role_name** (STR): Name of role. **(Required)**
    - **role_description** (STR): Description of role. **(Optional)**

    Return:
    Role details along with following information:
    - **id** (INT): Id of role.
    - **role_name** (STR): Name of role.
    - **role_description** (STR): Description of role.
    - **created_at** (DATETIME): Datetime of role creation.
    - **updated_at** (DATETIME): Datetime of role updation.

    """
    print("Calling update_role method")

    result: RoleTable = await role_view.update(
        db_session=db_session, record_id=role_id, record=record
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=role_response_message.ROLE_NOT_FOUND,
        )

    return RoleReadSchema.model_validate(obj=result)


# Partial update a single role route
@router.patch(
    path="/{role_id}/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Partial update a single role by providing id",
    response_description="Role updated successfully",
)
async def partial_update_role(
    role_id: int,
    record: RolePartialUpdateSchema,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> RoleReadSchema:
    """
    Partial update a single role

    Description:
    - This route is used to partial update a single role by providing id.

    Parameter:
    - **role_id** (INT): ID of role to be updated. **(Required)**
    Role details to be updated with following fields:
    - **role_name** (STR): Name of role. **(Optional)**
    - **role_description** (STR): Description of role. **(Optional)**

    Return:
    Role details along with following information:
    - **id** (INT): Id of role.
    - **role_name** (STR): Name of role.
    - **role_description** (STR): Description of role.
    - **created_at** (DATETIME): Datetime of role creation.
    - **updated_at** (DATETIME): Datetime of role updation.

    """
    print("Calling partial_update_role method")

    result: RoleTable = await role_view.update(
        db_session=db_session, record_id=role_id, record=record
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=role_response_message.ROLE_NOT_FOUND,
        )

    return RoleReadSchema.model_validate(obj=result)


# Delete a single role route
@router.delete(
    path="/{role_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a single role by providing id",
    response_description="Role deleted successfully",
)
async def delete_role(
    role_id: int,
    db_session: AsyncSession = Depends(get_session),
    current_user: CurrentUserReadSchema = Security(get_current_active_user),
) -> None:
    """
    Delete a single role

    Description:
    - This route is used to delete a single role by providing id.

    Parameter:
    - **role_id** (INT): ID of role to be deleted. **(Required)**

    Return:
    - **None**

    """
    print("Calling delete_role method")

    result: RoleTable = await role_view.delete(
        db_session=db_session, record_id=role_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=role_response_message.ROLE_NOT_FOUND,
        )
