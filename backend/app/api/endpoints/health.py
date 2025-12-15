"""
Health check and system status endpoints.
"""

import time
from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_async_session
from app.schemas.asset import HealthResponse
from app.services.fibo_service import FiboService
from app.services.storage_service import StorageService

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check(
    db: AsyncSession = Depends(get_async_session),
    settings = Depends(get_settings)
) -> HealthResponse:
    """
    Comprehensive health check for all system components.
    """
    
    # Check database connectivity
    database_status = "connected"
    try:
        await db.execute("SELECT 1")
    except Exception:
        database_status = "disconnected"
    
    # Check storage availability
    storage_service = StorageService()
    storage_status = "available" if await storage_service.is_available() else "unavailable"
    
    # Check FIBO model status
    fibo_service = FiboService()
    fibo_status = "ready" if await fibo_service.is_ready() else "unavailable"
    
    return HealthResponse(
        status="healthy" if all([
            database_status == "connected",
            storage_status == "available",
            fibo_status == "ready"
        ]) else "degraded",
        service="procedural-game-asset-foundry",
        version="0.1.0",
        timestamp=time.time(),
        database_status=database_status,
        storage_status=storage_status,
        fibo_model_status=fibo_status,
    )


@router.get("/health/detailed")
async def detailed_health_check(
    db: AsyncSession = Depends(get_async_session),
    settings = Depends(get_settings)
) -> Dict:
    """
    Detailed health check with component-specific information.
    Only available in debug mode.
    """
    
    if not settings.DEBUG:
        return {"error": "Detailed health check only available in debug mode"}
    
    # Database details
    db_details = {"status": "connected", "type": "sqlite"}
    try:
        result = await db.execute("SELECT COUNT(*) FROM assets")
        asset_count = result.scalar()
        db_details["asset_count"] = asset_count
    except Exception as e:
        db_details["status"] = "error"
        db_details["error"] = str(e)
    
    # Storage details
    storage_service = StorageService()
    storage_details = await storage_service.get_status()
    
    # FIBO model details
    fibo_service = FiboService()
    fibo_details = await fibo_service.get_status()
    
    # System resources
    import psutil
    system_details = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
    }
    
    return {
        "service": "procedural-game-asset-foundry",
        "version": "0.1.0",
        "timestamp": time.time(),
        "components": {
            "database": db_details,
            "storage": storage_details,
            "fibo_model": fibo_details,
            "system": system_details,
        },
        "configuration": {
            "debug": settings.DEBUG,
            "fibo_model_type": settings.FIBO_MODEL_TYPE,
            "storage_type": settings.STORAGE_TYPE,
            "max_batch_size": settings.MAX_BATCH_SIZE,
        }
    }