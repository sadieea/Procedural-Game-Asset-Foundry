"""
Generation orchestrator for managing asset generation.
Integrates with Bria Fibo API for real image generation.
"""

import uuid
from typing import Dict, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
import structlog
from app.services.comfyui_service import ComfyUIService
from app.core.config import get_settings

logger = structlog.get_logger(__name__)


class GenerationOrchestrator:
    """Orchestrates asset generation using ComfyUI + Bria FIBO."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.settings = get_settings()
        self.comfyui_service = ComfyUIService()
    
    async def generate_single_asset(
        self,
        asset_type: str,
        parameters: Dict,
        notes: str = "",
        tags: List[str] = None,
        parent_asset_id: str = None
    ) -> Dict:
        """Generate a single asset using Bria Fibo API."""
        
        logger.info("Starting asset generation", 
                   asset_type=asset_type, 
                   parameters=parameters)
        
        try:
            # Build prompt from parameters
            prompt = self._build_prompt_from_parameters(asset_type, parameters)
            
            logger.info("Generated prompt", prompt=prompt)
            
            # Determine image dimensions based on asset type
            width, height = self._get_asset_dimensions(asset_type)
            
            # Extract generation parameters
            seed = parameters.get("seed")
            
            # Generate the image using ComfyUI + Bria FIBO (which will fallback to enhanced mock service)
            result = await self.comfyui_service.generate_image(
                prompt=prompt,
                asset_type=asset_type,
                parameters=parameters,
                width=width,
                height=height,
                seed=seed
            )
            
            # Add additional metadata
            if result.get("metadata"):
                result["metadata"].update({
                    "notes": notes,
                    "tags": tags or [],
                    "parent_asset_id": parent_asset_id,
                    "prompt": prompt
                })
            
            logger.info("Asset generation completed successfully", 
                       asset_id=result.get("metadata", {}).get("asset_id"))
            
            return result
            
        except Exception as e:
            logger.error("Asset generation failed", error=str(e))
            # Return error response in expected format
            return {
                "success": False,
                "error": str(e),
                "asset_url": None,
                "metadata": {
                    "asset_id": str(uuid.uuid4()),
                    "asset_type": asset_type,
                    "parameters": parameters,
                    "error": str(e)
                }
            }
    
    def _get_asset_dimensions(self, asset_type: str) -> tuple[int, int]:
        """Get appropriate dimensions for different asset types."""
        if asset_type == "npc_portrait":
            return (512, 512)  # Square portraits
        elif asset_type == "weapon_item":
            return (512, 512)  # Square items
        elif asset_type == "environment_concept":
            return (1024, 768)  # Landscape format
        else:
            return (1024, 1024)  # Default square
    
    async def generate_batch_assets(
        self,
        asset_type: str,
        base_parameters: Dict,
        variants: List[Dict],
        notes: str = "",
        tags: List[str] = None
    ) -> Dict:
        """Generate batch assets using Bria Fibo API."""
        
        batch_id = str(uuid.uuid4())
        successful_generations = 0
        failed_generations = 0
        
        logger.info("Starting batch generation", 
                   batch_id=batch_id, 
                   variant_count=len(variants))
        
        # Process each variant
        for i, variant_params in enumerate(variants):
            try:
                # Merge base parameters with variant-specific parameters
                merged_params = {**base_parameters, **variant_params}
                
                # Generate single asset
                result = await self.generate_single_asset(
                    asset_type=asset_type,
                    parameters=merged_params,
                    notes=f"{notes} (Batch {batch_id}, Variant {i+1})",
                    tags=tags
                )
                
                if result.get("success"):
                    successful_generations += 1
                else:
                    failed_generations += 1
                    
            except Exception as e:
                logger.error("Batch variant generation failed", 
                           batch_id=batch_id, 
                           variant_index=i, 
                           error=str(e))
                failed_generations += 1
        
        logger.info("Batch generation completed", 
                   batch_id=batch_id,
                   successful=successful_generations,
                   failed=failed_generations)
        
        return {
            "batch_id": batch_id,
            "successful_generations": successful_generations,
            "failed_generations": failed_generations,
            "total_generation_time_ms": 0  # Could track actual time if needed
        }
    
    def _build_prompt_from_parameters(self, asset_type: str, parameters: Dict[str, Any]) -> str:
        """Build a detailed prompt from the UI parameters."""
        
        if asset_type == "npc_portrait":
            return self._build_npc_prompt(parameters)
        elif asset_type == "weapon_item":
            return self._build_weapon_prompt(parameters)
        elif asset_type == "environment_concept":
            return self._build_environment_prompt(parameters)
        else:
            return "A game asset"
    
    def _build_npc_prompt(self, params: Dict[str, Any]) -> str:
        """Build prompt for NPC portrait generation."""
        parts = []
        
        # Base description
        if params.get("character_class"):
            parts.append(f"A {params['character_class']}")
        else:
            parts.append("A character")
        
        # Physical attributes
        if params.get("race"):
            parts.append(f"{params['race']}")
        
        if params.get("gender"):
            parts.append(f"{params['gender']}")
        
        # Appearance details
        if params.get("age_category"):
            parts.append(f"{params['age_category']}")
        
        if params.get("build"):
            parts.append(f"with {params['build']} build")
        
        if params.get("hair_color") and params.get("hair_style"):
            parts.append(f"with {params['hair_color']} {params['hair_style']} hair")
        
        if params.get("eye_color"):
            parts.append(f"and {params['eye_color']} eyes")
        
        # Equipment and style
        if params.get("armor_type"):
            parts.append(f"wearing {params['armor_type']} armor")
        
        if params.get("weapon_visible"):
            parts.append(f"holding a {params['weapon_visible']}")
        
        # Mood and expression
        if params.get("mood"):
            parts.append(f"with a {params['mood']} expression")
        
        # Art style
        style_suffix = ""
        if params.get("art_style"):
            style_suffix = f", {params['art_style']} art style"
        
        prompt = " ".join(parts) + style_suffix + ", high quality, detailed, game character portrait"
        
        return prompt
    
    def _build_weapon_prompt(self, params: Dict[str, Any]) -> str:
        """Build prompt for weapon item generation."""
        parts = []
        
        # Base weapon type
        if params.get("weapon_type"):
            parts.append(f"A {params['weapon_type']}")
        else:
            parts.append("A weapon")
        
        # Material and craftsmanship
        if params.get("material"):
            parts.append(f"made of {params['material']}")
        
        if params.get("rarity"):
            rarity_desc = {
                "common": "simple",
                "uncommon": "well-crafted",
                "rare": "masterwork",
                "epic": "legendary",
                "legendary": "mythical"
            }
            parts.append(f"{rarity_desc.get(params['rarity'], 'quality')}")
        
        # Enchantments and effects
        if params.get("enchantment_type"):
            parts.append(f"with {params['enchantment_type']} enchantment")
        
        if params.get("visual_effects"):
            parts.append(f"glowing with {params['visual_effects']} effects")
        
        # Style and presentation
        parts.append("isolated on white background, game item art, highly detailed")
        
        if params.get("art_style"):
            parts.append(f"{params['art_style']} style")
        
        return " ".join(parts)
    
    def _build_environment_prompt(self, params: Dict[str, Any]) -> str:
        """Build prompt for environment concept generation."""
        parts = []
        
        # Base environment
        if params.get("biome"):
            parts.append(f"A {params['biome']} landscape")
        else:
            parts.append("A fantasy landscape")
        
        # Terrain features
        if params.get("terrain_features"):
            features = params["terrain_features"]
            if isinstance(features, list):
                parts.append(f"with {', '.join(features)}")
            else:
                parts.append(f"with {features}")
        
        # Structures and civilization
        if params.get("civilization_level"):
            civ_desc = {
                "pristine": "untouched by civilization",
                "ruins": "with ancient ruins",
                "settlements": "with small settlements",
                "cities": "with grand cities"
            }
            parts.append(civ_desc.get(params["civilization_level"], ""))
        
        # Atmospheric conditions
        if params.get("weather"):
            parts.append(f"under {params['weather']} weather")
        
        if params.get("time_of_day"):
            parts.append(f"during {params['time_of_day']}")
        
        # Mood and atmosphere
        if params.get("mood"):
            parts.append(f"with {params['mood']} atmosphere")
        
        # Art style
        parts.append("concept art, highly detailed, cinematic lighting")
        
        if params.get("art_style"):
            parts.append(f"{params['art_style']} style")
        
        return " ".join(parts)