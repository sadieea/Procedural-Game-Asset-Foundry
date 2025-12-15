# FIBO JSON → UI Control Implementation Guide

## 🎯 Implementation Overview

This guide provides the complete implementation strategy for deterministic UI → JSON mapping in the Procedural Game Asset Foundry. Every UI control maps exactly 1:1 with a JSON field, ensuring perfect reproducibility and professional workflow integration.

## 🔒 Core Architecture Principles

### 1. **Deterministic Mapping**
```typescript
// RULE: One JSON field = One UI control (no exceptions)
interface ControlMapping {
  jsonPath: string        // Exact JSON path: "lighting.keyLight"
  controlType: ControlType // UI control type
  value: any             // Current value
  onChange: (value: any) => void // Direct update function
}
```

### 2. **Path-Based Updates**
```typescript
// All updates use dot-notation paths
const updateConfig = (path: string, value: any) => {
  // "facialFeatures.jawWidth" → config.facialFeatures.jawWidth = 0.7
  const keys = path.split('.')
  let current = config
  for (let i = 0; i < keys.length - 1; i++) {
    if (!current[keys[i]]) current[keys[i]] = {}
    current = current[keys[i]]
  }
  current[keys[keys.length - 1]] = value
}
```

### 3. **Live JSON Synchronization**
```typescript
// JSON updates immediately when any control changes
useEffect(() => {
  updateJSONDisplay(config)
  validateConfiguration(config)
}, [config])
```

## 🧩 Control Type Implementation

### Slider Control (Numeric Fields)
```typescript
interface SliderControlProps extends BaseControlProps<number> {
  min: number
  max: number
  step: number
  formatDisplay?: (value: number) => string
}

// Usage Examples:
<SliderControl
  value={getValue('facialFeatures.jawWidth', 0.5)}
  onChange={(value) => onChange('facialFeatures.jawWidth', value)}
  jsonPath="facialFeatures.jawWidth"
  min={0.0}
  max={1.0}
  step={0.01}
  label="Jaw Width"
/>

<SliderControl
  value={getValue('camera.fov', 50)}
  onChange={(value) => onChange('camera.fov', value)}
  jsonPath="camera.fov"
  min={35}
  max={85}
  step={1}
  formatDisplay={(value) => `${value}mm`}
  label="Field of View"
/>
```

### Segmented Control (2-5 Enum Options)
```typescript
interface SegmentedControlProps<T> extends BaseControlProps<T> {
  options: Array<{
    value: T
    label: string
    icon?: React.ComponentType
    color?: string // For rarity color-coding
  }>
}

// Usage Examples:
<SegmentedControl
  value={getValue('identity.ageRange', 'adult')}
  onChange={(value) => onChange('identity.ageRange', value)}
  jsonPath="identity.ageRange"
  options={[
    { value: 'young', label: 'Young' },
    { value: 'adult', label: 'Adult' },
    { value: 'middle_aged', label: 'Middle Aged' },
    { value: 'elderly', label: 'Elderly' }
  ]}
/>

// Rarity with color coding:
<SegmentedControl
  value={getValue('item.rarity', 'common')}
  onChange={(value) => onChange('item.rarity', value)}
  jsonPath="item.rarity"
  options={[
    { value: 'common', label: 'Common', color: '#9CA3AF' },
    { value: 'legendary', label: 'Legendary', color: '#F59E0B' }
  ]}
/>
```

### Dropdown Control (5+ Enum Options)
```typescript
interface DropdownControlProps<T> extends BaseControlProps<T> {
  options: Array<{
    value: T
    label: string
    description?: string
    group?: string // For grouped options
  }>
  searchable?: boolean
}

// Usage Examples:
<DropdownControl
  value={getValue('identity.ethnicity', 'caucasian')}
  onChange={(value) => onChange('identity.ethnicity', value)}
  jsonPath="identity.ethnicity"
  searchable
  options={[
    { value: 'east_asian', label: 'East Asian', group: 'Human' },
    { value: 'fantasy_elf', label: 'Elf', group: 'Fantasy' }
  ]}
/>
```

## 📊 Asset Type Implementations

