"""
Asset generation endpoints.
Handles single and batch generation requests with proper validation.
"""

import uuid
from typing import Any, Dict, List

import structlog
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.exceptions import AssetGenerationError, ValidationError
from app.schemas.asset import (
    BatchGenerationRequest,
    BatchGenerationResponse,
    GenerationRequest,
    GenerationResponse,
    RegenerationRequest,
)
from app.services.asset_service import AssetService
from app.services.generation_orchestrator import GenerationOrchestrator
from app.services.validation_service import ValidationService

router = APIRouter()
logger = structlog.get_logger()


def make_absolute_url(request: Request, relative_url: str) -> str:
    """Convert a relative URL to an absolute URL using the request context."""
    if relative_url and relative_url.startswith('/'):
        base_url = f"{request.url.scheme}://{request.url.netloc}"
        return f"{base_url}{relative_url}"
    return relative_url


@router.post("")
async def generate_asset(
    request_data: dict,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Generate a single asset from JSON configuration.
    
    This endpoint validates the input schema, orchestrates generation,
    stores the result, and returns the asset metadata.
    """
    
    logger.info(
        "Asset generation requested",
        asset_type=request_data.get("asset_type"),
        schema_version=request_data.get("schema_version"),
    )
    
    print(f"🔍 DEBUG: Generation endpoint called with asset_type={request_data.get('asset_type')}")
    print(f"🔍 DEBUG: Parameters={request_data.get('parameters', {})}")
    
    try:
        # Create generation orchestrator
        print(f"🔍 DEBUG: Creating GenerationOrchestrator")
        orchestrator = GenerationOrchestrator(db)
        print(f"🔍 DEBUG: Orchestrator created successfully")
        
        # Generate the asset using the new Bria Fibo integration
        print(f"🔍 DEBUG: Calling generate_single_asset")
        result = await orchestrator.generate_single_asset(
            asset_type=request_data.get("asset_type"),
            parameters=request_data.get("parameters", {}),
            notes=request_data.get("notes", ""),
            tags=request_data.get("tags", [])
        )
        
        # Convert relative asset URL to absolute URL
        if result.get("success") and result.get("asset_url"):
            result["asset_url"] = make_absolute_url(request, result["asset_url"])
        
        logger.info(
            "Asset generation completed",
            asset_id=result.get("metadata", {}).get("asset_id"),
            success=result.get("success")
        )
        
        return result
        
    except ValidationError as e:
        logger.error("Validation failed", error=str(e), asset_type=request_data.get("asset_type"))
        raise HTTPException(status_code=400, detail=str(e))
        
    except AssetGenerationError as e:
        logger.error("Generation failed", error=str(e), asset_type=request_data.get("asset_type"))
        raise HTTPException(status_code=500, detail=str(e))
        
    except Exception as e:
        logger.error("Unexpected error during generation", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/batch", response_model=BatchGenerationResponse)
async def generate_batch_assets(
    request: BatchGenerationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_session),
) -> BatchGenerationResponse:
    """
    Generate multiple asset variants from a base configuration.
    
    Applies parameter overrides to create variations while maintaining
    the base configuration structure.
    """
    
    logger.info(
        "Batch generation requested",
        asset_type=request.asset_type,
        variant_count=len(request.variants),
    )
    
    try:
        # Validate the request
        validation_service = ValidationService()
        validated_base = await validation_service.validate_generation_request(
            GenerationRequest(
                asset_type=request.asset_type,
                schema_version=request.schema_version,
                parameters=request.base_parameters,
                notes=request.notes,
                tags=request.tags,
            )
        )
        
        # Validate variants
        validated_variants = []
        for i, variant in enumerate(request.variants):
            try:
                validated_variant = await validation_service.validate_batch_variant(
                    base_parameters=validated_base,
                    variant=variant,
                    asset_type=request.asset_type,
                )
                validated_variants.append(validated_variant)
            except ValidationError as e:
                logger.error(f"Variant {i} validation failed", error=str(e))
                raise HTTPException(
                    status_code=400, 
                    detail=f"Variant {i} validation failed: {str(e)}"
                )
        
        # Create generation orchestrator
        orchestrator = GenerationOrchestrator(db)
        
        # Generate batch
        result = await orchestrator.generate_batch_assets(
            asset_type=request.asset_type,
            base_parameters=validated_base,
            variants=validated_variants,
            notes=request.notes,
            tags=request.tags or [],
        )
        
        logger.info(
            "Batch generation completed",
            batch_id=result.batch_id,
            successful=result.successful_generations,
            failed=result.failed_generations,
            total_time_ms=result.total_generation_time_ms,
        )
        
        return result
        
    except ValidationError as e:
        logger.error("Batch validation failed", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
        
    except AssetGenerationError as e:
        logger.error("Batch generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
        
    except Exception as e:
        logger.error("Unexpected error during batch generation", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/regenerate", response_model=GenerationResponse)
async def regenerate_asset(
    request: RegenerationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_session),
) -> GenerationResponse:
    """
    Regenerate an asset from existing configuration with optional overrides.
    
    Loads the original asset configuration and applies any parameter
    overrides before regenerating.
    """
    
    logger.info(
        "Asset regeneration requested",
        original_asset_id=request.asset_id,
        has_overrides=bool(request.parameter_overrides),
    )
    
    try:
        # Get asset service
        asset_service = AssetService(db)
        
        # Load original asset
        original_asset = await asset_service.get_asset_by_id(request.asset_id)
        if not original_asset:
            raise HTTPException(status_code=404, detail="Original asset not found")
        
        # Create regeneration request
        regen_request = GenerationRequest(
            asset_type=original_asset.asset_type,
            schema_version=original_asset.schema_version,
            parameters=original_asset.parameters,
            notes=request.notes,
            tags=request.tags or [],
        )
        
        # Apply parameter overrides
        if request.parameter_overrides:
            validation_service = ValidationService()
            regen_request.parameters = await validation_service.apply_parameter_overrides(
                base_parameters=regen_request.parameters,
                overrides=request.parameter_overrides,
                asset_type=original_asset.asset_type,
            )
        
        # Apply new seed if provided
        if request.new_seed is not None:
            regen_request.parameters.seed = request.new_seed
        
        # Validate the modified request
        validation_service = ValidationService()
        validated_params = await validation_service.validate_generation_request(regen_request)
        
        # Create generation orchestrator
        orchestrator = GenerationOrchestrator(db)
        
        # Generate with parent reference
        result = await orchestrator.generate_single_asset(
            asset_type=regen_request.asset_type,
            parameters=validated_params,
            notes=regen_request.notes,
            tags=regen_request.tags or [],
            parent_asset_id=request.asset_id,
        )
        
        logger.info(
            "Asset regeneration completed",
            original_asset_id=request.asset_id,
            new_asset_id=result.asset_id,
            generation_time_ms=result.metadata.generation_time_ms,
        )
        
        return result
        
    except ValidationError as e:
        logger.error("Regeneration validation failed", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
        
    except AssetGenerationError as e:
        logger.error("Regeneration failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
        
    except Exception as e:
        logger.error("Unexpected error during regeneration", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/validate")
async def validate_configuration(
    config_data: Dict,
) -> Dict:
    """
    Validate a FIBO configuration against strict schemas.
    
    This endpoint validates the configuration without generating an asset,
    providing detailed error messages and warnings.
    """
    
    logger.info("Configuration validation requested")
    
    try:
        validation_service = ValidationService()
        result = validation_service.validate_config_strict(config_data)
        
        logger.info(
            "Configuration validation completed",
            success=result.success,
            error_count=len(result.errors),
            warning_count=len(result.warnings)
        )
        
        return result.to_dict()
        
    except Exception as e:
        logger.error("Unexpected validation error", error=str(e))
        return {
            "success": False,
            "errorType": "ValidationError",
            "message": f"Validation failed: {str(e)}",
            "errors": [str(e)],
            "warnings": []
        }


@router.get("/defaults/{asset_type}")
async def get_default_configuration(asset_type: str) -> Dict:
    """
    Get default configuration for an asset type.
    
    Returns a valid, complete configuration that can be used
    as a starting point for generation.
    """
    
    logger.info("Default configuration requested", asset_type=asset_type)
    
    try:
        validation_service = ValidationService()
        default_config = validation_service.get_default_configuration(asset_type)
        
        if not default_config:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid asset type: {asset_type}"
            )
        
        logger.info("Default configuration retrieved", asset_type=asset_type)
        
        return {
            "success": True,
            "asset_type": asset_type,
            "schema_version": "v1",
            "default_config": default_config,
            "validation_status": "valid",
            "warnings": []
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting default configuration", error=str(e), asset_type=asset_type)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/schemas/{asset_type}")
async def get_asset_schema(asset_type: str) -> Dict:
    """
    Get JSON schema for an asset type.
    
    Returns the complete Pydantic schema that defines the structure
    and validation rules for the asset type.
    """
    
    logger.info("Schema requested", asset_type=asset_type)
    
    try:
        validation_service = ValidationService()
        schema = validation_service.get_validation_schema(asset_type)
        
        if not schema:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid asset type: {asset_type}"
            )
        
        logger.info("Schema retrieved", asset_type=asset_type)
        
        return {
            "success": True,
            "asset_type": asset_type,
            "schema_version": "v1",
            "schema": schema
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting schema", error=str(e), asset_type=asset_type)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/test")
async def test_endpoint() -> Dict:
    """Test endpoint to verify routing."""
    import os
    from app.core.config import get_settings
    
    settings = get_settings()
    storage_path = settings.STORAGE_PATH
    abs_path = os.path.abspath(storage_path)
    exists = os.path.exists(abs_path)
    
    files = []
    if exists:
        files = [f for f in os.listdir(abs_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    return {
        "message": "Test endpoint working",
        "storage_path": storage_path,
        "absolute_path": abs_path,
        "exists": exists,
        "file_count": len(files),
        "sample_files": files[:3]
    }

@router.get("/history")
async def get_asset_history() -> Dict:
    """
    Get all existing assets from storage directory.
    
    Scans the storage directory and returns metadata for all generated assets.
    """
    
    try:
        import os
        import re
        from datetime import datetime
        from app.core.config import get_settings
        
        settings = get_settings()
        storage_path = settings.STORAGE_PATH
        
        # Make sure the path exists
        if not os.path.exists(storage_path):
            return {
                "success": True,
                "assets": [],
                "count": 0
            }
        
        assets = []
        all_files = os.listdir(storage_path)
        image_files = [f for f in all_files if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        for filename in image_files:
            # Simple parsing - just create basic asset info
            parts = filename.split('_')
            if len(parts) >= 4:
                asset_type = parts[0]
                asset_id = parts[-1].split('.')[0]  # Remove extension
                
                # Create basic asset
                asset = {
                    "id": asset_id,
                    "type": asset_type,
                    "image_url": f"/storage/{filename}",
                    "thumbnail_url": f"/storage/{filename}",
                    "created_at": datetime.now().isoformat() + "Z",
                    "metadata": {
                        "asset_id": asset_id,
                        "asset_type": asset_type,
                        "file_size": 1024000,
                        "format": "png",
                        "dimensions": {"width": 1024, "height": 1024},
                        "generation_time": "N/A",
                        "service": "historical",
                        "ai_service": "Previously Generated"
                    },
                    "config": {
                        "assetType": asset_type,
                        "parameters": {}
                    }
                }
                
                assets.append(asset)
        
        logger.info("Retrieved asset history", count=len(assets))
        
        return {
            "success": True,
            "assets": assets,
            "count": len(assets)
        }
        
    except Exception as e:
        logger.error("Error getting asset history", error=str(e))
        return {
            "success": False,
            "assets": [],
            "count": 0,
            "error": str(e)
        }


@router.get("/status/{generation_id}")
async def get_generation_status(
    generation_id: str,
    db: AsyncSession = Depends(get_async_session),
) -> Dict:
    """
    Get the status of a generation request.
    
    Useful for tracking long-running batch generations or checking
    if a generation is still in progress.
    """
    
    try:
        asset_service = AssetService(db)
        status = await asset_service.get_generation_status(generation_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Generation not found")
        
        return status
        
    except Exception as e:
        logger.error("Error getting generation status", error=str(e), generation_id=generation_id)
        raise HTTPException(status_code=500, detail="Internal server error")