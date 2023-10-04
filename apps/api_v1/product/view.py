"""
    Product View Module

    Description:
    - This module is responsible for product views.

"""

# Importing Python Packages
from math import ceil
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.selectable import Select

# Importing FastAPI Packages

# Importing Project Files
from apps.base import BaseView
from .model import ProductTable
from .schema import (
    ProductCreateSchema,
    ProductUpdateSchema,
)


# -----------------------------------------------------------------------------


# Product class
class ProductView(
    BaseView[
        ProductTable,
        ProductCreateSchema,
        ProductUpdateSchema,
    ]
):
    """
    Product View Class

    Description:
    - This class is responsible for product views.

    """

    def __init__(
        self,
        model: ProductTable,
    ):
        """
        Product View Class Initialization

        Description:
        - This method is responsible for initializing class.

        Parameter:
        - **model** (ProductTable): product Database Model.

        """

        super().__init__(model=model)

    async def read_all_by_category_id(
        self,
        db_session: AsyncSession,
        category_id: int,
        page: int | None = None,
        limit: int | None = None,
    ) -> dict:
        """
        Read All Method

        Description:
        - This method is responsible for reading all products by product
        category id.

        Parameter:
        - **db_session** (Session): Database session. **(Required)**
        - **category_id** (int): Product category id. **(Required)**
        - **page** (int): Page number. **(Optional)**
        - **limit** (int): Limit number. **(Optional)**

        Return:
        - **records** (JSON): Pagination Read Schema.

        """

        query: Select = select(count(self.model.id)).where(
            self.model.category_id == category_id
        )
        total_records: ChunkedIteratorResult = await db_session.execute(
            statement=query
        )
        total_records: int = total_records.scalar()

        query: Select = (
            select(self.model)
            .where(self.model.category_id == category_id)
            .order_by(self.model.id)
        )

        if page and limit:
            query: Select = (
                select(self.model)
                .where(
                    self.model.category_id == category_id,
                    self.model.id > (page - 1) * limit,
                )
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


product_view = ProductView(model=ProductTable)
