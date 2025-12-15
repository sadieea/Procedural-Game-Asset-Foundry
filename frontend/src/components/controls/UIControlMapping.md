# FIBO JSON → UI Control Mapping Specification

## 🎯 Mapping Principles

### Deterministic Rules
1. **One JSON field = One UI control** (no exceptions)
2. **No hidden conversions** or magic transformations
3. **Live synchronization** between UI and JSON
4. **Visible defaults** for every parameter
5. **Asset type switching** swaps entire control set

### Control Type Standards
| JSON Type | UI Control | Implementation |
|-----------|------------|----------------|
| `enum` (2-4 options) | Segmented Button | Radio-style selection |
| `enum` (5+ options) | Dropdown | Select with search |
| `number` (0-1 range) | Slider | Step 0.01, live update |
| `number` (angles/FOV) | Slider | Step 1, degree labels |
| `string` (fixed) | Read-only Label | Display only |
| `object` | Accordion Section | Collapsible group |

## 🧑 NPC Portrait Control Mapping

### Identity Section
```typescript
interface IdentityControls {
  ageRange: SegmentedControl<"young" | "adult" | "middle_aged" | "elderly">
  genderPresentation: SegmentedControl<"masculine" | "feminine" | "androgynous">
  ethnicity: Dropdown<EthnicityOptions>
  archetype: Dropdown<ArchetypeOptions>
}
```

| JSON Path | Control Type | Options/Range | Default | Notes |
|-----------|--------------|---------------|---------|-------|
| `identity.ageRange` | Segmented | young, adult, middle_aged, elderly | "adult" | Affects facial structure |
| `identity.genderPresentation` | Segmented | masculine, feminine, androgynous | "masculine" | Controls feature softness |
| `identity.ethnicity` | Dropdown | east_asian, south_asian, african, caucasian, middle_eastern, latino, mixed, fantasy_elf, fantasy_dwarf, fantasy_orc | "caucasian" | Searchable dropdown |
| `identity.archetype` | Dropdown | warrior, mage, rogue, noble, merchant, scholar, assassin, paladin, villager, blacksmith | "warrior" | Affects styling hints |

### Facial Features Section
```typescript
interface FacialFeaturesControls {
  jawWidth: Slider // 0.0 - 1.0, step 0.01
  cheekboneHeight: Slider // 0.0 - 1.0, step 0.01
  noseLength: Slider // 0.0 - 1.0, step 0.01
  eyeSize: Slider // 0.0 - 1.0, step 0.01
  browIntensity: Slider // 0.0 - 1.0, step 0.01
  scars: SegmentedControl<"none" | "light" | "heavy" | "ritual" | "battle">
  facialHair: Dropdown<FacialHairOptions>
}
```

| JSON Path | Control Type | Range/Options | Default | Display Label |
|-----------|--------------|---------------|---------|---------------|
| `facialFeatures.jawWidth` | Slider | 0.0 - 1.0 | 0.5 | "Jaw Width" |
| `facialFeatures.cheekboneHeight` | Slider | 0.0 - 1.0 | 0.5 | "Cheekbone Height" |
| `facialFeatures.noseLength` | Slider | 0.0 - 1.0 | 0.5 | "Nose Length" |
| `facialFeatures.eyeSize` | Slider | 0.0 - 1.0 | 0.5 | "Eye Size" |
| `facialFeatures.browIntensity` | Slider | 0.0 - 1.0 | 0.5 | "Brow Intensity" |
| `facialFeatures.scars` | Segmented | none, light, heavy, ritual, battle | "none" | "Battle Scars" |
| `facialFeatures.facialHair` | Dropdown | none, stubble, beard, mustache, goatee, full | "none" | "Facial Hair" |

### Expression Section
```typescript
interface ExpressionControls {
  emotion: Dropdown<EmotionOptions>
  intensity: Slider // 0.0 - 1.0, step 0.01
}
```

| JSON Path | Control Type | Options/Range | Default | Notes |
|-----------|--------------|---------------|---------|-------|
| `expression.emotion` | Dropdown | neutral, stern, friendly, angry, mysterious, wise, fierce, sad, determined | "neutral" | Primary expression |
| `expression.intensity` | Slider | 0.0 - 1.0 | 0.4 | Expression strength |

