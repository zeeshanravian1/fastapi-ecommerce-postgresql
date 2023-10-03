"""
    Insert initial data in database.

    Description:
    - This module is responsible for inserting initial data in database.

"""

# Importing Python Packages
import logging
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql.selectable import Select
from sqlalchemy.exc import IntegrityError, ProgrammingError

# Importing FastAPI Packages

# Importing Project Files
from apps.api_v1.role.model import RoleTable
from apps.api_v1.user.model import UserTable
from core import core_configuration


insert_logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------


async def insert_db_data(db_session: async_sessionmaker[AsyncSession]) -> None:
    """
    Insert Database Data

    Description:
    - This function is used to insert initial data in database.

    Parameter:
    - **db_session** (async_sessionmaker[AsyncSession]): Database session.
    **(Required)**

    Return:
    - **None**

    """
    insert_logger.debug("Calling insert_db_data method")

    # Insert Roles in database
    roles = [
        RoleTable(
            role_name=core_configuration.SUPERUSER_ROLE,
            role_description=core_configuration.SUPERUSER_ROLE_DESCRIPTION,
        ),
        RoleTable(
            role_name="admin",
            role_description="Admin Role Description",
        ),
        RoleTable(
            role_name="manager",
            role_description="Manager Role Description",
        ),
        RoleTable(
            role_name="user",
            role_description="User Role Description",
        ),
    ]

    try:
        async with db_session() as session:
            async with session.begin():
                session.add_all(instances=roles)
                await session.commit()

    except (IntegrityError, ProgrammingError):
        insert_logger.error("Error in insert roles in database", exc_info=True)

    # Insert Super Admin in database
    try:
        async with db_session() as session:
            async with session.begin():
                # Get role id of Super Admin
                query: Select = select(RoleTable).where(
                    RoleTable.role_name == core_configuration.SUPERUSER_ROLE
                )
                result: ChunkedIteratorResult = await session.execute(
                    statement=query
                )
                role: RoleTable = result.scalars().first()

                # Insert Super Admin
                session.add(
                    instance=UserTable(
                        first_name=core_configuration.SUPERUSER_FIRST_NAME,
                        last_name=core_configuration.SUPERUSER_LAST_NAME,
                        contact=core_configuration.SUPERUSER_CONTACT,
                        username=core_configuration.SUPERUSER_USERNAME,
                        email=core_configuration.SUPERUSER_EMAIL,
                        password=pbkdf2_sha256.hash(
                            core_configuration.SUPERUSER_PASSWORD
                        ),
                        address=core_configuration.SUPERUSER_ADDRESS,
                        city=core_configuration.SUPERUSER_CITY,
                        state=core_configuration.SUPERUSER_STATE,
                        country=core_configuration.SUPERUSER_COUNTRY,
                        postal_code=core_configuration.SUPERUSER_POSTAL_CODE,
                        email_verified=True,
                        is_active=True,
                        role_id=role.id,
                    )
                )

                await session.commit()

    except (IntegrityError, ProgrammingError):
        insert_logger.error(
            "Error in insert super admin in database", exc_info=True
        )
