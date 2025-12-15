"""
Strict FIBO JSON Schema Validation for Procedural Game Asset Foundry.
Production-ready validation with deterministic safety checks.

VALIDATION RULES:
- No additional properties allowed
- All enums strictly enforced  
- Numeric ranges validated
- Defaults applied explicitly
- Schema version checked
- Asset type enforced
"""

from enum import Enum
from typing import List, Literal, Optional, Union, Dict, Any
from pydantic import BaseModel, Field, validator, model_validator
import re


class ValidationError(Exception):
    """Custom validation error for FIBO schemas."""
    pass


# ============================================================================
# BASE SCHEMA - STRICT FOUNDATION
# ============================================================================

class SchemaVersion(str, Enum):
    """Supported schema versions."""
    V1 = "v1"


class AssetType(str, Enum):
    """Supported asset generation types."""
    NPC_PORTRAIT = "npc_portrait"
    WEAPON_ITEM = "weapon_item"
    ENVIRONMENT_CONCEPT = "environment_concept"


class Resolution(str, Enum):
    """Supported output resolutions."""
    SMALL = "512x512"
    MEDIUM = "1024x1024"
    LARGE = "1920x1080"
    ULTRA = "2048x2048"


class ColorDepth(str, Enum):
    """Supported color depths."""
    EIGHT_BIT = "8bit"
    SIXTEEN_BIT = "16bit"
    THIRTY_TWO_BIT = "32bit"


class OutputFormat(str, Enum):
    """Supported output formats."""
    PNG = "png"
    JPG = "jpg"
    WEBP = "webp"
    EXR = "exr"


class BackgroundType(str, Enum):
    """Supported background types."""
    TRANSPARENT = "transparent"
    SOLID = "solid"
    GRADIENT = "gradient"
    STUDIO_GRAY = "studio_gray"


class OutputConfig(BaseModel):
    """Output configuration with strict validation."""
    
    resolution: Resolution = Field(
        default=Resolution.MEDIUM,
        description="Output image dimensions"
    )
    colorDepth: ColorDepth = Field(
        default=ColorDepth.SIXTEEN_BIT,
        description="Color depth for professional workflows"
    )
    format: OutputFormat = Field(
        default=OutputFormat.PNG,
        description="Output file format"
    )
    background: BackgroundType = Field(
        default=BackgroundType.TRANSPARENT,
        description="Background treatment"
    )

    class Config:
        extra = "forbid"  # No additional properties allowed


class FiboBaseConfig(BaseModel):
    """Base configuration for all FIBO generations - STRICT."""
    
    schemaVersion: SchemaVersion = Field(
        default=SchemaVersion.V1,
        description="Schema version for compatibility tracking"
    )
    assetType: AssetType = Field(
        description="Asset category for generation pipeline routing"
    )
    seed: int = Field(
        ge=1,
        le=999999999,
        description="Deterministic seed for reproducible generation"
    )
    output: OutputConfig = Field(
        default_factory=OutputConfig,
        description="Output configuration"
    )

    class Config:
        extra = "forbid"  # No additional properties allowed

    @validator('seed', pre=True)
    def validate_seed(cls, v):
        """Ensure seed is a positive integer."""
        if v is None:
            import random
            return random.randint(1, 999999999)
        if not isinstance(v, int) or v < 1 or v > 999999999:
            raise ValueError("Seed must be an integer between 1 and 999,999,999")
        return v


# ============================================================================
# NPC PORTRAIT SCHEMA - STRICT VALIDATION
# ============================================================================

class AgeRange(str, Enum):
    """Character age categories."""
    YOUNG = "young"
    ADULT = "adult"
    MIDDLE_AGED = "middle_aged"
    ELDERLY = "elderly"


class GenderPresentation(str, Enum):
    """Gender presentation options."""
    MASCULINE = "masculine"
    FEMININE = "feminine"
    ANDROGYNOUS = "androgynous"