### Camera Section
```typescript
interface CameraControls {
  angle: SegmentedControl<CameraAngle>
  fov: Slider // 35 - 85, step 1
  headTilt: Slider // -0.3 - 0.3, step 0.01
  distance: SegmentedControl<"close" | "medium" | "far">
}
```

| JSON Path | Control Type | Range/Options | Default | Display Format |
|-----------|--------------|---------------|---------|----------------|
| `camera.angle` | Segmented | frontal, three_quarter_left, three_quarter_right, profile_left, profile_right | "three_quarter_left" | Icon + label |
| `camera.fov` | Slider | 35 - 85 | 50 | "50mm" format |
| `camera.headTilt` | Slider | -0.3 - 0.3 | 0.0 | "±17°" format |
| `camera.distance` | Segmented | close, medium, far | "medium" | Text labels |

### Lighting Section
```typescript
interface LightingControls {
  keyLight: SegmentedControl<"soft" | "dramatic" | "studio" | "natural">
  fillRatio: Slider // 0.0 - 1.0, step 0.01
  rimLight: SegmentedControl<"none" | "subtle" | "strong">
  colorTemperature: SegmentedControl<ColorTemp>
}
```

| JSON Path | Control Type | Options/Range | Default | Notes |
|-----------|--------------|---------------|---------|-------|
| `lighting.keyLight` | Segmented | soft, dramatic, studio, natural | "studio" | Light quality |
| `lighting.fillRatio` | Slider | 0.0 - 1.0 | 0.4 | "1:2.5" ratio display |
| `lighting.rimLight` | Segmented | none, subtle, strong | "subtle" | Edge lighting |
| `lighting.colorTemperature` | Segmented | warm, neutral, cool, candlelight, daylight, moonlight | "neutral" | Color icons |

### Style Section
```typescript
interface StyleControls {
  renderStyle: SegmentedControl<RenderStyle>
  detailLevel: SegmentedControl<"low" | "medium" | "high" | "ultra">
  skinTexture: SegmentedControl<SkinTexture>
}
```

| JSON Path | Control Type | Options | Default | Performance Impact |
|-----------|--------------|---------|---------|-------------------|
| `style.renderStyle` | Segmented | photorealistic, stylized, painterly, cel_shaded, concept_art | "photorealistic" | High |
| `style.detailLevel` | Segmented | low, medium, high, ultra | "high" | Affects gen time |
| `style.skinTexture` | Segmented | smooth, natural, rough, weathered, fantasy | "natural" | Surface detail |

## 🗡️ Weapon/Item Control Mapping

### Item Section
```typescript
interface ItemControls {
  category: Dropdown<ItemCategory>
  rarity: SegmentedControl<RarityLevel> // Color-coded
  material: Dropdown<MaterialType>
  styleTheme: SegmentedControl<StyleTheme>
}
```

| JSON Path | Control Type | Options | Default | Visual Treatment |
|-----------|--------------|---------|---------|------------------|
| `item.category` | Dropdown | sword, axe, bow, staff, dagger, hammer, gun, potion, artifact, shield, armor, accessory | "sword" | Icon + text |
| `item.rarity` | Segmented | common, uncommon, rare, epic, legendary, artifact, unique | "common" | Color-coded borders |
| `item.material` | Dropdown | steel, iron, bronze, silver, gold, crystal, wood, bone, obsidian, mithril, adamantine, ethereal | "steel" | Material swatches |
| `item.styleTheme` | Segmented | fantasy, sci_fi, modern, steampunk, medieval, ancient, tribal, elven, dwarven, orcish | "fantasy" | Theme icons |

### Form Section
```typescript
interface FormControls {
  length: Slider // 0.1 - 1.0, step 0.01
  thickness: Slider // 0.1 - 1.0, step 0.01
  symmetry: SegmentedControl<"symmetrical" | "asymmetrical" | "curved" | "twisted">
  ornamentation: Slider // 0.0 - 1.0, step 0.01
}
```

| JSON Path | Control Type | Range/Options | Default | Constraint Notes |
|-----------|--------------|---------------|---------|------------------|
| `form.length` | Slider | 0.1 - 1.0 | 0.6 | Dagger=0.1, Greatsword=1.0 |
| `form.thickness` | Slider | 0.1 - 1.0 | 0.4 | Thin=0.1, Bulky=1.0 |
| `form.symmetry` | Segmented | symmetrical, asymmetrical, curved, twisted | "symmetrical" | Form variation |
| `form.ornamentation` | Slider | 0.0 - 1.0 | 0.5 | Rarity-dependent max |

