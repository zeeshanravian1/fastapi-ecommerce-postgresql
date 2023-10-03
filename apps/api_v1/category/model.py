"""
    Category Model

    Description:
    - This file contains model for category table.

"""

# Importing Python Packages
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

# Importing FastAPI Packages

# Importing Project Files
from database import BaseTable


# -----------------------------------------------------------------------------


class CategoryTable(BaseTable):
    """
    Category Table

    Description:
    - This table is used to create category in database.

    """

    category_name: Mapped[str] = mapped_column(String(2_55), unique=True)
    category_description: Mapped[str] = mapped_column(
        String(2_55), nullable=True
    )