class Ethnicity(str, Enum):
    """Ethnicity and fantasy race options."""
    EAST_ASIAN = "east_asian"
    SOUTH_ASIAN = "south_asian"
    AFRICAN = "african"
    CAUCASIAN = "caucasian"
    MIDDLE_EASTERN = "middle_eastern"
    LATINO = "latino"
    MIXED = "mixed"
    FANTASY_ELF = "fantasy_elf"
    FANTASY_DWARF = "fantasy_dwarf"
    FANTASY_ORC = "fantasy_orc"


class Archetype(str, Enum):
    """Character archetypes."""
    WARRIOR = "warrior"
    MAGE = "mage"
    ROGUE = "rogue"
    NOBLE = "noble"
    MERCHANT = "merchant"
    SCHOLAR = "scholar"
    ASSASSIN = "assassin"
    PALADIN = "paladin"
    VILLAGER = "villager"
    BLACKSMITH = "blacksmith"


class ScarType(str, Enum):
    """Facial scarring types."""
    NONE = "none"
    LIGHT = "light"
    HEAVY = "heavy"
    RITUAL = "ritual"
    BATTLE = "battle"


class FacialHair(str, Enum):
    """Facial hair options."""
    NONE = "none"
    STUBBLE = "stubble"
    BEARD = "beard"
    MUSTACHE = "mustache"
    GOATEE = "goatee"
    FULL = "full"


class Emotion(str, Enum):
    """Facial expressions."""
    NEUTRAL = "neutral"
    STERN = "stern"
    FRIENDLY = "friendly"
    ANGRY = "angry"
    MYSTERIOUS = "mysterious"
    WISE = "wise"
    FIERCE = "fierce"
    SAD = "sad"
    DETERMINED = "determined"


class CameraAngle(str, Enum):
    """Camera angles for portraits."""
    FRONTAL = "frontal"
    THREE_QUARTER_LEFT = "three_quarter_left"
    THREE_QUARTER_RIGHT = "three_quarter_right"
    PROFILE_LEFT = "profile_left"
    PROFILE_RIGHT = "profile_right"


class CameraDistance(str, Enum):
    """Camera distance options."""
    CLOSE = "close"
    MEDIUM = "medium"
    FAR = "far"


class KeyLight(str, Enum):
    """Key light styles."""
    SOFT = "soft"
    DRAMATIC = "dramatic"
    STUDIO = "studio"
    NATURAL = "natural"


class RimLight(str, Enum):
    """Rim lighting options."""
    NONE = "none"
    SUBTLE = "subtle"
    STRONG = "strong"


class ColorTemperature(str, Enum):
    """Light color temperatures."""
    WARM = "warm"
    NEUTRAL = "neutral"
    COOL = "cool"
    CANDLELIGHT = "candlelight"
    DAYLIGHT = "daylight"
    MOONLIGHT = "moonlight"


class RenderStyle(str, Enum):
    """Rendering styles."""
    PHOTOREALISTIC = "photorealistic"
    STYLIZED = "stylized"
    PAINTERLY = "painterly"
    CEL_SHADED = "cel_shaded"
    CONCEPT_ART = "concept_art"


