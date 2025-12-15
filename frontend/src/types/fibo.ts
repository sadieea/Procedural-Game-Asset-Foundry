// FIBO JSON Schema Types for Procedural Game Asset Foundry
// Deterministic, production-ready asset generation

export interface FiboBaseConfig {
  schemaVersion: 'v1';
  assetType: 'npc_portrait' | 'weapon_item' | 'environment_concept';
  seed: number;
  output: {
    resolution: '512x512' | '1024x1024' | '1024x768' | '768x1024';
    colorDepth: '8bit' | '16bit';
    format: 'png' | 'jpg' | 'webp';
    background: 'transparent' | 'white' | 'black';
  };
}

// NPC Portrait Generation Schema (matches backend Pydantic schema)
export interface NPCPortraitConfig extends FiboBaseConfig {
  assetType: 'npc_portrait';
  identity: {
    ageRange: 'young' | 'adult' | 'middle_aged' | 'elderly';
    archetype: 'warrior' | 'mage' | 'rogue' | 'noble' | 'merchant' | 'scholar' | 'assassin' | 'paladin';
    ethnicity: 'human' | 'elf' | 'dwarf' | 'orc' | 'halfling' | 'tiefling' | 'dragonborn';
    role: 'protagonist' | 'antagonist' | 'ally' | 'neutral' | 'merchant' | 'guard';
  };
  facialFeatures: {
    jawWidth: number; // 0.0-1.0
    noseShape: 'straight' | 'aquiline' | 'button' | 'broad' | 'narrow';
    eyeShape: 'narrow' | 'wide' | 'deep_set' | 'prominent' | 'almond';
    cheekboneHeight: number; // 0.0-1.0
    facialHair: 'none' | 'stubble' | 'beard' | 'mustache' | 'goatee' | 'full';
    scars: boolean;
    tattoos: boolean;
  };
  expression: {
    emotion: 'neutral' | 'stern' | 'friendly' | 'mysterious' | 'wise' | 'fierce' | 'sad' | 'angry' | 'happy';
    intensity: number; // 0.0-1.0
    eyeContact: boolean;
    mouthExpression: 'closed' | 'slight_smile' | 'open' | 'frown' | 'smirk';
  };
  camera: {
    angle: 'front' | 'three_quarter' | 'profile' | 'slight_turn';
    fov: number; // 35-85
    distance: 'close' | 'medium' | 'far';
    headTilt: number; // -0.3 to 0.3
  };
  lighting: {
    keyFillRatio: number; // 1.0-8.0
    rimLighting: boolean;
    lightDirection: 'front' | 'side' | 'back' | 'top' | 'bottom';
    softness: number; // 0.0-1.0
    colorTemperature: number; // 2000-10000
  };
  style: {
    renderingStyle: 'realistic' | 'stylized' | 'painterly' | 'cel_shaded' | 'sketch';
    detailLevel: 'low' | 'medium' | 'high' | 'ultra';
    colorPalette: 'natural' | 'desaturated' | 'vibrant' | 'monochrome' | 'sepia';
    postProcessing: 'none' | 'film_grain' | 'vignette' | 'both';
  };
}

// Weapons & Items Generation Schema (matches backend Pydantic schema)
export interface WeaponItemConfig extends FiboBaseConfig {
  assetType: 'weapon_item';
  item: {
    category: 'sword' | 'bow' | 'staff' | 'shield' | 'dagger' | 'axe' | 'hammer' | 'potion' | 'artifact' | 'armor' | 'accessory';
    subcategory: 'longsword' | 'shortsword' | 'greatsword' | 'longbow' | 'crossbow' | 'battle_axe' | 'war_hammer' | 'healing_potion' | 'mana_potion' | 'ancient_relic' | 'leather_armor' | 'plate_armor' | 'ring' | 'amulet';
    material: 'steel' | 'iron' | 'crystal' | 'wood' | 'bone' | 'obsidian' | 'mithril' | 'adamantine' | 'gold' | 'silver';
    rarity: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary' | 'artifact' | 'unique';
  };
  form: {
    proportions: number; // 0.0-1.0
    symmetry: number; // 0.0-1.0
    ornamentation: number; // 0.0-1.0
    size: 'tiny' | 'small' | 'medium' | 'large' | 'huge';
    condition: 'pristine' | 'worn' | 'battle_scarred' | 'ancient' | 'broken';
  };
  surface: {
    texture: 'smooth' | 'rough' | 'polished' | 'etched' | 'hammered' | 'crystalline';
    patina: 'none' | 'light' | 'moderate' | 'heavy' | 'rust' | 'verdigris' | 'tarnish';
    emissiveGlow: number; // 0.0-1.0
    inscriptions: boolean;
    gemstones: boolean;
    enchantmentEffects: 'none' | 'fire' | 'ice' | 'lightning' | 'poison' | 'holy' | 'shadow' | 'arcane';
  };
  camera: {
    mode: 'isometric' | 'flat_icon' | 'hero_render' | 'three_quarter' | 'side_profile';
    rotationX: number; // 0.0-360.0
    rotationY: number; // 0.0-360.0
    rotationZ: number; // 0.0-360.0
    distance: 'close' | 'medium' | 'far';
    fov: number; // 35-85
  };
  background: {
    type: 'transparent' | 'solid' | 'gradient' | 'radial_glow' | 'environment';
    color: 'black' | 'white' | 'gray' | 'blue' | 'red' | 'gold' | 'purple' | 'green';
    intensity: number; // 0.0-1.0
  };
  lighting: {
    setup: 'studio' | 'dramatic' | 'soft' | 'rim' | 'environmental';
    keyLightAngle: number; // 0.0-360.0
    fillLightIntensity: number; // 0.0-1.0
    rimLightIntensity: number; // 0.0-1.0
    shadowSoftness: number; // 0.0-1.0
  };
}

