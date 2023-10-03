"""
    Organization View Module

    Description:
    - This module is responsible for organization views.

"""

# Importing Python Packages

# Importing FastAPI Packages

# Importing Project Files
from apps.base import BaseView
from .model import OrganizationTable
from .schema import (
    OrganizationCreateSchema,
    OrganizationUpdateSchema,
)


# -----------------------------------------------------------------------------


# Organization class
class OrganizationView(
    BaseView[
        OrganizationTable,
        OrganizationCreateSchema,
        OrganizationUpdateSchema,
    ]
):
    """
    Organization View Class

    Description:
    - This class is responsible for organization views.

    """

    def __init__(
        self,
        model: OrganizationTable,
    ):
        """
        Organization View Class Initialization

        Description:
        - This method is responsible for initializing class.

        Parameter:
        - **model** (OrganizationTable): Organization Database Model.

        """

        super().__init__(model=model)


organization_view = OrganizationView(model=OrganizationTable)