### NPC Portrait Control Mapping
```typescript
// Complete mapping for NPCPortraitConfig
const npcControlMap = {
  // Identity Section
  'identity.ageRange': SegmentedControl,
  'identity.genderPresentation': SegmentedControl,
  'identity.ethnicity': DropdownControl,
  'identity.archetype': DropdownControl,
  
  // Facial Features Section  
  'facialFeatures.jawWidth': SliderControl,        // 0.0-1.0
  'facialFeatures.cheekboneHeight': SliderControl, // 0.0-1.0
  'facialFeatures.noseLength': SliderControl,      // 0.0-1.0
  'facialFeatures.eyeSize': SliderControl,         // 0.0-1.0
  'facialFeatures.browIntensity': SliderControl,   // 0.0-1.0
  'facialFeatures.scars': SegmentedControl,
  'facialFeatures.facialHair': DropdownControl,
  
  // Expression Section
  'expression.emotion': DropdownControl,
  'expression.intensity': SliderControl,           // 0.0-1.0
  
  // Camera Section
  'camera.angle': SegmentedControl,
  'camera.fov': SliderControl,                     // 35-85
  'camera.headTilt': SliderControl,                // -0.3 to 0.3
  'camera.distance': SegmentedControl,
  
  // Lighting Section
  'lighting.keyLight': SegmentedControl,
  'lighting.fillRatio': SliderControl,             // 0.0-1.0
  'lighting.rimLight': SegmentedControl,
  'lighting.colorTemperature': SegmentedControl,
  
  // Style Section
  'style.renderStyle': SegmentedControl,
  'style.detailLevel': SegmentedControl,
  'style.skinTexture': SegmentedControl
}
```

### Weapon/Item Control Mapping
```typescript
const weaponControlMap = {
  // Item Identity
  'item.category': DropdownControl,
  'item.rarity': SegmentedControl,                 // Color-coded
  'item.material': DropdownControl,
  'item.styleTheme': SegmentedControl,
  
  // Form & Shape
  'form.length': SliderControl,                    // 0.1-1.0
  'form.thickness': SliderControl,                 // 0.1-1.0
  'form.symmetry': SegmentedControl,
  'form.ornamentation': SliderControl,             // 0.0-1.0
  
  // Surface Details
  'surface.wearLevel': SliderControl,              // 0.0-1.0
  'surface.scratches': SegmentedControl,
  'surface.emissiveGlow': SliderControl,           // 0.0-1.0
  'surface.patina': SegmentedControl,
  'surface.inscriptions': SegmentedControl,
  
  // Camera & Presentation
  'camera.mode': SegmentedControl,
  'camera.angle': SliderControl,                   // 0-360
  'camera.fov': SliderControl,                     // 25-75
  'camera.distance': SegmentedControl,
  
  // Lighting
  'lighting.keyLight': SegmentedControl,
  'lighting.contrast': SliderControl,              // 0.0-1.0
  'lighting.rimLight': SegmentedControl,
  'lighting.reflections': SliderControl,           // 0.0-1.0
  
  // Background & Effects
  'background.type': SegmentedControl,
  'background.shadow': SegmentedControl,
  'background.particles': SegmentedControl
}
```

### Environment Control Mapping
```typescript
const environmentControlMap = {
  // Scene Definition
  'scene.type': DropdownControl,
  'scene.era': SegmentedControl,
  'scene.scale': SegmentedControl,
  'scene.biome': SegmentedControl,
  
  // Composition
  'composition.cameraHeight': SegmentedControl,
  'composition.horizonPosition': SliderControl,    // 0.0-1.0
  'composition.depthLayers': SegmentedControl,
  'composition.focalPoint': SegmentedControl,
  
  // Atmosphere
  'atmosphere.timeOfDay': SegmentedControl,
  'atmosphere.weather': DropdownControl,
  'atmosphere.fogDensity': SliderControl,          // 0.0-1.0
  'atmosphere.visibility': SliderControl,          // 0.1-1.0
  
  // Lighting & Mood
  'lighting.lightStyle': SegmentedControl,
  'lighting.contrast': SliderControl,              // 0.0-1.0
  'lighting.godRays': SliderControl,               // 0.0-1.0
  'lighting.colorTemperature': SegmentedControl,
  'lighting.ambientOcclusion': SliderControl,      // 0.0-1.0
  
  // Style & Rendering
  'style.renderStyle': SegmentedControl,
  'style.detailLevel': SegmentedControl,
  'style.colorPalette': SegmentedControl
}
```

## 🔧 State Management Implementation

### Configuration State Structure
```typescript
interface ConfigurationState {
  // Current configuration matching JSON schema exactly
  config: Partial<AssetConfig>
  
  // Validation state for each field
  errors: Record<string, string>
  warnings: Record<string, string>
  
  // UI state
  expandedSections: Set<string>
  
  // Methods
  updateField: (path: string, value: any) => void
  resetToDefaults: () => void
  validateConfiguration: () => ValidationResult
}
```

### Update Flow Implementation
```typescript
const updateField = (path: string, value: any) => {
  // 1. Update configuration
  const newConfig = updateNestedValue(config, path, value)
  
  // 2. Add required base fields
  const completeConfig = {
    ...newConfig,
    schemaVersion: 'v1',
    assetType: currentAssetType,
    seed: generateSeed(),
    output: getDefaultOutput()
  }
  
  // 3. Validate configuration
  const validation = validateConfiguration(completeConfig)
  
  // 4. Update state
  setConfig(completeConfig)
  setErrors(validation.errors)
  setWarnings(validation.warnings)
  
  // 5. Notify parent component
  onConfigChange(completeConfig)
  
  // 6. Update JSON display
  updateJSONDisplay(completeConfig)
}
```

