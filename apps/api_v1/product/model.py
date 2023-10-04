"""
    Product Model

    Description:
    - This file contains model for product table.

"""

# Importing Python Packages
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Importing FastAPI Packages

# Importing Project Files
from database import BaseTable
from apps.api_v1.category.model import CategoryTable


# -----------------------------------------------------------------------------


class ProductTable(BaseTable):
    """
    Product Table

    Description:
    - This table is used to create product in database.

    """

    product_name: Mapped[str] = mapped_column(String(2_55), unique=True)
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    low_stock_threshold: Mapped[int] = mapped_column(Integer, default=5_0)

    category_id: Mapped[int] = mapped_column(
        ForeignKey(CategoryTable.id, ondelete="CASCADE")
    )

    # Relationship
    product_category: Mapped[CategoryTable] = relationship(
        back_populates="category_product", lazy="joined"
    )
