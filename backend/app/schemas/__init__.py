"""
Pydantic schemas for request/response validation and JSON schema definitions.
"""

from app.schemas.asset import (
    AssetResponse,
    BatchGenerationRequest,
    BatchGenerationResponse,
    GenerationRequest,
    GenerationResponse,
)
from app.schemas.fibo import (
    EnvironmentConfig,
    FiboBaseConfig,
    NPCPortraitConfig,
    WeaponItemConfig,
)

__all__ = [
    # Asset schemas
    "AssetResponse",
    "BatchGenerationRequest", 
    "BatchGenerationResponse",
    "GenerationRequest",
    "GenerationResponse",
    # FIBO schemas
    "EnvironmentConfig",
    "FiboBaseConfig", 
    "NPCPortraitConfig",
    "WeaponItemConfig",
]