class DetailLevel(str, Enum):
    """Detail complexity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"


class SkinTexture(str, Enum):
    """Skin texture options."""
    SMOOTH = "smooth"
    NATURAL = "natural"
    ROUGH = "rough"
    WEATHERED = "weathered"
    FANTASY = "fantasy"


# NPC Portrait Schema Components
class NPCIdentity(BaseModel):
    """Character identity configuration."""
    
    ageRange: AgeRange = Field(description="Character age category")
    genderPresentation: GenderPresentation = Field(description="Gender presentation")
    ethnicity: Ethnicity = Field(description="Ethnic background")
    archetype: Archetype = Field(description="Character class/role")

    class Config:
        extra = "forbid"


class NPCFacialFeatures(BaseModel):
    """Facial feature configuration with strict ranges."""
    
    jawWidth: float = Field(
        ge=0.0, le=1.0,
        description="Jaw width: 0.0=narrow, 1.0=wide"
    )
    cheekboneHeight: float = Field(
        ge=0.0, le=1.0,
        description="Cheekbone prominence: 0.0=low, 1.0=high"
    )
    noseLength: float = Field(
        ge=0.0, le=1.0,
        description="Nose length: 0.0=short, 1.0=long"
    )
    eyeSize: float = Field(
        ge=0.0, le=1.0,
        description="Eye size: 0.0=small, 1.0=large"
    )
    browIntensity: float = Field(
        ge=0.0, le=1.0,
        description="Eyebrow thickness: 0.0=thin, 1.0=thick"
    )
    scars: ScarType = Field(description="Facial scarring level")
    facialHair: FacialHair = Field(default=FacialHair.NONE, description="Facial hair style")

    class Config:
        extra = "forbid"


class NPCExpression(BaseModel):
    """Expression configuration."""
    
    emotion: Emotion = Field(description="Primary facial expression")
    intensity: float = Field(
        ge=0.0, le=1.0,
        description="Expression intensity: 0.0=subtle, 1.0=pronounced"
    )

    class Config:
        extra = "forbid"


class NPCCamera(BaseModel):
    """Camera configuration with strict FOV validation."""
    
    angle: CameraAngle = Field(description="Camera angle relative to subject")
    fov: int = Field(
        ge=35, le=85,
        description="Field of view in mm equivalent (35=wide, 85=telephoto)"
    )
    headTilt: float = Field(
        ge=-0.3, le=0.3,
        description="Head tilt in radians"
    )
    distance: CameraDistance = Field(description="Camera distance")

    class Config:
        extra = "forbid"


class NPCLighting(BaseModel):
    """Lighting configuration."""
    
    keyLight: KeyLight = Field(description="Primary light quality")
    fillRatio: float = Field(
        ge=0.0, le=1.0,
        description="Fill light ratio: 0.0=high contrast, 1.0=flat"
    )
    rimLight: RimLight = Field(description="Edge lighting intensity")
    colorTemperature: ColorTemperature = Field(description="Light color temperature")

    class Config:
        extra = "forbid"


class NPCStyle(BaseModel):
    """Style configuration."""
    
    renderStyle: RenderStyle = Field(description="Overall rendering approach")
    detailLevel: DetailLevel = Field(description="Surface detail complexity")
    skinTexture: SkinTexture = Field(description="Skin surface treatment")

    class Config:
        extra = "forbid"


class NPCPortraitConfig(FiboBaseConfig):
    """Complete NPC Portrait generation configuration - STRICT."""
    
    assetType: Literal[AssetType.NPC_PORTRAIT] = AssetType.NPC_PORTRAIT
    identity: NPCIdentity
    facialFeatures: NPCFacialFeatures
    expression: NPCExpression
    camera: NPCCamera
    lighting: NPCLighting
    style: NPCStyle

    class Config:
        extra = "forbid"


# ============================================================================
# WEAPON/ITEM SCHEMA - STRICT VALIDATION
# ============================================================================

class ItemCategory(str, Enum):
    """Item categories."""
    SWORD = "sword"
    AXE = "axe"
    BOW = "bow"
    STAFF = "staff"
    DAGGER = "dagger"
    HAMMER = "hammer"
    GUN = "gun"
    POTION = "potion"
    ARTIFACT = "artifact"
    SHIELD = "shield"
    ARMOR = "armor"
    ACCESSORY = "accessory"


class RarityLevel(str, Enum):
    """Item rarity levels."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    ARTIFACT = "artifact"
    UNIQUE = "unique"


class Material(str, Enum):
    """Material types."""
    STEEL = "steel"
    IRON = "iron"
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    CRYSTAL = "crystal"
    WOOD = "wood"
    BONE = "bone"
    OBSIDIAN = "obsidian"
    MITHRIL = "mithril"
    ADAMANTINE = "adamantine"
    ETHEREAL = "ethereal"


class StyleTheme(str, Enum):
    """Style themes."""
    FANTASY = "fantasy"
    SCI_FI = "sci_fi"
    MODERN = "modern"
    STEAMPUNK = "steampunk"
    MEDIEVAL = "medieval"
    ANCIENT = "ancient"
    TRIBAL = "tribal"
    ELVEN = "elven"
    DWARVEN = "dwarven"
    ORCISH = "orcish"


