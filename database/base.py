"""
    Base Model

    Description:
    - This file contains base model for all tables.

"""

# Importing Python Packages
from datetime import datetime
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

# Importing FastAPI Packages

# Importing Project Files
from .connection import Base


# -----------------------------------------------------------------------------


class BaseTable(Base):
    """
    Base Table

    Description:
    - This is base model for all tables.

    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=now())
    updated_at: Mapped[datetime] = mapped_column(nullable=True, onupdate=now())

    @declared_attr
    def __tablename__(self) -> str:
        """
        Generate table name automatically.

        """
        return self.__name__.lower().replace("table", "")

    # Convert to dictionary
    def to_dict(self) -> dict:
        """
        Convert to dictionary.

        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
