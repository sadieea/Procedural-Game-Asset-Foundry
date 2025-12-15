"""
Enhanced mock generation service that creates more realistic assets.
Uses AI-powered image generation APIs as fallback when Bria FIBO unavailable.
"""

import asyncio
import base64
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import httpx
import structlog
from app.core.config import get_settings
from app.core.exceptions import GenerationError
from app.services.realistic_local_ai_service import RealisticLocalAIService
from app.services.improved_local_ai_service import ImprovedLocalAIService

logger = structlog.get_logger(__name__)


class EnhancedMockService:
    """Enhanced mock generation with multiple AI services as fallback."""
    
    def __init__(self):
        self.settings = get_settings()
        self.timeout = 30
        
    async def generate_image(
        self,
        prompt: str,
        asset_type: str,
        parameters: Dict[str, Any],
        width: int = 1024,
        height: int = 1024,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate an image using enhanced mock generation.
        Tries multiple AI services before falling back to placeholder.
        """
        
        logger.info("Starting enhanced mock generation", 
                   asset_type=asset_type, 
                   prompt=prompt[:100])
        
        # Try different AI services in order of preference
        services = [
            self._try_external_ai_service,  # NEW: Real AI APIs first
            self._try_realistic_local_ai,
            self._try_improved_local_ai,
            self._try_local_ai_service,
            self._try_pollinations_ai,
            self._try_huggingface_api,
            self._try_picsum_enhanced,
            self._try_placeholder_api,
            self._generate_local_placeholder
        ]
        
        for service in services:
            try:
                logger.info(f"Trying service: {service.__name__}")
                result = await service(prompt, asset_type, parameters, width, height, seed)
                if result:
                    logger.info(f"Service {service.__name__} succeeded")
                    return result
                else:
                    logger.info(f"Service {service.__name__} returned None")
            except Exception as e:
                logger.error(f"Service {service.__name__} failed", error=str(e))
                continue
        


    async def _try_realistic_local_ai(
        self, 
        prompt: str, 
        asset_type: str, 
        parameters: Dict[str, Any],
        width: int, 
        height: int, 
        seed: Optional[int]
    ) -> Optional[Dict[str, Any]]:
        """Try realistic local AI service for high-quality generation."""
        
        try:
            realistic_ai = RealisticLocalAIService()
            result = await realistic_ai.generate_image(
                prompt=prompt,
                asset_type=asset_type,
                parameters=parameters,
                width=width,
                height=height,
                seed=seed
            )
            
            logger.info("Realistic local AI service succeeded", asset_type=asset_type)
            return result
            
        except Exception as e:
            logger.debug("Realistic local AI service failed", error=str(e))
            return None

    async def _try_improved_local_ai(
        self, 
        prompt: str, 
        asset_type: str, 
        parameters: Dict[str, Any],
        width: int, 
        height: int, 
        seed: Optional[int]
    ) -> Optional[Dict[str, Any]]:
        """Try improved local AI service for high-quality generation."""
        
        try:
            improved_ai = ImprovedLocalAIService()
            result = await improved_ai.generate_image(
                prompt=prompt,
                asset_type=asset_type,
                parameters=parameters,
                width=width,
                height=height,
                seed=seed
            )
            
            logger.info("Improved local AI service succeeded", asset_type=asset_type)
            return result
            
        except Exception as e:
            logger.debug("Improved local AI service failed", error=str(e))
            return None

    async def _try_external_ai_service(
        self, 
        prompt: str, 
        asset_type: str, 
        parameters: Dict[str, Any],
        width: int, 
        height: int, 
        seed: Optional[int]
    ) -> Optional[Dict[str, Any]]:
        """Try external AI service for real AI generation."""
        
        try:
            # Import here to avoid circular imports
            from app.services.external_ai_service import ExternalAIService
            
            external_ai = ExternalAIService()
            result = await external_ai.generate_image(
                prompt=prompt,
                asset_type=asset_type,
                parameters=parameters,
                width=width,
                height=height,
                seed=seed
            )
            
            logger.info("External AI service succeeded", asset_type=asset_type)
            return result
            
        except Exception as e:
            logger.error("External AI service failed", error=str(e), exc_info=True)
            return None

        # Final fallback
        return await self._generate_local_placeholder(prompt, asset_type, parameters, width, height, seed)
    
    async def _try_local_ai_service(
        self, 
        prompt: str, 
        asset_type: str, 
        parameters: Dict[str, Any],
        width: int, 
        height: int, 
        seed: Optional[int]
    ) -> Optional[Dict[str, Any]]:
        """Try local AI service for realistic generation."""
        
        try:
            from app.services.local_ai_service import LocalAIService
            
            local_ai = LocalAIService()
            result = await local_ai.generate_image(
                prompt=prompt,
                asset_type=asset_type,
                parameters=parameters,
                width=width,
                height=height,
                seed=seed
            )
            
            logger.info("Local AI service succeeded", asset_type=asset_type)
            return result
            
        except Exception as e:
            logger.debug("Local AI service failed", error=str(e))
            return None
    
    async def _try_pollinations_ai(
        self, 
        prompt: str, 
        asset_type: str, 
        parameters: Dict[str, Any],
        width: int, 
        height: int, 
        seed: Optional[int]
    ) -> Optional[Dict[str, Any]]:
        """Try Pollinations.AI free service."""
        
        try:
            # Pollinations.AI is a free AI image generation service
            enhanced_prompt = self._enhance_prompt_for_service(prompt, asset_type, "pollinations")
            
            # Try different Pollinations endpoints
            endpoints = [
                f"https://image.pollinations.ai/prompt/{enhanced_prompt}?width={width}&height={height}&seed={seed or 42}&model=flux",
                f"https://pollinations.ai/p/{enhanced_prompt}?width={width}&height={height}&seed={seed or 42}",
                f"https://image.pollinations.ai/prompt/{enhanced_prompt}?width={width}&height={height}&seed={seed or 42}"
            ]
            
            async with httpx.AsyncClient(timeout=20.0) as client:
                for endpoint in endpoints:
                    try:
                        response = await client.get(endpoint)
                        
                        if response.status_code == 200 and response.headers.get('content-type', '').startswith('image/'):
                            # Save the generated image
                            asset_url = await self._save_image_bytes(response.content, asset_type)
                            
                            return {
                                "success": True,
                                "asset_url": asset_url,
                                "metadata": {
                                    "asset_id": str(uuid.uuid4()),
                                    "asset_type": asset_type,
                                    "parameters": parameters,
                                    "created_at": datetime.utcnow().isoformat() + "Z",
                                    "file_size": len(response.content),
                                    "dimensions": {"width": width, "height": height},
                                    "format": "png",
                                    "generation_time_ms": 3000,
                                    "service": "pollinations_ai",
                                    "prompt": enhanced_prompt,
                                    "is_mock": False,  # This is real AI generation!
                                    "ai_service": "Pollinations.AI"
                                }
                            }
                    except Exception:
                        continue
                        
        except Exception as e:
            logger.debug("Pollinations.AI failed", error=str(e))
            return None
    
    async def _try_huggingface_api(
        self, 
        prompt: str, 
        asset_type: str, 
        parameters: Dict[str, Any],
        width: int, 
        height: int, 
        seed: Optional[int]
    ) -> Optional[Dict[str, Any]]:
        """Try Hugging Face Inference API (free tier)."""
        
        try:
            # Use Hugging Face's free inference API
            # This uses Stable Diffusion models hosted on HF
            models = [
                "stabilityai/stable-diffusion-2-1",
                "runwayml/stable-diffusion-v1-5",
                "CompVis/stable-diffusion-v1-4"
            ]
            
            enhanced_prompt = self._enhance_prompt_for_service(prompt, asset_type, "huggingface")
            
            for model in models:
                try:
                    url = f"https://api-inference.huggingface.co/models/{model}"
                    
                    payload = {
                        "inputs": enhanced_prompt,
                        "parameters": {
                            "width": width,
                            "height": height,
                            "num_inference_steps": 20,
                            "guidance_scale": 7.5
                        }
                    }
                    
                    # Note: HF API is free but has rate limits
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        response = await client.post(
                            url,
                            json=payload,
                            headers={"Content-Type": "application/json"}
                        )
                        
                        if response.status_code == 200 and response.headers.get('content-type', '').startswith('image/'):
                            # Save the generated image
                            asset_url = await self._save_image_bytes(response.content, asset_type)
                            
                            return {
                                "success": True,
                                "asset_url": asset_url,
                                "metadata": {
                                    "asset_id": str(uuid.uuid4()),
                                    "asset_type": asset_type,
                                    "parameters": parameters,
                                    "created_at": datetime.utcnow().isoformat() + "Z",
                                    "file_size": len(response.content),
                                    "dimensions": {"width": width, "height": height},
                                    "format": "png",
                                    "generation_time_ms": 5000,
                                    "service": "huggingface_api",
                                    "prompt": enhanced_prompt,
                                    "is_mock": False,  # This is real AI generation!
                                    "ai_service": f"Hugging Face ({model})"
                                }
                            }
                        elif response.status_code == 503:
                            # Model is loading, try next one
                            continue
                            
                except Exception:
                    continue
                    
        except Exception as e:
            logger.debug("Hugging Face API failed", error=str(e))
            return None
    
    async def _try_picsum_enhanced(
        self, 
        prompt: str, 
        asset_type: str, 
        parameters: Dict[str, Any],
        width: int, 
        height: int, 
        seed: Optional[int]
    ) -> Optional[Dict[str, Any]]:
        """Enhanced Picsum with better categorization."""
        
        try:
            # Use different Picsum categories based on asset type
            category_map = {
                "npc_portrait": "people",
                "weapon_item": "objects", 
                "environment_concept": "nature"
            }
            
            category = category_map.get(asset_type, "random")
            seed_val = seed or hash(prompt) % 1000
            
            # Try Unsplash API first (higher quality)
            unsplash_url = f"https://source.unsplash.com/{width}x{height}/?{category}&sig={seed_val}"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(unsplash_url)
                
                if response.status_code == 200:
                    asset_url = await self._save_image_bytes(response.content, asset_type)
                    
                    return {
                        "success": True,
                        "asset_url": asset_url,
                        "metadata": {
                            "asset_id": str(uuid.uuid4()),
                            "asset_type": asset_type,
                            "parameters": parameters,
                            "created_at": datetime.utcnow().isoformat() + "Z",
                            "file_size": len(response.content),
                            "dimensions": {"width": width, "height": height},
                            "format": "jpg",
                            "generation_time_ms": 1500,
                            "service": "unsplash",
                            "prompt": prompt,
                            "is_mock": True,
                            "mock_service": "Unsplash (High-quality photos)"
                        }
                    }
        except Exception as e:
            logger.debug("Enhanced Picsum failed", error=str(e))
            return None
    
    async def _try_placeholder_api(
        self, 
        prompt: str, 
        asset_type: str, 
        parameters: Dict[str, Any],
        width: int, 
        height: int, 
        seed: Optional[int]
    ) -> Optional[Dict[str, Any]]:
        """Try placeholder.com with custom text."""
        
        try:
            # Create custom placeholder with asset info
            text = self._generate_placeholder_text(asset_type, parameters)
            seed_val = seed or hash(prompt) % 1000
            
            # Use placeholder.com with custom text
            url = f"https://via.placeholder.com/{width}x{height}/4A90E2/FFFFFF"
            params = {"text": text}
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                
                if response.status_code == 200:
                    asset_url = await self._save_image_bytes(response.content, asset_type)
                    
                    return {
                        "success": True,
                        "asset_url": asset_url,
                        "metadata": {
                            "asset_id": str(uuid.uuid4()),
                            "asset_type": asset_type,
                            "parameters": parameters,
                            "created_at": datetime.utcnow().isoformat() + "Z",
                            "file_size": len(response.content),
                            "dimensions": {"width": width, "height": height},
                            "format": "png",
                            "generation_time_ms": 1000,
                            "service": "placeholder",
                            "prompt": prompt,
                            "is_mock": True,
                            "mock_service": "Custom Placeholder"
                        }
                    }
        except Exception as e:
            logger.debug("Placeholder API failed", error=str(e))
            return None
    
    async def _generate_local_placeholder(
        self, 
        prompt: str, 
        asset_type: str, 
        parameters: Dict[str, Any],
        width: int, 
        height: int, 
        seed: Optional[int]
    ) -> Dict[str, Any]:
        """Generate a local placeholder as final fallback."""
        
        # Simulate generation delay
        await asyncio.sleep(1)
        
        # Use different placeholder services based on asset type
        base_urls = {
            "npc_portrait": "https://thispersondoesnotexist.com/image",
            "weapon_item": "https://picsum.photos",
            "environment_concept": "https://picsum.photos"
        }
        
        base_url = base_urls.get(asset_type, "https://picsum.photos")
        seed_val = seed or hash(str(parameters)) % 1000
        
        if asset_type == "npc_portrait":
            mock_url = f"{base_url}?{seed_val}"
        else:
            mock_url = f"{base_url}/{width}/{height}?random={seed_val}"
            if asset_type == "weapon_item":
                mock_url += "&grayscale"
        
        return {
            "success": True,
            "asset_url": mock_url,
            "metadata": {
                "asset_id": str(uuid.uuid4()),
                "asset_type": asset_type,
                "parameters": parameters,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "file_size": 1024000,
                "dimensions": {"width": width, "height": height},
                "format": "png",
                "generation_time_ms": 1000,
                "service": "local_placeholder",
                "prompt": prompt,
                "is_mock": True,
                "mock_service": "Local Placeholder Generator"
            }
        }
    
    def _enhance_prompt_for_service(self, prompt: str, asset_type: str, service: str) -> str:
        """Enhance prompt for specific AI service."""
        
        enhancements = {
            "pollinations": {
                "npc_portrait": "portrait, character design, high quality, detailed face",
                "weapon_item": "weapon design, game asset, isolated object, white background",
                "environment_concept": "landscape, environment art, concept art, detailed"
            },
            "huggingface": {
                "npc_portrait": "portrait, character art, fantasy character, detailed, high quality",
                "weapon_item": "weapon concept art, game asset, item design, white background",
                "environment_concept": "environment concept art, landscape, fantasy art, detailed"
            }
        }
        
        enhancement = enhancements.get(service, {}).get(asset_type, "high quality, detailed")
        return f"{prompt}, {enhancement}"
    
    def _generate_placeholder_text(self, asset_type: str, parameters: Dict[str, Any]) -> str:
        """Generate descriptive text for placeholder images."""
        
        if asset_type == "npc_portrait":
            char_class = parameters.get("character_class", "Character")
            race = parameters.get("race", "")
            return f"{char_class} {race}".strip()
        elif asset_type == "weapon_item":
            weapon_type = parameters.get("weapon_type", "Weapon")
            material = parameters.get("material", "")
            return f"{material} {weapon_type}".strip()
        elif asset_type == "environment_concept":
            biome = parameters.get("biome", "Environment")
            return f"{biome} Concept"
        else:
            return "Game Asset"
    
    async def _save_image_bytes(self, image_bytes: bytes, asset_type: str) -> str:
        """Save image bytes to storage and return URL."""
        
        try:
            # Generate filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"{asset_type}_{timestamp}_{uuid.uuid4().hex[:8]}.png"
            
            # Save to storage
            import os
            storage_path = self.settings.STORAGE_PATH
            os.makedirs(storage_path, exist_ok=True)
            
            file_path = os.path.join(storage_path, filename)
            
            with open(file_path, "wb") as f:
                f.write(image_bytes)
            
            logger.info("Image saved", filename=filename, size=len(image_bytes))
            
            return f"/storage/{filename}"
            
        except Exception as e:
            logger.error("Failed to save image", error=str(e))
            # Return external URL as fallback
            return f"data:image/png;base64,{base64.b64encode(image_bytes).decode()}"