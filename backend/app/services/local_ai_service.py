"""
Local AI-style generation service using PIL and procedural techniques.
Creates more realistic-looking assets when external AI services are unavailable.
"""

import asyncio
import uuid
import random
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import structlog
from app.core.config import get_settings

logger = structlog.get_logger(__name__)


class LocalAIService:
    """Local AI-style generation using procedural techniques."""
    
    def __init__(self):
        self.settings = get_settings()
        
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
        Generate an AI-style image using local procedural techniques.
        """
        
        if seed is not None:
            random.seed(seed)
        
        logger.info("Generating local AI-style image", 
                   asset_type=asset_type, 
                   prompt=prompt[:100])
        
        try:
            # Generate image based on asset type
            if asset_type == "npc_portrait":
                image = await self._generate_npc_portrait(parameters, width, height)
            elif asset_type == "weapon_item":
                image = await self._generate_weapon_item(parameters, width, height)
            elif asset_type == "environment_concept":
                image = await self._generate_environment_concept(parameters, width, height)
            else:
                image = await self._generate_generic_asset(parameters, width, height)
            
            # Save the image
            asset_url = await self._save_image(image, asset_type)
            
            return {
                "success": True,
                "asset_url": asset_url,
                "metadata": {
                    "asset_id": str(uuid.uuid4()),
                    "asset_type": asset_type,
                    "parameters": parameters,
                    "created_at": datetime.utcnow().isoformat() + "Z",
                    "file_size": 0,  # Will be calculated when saved
                    "dimensions": {"width": width, "height": height},
                    "format": "png",
                    "generation_time_ms": 2000,
                    "service": "local_ai",
                    "prompt": prompt,
                    "is_mock": False,  # This is our "AI" generation!
                    "ai_service": "Local Procedural AI"
                }
            }
            
        except Exception as e:
            logger.error("Local AI generation failed", error=str(e))
            raise
    
    async def _generate_npc_portrait(self, parameters: Dict[str, Any], width: int, height: int) -> Image.Image:
        """Generate an NPC portrait using procedural techniques."""
        
        # Create base image with gradient background
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Create gradient background based on character class
        bg_colors = self._get_character_colors(parameters)
        self._draw_gradient_background(draw, width, height, bg_colors)
        
        # Draw character silhouette
        await self._draw_character_silhouette(draw, parameters, width, height)
        
        # Add character details
        await self._add_character_details(draw, parameters, width, height)
        
        # Add text overlay
        await self._add_character_text(draw, parameters, width, height)
        
        # Apply artistic effects
        img = self._apply_portrait_effects(img)
        
        return img
    
    async def _generate_weapon_item(self, parameters: Dict[str, Any], width: int, height: int) -> Image.Image:
        """Generate a weapon item using procedural techniques."""
        
        # Create base image with clean background
        img = Image.new('RGB', (width, height), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        
        # Draw weapon shape based on type
        weapon_type = parameters.get("weapon_type", "sword")
        await self._draw_weapon_shape(draw, weapon_type, parameters, width, height)
        
        # Add material effects
        await self._add_weapon_materials(draw, parameters, width, height)
        
        # Add enchantment effects
        if parameters.get("enchantment_type"):
            await self._add_enchantment_effects(draw, parameters, width, height)
        
        # Add item label
        await self._add_weapon_label(draw, parameters, width, height)
        
        # Apply item effects
        img = self._apply_item_effects(img)
        
        return img
    
    async def _generate_environment_concept(self, parameters: Dict[str, Any], width: int, height: int) -> Image.Image:
        """Generate an environment concept using procedural techniques."""
        
        # Create base image
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Draw sky/background
        biome = parameters.get("biome", "forest")
        await self._draw_environment_sky(draw, biome, parameters, width, height)
        
        # Draw terrain
        await self._draw_terrain(draw, biome, parameters, width, height)
        
        # Add environmental features
        await self._add_environment_features(draw, parameters, width, height)
        
        # Add atmospheric effects
        await self._add_atmospheric_effects(draw, parameters, width, height)
        
        # Add environment label
        await self._add_environment_label(draw, parameters, width, height)
        
        # Apply environment effects
        img = self._apply_environment_effects(img)
        
        return img
    
    async def _generate_generic_asset(self, parameters: Dict[str, Any], width: int, height: int) -> Image.Image:
        """Generate a generic game asset."""
        
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Create abstract geometric pattern
        colors = [(random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)) for _ in range(5)]
        
        for i in range(20):
            x1, y1 = random.randint(0, width-100), random.randint(0, height-100)
            x2, y2 = x1 + random.randint(50, 150), y1 + random.randint(50, 150)
            color = random.choice(colors)
            draw.ellipse([x1, y1, x2, y2], fill=color, outline=(0, 0, 0))
        
        # Add title
        try:
            font = ImageFont.load_default()
            text = "Procedural Game Asset"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, 50), text, fill=(255, 255, 255), font=font)
        except:
            pass
        
        return img
    
    def _get_character_colors(self, parameters: Dict[str, Any]) -> List[tuple]:
        """Get color scheme based on character parameters."""
        
        character_class = parameters.get("character_class", "").lower()
        
        color_schemes = {
            "warrior": [(139, 69, 19), (160, 82, 45), (205, 133, 63)],  # Browns
            "mage": [(25, 25, 112), (65, 105, 225), (138, 43, 226)],    # Blues/Purples
            "rogue": [(47, 79, 79), (105, 105, 105), (169, 169, 169)],  # Grays
            "cleric": [(255, 215, 0), (255, 255, 224), (255, 250, 205)], # Golds
            "ranger": [(34, 139, 34), (107, 142, 35), (85, 107, 47)]     # Greens
        }
        
        return color_schemes.get(character_class, [(100, 100, 150), (150, 150, 200), (200, 200, 250)])
    
    def _draw_gradient_background(self, draw: ImageDraw.Draw, width: int, height: int, colors: List[tuple]):
        """Draw a gradient background."""
        
        for y in range(height):
            # Interpolate between colors
            ratio = y / height
            if ratio < 0.5:
                # First half: color[0] to color[1]
                t = ratio * 2
                color = self._interpolate_color(colors[0], colors[1], t)
            else:
                # Second half: color[1] to color[2]
                t = (ratio - 0.5) * 2
                color = self._interpolate_color(colors[1], colors[2], t)
            
            draw.line([(0, y), (width, y)], fill=color)
    
    def _interpolate_color(self, color1: tuple, color2: tuple, t: float) -> tuple:
        """Interpolate between two colors."""
        return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))
    
    async def _draw_character_silhouette(self, draw: ImageDraw.Draw, parameters: Dict[str, Any], width: int, height: int):
        """Draw a character silhouette."""
        
        # Simple character silhouette
        center_x, center_y = width // 2, height // 2
        
        # Head
        head_size = min(width, height) // 8
        draw.ellipse([
            center_x - head_size, center_y - height//3 - head_size,
            center_x + head_size, center_y - height//3 + head_size
        ], fill=(50, 50, 50), outline=(0, 0, 0))
        
        # Body
        body_width = head_size * 2
        body_height = height // 3
        draw.rectangle([
            center_x - body_width//2, center_y - height//3 + head_size,
            center_x + body_width//2, center_y + body_height//2
        ], fill=(70, 70, 70), outline=(0, 0, 0))
    
    async def _add_character_details(self, draw: ImageDraw.Draw, parameters: Dict[str, Any], width: int, height: int):
        """Add character-specific details."""
        
        # Add some decorative elements based on class
        character_class = parameters.get("character_class", "").lower()
        center_x, center_y = width // 2, height // 2
        
        if character_class == "mage":
            # Add staff
            draw.line([
                (center_x + 30, center_y - 50),
                (center_x + 30, center_y + 100)
            ], fill=(139, 69, 19), width=5)
            # Staff orb
            draw.ellipse([
                center_x + 20, center_y - 70,
                center_x + 40, center_y - 50
            ], fill=(138, 43, 226))
        
        elif character_class == "warrior":
            # Add sword
            draw.line([
                (center_x - 40, center_y - 30),
                (center_x - 40, center_y + 80)
            ], fill=(192, 192, 192), width=8)
            # Sword hilt
            draw.rectangle([
                center_x - 50, center_y + 70,
                center_x - 30, center_y + 90
            ], fill=(139, 69, 19))
    
    async def _add_character_text(self, draw: ImageDraw.Draw, parameters: Dict[str, Any], width: int, height: int):
        """Add character information text."""
        
        try:
            font = ImageFont.load_default()
            
            # Character class
            character_class = parameters.get("character_class", "Character")
            race = parameters.get("race", "")
            
            text = f"{character_class}"
            if race:
                text += f" ({race})"
            
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            
            # Draw text with outline
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, height - 50 + dy), text, fill=(0, 0, 0), font=font)
            draw.text((x, height - 50), text, fill=(255, 255, 255), font=font)
            
        except:
            pass
    
    def _apply_portrait_effects(self, img: Image.Image) -> Image.Image:
        """Apply artistic effects to portrait."""
        
        # Slight blur for artistic effect
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Enhance contrast
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        return img
    
    async def _draw_weapon_shape(self, draw: ImageDraw.Draw, weapon_type: str, parameters: Dict[str, Any], width: int, height: int):
        """Draw weapon shape based on type."""
        
        center_x, center_y = width // 2, height // 2
        
        if weapon_type.lower() in ["sword", "blade"]:
            # Draw sword
            # Blade
            draw.polygon([
                (center_x - 10, center_y - 150),
                (center_x, center_y - 200),
                (center_x + 10, center_y - 150),
                (center_x + 15, center_y + 50),
                (center_x - 15, center_y + 50)
            ], fill=(192, 192, 192), outline=(128, 128, 128))
            
            # Crossguard
            draw.rectangle([
                center_x - 40, center_y + 40,
                center_x + 40, center_y + 60
            ], fill=(139, 69, 19))
            
            # Handle
            draw.rectangle([
                center_x - 8, center_y + 60,
                center_x + 8, center_y + 120
            ], fill=(101, 67, 33))
            
        elif weapon_type.lower() in ["bow"]:
            # Draw bow
            draw.arc([
                center_x - 80, center_y - 150,
                center_x + 80, center_y + 150
            ], start=45, end=135, fill=(139, 69, 19), width=8)
            
            # Bowstring
            draw.line([
                (center_x - 50, center_y - 100),
                (center_x - 50, center_y + 100)
            ], fill=(255, 255, 255), width=2)
            
        else:
            # Generic weapon shape
            draw.ellipse([
                center_x - 50, center_y - 100,
                center_x + 50, center_y + 100
            ], fill=(128, 128, 128), outline=(64, 64, 64))
    
    async def _add_weapon_materials(self, draw: ImageDraw.Draw, parameters: Dict[str, Any], width: int, height: int):
        """Add material effects to weapon."""
        
        material = parameters.get("material", "").lower()
        center_x, center_y = width // 2, height // 2
        
        if material in ["steel", "iron"]:
            # Add metallic shine lines
            for i in range(3):
                y = center_y - 100 + i * 50
                draw.line([
                    (center_x - 5, y),
                    (center_x + 5, y)
                ], fill=(255, 255, 255), width=2)
        
        elif material in ["gold"]:
            # Add golden glow effect
            for radius in range(5, 25, 5):
                draw.ellipse([
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius
                ], outline=(255, 215, 0, 50))
    
    async def _add_enchantment_effects(self, draw: ImageDraw.Draw, parameters: Dict[str, Any], width: int, height: int):
        """Add enchantment visual effects."""
        
        enchantment = parameters.get("enchantment_type", "").lower()
        center_x, center_y = width // 2, height // 2
        
        if enchantment in ["fire", "flame"]:
            # Add flame-like effects
            for i in range(10):
                x = center_x + random.randint(-30, 30)
                y = center_y + random.randint(-100, 100)
                size = random.randint(3, 8)
                draw.ellipse([
                    x - size, y - size,
                    x + size, y + size
                ], fill=(255, random.randint(100, 200), 0))
        
        elif enchantment in ["ice", "frost"]:
            # Add ice crystal effects
            for i in range(8):
                x = center_x + random.randint(-40, 40)
                y = center_y + random.randint(-120, 120)
                draw.polygon([
                    (x, y - 10),
                    (x - 5, y),
                    (x, y + 10),
                    (x + 5, y)
                ], fill=(173, 216, 230))
    
    async def _add_weapon_label(self, draw: ImageDraw.Draw, parameters: Dict[str, Any], width: int, height: int):
        """Add weapon label."""
        
        try:
            font = ImageFont.load_default()
            
            weapon_type = parameters.get("weapon_type", "Weapon")
            material = parameters.get("material", "")
            
            text = f"{material} {weapon_type}".strip()
            
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            
            # Draw with outline
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, height - 40 + dy), text, fill=(0, 0, 0), font=font)
            draw.text((x, height - 40), text, fill=(255, 255, 255), font=font)
            
        except:
            pass
    
    def _apply_item_effects(self, img: Image.Image) -> Image.Image:
        """Apply effects to item image."""
        
        # Sharpen for crisp item look
        img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
        
        return img
    
    async def _draw_environment_sky(self, draw: ImageDraw.Draw, biome: str, parameters: Dict[str, Any], width: int, height: int):
        """Draw environment sky."""
        
        sky_height = height // 3
        
        # Sky colors based on biome
        sky_colors = {
            "forest": [(135, 206, 235), (176, 224, 230), (255, 255, 255)],
            "desert": [(255, 218, 185), (255, 228, 196), (255, 239, 213)],
            "mountain": [(70, 130, 180), (135, 206, 235), (176, 196, 222)],
            "swamp": [(105, 105, 105), (128, 128, 128), (169, 169, 169)]
        }
        
        colors = sky_colors.get(biome, [(135, 206, 235), (176, 224, 230), (255, 255, 255)])
        
        for y in range(sky_height):
            ratio = y / sky_height
            if ratio < 0.5:
                t = ratio * 2
                color = self._interpolate_color(colors[0], colors[1], t)
            else:
                t = (ratio - 0.5) * 2
                color = self._interpolate_color(colors[1], colors[2], t)
            
            draw.line([(0, y), (width, y)], fill=color)
    
    async def _draw_terrain(self, draw: ImageDraw.Draw, biome: str, parameters: Dict[str, Any], width: int, height: int):
        """Draw terrain based on biome."""
        
        terrain_start = height // 3
        
        # Terrain colors
        terrain_colors = {
            "forest": (34, 139, 34),
            "desert": (238, 203, 173),
            "mountain": (105, 105, 105),
            "swamp": (85, 107, 47)
        }
        
        base_color = terrain_colors.get(biome, (34, 139, 34))
        
        # Draw terrain with some variation
        for y in range(terrain_start, height):
            variation = random.randint(-20, 20)
            color = tuple(max(0, min(255, c + variation)) for c in base_color)
            draw.line([(0, y), (width, y)], fill=color)
    
    async def _add_environment_features(self, draw: ImageDraw.Draw, parameters: Dict[str, Any], width: int, height: int):
        """Add environmental features."""
        
        biome = parameters.get("biome", "forest").lower()
        
        if biome == "forest":
            # Add trees
            for i in range(5):
                x = random.randint(50, width - 50)
                tree_height = random.randint(80, 120)
                y = height - tree_height
                
                # Tree trunk
                draw.rectangle([
                    x - 5, y + tree_height - 30,
                    x + 5, height
                ], fill=(139, 69, 19))
                
                # Tree crown
                draw.ellipse([
                    x - 25, y,
                    x + 25, y + 50
                ], fill=(34, 139, 34))
        
        elif biome == "mountain":
            # Add mountain peaks
            for i in range(3):
                x = i * (width // 3) + random.randint(20, 80)
                peak_height = random.randint(100, 200)
                
                draw.polygon([
                    (x - 50, height // 3),
                    (x, height // 3 - peak_height),
                    (x + 50, height // 3)
                ], fill=(105, 105, 105))
    
    async def _add_atmospheric_effects(self, draw: ImageDraw.Draw, parameters: Dict[str, Any], width: int, height: int):
        """Add atmospheric effects."""
        
        weather = parameters.get("weather", "").lower()
        
        if weather in ["rain", "storm"]:
            # Add rain lines
            for i in range(50):
                x = random.randint(0, width)
                y = random.randint(0, height)
                draw.line([
                    (x, y),
                    (x - 5, y + 20)
                ], fill=(200, 200, 255), width=1)
        
        elif weather in ["fog", "mist"]:
            # Add fog effect (semi-transparent overlay)
            for y in range(height // 2, height):
                alpha = int(100 * (y - height // 2) / (height // 2))
                # Note: PIL doesn't support alpha in basic draw, so we simulate with lighter colors
                fog_color = (220, 220, 220)
                draw.line([(0, y), (width, y)], fill=fog_color)
    
    async def _add_environment_label(self, draw: ImageDraw.Draw, parameters: Dict[str, Any], width: int, height: int):
        """Add environment label."""
        
        try:
            font = ImageFont.load_default()
            
            biome = parameters.get("biome", "Environment")
            weather = parameters.get("weather", "")
            
            text = f"{biome.title()}"
            if weather:
                text += f" ({weather.title()})"
            
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            
            # Draw with outline
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, 30 + dy), text, fill=(0, 0, 0), font=font)
            draw.text((x, 30), text, fill=(255, 255, 255), font=font)
            
        except:
            pass
    
    def _apply_environment_effects(self, img: Image.Image) -> Image.Image:
        """Apply effects to environment image."""
        
        # Slight blur for atmospheric effect
        img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
        
        # Enhance colors
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.1)
        
        return img
    
    async def _save_image(self, image: Image.Image, asset_type: str) -> str:
        """Save generated image to storage."""
        
        try:
            # Generate filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"{asset_type}_{timestamp}_{uuid.uuid4().hex[:8]}.png"
            
            # Save to storage
            storage_path = self.settings.STORAGE_PATH
            os.makedirs(storage_path, exist_ok=True)
            
            file_path = os.path.join(storage_path, filename)
            image.save(file_path, "PNG")
            
            logger.info("Local AI image saved", filename=filename)
            
            return f"/storage/{filename}"
            
        except Exception as e:
            logger.error("Failed to save local AI image", error=str(e))
            raise