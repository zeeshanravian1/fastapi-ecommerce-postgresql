"""
    Session Module

    Description:
    - This module is used to configure database session.

"""

# Importing Python Packages
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# Importing FastAPI Packages

# Importing Project Files
from .connection import engine


# -----------------------------------------------------------------------------


async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get session

    Description:
    - This function is used to get session.

    Parameter:
    - **None**

    Return:
    - **session** (AsyncSession): Database Session.

    """
    print("Calling get_session method")

    session: AsyncSession = async_session()

    try:
        await session.begin()
        yield session

    except Exception as err:
        await session.rollback()
        raise err

    finally:
        await session.close()