### Surface Section
```typescript
interface SurfaceControls {
  wearLevel: Slider // 0.0 - 1.0, step 0.01
  scratches: SegmentedControl<ScratchType>
  emissiveGlow: Slider // 0.0 - 1.0, step 0.01
  patina: SegmentedControl<PatinaType>
  inscriptions: SegmentedControl<InscriptionType>
}
```

| JSON Path | Control Type | Options/Range | Default | Material Constraints |
|-----------|--------------|---------------|---------|---------------------|
| `surface.wearLevel` | Slider | 0.0 - 1.0 | 0.3 | Pristine=0, Worn=1 |
| `surface.scratches` | Segmented | none, light, heavy, battle_worn, ritual | "light" | Wear pattern |
| `surface.emissiveGlow` | Slider | 0.0 - 1.0 | 0.2 | Rarity affects max |
| `surface.patina` | Dropdown | none, light, heavy, verdigris, rust, tarnish | "none" | Material-dependent |
| `surface.inscriptions` | Segmented | none, runes, text, symbols, geometric | "none" | Surface markings |

### Camera Section
```typescript
interface WeaponCameraControls {
  mode: SegmentedControl<CameraMode>
  angle: Slider // 0 - 360, step 1
  fov: Slider // 25 - 75, step 1
  distance: SegmentedControl<"close" | "medium" | "far">
}
```

| JSON Path | Control Type | Range/Options | Default | Use Case |
|-----------|--------------|---------------|---------|----------|
| `camera.mode` | Segmented | isometric, flat_icon, hero_render, three_quarter, profile | "hero_render" | Presentation style |
| `camera.angle` | Slider | 0 - 360 | 315 | "315°" display |
| `camera.fov` | Slider | 25 - 75 | 45 | "45°" display |
| `camera.distance` | Segmented | close, medium, far | "medium" | Framing control |

## 🌍 Environment Control Mapping

### Scene Section
```typescript
interface SceneControls {
  type: Dropdown<EnvironmentType>
  era: SegmentedControl<Era>
  scale: SegmentedControl<Scale>
  biome: SegmentedControl<Biome>
}
```

| JSON Path | Control Type | Options | Default | Compatibility |
|-----------|--------------|---------|---------|---------------|
| `scene.type` | Dropdown | city, village, forest, desert, mountains, ruins, dungeon, castle, temple, sci_fi_interior, space_station, underwater | "forest" | Searchable |
| `scene.era` | Segmented | prehistoric, ancient, medieval, renaissance, industrial, modern, futuristic, post_apocalyptic | "medieval" | Tech level |
| `scene.scale` | Segmented | intimate, medium, wide, epic, panoramic | "medium" | Scope control |
| `scene.biome` | Segmented | temperate, tropical, arctic, desert, swamp, volcanic, alien, magical | "temperate" | Climate type |

### Composition Section
```typescript
interface CompositionControls {
  cameraHeight: SegmentedControl<CameraHeight>
  horizonPosition: Slider // 0.0 - 1.0, step 0.01
  depthLayers: SegmentedControl<"shallow" | "medium" | "deep" | "infinite">
  focalPoint: SegmentedControl<FocalPoint>
}
```

| JSON Path | Control Type | Options/Range | Default | Rule of Thirds |
|-----------|--------------|---------------|---------|----------------|
| `composition.cameraHeight` | Segmented | ground, eye_level, elevated, aerial, birds_eye | "eye_level" | Perspective type |
| `composition.horizonPosition` | Slider | 0.0 - 1.0 | 0.33 | Thirds markers |
| `composition.depthLayers` | Segmented | shallow, medium, deep, infinite | "medium" | Depth complexity |
| `composition.focalPoint` | Segmented | center, left_third, right_third, foreground, background | "center" | Focus placement |

### Atmosphere Section
```typescript
interface AtmosphereControls {
  timeOfDay: SegmentedControl<TimeOfDay>
  weather: Dropdown<WeatherType>
  fogDensity: Slider // 0.0 - 1.0, step 0.01
  visibility: Slider // 0.1 - 1.0, step 0.01
}
```

