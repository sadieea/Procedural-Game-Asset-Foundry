"""
Pydantic schemas for asset generation requests and responses.
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, validator

from app.schemas.fibo import AssetConfig, EnvironmentConfig, NPCPortraitConfig, WeaponItemConfig


class GenerationRequest(BaseModel):
    """Request schema for single asset generation."""
    
    asset_type: Literal["npc_portrait", "weapon_item", "environment_concept"]
    schema_version: str = Field(default="v1", pattern=r"^v\d+$")
    parameters: Dict[str, Any]  # Use flexible dict instead of strict Union
    notes: Optional[str] = Field(None, max_length=1000)
    tags: Optional[List[str]] = Field(default_factory=list, max_items=10)
    
    @validator("parameters")
    def validate_parameters_match_type(cls, v, values):
        """Ensure parameters match the specified asset type."""
        if "asset_type" not in values:
            return v
            
        asset_type = values["asset_type"]
        
        # Handle both dict and object types
        if isinstance(v, dict):
            param_type = v.get("assetType")
        else:
            param_type = getattr(v, "assetType", None)
        
        if param_type != asset_type:
            raise ValueError(f"Parameters assetType '{param_type}' does not match asset_type '{asset_type}'")
        
        return v
    
    @validator("tags")
    def validate_tags(cls, v):
        """Validate tag format and content."""
        if not v:
            return v
            
        for tag in v:
            if not isinstance(tag, str):
                raise ValueError("All tags must be strings")
            if len(tag.strip()) == 0:
                raise ValueError("Tags cannot be empty")
            if len(tag) > 50:
                raise ValueError("Tags cannot exceed 50 characters")
                
        return [tag.strip().lower() for tag in v]


class BatchVariant(BaseModel):
    """Single variant for batch generation."""
    
    name: Optional[str] = Field(None, max_length=100)
    parameters: Dict[str, Any] = Field(description="Parameter overrides for this variant")
    
    @validator("parameters")
    def validate_parameters_not_empty(cls, v):
        """Ensure parameters dict is not empty."""
        if not v:
            raise ValueError("Variant parameters cannot be empty")
        return v


class BatchGenerationRequest(BaseModel):
    """Request schema for batch asset generation."""
    
    asset_type: Literal["npc_portrait", "weapon_item", "environment_concept"]
    schema_version: str = Field(default="v1", pattern=r"^v\d+$")
    base_parameters: Dict[str, Any]  # Use flexible dict instead of strict Union
    variants: List[BatchVariant] = Field(min_items=1, max_items=10)
    notes: Optional[str] = Field(None, max_length=1000)
    tags: Optional[List[str]] = Field(default_factory=list, max_items=10)
    
    @validator("base_parameters")
    def validate_base_parameters_match_type(cls, v, values):
        """Ensure base parameters match the specified asset type."""
        if "asset_type" not in values:
            return v
            
        asset_type = values["asset_type"]
        param_type = getattr(v, "type", None)
        
        if param_type != asset_type:
            raise ValueError(f"Base parameters type '{param_type}' does not match asset_type '{asset_type}'")
        
        return v


class AssetMetadata(BaseModel):
    """Asset metadata for responses."""
    
    generation_time_ms: float
    file_size: int
    dimensions: Dict[str, int]  # {"width": 512, "height": 512}
    format: str = "png"
    has_transparency: bool = False
    color_depth: str = "8bit"
    model_version: str


class GenerationResponse(BaseModel):
    """Response schema for single asset generation."""
    
    success: bool = True
    asset_id: str
    asset_type: str
    image_url: str
    thumbnail_url: Optional[str] = None
    parameters: Dict[str, Any]
    seed: Optional[int] = None
    metadata: AssetMetadata
    tags: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class BatchGenerationResponse(BaseModel):
    """Response schema for batch asset generation."""
    
    success: bool = True
    batch_id: str
    asset_type: str
    total_variants: int
    successful_generations: int
    failed_generations: int
    assets: List[GenerationResponse]
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    total_generation_time_ms: float
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AssetResponse(BaseModel):
    """Response schema for asset retrieval."""
    
    id: str
    asset_type: str
    schema_version: str
    parameters: Dict[str, Any]
    seed: Optional[int] = None
    image_url: str
    thumbnail_url: Optional[str] = None
    file_size: int
    mime_type: str
    width: int
    height: int
    color_depth: str
    has_transparency: bool
    generation_time_ms: float
    model_version: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AssetListResponse(BaseModel):
    """Response schema for asset listing."""
    
    assets: List[AssetResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool


class RegenerationRequest(BaseModel):
    """Request schema for asset regeneration."""
    
    asset_id: str = Field(description="ID of the asset to regenerate from")
    parameter_overrides: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Parameters to override from the original"
    )
    new_seed: Optional[int] = Field(None, ge=0, le=2**32-1)
    notes: Optional[str] = Field(None, max_length=1000)
    tags: Optional[List[str]] = Field(default_factory=list, max_items=10)


class HealthResponse(BaseModel):
    """Health check response schema."""
    
    status: str = "healthy"
    service: str = "procedural-game-asset-foundry"
    version: str = "0.1.0"
    timestamp: float
    database_status: str = "connected"
    storage_status: str = "available"
    fibo_model_status: str = "ready"


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    
    success: bool = False
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }