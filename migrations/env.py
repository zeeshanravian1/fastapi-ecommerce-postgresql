"""
    Migration environment for database.

    Description:
    - This file is used to configure migration environment for database.

"""

# Importing Python Packages
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from alembic import context

# Importing FastAPI Packages

# Importing Project Files
from core import core_configuration
from database import metadata, async_session, insert_db_data


# -----------------------------------------------------------------------------


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set the database URL in the config object
config.set_main_option(
    name="sqlalchemy.url", value=core_configuration.DATABASE_URL
)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(fname=config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    Description:
    - This configures the context with just a URL and not an Engine,
    though an Engine is acceptable here as well.
    By skipping the Engine creation we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url: str = config.get_main_option(name="sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Run migrations in 'online' mode.

    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        compare_server_default=True,
        compare_type=True,
        version_table_schema=core_configuration.DB_SCHEMA,
    )

    with context.begin_transaction():
        context.execute(
            f"CREATE SCHEMA IF NOT EXISTS {core_configuration.DB_SCHEMA}"
        )
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    In this scenario we need to create an Engine and associate a connection
    with the context.

    """

    connectable: AsyncEngine = async_engine_from_config(
        configuration=config.get_section(
            name=config.config_ini_section, default={}
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    """

    asyncio.run(main=run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

    # Create Initial Data in database
    asyncio.run(main=insert_db_data(async_session))