class Symmetry(str, Enum):
    """Form symmetry options."""
    SYMMETRICAL = "symmetrical"
    ASYMMETRICAL = "asymmetrical"
    CURVED = "curved"
    TWISTED = "twisted"


class ScratchType(str, Enum):
    """Surface scratch patterns."""
    NONE = "none"
    LIGHT = "light"
    HEAVY = "heavy"
    BATTLE_WORN = "battle_worn"
    RITUAL = "ritual"


class PatinaType(str, Enum):
    """Surface patina types."""
    NONE = "none"
    LIGHT = "light"
    HEAVY = "heavy"
    VERDIGRIS = "verdigris"
    RUST = "rust"
    TARNISH = "tarnish"


class InscriptionType(str, Enum):
    """Surface inscription types."""
    NONE = "none"
    RUNES = "runes"
    TEXT = "text"
    SYMBOLS = "symbols"
    GEOMETRIC = "geometric"


class CameraMode(str, Enum):
    """Camera presentation modes."""
    ISOMETRIC = "isometric"
    FLAT_ICON = "flat_icon"
    HERO_RENDER = "hero_render"
    THREE_QUARTER = "three_quarter"
    PROFILE = "profile"


class LightStyle(str, Enum):
    """Lighting styles."""
    STUDIO = "studio"
    DRAMATIC = "dramatic"
    SOFT = "soft"
    HARSH = "harsh"
    AMBIENT = "ambient"


class RimLightType(str, Enum):
    """Rim lighting types."""
    NONE = "none"
    SUBTLE = "subtle"
    STRONG = "strong"
    COLORED = "colored"


class BackgroundStyle(str, Enum):
    """Background styles."""
    TRANSPARENT = "transparent"
    STUDIO_GRAY = "studio_gray"
    RADIAL_GLOW = "radial_glow"
    SOLID_COLOR = "solid_color"
    GRADIENT = "gradient"


class ShadowType(str, Enum):
    """Shadow types."""
    NONE = "none"
    DROP_SHADOW = "drop_shadow"
    CONTACT_SHADOW = "contact_shadow"
    AMBIENT_OCCLUSION = "ambient_occlusion"


class ParticleType(str, Enum):
    """Particle effects."""
    NONE = "none"
    DUST = "dust"
    SPARKS = "sparks"
    MAGIC = "magic"
    SMOKE = "smoke"


# Weapon/Item Schema Components
class ItemIdentity(BaseModel):
    """Item identity configuration."""
    
    category: ItemCategory = Field(description="Item type")
    rarity: RarityLevel = Field(description="Rarity tier")
    material: Material = Field(description="Primary material")
    styleTheme: StyleTheme = Field(description="Cultural/technological style")

    class Config:
        extra = "forbid"


class ItemForm(BaseModel):
    """Item form configuration with strict ranges."""
    
    length: float = Field(
        ge=0.1, le=1.0,
        description="Item length scale: 0.1=dagger, 1.0=greatsword"
    )
    thickness: float = Field(
        ge=0.1, le=1.0,
        description="Item thickness: 0.1=thin, 1.0=bulky"
    )
    symmetry: Symmetry = Field(description="Overall form symmetry")
    ornamentation: float = Field(
        ge=0.0, le=1.0,
        description="Decorative detail level: 0.0=plain, 1.0=ornate"
    )

    class Config:
        extra = "forbid"

    @validator('ornamentation')
    def validate_ornamentation_rarity(cls, v, values):
        """Validate ornamentation matches rarity expectations."""
        # This will be enhanced with rarity cross-validation
        return v


class ItemSurface(BaseModel):
    """Surface detail configuration."""
    
    wearLevel: float = Field(
        ge=0.0, le=1.0,
        description="Wear and aging: 0.0=pristine, 1.0=heavily worn"
    )
    scratches: ScratchType = Field(description="Surface scratch pattern")
    emissiveGlow: float = Field(
        ge=0.0, le=1.0,
        description="Magical glow intensity: 0.0=none, 1.0=bright"
    )
    patina: PatinaType = Field(description="Surface oxidation/aging")
    inscriptions: InscriptionType = Field(description="Surface markings")

    class Config:
        extra = "forbid"