## 🎨 Visual Feedback Implementation

### Field Validation Display
```typescript
// Error states
<SliderControl
  value={value}
  onChange={onChange}
  error={errors[jsonPath]}        // Red border + error message
  warning={warnings[jsonPath]}    // Amber border + warning message
  jsonPath={jsonPath}
/>

// JSON highlighting
const highlightJSONField = (path: string, type: 'error' | 'warning' | 'changed') => {
  const colors = {
    error: 'text-red-400 bg-red-500/10',
    warning: 'text-studio-amber bg-studio-amber/10', 
    changed: 'text-studio-cyan bg-studio-cyan/10'
  }
  return colors[type]
}
```

### Real-time JSON Updates
```typescript
// JSON panel updates live as controls change
useEffect(() => {
  const formattedJSON = JSON.stringify(config, null, 2)
  setJSONDisplay(formattedJSON)
  
  // Highlight changed fields
  highlightChangedFields(previousConfig, config)
}, [config])
```

## 🔄 Asset Type Switching

### Complete Control Set Replacement
```typescript
const switchAssetType = (newType: AssetType) => {
  // 1. Clear current configuration
  setConfig({})
  setErrors({})
  setWarnings({})
  
  // 2. Load default configuration for new type
  const defaultConfig = getDefaultConfigForType(newType)
  setConfig(defaultConfig)
  
  // 3. Update asset type
  setAssetType(newType)
  
  // 4. Reset UI state
  setExpandedSections(new Set(['identity', 'camera', 'lighting']))
  
  // 5. Update JSON display
  updateJSONDisplay(defaultConfig)
}
```

## 📋 Validation Integration

### Field-Level Validation
```typescript
const validateField = (path: string, value: any, config: AssetConfig) => {
  const validation: FieldValidation = {
    isValid: true,
    error: null,
    warning: null
  }
  
  // Schema validation
  if (!validateAgainstSchema(path, value)) {
    validation.isValid = false
    validation.error = "Value doesn't match schema requirements"
  }
  
  // Business logic validation
  if (path === 'item.rarity' && value === 'legendary') {
    const ornamentation = getValue('form.ornamentation', 0)
    if (ornamentation < 0.7) {
      validation.warning = "Legendary items typically have high ornamentation (>0.7)"
    }
  }
  
  return validation
}
```

### Cross-Field Validation
```typescript
const validateCrossFields = (config: AssetConfig) => {
  const warnings: Record<string, string> = {}
  
  // Material-patina compatibility
  if (config.item?.material === 'crystal' && config.surface?.patina === 'rust') {
    warnings['surface.patina'] = "Crystal materials don't rust - consider 'none' or 'tarnish'"
  }
  
  // Time-weather compatibility
  if (config.atmosphere?.timeOfDay === 'night' && config.atmosphere?.weather === 'sunny') {
    warnings['atmosphere.weather'] = "Sunny weather is unusual at night"
  }
  
  return warnings
}
```

## 🚀 Performance Optimization

### Debounced Updates
```typescript
const debouncedUpdate = useMemo(
  () => debounce((path: string, value: any) => {
    updateField(path, value)
  }, 100),
  []
)

// Use for high-frequency controls like sliders
<SliderControl
  onChange={debouncedUpdate}
  // ... other props
/>
```

### Memoized Components
```typescript
const MemoizedSliderControl = memo(SliderControl, (prev, next) => {
  return prev.value === next.value && 
         prev.error === next.error && 
         prev.warning === next.warning
})
```

## 🎯 Integration Checklist

### Frontend Implementation
- [ ] All controls implement BaseControlProps interface
- [ ] Every control has exact jsonPath mapping
- [ ] Validation state displays in UI
- [ ] JSON panel updates live
- [ ] Asset type switching clears state
- [ ] Error/warning states are visible
- [ ] Performance optimizations applied

### Backend Integration
- [ ] Validation endpoints match frontend rules
- [ ] Schema validation implemented
- [ ] Cross-field validation rules
- [ ] Error response format matches frontend expectations
- [ ] Generation API accepts exact JSON format

### Quality Assurance
- [ ] Every JSON field has corresponding UI control
- [ ] No hidden transformations or magic conversions
- [ ] Deterministic: same UI state = same JSON
- [ ] All enum values tested
- [ ] Numeric ranges validated
- [ ] Cross-field dependencies work correctly

This implementation ensures perfect 1:1 mapping between UI controls and FIBO JSON schemas, providing the deterministic, professional workflow that game studios require.