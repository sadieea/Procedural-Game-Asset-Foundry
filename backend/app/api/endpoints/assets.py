"""
Asset management endpoints.
Handles asset retrieval, listing, and metadata operations.
"""

from typing import List, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.schemas.asset import AssetListResponse, AssetResponse
from app.services.asset_service import AssetService
from app.services.storage_service import StorageService

router = APIRouter()
logger = structlog.get_logger()


@router.get("", response_model=AssetListResponse)
async def list_assets(
    asset_type: Optional[str] = Query(None, description="Filter by asset type"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: AsyncSession = Depends(get_async_session),
) -> AssetListResponse:
    """
    List assets with filtering, pagination, and sorting.
    
    Supports filtering by asset type and tags, with configurable
    pagination and sorting options.
    """
    
    try:
        asset_service = AssetService(db)
        
        result = await asset_service.list_assets(
            asset_type=asset_type,
            tags=tags,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        
        logger.info(
            "Assets listed",
            total=result.total,
            page=page,
            page_size=page_size,
            asset_type=asset_type,
        )
        
        return result
        
    except Exception as e:
        logger.error("Error listing assets", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: str,
    db: AsyncSession = Depends(get_async_session),
) -> AssetResponse:
    """
    Get a specific asset by ID.
    
    Returns complete asset metadata including generation parameters,
    file information, and timestamps.
    """
    
    try:
        asset_service = AssetService(db)
        asset = await asset_service.get_asset_by_id(asset_id)
        
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        logger.info("Asset retrieved", asset_id=asset_id, asset_type=asset.asset_type)
        
        return AssetResponse(
            id=asset.id,
            asset_type=asset.asset_type,
            schema_version=asset.schema_version,
            parameters=asset.parameters,
            seed=asset.seed,
            image_url=f"/api/assets/{asset_id}/image",
            thumbnail_url=f"/api/assets/{asset_id}/thumbnail" if asset.thumbnail_path else None,
            file_size=asset.file_size,
            mime_type=asset.mime_type,
            width=asset.width,
            height=asset.height,
            color_depth=asset.color_depth,
            has_transparency=asset.has_transparency,
            generation_time_ms=asset.generation_time_ms,
            model_version=asset.model_version,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            tags=asset.tags or [],
            notes=asset.notes,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error retrieving asset", error=str(e), asset_id=asset_id)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{asset_id}/image")
async def get_asset_image(
    asset_id: str,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Download the full-resolution asset image.
    
    Returns the image file with appropriate headers for browser display
    or download.
    """
    
    try:
        asset_service = AssetService(db)
        asset = await asset_service.get_asset_by_id(asset_id)
        
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        storage_service = StorageService()
        file_path = await storage_service.get_file_path(asset.file_path)
        
        if not await storage_service.file_exists(asset.file_path):
            raise HTTPException(status_code=404, detail="Asset file not found")
        
        logger.info("Asset image served", asset_id=asset_id, file_path=asset.file_path)
        
        return FileResponse(
            path=file_path,
            media_type=asset.mime_type,
            filename=f"{asset_id}.png",
            headers={
                "Cache-Control": "public, max-age=31536000",  # 1 year cache
                "Content-Length": str(asset.file_size),
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error serving asset image", error=str(e), asset_id=asset_id)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{asset_id}/thumbnail")
async def get_asset_thumbnail(
    asset_id: str,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Download the asset thumbnail image.
    
    Returns a smaller version of the asset optimized for previews
    and listing views.
    """
    
    try:
        asset_service = AssetService(db)
        asset = await asset_service.get_asset_by_id(asset_id)
        
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        if not asset.thumbnail_path:
            # Fallback to main image if no thumbnail
            return await get_asset_image(asset_id, db)
        
        storage_service = StorageService()
        file_path = await storage_service.get_file_path(asset.thumbnail_path)
        
        if not await storage_service.file_exists(asset.thumbnail_path):
            # Fallback to main image if thumbnail missing
            return await get_asset_image(asset_id, db)
        
        logger.info("Asset thumbnail served", asset_id=asset_id, file_path=asset.thumbnail_path)
        
        return FileResponse(
            path=file_path,
            media_type=asset.mime_type,
            filename=f"{asset_id}_thumb.png",
            headers={
                "Cache-Control": "public, max-age=31536000",  # 1 year cache
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error serving asset thumbnail", error=str(e), asset_id=asset_id)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{asset_id}")
async def delete_asset(
    asset_id: str,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Soft delete an asset.
    
    Marks the asset as deleted without removing the files,
    allowing for potential recovery.
    """
    
    try:
        asset_service = AssetService(db)
        success = await asset_service.soft_delete_asset(asset_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        logger.info("Asset soft deleted", asset_id=asset_id)
        
        return {"success": True, "message": "Asset deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error deleting asset", error=str(e), asset_id=asset_id)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{asset_id}/restore")
async def restore_asset(
    asset_id: str,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Restore a soft-deleted asset.
    
    Removes the deletion timestamp, making the asset available again.
    """
    
    try:
        asset_service = AssetService(db)
        success = await asset_service.restore_asset(asset_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Asset not found or not deleted")
        
        logger.info("Asset restored", asset_id=asset_id)
        
        return {"success": True, "message": "Asset restored successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error restoring asset", error=str(e), asset_id=asset_id)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{asset_id}/history")
async def get_asset_history(
    asset_id: str,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Get the generation history for an asset.
    
    Returns all generation attempts, including failures and regenerations.
    """
    
    try:
        asset_service = AssetService(db)
        history = await asset_service.get_asset_history(asset_id)
        
        if not history:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        logger.info("Asset history retrieved", asset_id=asset_id, history_count=len(history))
        
        return {
            "asset_id": asset_id,
            "history": [entry.to_dict() for entry in history]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error retrieving asset history", error=str(e), asset_id=asset_id)
        raise HTTPException(status_code=500, detail="Internal server error")