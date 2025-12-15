"""
Main API router that includes all endpoint modules.
"""

from fastapi import APIRouter

from app.api.endpoints import assets, generation, health

# Create main API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    health.router,
    tags=["health"]
)

api_router.include_router(
    generation.router,
    prefix="/generate",
    tags=["generation"]
)

api_router.include_router(
    assets.router,
    prefix="/assets",
    tags=["assets"]
)