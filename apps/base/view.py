"""
    Base View Module

    Description:
    - This module is responsible for base views.

"""

# Importing Python Packages
from math import ceil
from typing import Generic, TypeVar, Type
from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.dml import Update, Delete

# Importing FastAPI Packages

# Importing Project Files
from database import BaseTable


Model = TypeVar("Model", bound=BaseTable)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)


# -----------------------------------------------------------------------------


class BaseView(
    Generic[
        Model,
        CreateSchema,
        UpdateSchema,
    ]
):
    """
    Base View Class

    Description:
    - This class is responsible for base views.

    """

    def __init__(self, model: Type[Model]):
        """
        Base View Class Initialization

        Description:
        - This method is responsible for CRUD object with default methods to
        Create, Read, Update and Delete.

        Parameter:
        - **model** (Model): SqlAlchemy Model. **(Required)**

        """

        self.model = model

    async def create(
        self, db_session: AsyncSession, record: CreateSchema
    ) -> Model:
        """
        Create method

        Description:
        - This method is responsible for creating a single record.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record** (CreateSchema): Create Schema. **(Required)**

        Return:
        - **record** (Model): SqlAlchemy Model Object.

        """

        record: self.model = self.model(**record.model_dump())
        db_session.add(instance=record)
        await db_session.commit()
        await db_session.refresh(instance=record)

        return record

    async def read_by_id(
        self, db_session: AsyncSession, record_id: int
    ) -> Model:
        """
        Read Method

        Description:
        - This method is responsible for reading a single record by ID.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record_id** (int): Record ID. **(Required)**

        Return:
        - **record** (Model): SqlAlchemy Model Object.

        """

        query: Select = select(self.model).where(self.model.id == record_id)
        result: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )
        return result.scalars().first()

    async def read_by_value(
        self, db_session: AsyncSession, column_name: str, column_value: str
    ) -> Model:
        """
        Read Method

        Description:
        - This method is responsible for reading a single record by value.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **column_name** (str): Column name. **(Required)**
        - **column_value** (str): Column value. **(Required)**

        Return:
        - **record** (Model): SqlAlchemy Model Object.

        """

        query: Select = select(self.model).where(
            getattr(self.model, column_name) == column_value
        )
        result: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )
        return result.scalars().first()

    async def read_all(
        self,
        db_session: AsyncSession,
        page: int | None = None,
        limit: int | None = None,
    ) -> dict:
        """
        Read All Method

        Description:
        - This method is responsible for reading all records.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **page** (int): Page number. **(Optional)**
        - **limit** (int): Limit number. **(Optional)**

        Return:
        - **records** (JSON): Pagination Read Schema.

        """

        query: Select = select(count(self.model.id))
        total_records: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )
        total_records: int = total_records.scalar()

        query: Select = select(self.model).order_by(self.model.id)

        if page and limit:
            query: Select = (
                select(self.model)
                .where(self.model.id > (page - 1) * limit)
                .order_by(self.model.id)
                .limit(limit)
            )

        result: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )

        if not (page and limit):
            return {
                "total_records": total_records,
                "total_pages": 1,
                "page": 1,
                "limit": total_records,
                "records": result.scalars().all(),
            }

        return {
            "total_records": total_records,
            "total_pages": ceil(total_records / limit),
            "page": page,
            "limit": limit,
            "records": result.scalars().all(),
        }

    async def update(
        self, db_session: AsyncSession, record_id: int, record: UpdateSchema
    ) -> Model:
        """
        Update Method

        Description:
        - This method is responsible for updating a single record.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record_id** (int): Record ID. **(Required)**
        - **record** (UpdateSchema): Update Schema. **(Required)**

        Return:
        - **record** (Model): SqlAlchemy Model Object.

        """

        query: Update = (
            update(self.model)
            .where(self.model.id == record_id)
            .values(record.model_dump(exclude_unset=True))
        )
        await db_session.execute(statement=query)
        await db_session.commit()

        return await self.read_by_id(
            db_session=db_session, record_id=record_id
        )

    async def delete(self, db_session: AsyncSession, record_id: int) -> Model:
        """
        Delete Method

        Description:
        - This method is responsible for deleting a single record.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **record_id** (int): Record ID. **(Required)**

        Return:
        - **record** (Model): SqlAlchemy Model Object.

        """

        result: Model = await self.read_by_id(
            db_session=db_session, record_id=record_id
        )

        if not result:
            return None

        query: Delete = delete(self.model).where(self.model.id == record_id)
        await db_session.execute(statement=query)
        await db_session.commit()

        return result
