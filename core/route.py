"""
    FastAPI Route module

    Description:
    - This module is used to create routes for application.

"""

# Importing Python Packages

# Importing FastAPI Packages
from fastapi import APIRouter

# Importing Project Files
from apps.auth.route import router as auth_router
from apps.email.route import router as email_router
from apps.api_v1.routes import router as v1_routers


# Router Object to Create Routes
router = APIRouter()


# -----------------------------------------------------------------------------


# Include all file routes
router.include_router(v1_routers)
router.include_router(email_router)
router.include_router(auth_router)