// Environment Concept Generation Schema (matches backend Pydantic schema)
export interface EnvironmentConfig extends FiboBaseConfig {
  assetType: 'environment_concept';
  scene: {
    type: 'city' | 'ruins' | 'forest' | 'dungeon' | 'castle' | 'village' | 'cave' | 'temple' | 'sci_fi_interior' | 'fantasy_landscape' | 'mountain' | 'desert' | 'swamp' | 'tundra';
    biome: 'temperate' | 'tropical' | 'arctic' | 'desert' | 'mountain' | 'swamp' | 'underground' | 'urban' | 'magical' | 'alien';
    scale?: 'intimate' | 'medium' | 'vast' | 'epic';
    timePeriod: 'prehistoric' | 'ancient' | 'medieval' | 'renaissance' | 'industrial' | 'modern' | 'futuristic' | 'post_apocalyptic';
    population: 'abandoned' | 'sparse' | 'moderate' | 'crowded' | 'overpopulated';
  };
  atmosphere: {
    timeOfDay: 'dawn' | 'morning' | 'midday' | 'afternoon' | 'dusk' | 'night' | 'midnight';
    weather: 'clear' | 'overcast' | 'foggy' | 'rainy' | 'stormy' | 'snowy' | 'misty' | 'windy';
    mood: 'peaceful' | 'ominous' | 'mysterious' | 'epic' | 'melancholic' | 'hopeful' | 'tense' | 'serene';
    visibility: number; // 0.0-1.0
    fogDensity: number; // 0.0-1.0
    particleEffects: 'none' | 'dust' | 'pollen' | 'ash' | 'snow' | 'rain' | 'magical';
  };
  composition: {
    cameraHeight: 'ground' | 'eye_level' | 'elevated' | 'aerial' | 'birds_eye';
    horizonPosition: number; // 0.0-1.0
    focalPoint: 'center' | 'left_third' | 'right_third' | 'foreground' | 'background';
    depthLayers: number; // 2-5
    leadingLines: boolean;
    frameElements: boolean;
  };
  lighting: {
    lightStyle: 'natural' | 'dramatic' | 'soft' | 'harsh' | 'magical' | 'artificial';
    primarySource: 'sun' | 'moon' | 'fire' | 'magic' | 'artificial' | 'multiple';
    hdrContrast: number; // 0.0-1.0
    godRays: number; // 0.0-1.0
    volumetrics: number; // 0.0-1.0
    colorTemperature: number; // 2000-10000
    ambientOcclusion: boolean;
    shadowIntensity: number; // 0.0-1.0
  };
  style: {
    renderingStyle: 'photorealistic' | 'cinematic_realism' | 'matte_painting' | 'stylized' | 'concept_art' | 'impressionistic' | 'minimalist';
    colorGrading: 'natural' | 'cinematic' | 'desaturated' | 'high_contrast' | 'warm' | 'cool' | 'monochrome' | 'vintage';
    detailLevel: 'low' | 'medium' | 'high' | 'ultra';
    postProcessing: 'none' | 'film_grain' | 'vignette' | 'chromatic_aberration' | 'all';
  };
}

// Union type for all asset configurations
export type AssetConfig = NPCPortraitConfig | WeaponItemConfig | EnvironmentConfig;

// Asset generation result with metadata
export interface GeneratedAsset {
  id: string;
  type: AssetConfig['assetType'];
  config: AssetConfig;
  image_url: string;
  thumbnail_url?: string;
  created_at: string;
  metadata: {
    generation_time: number;
    file_size: number;
    dimensions: { width: number; height: number };
    format: 'png' | 'jpg' | 'webp';
    has_transparency: boolean;
  };
  tags: string[];
  notes?: string;
}

// Asset history and versioning
export interface AssetHistoryEntry {
  id: string;
  asset: GeneratedAsset;
  version: number;
  parent_id?: string;
  branch_name?: string;
  notes?: string;
  created_at: string;
}

// Batch generation configuration
export interface BatchGenerationConfig {
  base_config: AssetConfig;
  variations: {
    parameter_path: string;
    values: any[];
  }[];
  naming_pattern: string;
  output_format: 'png' | 'jpg' | 'webp';
}

// Export formats and options
export interface ExportOptions {
  format: 'png' | 'jpg' | 'webp' | 'json';
  quality?: number; // 1-100 for jpg/webp
  transparency?: boolean;
  metadata_embedded?: boolean;
  batch_zip?: boolean;
}

// Application state types
export interface AppState {
  activeAssetType: AssetConfig['assetType'];
  currentConfig: AssetConfig | null;
  generatedAssets: GeneratedAsset[];
  assetHistory: AssetHistoryEntry[];
  isGenerating: boolean;
  connectionStatus: 'connected' | 'disconnected' | 'error';
  lastError?: string;
}

// Preset configurations for quick start
export interface AssetPreset {
  id: string;
  name: string;
  description: string;
  type: AssetConfig['assetType'];
  config: Partial<AssetConfig>;
  thumbnail?: string;
  tags: string[];
}