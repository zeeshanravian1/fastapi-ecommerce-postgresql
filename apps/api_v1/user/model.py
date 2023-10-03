"""
    User Model

    Description:
    - This file contains model for user table.

"""

# Importing Python Packages
from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Importing FastAPI Packages

# Importing Project Files
from database import BaseTable
from core import UserTokenStatus, core_configuration
from ..role.model import RoleTable
from ..organization.model import OrganizationTable


# -----------------------------------------------------------------------------


class UserTable(BaseTable):
    """
    User Table

    Description:
    - This table is used to create user in database.

    """

    first_name: Mapped[str] = mapped_column(String(2_55))
    last_name: Mapped[str] = mapped_column(String(2_55))
    contact: Mapped[str] = mapped_column(String(2_55), nullable=True)
    username: Mapped[str] = mapped_column(String(2_55), unique=True)
    email: Mapped[str] = mapped_column(String(2_55), unique=True)
    password: Mapped[str] = mapped_column(String(2_55))
    address: Mapped[str] = mapped_column(String(2_55), nullable=True)
    city: Mapped[str] = mapped_column(String(2_55), nullable=True)
    state: Mapped[str] = mapped_column(String(2_55), nullable=True)
    country: Mapped[str] = mapped_column(String(2_55), nullable=True)
    postal_code: Mapped[str] = mapped_column(String(2_55), nullable=True)
    profile_image_path: Mapped[str] = mapped_column(
        String(2_55), nullable=True
    )
    email_otp: Mapped[str] = mapped_column(String(2_55), nullable=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    password_otp: Mapped[str] = mapped_column(String(2_55), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    token_status: Mapped[str] = mapped_column(
        Enum(UserTokenStatus, schema=core_configuration.DB_SCHEMA),
        default=UserTokenStatus.LOGOUT,
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey(RoleTable.id, ondelete="CASCADE")
    )
    organization_id: Mapped[int | None] = mapped_column(
        ForeignKey(OrganizationTable.id, ondelete="CASCADE")
    )

    # Relationship
    user_role: Mapped[RoleTable] = relationship(
        back_populates="role_user", lazy="joined"
    )
    user_organization: Mapped[OrganizationTable | None] = relationship(
        back_populates="organization_user", lazy="joined"
    )
