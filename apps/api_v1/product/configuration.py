"""
    Product Configuration Module

    Description:
    - This module is responsible for product configuration.

"""

# Importing Python Packages

# Importing FastAPI Packages

# Importing Project Files


# -----------------------------------------------------------------------------


class ProductConfiguration:
    """
    Product Settings Class

    Description:
    - This class is used to define product configurations.

    """

    PRODUCT_NAME: str = "Laptop"
    PRICE: float = 500
    QUANTITY: int = 100
    IS_AVAILABLE: bool = True
    LOW_STOCK_THRESHOLD: int = 5_0
    CATEGORY_ID: int = 1
    PRODUCT_COLUMN_NAME: str = "product_name"


product_configuration = ProductConfiguration()
