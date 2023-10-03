"""
    Role View Module

    Description:
    - This module is responsible for role views.

"""

# Importing Python Packages

# Importing FastAPI Packages

# Importing Project Files
from apps.base import BaseView
from .model import RoleTable
from .schema import (
    RoleCreateSchema,
    RoleUpdateSchema,
)


# -----------------------------------------------------------------------------


# Role class
class RoleView(
    BaseView[
        RoleTable,
        RoleCreateSchema,
        RoleUpdateSchema,
    ]
):
    """
    Role View Class

    Description:
    - This class is responsible for role views.

    """

    def __init__(
        self,
        model: RoleTable,
    ):
        """
        Role View Class Initialization

        Description:
        - This method is responsible for initializing class.

        Parameter:
        - **model** (RoleTable): Role Database Model.

        """

        super().__init__(model=model)


role_view = RoleView(model=RoleTable)