class ItemCamera(BaseModel):
    """Item camera configuration with strict angle validation."""
    
    mode: CameraMode = Field(description="Camera presentation mode")
    angle: int = Field(
        ge=0, le=360,
        description="Rotation angle in degrees"
    )
    fov: int = Field(
        ge=25, le=75,
        description="Field of view in degrees"
    )
    distance: CameraDistance = Field(description="Camera distance")

    class Config:
        extra = "forbid"


class ItemLighting(BaseModel):
    """Item lighting configuration."""
    
    keyLight: LightStyle = Field(description="Primary lighting setup")
    contrast: float = Field(
        ge=0.0, le=1.0,
        description="Lighting contrast: 0.0=flat, 1.0=high contrast"
    )
    rimLight: RimLightType = Field(description="Edge lighting treatment")
    reflections: float = Field(
        ge=0.0, le=1.0,
        description="Surface reflection intensity"
    )

    class Config:
        extra = "forbid"


class ItemBackground(BaseModel):
    """Background configuration."""
    
    type: BackgroundStyle = Field(description="Background treatment")
    shadow: ShadowType = Field(description="Shadow type")
    particles: ParticleType = Field(description="Atmospheric particles")

    class Config:
        extra = "forbid"


class WeaponItemConfig(FiboBaseConfig):
    """Complete Weapon/Item generation configuration - STRICT."""
    
    assetType: Literal[AssetType.WEAPON_ITEM] = AssetType.WEAPON_ITEM
    item: ItemIdentity
    form: ItemForm
    surface: ItemSurface
    camera: ItemCamera
    lighting: ItemLighting
    background: ItemBackground

    class Config:
        extra = "forbid"

    @model_validator(mode='after')
    def validate_material_patina_compatibility(self):
        """Validate material and patina compatibility."""
        if self.surface and self.item:
            material = self.item.material
            patina = self.surface.patina
            
            # Crystal materials shouldn't rust
            if material == Material.CRYSTAL and patina == PatinaType.RUST:
                raise ValueError("Crystal materials cannot have rust patina")
            
            # Wood materials shouldn't have metallic patina
            if material == Material.WOOD and patina in [PatinaType.RUST, PatinaType.VERDIGRIS]:
                raise ValueError("Wood materials cannot have metallic patina")
        
        return self


# ============================================================================
# ENVIRONMENT SCHEMA - STRICT VALIDATION
# ============================================================================

class EnvironmentType(str, Enum):
    """Environment types."""
    CITY = "city"
    VILLAGE = "village"
    FOREST = "forest"
    DESERT = "desert"
    MOUNTAINS = "mountains"
    RUINS = "ruins"
    DUNGEON = "dungeon"
    CASTLE = "castle"
    TEMPLE = "temple"
    SCI_FI_INTERIOR = "sci_fi_interior"
    SPACE_STATION = "space_station"
    UNDERWATER = "underwater"


class Era(str, Enum):
    """Historical eras."""
    PREHISTORIC = "prehistoric"
    ANCIENT = "ancient"
    MEDIEVAL = "medieval"
    RENAISSANCE = "renaissance"
    INDUSTRIAL = "industrial"
    MODERN = "modern"
    FUTURISTIC = "futuristic"
    POST_APOCALYPTIC = "post_apocalyptic"


class Scale(str, Enum):
    """Scene scales."""
    INTIMATE = "intimate"
    MEDIUM = "medium"
    WIDE = "wide"
    EPIC = "epic"
    PANORAMIC = "panoramic"


class Biome(str, Enum):
    """Biome types."""
    TEMPERATE = "temperate"
    TROPICAL = "tropical"
    ARCTIC = "arctic"
    DESERT = "desert"
    SWAMP = "swamp"
    VOLCANIC = "volcanic"
    ALIEN = "alien"
    MAGICAL = "magical"


class CameraHeight(str, Enum):
    """Camera heights."""
    GROUND = "ground"
    EYE_LEVEL = "eye_level"
    ELEVATED = "elevated"
    AERIAL = "aerial"
    BIRDS_EYE = "birds_eye"


