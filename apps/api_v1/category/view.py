"""
    Category View Module

    Description:
    - This module is responsible for category views.

"""

# Importing Python Packages

# Importing FastAPI Packages

# Importing Project Files
from apps.base import BaseView
from .model import CategoryTable
from .schema import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
)


# -----------------------------------------------------------------------------


# Category class
class CategoryView(
    BaseView[
        CategoryTable,
        CategoryCreateSchema,
        CategoryUpdateSchema,
    ]
):
    """
    Category View Class

    Description:
    - This class is responsible for category views.

    """

    def __init__(
        self,
        model: CategoryTable,
    ):
        """
        Category View Class Initialization

        Description:
        - This method is responsible for initializing class.

        Parameter:
        - **model** (CategoryTable): Category Database Model.

        """

        super().__init__(model=model)


category_view = CategoryView(model=CategoryTable)
