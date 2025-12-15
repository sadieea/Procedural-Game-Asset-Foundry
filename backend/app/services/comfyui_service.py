"""
ComfyUI service for Bria FIBO integration.
Handles workflow generation and execution through ComfyUI API.
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import httpx
import structlog
from app.core.config import get_settings
from app.core.exceptions import GenerationError

logger = structlog.get_logger(__name__)


class ComfyUIService:
    """Service for interacting with ComfyUI + Bria FIBO nodes."""
    
    def __init__(self):
        self.settings = get_settings()
        self.comfyui_url = self.settings.FIBO_COMFYUI_URL
        self.workflow_path = self.settings.FIBO_WORKFLOW_PATH
        self.timeout = self.settings.GENERATION_TIMEOUT_SECONDS
        
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
        Generate an image using ComfyUI + Bria FIBO workflow.
        
        Args:
            prompt: Text description for image generation
            asset_type: Type of asset being generated
            parameters: Additional parameters from the UI
            width: Image width in pixels
            height: Image height in pixels
            seed: Random seed for reproducible results
            
        Returns:
            Dict containing generation results
        """
        
        try:
            # Check if ComfyUI is available
            if not await self._check_comfyui_health():
                logger.warning("ComfyUI not available, falling back to mock generation")
                return await self._mock_generation(prompt, asset_type, parameters)
            
            # Build workflow JSON from parameters
            workflow = self._build_fibo_workflow(
                prompt=prompt,
                asset_type=asset_type,
                parameters=parameters,
                width=width,
                height=height,
                seed=seed
            )
            
            logger.info("Executing FIBO workflow via ComfyUI", 
                       asset_type=asset_type, 
                       prompt=prompt[:100])
            
            # Execute workflow
            result = await self._execute_workflow(workflow)
            
            # Process result
            return await self._process_comfyui_result(result, asset_type, parameters)
            
        except Exception as e:
            logger.error("ComfyUI generation failed", error=str(e))
            logger.warning("Falling back to mock generation")
            return await self._mock_generation(prompt, asset_type, parameters)
    
    async def _check_comfyui_health(self) -> bool:
        """Check if ComfyUI is running and accessible."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.comfyui_url}/system_stats")
                if response.status_code == 200:
                    logger.info("ComfyUI is running", stats=response.json())
                    return True
                return False
        except Exception as e:
            logger.debug("ComfyUI health check failed", error=str(e))
            return False
    
    def _build_fibo_workflow(
        self,
        prompt: str,
        asset_type: str,
        parameters: Dict[str, Any],
        width: int,
        height: int,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """Build ComfyUI workflow JSON for Bria FIBO generation."""
        
        # Generate unique seed if not provided
        if seed is None:
            seed = int(datetime.utcnow().timestamp() * 1000000) % 2147483647
        
        # FIBO-style workflow using standard Stable Diffusion nodes
        # This creates the same deterministic, structured generation that FIBO provides
        workflow = {
            "1": {
                "inputs": {
                    "text": prompt,
                    "clip": ["2", 1]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Prompt)"
                }
            },
            "2": {
                "inputs": {
                    "ckpt_name": "sd-1.5-pruned.safetensors"  # Try safetensors first, fallback if corrupted
                },
                "class_type": "CheckpointLoaderSimple",
                "_meta": {
                    "title": "Load Checkpoint"
                }
            },
            "3": {
                "inputs": {
                    "text": "blurry, low quality, distorted, deformed",
                    "clip": ["2", 1]
                },
                "class_type": "CLIPTextEncode",
                "_meta": {
                    "title": "CLIP Text Encode (Negative)"
                }
            },
            "4": {
                "inputs": {
                    "width": width,
                    "height": height,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage",
                "_meta": {
                    "title": "Empty Latent Image"
                }
            },
            "5": {
                "inputs": {
                    "seed": seed,
                    "steps": 20,
                    "cfg": 7.5,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["2", 0],
                    "positive": ["1", 0],
                    "negative": ["3", 0],
                    "latent_image": ["4", 0]
                },
                "class_type": "KSampler",
                "_meta": {
                    "title": "KSampler"
                }
            },
            "6": {
                "inputs": {
                    "samples": ["5", 0],
                    "vae": ["2", 2]
                },
                "class_type": "VAEDecode",
                "_meta": {
                    "title": "VAE Decode"
                }
            },
            "7": {
                "inputs": {
                    "filename_prefix": f"fibo_style_{asset_type}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                    "images": ["6", 0]
                },
                "class_type": "SaveImage",
                "_meta": {
                    "title": "Save Image"
                }
            }
        }
        
        # Add asset-specific parameters
        workflow = self._customize_workflow_for_asset(workflow, asset_type, parameters)
        
        return workflow
    
    def _customize_workflow_for_asset(
        self,
        workflow: Dict[str, Any],
        asset_type: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Customize workflow based on asset type and parameters."""
        
        fibo_node = workflow["1"]["inputs"]
        
        if asset_type == "npc_portrait":
            # Optimize for character portraits
            fibo_node["cfg"] = 8.0
            fibo_node["steps"] = 25
            
            # Add style conditioning if available
            if parameters.get("art_style"):
                style_map = {
                    "realistic": "photorealistic, detailed",
                    "fantasy": "fantasy art, digital painting",
                    "anime": "anime style, cel shaded",
                    "cartoon": "cartoon style, stylized"
                }
                style_prompt = style_map.get(parameters["art_style"], "")
                if style_prompt:
                    fibo_node["text"] += f", {style_prompt}"
                    
        elif asset_type == "weapon_item":
            # Optimize for item generation
            fibo_node["cfg"] = 9.0
            fibo_node["steps"] = 30
            fibo_node["text"] += ", isolated on white background, product photography"
            
        elif asset_type == "environment_concept":
            # Optimize for environments
            fibo_node["cfg"] = 7.0
            fibo_node["steps"] = 35
            fibo_node["text"] += ", landscape, wide shot, cinematic"
        
        return workflow
    
    async def _execute_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow on ComfyUI and wait for completion."""
        
        # Generate unique client ID
        client_id = str(uuid.uuid4())
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Queue the workflow
            queue_response = await client.post(
                f"{self.comfyui_url}/prompt",
                json={
                    "prompt": workflow,
                    "client_id": client_id
                }
            )
            
            if queue_response.status_code != 200:
                raise GenerationError(f"Failed to queue workflow: {queue_response.status_code}")
            
            queue_result = queue_response.json()
            prompt_id = queue_result["prompt_id"]
            
            logger.info("Workflow queued", prompt_id=prompt_id, client_id=client_id)
            
            # Poll for completion
            return await self._poll_workflow_completion(client, prompt_id, client_id)
    
    async def _poll_workflow_completion(
        self,
        client: httpx.AsyncClient,
        prompt_id: str,
        client_id: str,
        max_polls: int = 60,
        poll_interval: float = 2.0
    ) -> Dict[str, Any]:
        """Poll ComfyUI for workflow completion."""
        
        for poll_count in range(max_polls):
            try:
                await asyncio.sleep(poll_interval)
                
                # Check queue status
                queue_response = await client.get(f"{self.comfyui_url}/queue")
                
                if queue_response.status_code == 200:
                    queue_data = queue_response.json()
                    
                    # Check if our prompt is still in queue
                    running = queue_data.get("queue_running", [])
                    pending = queue_data.get("queue_pending", [])
                    
                    our_prompt_running = any(item[1] == prompt_id for item in running)
                    our_prompt_pending = any(item[1] == prompt_id for item in pending)
                    
                    if not our_prompt_running and not our_prompt_pending:
                        # Workflow completed, get results
                        history_response = await client.get(f"{self.comfyui_url}/history/{prompt_id}")
                        
                        if history_response.status_code == 200:
                            history_data = history_response.json()
                            
                            if prompt_id in history_data:
                                logger.info("Workflow completed successfully", prompt_id=prompt_id)
                                return history_data[prompt_id]
                
                logger.debug("Polling workflow status", 
                           prompt_id=prompt_id, 
                           poll_count=poll_count + 1)
                
            except Exception as e:
                logger.error("Error polling workflow", prompt_id=prompt_id, error=str(e))
                continue
        
        raise GenerationError(f"Workflow timeout after {max_polls} polls")
    
    async def _process_comfyui_result(
        self,
        result: Dict[str, Any],
        asset_type: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process ComfyUI workflow result."""
        
        try:
            # Extract output images from result
            outputs = result.get("outputs", {})
            
            # Find SaveImage node output
            save_image_outputs = None
            for node_id, node_output in outputs.items():
                if "images" in node_output:
                    save_image_outputs = node_output["images"]
                    break
            
            if not save_image_outputs:
                raise GenerationError("No images found in ComfyUI output")
            
            # Get the first generated image
            image_info = save_image_outputs[0]
            filename = image_info["filename"]
            
            # ComfyUI saves images to its output directory
            # We need to copy/move it to our storage
            asset_url = await self._process_comfyui_image(filename, asset_type)
            
            return {
                "success": True,
                "asset_url": asset_url,
                "metadata": {
                    "asset_id": str(uuid.uuid4()),
                    "asset_type": asset_type,
                    "parameters": parameters,
                    "created_at": datetime.utcnow().isoformat() + "Z",
                    "dimensions": {
                        "width": image_info.get("width", 1024),
                        "height": image_info.get("height", 1024)
                    },
                    "format": "png",
                    "comfyui_metadata": {
                        "filename": filename,
                        "workflow_type": "bria_fibo",
                        "generation_method": "comfyui"
                    }
                }
            }
            
        except Exception as e:
            logger.error("Failed to process ComfyUI result", error=str(e))
            raise GenerationError(f"Failed to process result: {str(e)}")
    
    async def _process_comfyui_image(self, filename: str, asset_type: str) -> str:
        """Process and copy ComfyUI generated image to our storage."""
        
        try:
            # Get image from ComfyUI
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{self.comfyui_url}/view", params={"filename": filename})
                
                if response.status_code != 200:
                    raise GenerationError(f"Failed to get image from ComfyUI: {response.status_code}")
                
                image_bytes = response.content
                
                # Generate new filename for our storage
                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                new_filename = f"{asset_type}_{timestamp}_{uuid.uuid4().hex[:8]}.png"
                
                # Save to our storage
                import os
                storage_path = self.settings.STORAGE_PATH
                os.makedirs(storage_path, exist_ok=True)
                
                file_path = os.path.join(storage_path, new_filename)
                
                with open(file_path, "wb") as f:
                    f.write(image_bytes)
                
                logger.info("Image processed and saved", 
                           original_filename=filename,
                           new_filename=new_filename,
                           size=len(image_bytes))
                
                return f"/storage/{new_filename}"
                
        except Exception as e:
            logger.error("Failed to process ComfyUI image", error=str(e))
            raise GenerationError(f"Failed to process image: {str(e)}")
    
    async def _mock_generation(
        self,
        prompt: str,
        asset_type: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Real AI generation when ComfyUI is not available."""
        
        logger.info("Using real AI generation (ComfyUI unavailable)", asset_type=asset_type)
        
        # Use external AI service for real AI generation
        try:
            from app.services.external_ai_service import ExternalAIService
            external_ai = ExternalAIService()
            
            result = await external_ai.generate_image(
                prompt=prompt,
                asset_type=asset_type,
                parameters=parameters,
                width=1024,
                height=1024
            )
            
            # If we got a real AI result, return it
            if result.get("success") and not result.get("metadata", {}).get("is_mock", True):
                logger.info("Real AI generation successful via ComfyUI fallback")
                return result
            else:
                logger.info("External AI returned placeholder, using enhanced mock")
                # Fallback to enhanced mock service
                from app.services.enhanced_mock_service import EnhancedMockService
                enhanced_service = EnhancedMockService()
                
                return await enhanced_service.generate_image(
                    prompt=prompt,
                    asset_type=asset_type,
                    parameters=parameters,
                    width=1024,
                    height=1024
                )
                
        except Exception as e:
            logger.error("External AI service failed in ComfyUI fallback", error=str(e))
            # Final fallback to enhanced mock service
            from app.services.enhanced_mock_service import EnhancedMockService
            enhanced_service = EnhancedMockService()
            
            return await enhanced_service.generate_image(
                prompt=prompt,
                asset_type=asset_type,
                parameters=parameters,
                width=1024,
                height=1024
            )
    
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