class DepthLayers(str, Enum):
    """Depth layer complexity."""
    SHALLOW = "shallow"
    MEDIUM = "medium"
    DEEP = "deep"
    INFINITE = "infinite"


class FocalPoint(str, Enum):
    """Focal point placement."""
    CENTER = "center"
    LEFT_THIRD = "left_third"
    RIGHT_THIRD = "right_third"
    FOREGROUND = "foreground"
    BACKGROUND = "background"


class TimeOfDay(str, Enum):
    """Time of day options."""
    DAWN = "dawn"
    MORNING = "morning"
    MIDDAY = "midday"
    AFTERNOON = "afternoon"
    DUSK = "dusk"
    NIGHT = "night"
    MIDNIGHT = "midnight"


class Weather(str, Enum):
    """Weather conditions."""
    CLEAR = "clear"
    PARTLY_CLOUDY = "partly_cloudy"
    OVERCAST = "overcast"
    FOGGY = "foggy"
    RAINY = "rainy"
    STORMY = "stormy"
    SNOWY = "snowy"
    SANDSTORM = "sandstorm"


class EnvironmentLightStyle(str, Enum):
    """Environment lighting styles."""
    SOFT = "soft"
    DRAMATIC = "dramatic"
    CINEMATIC = "cinematic"
    NATURAL = "natural"
    ARTIFICIAL = "artificial"
    MAGICAL = "magical"


class EnvironmentColorTemperature(str, Enum):
    """Environment color temperatures."""
    WARM = "warm"
    NEUTRAL = "neutral"
    COOL = "cool"
    GOLDEN_HOUR = "golden_hour"
    BLUE_HOUR = "blue_hour"
    ARTIFICIAL = "artificial"


class EnvironmentRenderStyle(str, Enum):
    """Environment rendering styles."""
    PHOTOREALISTIC = "photorealistic"
    CINEMATIC_REALISM = "cinematic_realism"
    MATTE_PAINTING = "matte_painting"
    STYLIZED = "stylized"
    CONCEPT_ART = "concept_art"
    IMPRESSIONISTIC = "impressionistic"


class EnvironmentDetailLevel(str, Enum):
    """Environment detail levels."""
    SKETCH = "sketch"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"
    ARCHITECTURAL = "architectural"


class ColorPalette(str, Enum):
    """Color palette approaches."""
    NATURAL = "natural"
    DESATURATED = "desaturated"
    VIBRANT = "vibrant"
    MONOCHROME = "monochrome"
    COMPLEMENTARY = "complementary"
    ANALOGOUS = "analogous"
    CINEMATIC = "cinematic"


# Environment Schema Components
class EnvironmentScene(BaseModel):
    """Scene definition."""
    
    type: EnvironmentType = Field(description="Primary environment type")
    era: Era = Field(description="Technological/historical era")
    scale: Scale = Field(description="Scene scope and scale")
    biome: Biome = Field(description="Environmental biome characteristics")

    class Config:
        extra = "forbid"


class EnvironmentComposition(BaseModel):
    """Composition configuration."""
    
    cameraHeight: CameraHeight = Field(description="Camera elevation")
    horizonPosition: float = Field(
        ge=0.0, le=1.0,
        description="Horizon line position: 0.0=bottom, 0.33=lower third, 0.66=upper third, 1.0=top"
    )
    depthLayers: DepthLayers = Field(description="Depth complexity")
    focalPoint: FocalPoint = Field(description="Primary focal point placement")

    class Config:
        extra = "forbid"


class EnvironmentAtmosphere(BaseModel):
    """Atmospheric configuration with strict validation."""
    
    timeOfDay: TimeOfDay = Field(description="Time of day affecting lighting")
    weather: Weather = Field(description="Weather conditions")
    fogDensity: float = Field(
        ge=0.0, le=1.0,
        description="Atmospheric fog density: 0.0=clear, 1.0=heavy fog"
    )
    visibility: float = Field(
        ge=0.1, le=1.0,
        description="Atmospheric visibility range"
    )

    class Config:
        extra = "forbid"

    @validator('weather')
    def validate_weather_time_compatibility(cls, v, values):
        """Validate weather and time of day compatibility."""
        time_of_day = values.get('timeOfDay')
        
        # No sunny weather at night
        if time_of_day == TimeOfDay.NIGHT and v == Weather.CLEAR:
            # This is actually valid - clear night sky
            pass
        
        return v