| JSON Path | Control Type | Options/Range | Default | Constraints |
|-----------|--------------|---------------|---------|-------------|
| `atmosphere.timeOfDay` | Segmented | dawn, morning, midday, afternoon, dusk, night, midnight | "dusk" | Light affects |
| `atmosphere.weather` | Dropdown | clear, partly_cloudy, overcast, foggy, rainy, stormy, snowy, sandstorm | "clear" | Biome-dependent |
| `atmosphere.fogDensity` | Slider | 0.0 - 1.0 | 0.3 | Visibility affects |
| `atmosphere.visibility` | Slider | 0.1 - 1.0 | 0.8 | Atmospheric range |

### Lighting Section
```typescript
interface EnvironmentLightingControls {
  lightStyle: SegmentedControl<LightStyle>
  contrast: Slider // 0.0 - 1.0, step 0.01
  godRays: Slider // 0.0 - 1.0, step 0.01
  colorTemperature: SegmentedControl<ColorTemp>
  ambientOcclusion: Slider // 0.0 - 1.0, step 0.01
}
```

| JSON Path | Control Type | Options/Range | Default | Technical Notes |
|-----------|--------------|---------------|---------|-----------------|
| `lighting.lightStyle` | Segmented | soft, dramatic, cinematic, natural, artificial, magical | "cinematic" | Overall approach |
| `lighting.contrast` | Slider | 0.0 - 1.0 | 0.7 | Dynamic range |
| `lighting.godRays` | Slider | 0.0 - 1.0 | 0.4 | Volumetric light |
| `lighting.colorTemperature` | Segmented | warm, neutral, cool, golden_hour, blue_hour, artificial | "warm" | Color cast |
| `lighting.ambientOcclusion` | Slider | 0.0 - 1.0 | 0.6 | Shadow detail |

## 🧠 JSON Panel Requirements

### Live Synchronization Rules
```typescript
interface JSONPanelBehavior {
  // Update JSON immediately when any control changes
  onControlChange: (path: string, value: any) => void
  
  // Highlight changed fields in JSON display
  highlightChanges: boolean
  
  // Read-only JSON (no direct editing)
  readOnly: true
  
  // Export capabilities
  exportOptions: {
    copyToClipboard: () => void
    downloadJSON: () => void
    shareConfiguration: () => void
  }
}
```

### Field Highlighting System
- **Changed fields**: Amber highlight in JSON
- **Invalid fields**: Red highlight with error tooltip
- **Default values**: Normal text color
- **Required fields**: Bold text weight

### Real-time Validation Display
```typescript
interface ValidationDisplay {
  fieldErrors: Map<string, string[]>
  fieldWarnings: Map<string, string[]>
  overallStatus: "valid" | "warning" | "error"
  
  // Show validation state in UI
  showFieldStatus: (fieldPath: string) => ValidationStatus
}
```

## 🔧 Implementation Architecture

### Control Component Structure
```typescript
// Base control interface
interface BaseControl<T> {
  value: T
  onChange: (value: T) => void
  disabled?: boolean
  error?: string
  warning?: string
}

// Specific control implementations
interface SliderControl extends BaseControl<number> {
  min: number
  max: number
  step: number
  formatDisplay?: (value: number) => string
}

interface SegmentedControl<T> extends BaseControl<T> {
  options: Array<{
    value: T
    label: string
    icon?: React.ComponentType
    color?: string
  }>
}

interface DropdownControl<T> extends BaseControl<T> {
  options: Array<{
    value: T
    label: string
    description?: string
    icon?: React.ComponentType
  }>
  searchable?: boolean
  groupBy?: (option: any) => string
}
```

### Asset Type Switching Logic
```typescript
interface AssetTypeManager {
  currentType: AssetType
  
  // Completely replace control set when switching types
  switchAssetType: (newType: AssetType) => void
  
  // Reset to defaults for new type
  resetToDefaults: () => void
  
  // Preserve compatible fields when switching
  preserveCompatibleFields?: boolean
}
```

### State Management Pattern
```typescript
interface ControlState {
  // Current configuration matching JSON schema exactly
  config: AssetConfig
  
  // Validation state for each field
  validation: ValidationState
  
  // UI state (expanded sections, etc.)
  ui: UIState
  
  // Update single field with validation
  updateField: (path: string, value: any) => void
  
  // Batch update multiple fields
  updateFields: (updates: Record<string, any>) => void
  
  // Reset to schema defaults
  resetToDefaults: () => void
}
```

This mapping ensures perfect determinism: every UI interaction maps to exactly one JSON field change, with no hidden transformations or magic conversions. The JSON panel reflects the exact state of all controls in real-time.