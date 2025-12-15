"""
Bria Fibo API service for image generation.
Handles communication with Bria's Fibo API for procedural asset generation.
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

logger = structlog.get_logger(__name__)


class BriaFiboService:
    """Service for interacting with Bria Fibo API."""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_url = self.settings.FIBO_API_URL
        self.api_key = self.settings.FIBO_API_KEY
        self.timeout = self.settings.GENERATION_TIMEOUT_SECONDS
        
        if not self.api_key:
            logger.warning("FIBO_API_KEY not configured, falling back to mock mode")
    
    async def generate_image(
        self,
        prompt: str,
        asset_type: str,
        parameters: Dict[str, Any],
        width: int = 1024,
        height: int = 1024,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate an image using Bria API (official specification).
        
        Args:
            prompt: Text description for image generation
            asset_type: Type of asset being generated
            parameters: Additional parameters from the UI
            width: Image width in pixels
            height: Image height in pixels
            num_inference_steps: Number of denoising steps
            guidance_scale: How closely to follow the prompt
            seed: Random seed for reproducible results
            
        Returns:
            Dict containing generation results
        """
        if not self.api_key:
            logger.warning("No API key configured, using mock generation")
            return await self._mock_generation(prompt, asset_type, parameters)
        
        try:
            # Prepare the request payload according to Bria API spec
            payload = {
                "prompt": prompt,
                "width": width,
                "height": height,
                "sync": False  # Use asynchronous processing by default
            }
            
            if seed is not None:
                payload["seed"] = seed
            
            # Use official Bria API authentication
            headers = {
                "api_token": self.api_key,  # Official Bria API uses api_token header
                "Content-Type": "application/json"
            }
            
            logger.info("Sending generation request to Bria API", 
                       asset_type=asset_type, prompt=prompt[:100])
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Try the official Bria API endpoints
                endpoints_to_try = [
                    f"{self.api_url}/text-to-image",
                    f"{self.api_url}/generate",
                    "https://engine.prod.bria-api.com/v1/text-to-image",
                    "https://api.bria.ai/v1/text-to-image"
                ]
                
                for endpoint in endpoints_to_try:
                    try:
                        logger.info("Trying Bria endpoint", endpoint=endpoint)
                        response = await client.post(
                            endpoint,
                            json=payload,
                            headers=headers
                        )
                        
                        logger.info("Bria API response", 
                                   endpoint=endpoint, 
                                   status=response.status_code)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            # Check if this is an asynchronous response
                            if "request_id" in result and "status_url" in result:
                                logger.info("Received async response, polling for completion", 
                                           request_id=result["request_id"])
                                return await self._poll_async_result(
                                    client, result, asset_type, parameters
                                )
                            else:
                                # Synchronous response
                                return await self._process_generation_result(result, asset_type, parameters)
                                
                        elif response.status_code == 401:
                            logger.error("Authentication failed", endpoint=endpoint)
                            # Try next endpoint in case of different auth requirements
                            continue
                        elif response.status_code == 404:
                            logger.warning("Endpoint not found", endpoint=endpoint)
                            continue
                        elif response.status_code == 429:
                            logger.warning("Rate limit exceeded", endpoint=endpoint)
                            # Wait and retry with exponential backoff
                            await asyncio.sleep(2)
                            continue
                        else:
                            error_msg = f"Bria API error: {response.status_code} - {response.text}"
                            logger.error("API error", error=error_msg, endpoint=endpoint)
                            continue
                            
                    except httpx.ConnectError as e:
                        logger.warning("Connection failed", endpoint=endpoint, error=str(e))
                        continue
                    except Exception as e:
                        logger.error("Unexpected error", endpoint=endpoint, error=str(e))
                        continue
                
                # If all endpoints failed, fall back to mock
                logger.warning("All Bria API endpoints failed, falling back to mock generation")
                return await self._mock_generation(prompt, asset_type, parameters)
                
        except httpx.TimeoutException:
            error_msg = f"Generation timeout after {self.timeout} seconds"
            logger.error("Generation timeout", timeout=self.timeout)
            logger.warning("Timeout occurred, falling back to mock generation")
            return await self._mock_generation(prompt, asset_type, parameters)
        except httpx.ConnectError as e:
            logger.warning("Connection error, falling back to mock generation", error=str(e))
            return await self._mock_generation(prompt, asset_type, parameters)
        except Exception as e:
            error_msg = f"Generation failed: {str(e)}"
            logger.error("Generation error", error=str(e))
            # For development, fall back to mock instead of failing
            logger.warning("Unexpected error, falling back to mock generation")
            return await self._mock_generation(prompt, asset_type, parameters)
    
    def _prepare_asset_parameters(self, asset_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare asset-specific parameters for the API request."""
        fibo_params = {}
        
        if asset_type == "npc_portrait":
            # Map NPC portrait parameters
            if "character_class" in parameters:
                fibo_params["style"] = f"{parameters['character_class']} character"
            if "mood" in parameters:
                fibo_params["mood"] = parameters["mood"]
            if "art_style" in parameters:
                fibo_params["art_style"] = parameters["art_style"]
                
        elif asset_type == "weapon_item":
            # Map weapon item parameters
            if "weapon_type" in parameters:
                fibo_params["object_type"] = parameters["weapon_type"]
            if "material" in parameters:
                fibo_params["material"] = parameters["material"]
            if "rarity" in parameters:
                fibo_params["quality"] = parameters["rarity"]
                
        elif asset_type == "environment_concept":
            # Map environment parameters
            if "biome" in parameters:
                fibo_params["environment"] = parameters["biome"]
            if "time_of_day" in parameters:
                fibo_params["lighting"] = parameters["time_of_day"]
            if "weather" in parameters:
                fibo_params["atmosphere"] = parameters["weather"]
        
        return fibo_params
    
    async def _poll_async_result(
        self,
        client: httpx.AsyncClient,
        initial_response: Dict[str, Any],
        asset_type: str,
        parameters: Dict[str, Any],
        max_polls: int = 30,
        poll_interval: float = 2.0
    ) -> Dict[str, Any]:
        """Poll the Bria API for async generation results."""
        
        request_id = initial_response["request_id"]
        status_url = initial_response["status_url"]
        
        headers = {
            "api_token": self.api_key,
            "Content-Type": "application/json"
        }
        
        logger.info("Starting async polling", request_id=request_id, status_url=status_url)
        
        for poll_count in range(max_polls):
            try:
                await asyncio.sleep(poll_interval)
                
                response = await client.get(status_url, headers=headers)
                
                if response.status_code != 200:
                    logger.error("Status polling failed", 
                               status_code=response.status_code, 
                               response=response.text)
                    continue
                
                status_result = response.json()
                status = status_result.get("status")
                
                logger.info("Polling status", 
                           request_id=request_id, 
                           status=status, 
                           poll_count=poll_count + 1)
                
                if status == "COMPLETED":
                    logger.info("Generation completed successfully", request_id=request_id)
                    return await self._process_generation_result(status_result, asset_type, parameters)
                elif status == "ERROR":
                    error_info = status_result.get("error", "Unknown error")
                    logger.error("Generation failed", request_id=request_id, error=error_info)
                    raise GenerationError(f"Bria API generation failed: {error_info}")
                elif status == "UNKNOWN":
                    logger.error("Unknown status", request_id=request_id)
                    raise GenerationError(f"Unknown status for request {request_id}")
                elif status == "IN_PROGRESS":
                    # Continue polling
                    continue
                else:
                    logger.warning("Unexpected status", request_id=request_id, status=status)
                    continue
                    
            except Exception as e:
                logger.error("Error during polling", request_id=request_id, error=str(e))
                continue
        
        # Timeout reached
        logger.error("Polling timeout reached", request_id=request_id, max_polls=max_polls)
        raise GenerationError(f"Generation timeout after {max_polls} polls")

    async def _process_generation_result(
        self, 
        result: Dict[str, Any], 
        asset_type: str, 
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process the generation result from Bria API."""
        
        # Check for image URL (Bria API V2 format)
        image_url = result.get("result", {}).get("image_url")
        if image_url:
            # Download and save the image
            asset_url = await self._download_and_save_image(image_url, asset_type)
            
            return {
                "success": True,
                "asset_url": asset_url,
                "metadata": {
                    "asset_id": str(uuid.uuid4()),
                    "asset_type": asset_type,
                    "parameters": parameters,
                    "created_at": datetime.utcnow().isoformat() + "Z",
                    "dimensions": {
                        "width": result.get("result", {}).get("width", 1024),
                        "height": result.get("result", {}).get("height", 1024)
                    },
                    "format": "png",
                    "seed": result.get("result", {}).get("seed"),
                    "prompt": result.get("result", {}).get("prompt"),
                    "refined_prompt": result.get("result", {}).get("refined_prompt"),
                    "bria_request_id": result.get("request_id"),
                    "bria_metadata": {
                        "status": result.get("status"),
                        "created_at": result.get("created_at"),
                        "updated_at": result.get("updated_at")
                    }
                }
            }
        
        # Fallback: check for base64 image data (legacy format)
        elif "image" in result:
            image_data = result["image"]
            asset_url = await self._save_generated_image(image_data, asset_type)
            
            return {
                "success": True,
                "asset_url": asset_url,
                "metadata": {
                    "asset_id": str(uuid.uuid4()),
                    "asset_type": asset_type,
                    "parameters": parameters,
                    "created_at": datetime.utcnow().isoformat() + "Z",
                    "file_size": len(base64.b64decode(image_data)) if isinstance(image_data, str) else 0,
                    "dimensions": {
                        "width": result.get("width", 1024),
                        "height": result.get("height", 1024)
                    },
                    "format": "png",
                    "seed": result.get("seed")
                }
            }
        else:
            raise GenerationError("No image data or URL in API response")
    
    async def _download_and_save_image(self, image_url: str, asset_type: str) -> str:
        """Download image from URL and save locally."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(image_url)
                
                if response.status_code != 200:
                    raise GenerationError(f"Failed to download image: {response.status_code}")
                
                image_bytes = response.content
                
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
                
                logger.info("Image downloaded and saved", 
                           filename=filename, 
                           size=len(image_bytes))
                
                # Return URL for serving
                return f"/storage/{filename}"
                
        except Exception as e:
            logger.error("Failed to download and save image", error=str(e))
            raise GenerationError(f"Failed to download image: {str(e)}")

    async def _save_generated_image(self, image_data: str, asset_type: str) -> str:
        """Save base64 encoded image and return its URL."""
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            
            # Generate filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"{asset_type}_{timestamp}_{uuid.uuid4().hex[:8]}.png"
            
            # Save to storage (local for now)
            import os
            storage_path = self.settings.STORAGE_PATH
            os.makedirs(storage_path, exist_ok=True)
            
            file_path = os.path.join(storage_path, filename)
            
            with open(file_path, "wb") as f:
                f.write(image_bytes)
            
            # Return URL (adjust based on your serving setup)
            return f"/storage/{filename}"
            
        except Exception as e:
            logger.error("Failed to save generated image", error=str(e))
            raise GenerationError(f"Failed to save image: {str(e)}")
    
    async def _mock_generation(
        self, 
        prompt: str, 
        asset_type: str, 
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback mock generation when API key is not available."""
        logger.info("Using mock generation", asset_type=asset_type)
        
        # Simulate API delay
        await asyncio.sleep(2)
        
        # Generate mock image URL
        mock_url = self._generate_mock_image_url(asset_type, parameters)
        
        return {
            "success": True,
            "asset_url": mock_url,
            "metadata": {
                "asset_id": str(uuid.uuid4()),
                "asset_type": asset_type,
                "parameters": parameters,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "file_size": 1024000,
                "dimensions": {"width": 1024, "height": 1024},
                "format": "png",
                "generation_time_ms": 2000,
                "is_mock": True
            }
        }
    
    def _generate_mock_image_url(self, asset_type: str, parameters: Dict) -> str:
        """Generate a mock image URL for development."""
        base_url = "https://picsum.photos"
        
        if asset_type == "npc_portrait":
            return f"{base_url}/512/512?random={hash(str(parameters)) % 1000}"
        elif asset_type == "weapon_item":
            return f"{base_url}/512/512?random={hash(str(parameters)) % 1000}&grayscale"
        elif asset_type == "environment_concept":
            return f"{base_url}/1024/768?random={hash(str(parameters)) % 1000}"
        else:
            return f"{base_url}/512/512?random={hash(str(parameters)) % 1000}"
    
    def build_prompt_from_parameters(self, asset_type: str, parameters: Dict[str, Any]) -> str:
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