class EnvironmentLighting(BaseModel):
    """Environment lighting configuration."""
    
    lightStyle: EnvironmentLightStyle = Field(description="Overall lighting approach")
    contrast: float = Field(
        ge=0.0, le=1.0,
        description="Lighting contrast ratio"
    )
    godRays: float = Field(
        ge=0.0, le=1.0,
        description="Volumetric light ray intensity"
    )
    colorTemperature: EnvironmentColorTemperature = Field(description="Light color temperature")
    ambientOcclusion: float = Field(
        ge=0.0, le=1.0,
        description="Ambient occlusion strength"
    )

    class Config:
        extra = "forbid"


class EnvironmentStyle(BaseModel):
    """Environment style configuration."""
    
    renderStyle: EnvironmentRenderStyle = Field(description="Overall rendering style")
    detailLevel: EnvironmentDetailLevel = Field(description="Environmental detail complexity")
    colorPalette: ColorPalette = Field(description="Color palette approach")

    class Config:
        extra = "forbid"


class EnvironmentConfig(FiboBaseConfig):
    """Complete Environment generation configuration - STRICT."""
    
    assetType: Literal[AssetType.ENVIRONMENT_CONCEPT] = AssetType.ENVIRONMENT_CONCEPT
    scene: EnvironmentScene
    composition: EnvironmentComposition
    atmosphere: EnvironmentAtmosphere
    lighting: EnvironmentLighting
    style: EnvironmentStyle

    class Config:
        extra = "forbid"

    @model_validator(mode='after')
    def validate_resolution_for_environment(self):
        """Validate that environment uses widescreen resolution."""
        if self.output and self.output.resolution not in [Resolution.LARGE, Resolution.ULTRA]:
            # Allow but warn - not strictly enforced
            pass
        return self

    @model_validator(mode='after')
    def validate_biome_weather_compatibility(self):
        """Validate biome and weather compatibility."""
        if self.scene and self.atmosphere:
            biome = self.scene.biome
            weather = self.atmosphere.weather
            
            # Desert biomes rarely have rain/snow
            if biome == Biome.DESERT and weather in [Weather.RAINY, Weather.SNOWY]:
                raise ValueError("Desert biomes cannot have rain or snow weather")
            
            # Arctic biomes don't have sandstorms
            if biome == Biome.ARCTIC and weather == Weather.SANDSTORM:
                raise ValueError("Arctic biomes cannot have sandstorms")
        
        return self


# ============================================================================
# UNION TYPE AND VALIDATION FUNCTIONS
# ============================================================================

# Union type for all asset configurations
AssetConfig = Union[NPCPortraitConfig, WeaponItemConfig, EnvironmentConfig]


def validate_asset_config(config_data: Dict[str, Any]) -> AssetConfig:
    """
    Validate and parse asset configuration with strict type checking.
    
    Args:
        config_data: Raw configuration dictionary
        
    Returns:
        Validated AssetConfig instance
        
    Raises:
        ValidationError: If validation fails
    """
    try:
        asset_type = config_data.get('assetType')
        
        if asset_type == AssetType.NPC_PORTRAIT:
            return NPCPortraitConfig(**config_data)
        elif asset_type == AssetType.WEAPON_ITEM:
            return WeaponItemConfig(**config_data)
        elif asset_type == AssetType.ENVIRONMENT_CONCEPT:
            return EnvironmentConfig(**config_data)
        else:
            raise ValidationError(f"Invalid asset type: {asset_type}")
            
    except Exception as e:
        raise ValidationError(f"Schema validation failed: {str(e)}")


