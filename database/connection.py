"""
    Database Module

    Description:
    - This module is used to configure database connection.

"""

# Importing Python Packages
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base

# Importing FastAPI Packages

# Importing Project Files
from core import core_configuration


# -----------------------------------------------------------------------------


engine: AsyncEngine = create_async_engine(url=core_configuration.DATABASE_URL)
metadata: MetaData = MetaData(schema=core_configuration.DB_SCHEMA)
Base: DeclarativeBase = declarative_base(metadata=metadata)