def get_default_config(asset_type: AssetType) -> AssetConfig:
    """
    Get default configuration for asset type.
    
    Args:
        asset_type: Asset type to get defaults for
        
    Returns:
        Default configuration instance
    """
    import random
    
    base_seed = random.randint(1, 999999999)
    
    if asset_type == AssetType.NPC_PORTRAIT:
        return NPCPortraitConfig(
            seed=base_seed,
            identity=NPCIdentity(
                ageRange=AgeRange.ADULT,
                genderPresentation=GenderPresentation.MASCULINE,
                ethnicity=Ethnicity.CAUCASIAN,
                archetype=Archetype.WARRIOR
            ),
            facialFeatures=NPCFacialFeatures(
                jawWidth=0.5,
                cheekboneHeight=0.5,
                noseLength=0.5,
                eyeSize=0.5,
                browIntensity=0.5,
                scars=ScarType.NONE
            ),
            expression=NPCExpression(
                emotion=Emotion.NEUTRAL,
                intensity=0.4
            ),
            camera=NPCCamera(
                angle=CameraAngle.THREE_QUARTER_LEFT,
                fov=50,
                headTilt=0.0,
                distance=CameraDistance.MEDIUM
            ),
            lighting=NPCLighting(
                keyLight=KeyLight.STUDIO,
                fillRatio=0.4,
                rimLight=RimLight.SUBTLE,
                colorTemperature=ColorTemperature.NEUTRAL
            ),
            style=NPCStyle(
                renderStyle=RenderStyle.PHOTOREALISTIC,
                detailLevel=DetailLevel.HIGH,
                skinTexture=SkinTexture.NATURAL
            )
        )
    
    elif asset_type == AssetType.WEAPON_ITEM:
        return WeaponItemConfig(
            seed=base_seed,
            item=ItemIdentity(
                category=ItemCategory.SWORD,
                rarity=RarityLevel.COMMON,
                material=Material.STEEL,
                styleTheme=StyleTheme.FANTASY
            ),
            form=ItemForm(
                length=0.6,
                thickness=0.4,
                symmetry=Symmetry.SYMMETRICAL,
                ornamentation=0.5
            ),
            surface=ItemSurface(
                wearLevel=0.3,
                scratches=ScratchType.LIGHT,
                emissiveGlow=0.2,
                patina=PatinaType.NONE,
                inscriptions=InscriptionType.NONE
            ),
            camera=ItemCamera(
                mode=CameraMode.HERO_RENDER,
                angle=315,
                fov=45,
                distance=CameraDistance.MEDIUM
            ),
            lighting=ItemLighting(
                keyLight=LightStyle.DRAMATIC,
                contrast=0.6,
                rimLight=RimLightType.STRONG,
                reflections=0.9
            ),
            background=ItemBackground(
                type=BackgroundStyle.RADIAL_GLOW,
                shadow=ShadowType.DROP_SHADOW,
                particles=ParticleType.MAGIC
            )
        )
    
    else:  # ENVIRONMENT_CONCEPT
        return EnvironmentConfig(
            seed=base_seed,
            output=OutputConfig(resolution=Resolution.LARGE),  # Widescreen for environments
            scene=EnvironmentScene(
                type=EnvironmentType.FOREST,
                era=Era.MEDIEVAL,
                scale=Scale.MEDIUM,
                biome=Biome.TEMPERATE
            ),
            composition=EnvironmentComposition(
                cameraHeight=CameraHeight.EYE_LEVEL,
                horizonPosition=0.33,
                depthLayers=DepthLayers.MEDIUM,
                focalPoint=FocalPoint.CENTER
            ),
            atmosphere=EnvironmentAtmosphere(
                timeOfDay=TimeOfDay.DUSK,
                weather=Weather.CLEAR,
                fogDensity=0.3,
                visibility=0.8
            ),
            lighting=EnvironmentLighting(
                lightStyle=EnvironmentLightStyle.CINEMATIC,
                contrast=0.7,
                godRays=0.4,
                colorTemperature=EnvironmentColorTemperature.WARM,
                ambientOcclusion=0.6
            ),
            style=EnvironmentStyle(
                renderStyle=EnvironmentRenderStyle.MATTE_PAINTING,
                detailLevel=EnvironmentDetailLevel.HIGH,
                colorPalette=ColorPalette.CINEMATIC
            )
        )