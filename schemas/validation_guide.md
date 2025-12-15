# FIBO JSON Schema Validation Guide

## Overview

This document provides comprehensive validation rules and integration guidelines for the Procedural Game Asset Foundry FIBO JSON schemas. These schemas are designed for deterministic, production-ready asset generation in game development workflows.

## Schema Validation Hierarchy

### 1. Structural Validation
- **JSON Schema Compliance**: All configurations must validate against their respective JSON Schema definitions
- **Required Fields**: Every required field must be present and non-null
- **Type Safety**: All fields must match their specified data types exactly

### 2. Business Logic Validation
- **Enum Constraints**: All enumerated values must match exactly (case-sensitive)
- **Numeric Ranges**: All numeric values must fall within specified min/max bounds
- **Cross-Field Dependencies**: Related fields must maintain logical consistency

### 3. Production Constraints
- **Seed Uniqueness**: Seeds should be unique per generation session for deterministic reproduction
- **Output Format Compatibility**: Format/resolution combinations must be supported by target pipeline
- **Performance Limits**: Complex configurations may require generation time warnings

## Field-by-Field Validation Rules

### Universal Fields (All Asset Types)

#### `schemaVersion`
- **Type**: String enum
- **Valid Values**: `["v1"]`
- **Validation**: Exact match required
- **Future-Proofing**: New versions will be additive, maintaining backward compatibility

#### `assetType`
- **Type**: String enum  
- **Valid Values**: `["npc_portrait", "weapon_item", "environment_concept"]`
- **Validation**: Must match the schema being validated against
- **Pipeline Routing**: Used to route generation requests to appropriate FIBO models

#### `seed`
- **Type**: Integer
- **Range**: 1 to 999,999,999
- **Validation**: Must be positive integer within range
- **Determinism**: Same seed + same config = identical output
- **Recommendation**: Use timestamp + random component for uniqueness

#### `output` Object
- **resolution**: Must match supported FIBO output dimensions
- **colorDepth**: Higher bit depths increase file size and generation time
- **format**: PNG recommended for transparency, JPG for smaller file sizes
- **background**: Must be compatible with chosen format (transparent requires PNG)

### NPC Portrait Specific Validation

#### `identity` Object Constraints
```javascript
// Age-Gender Presentation Logic
if (identity.ageRange === "young" && identity.genderPresentation === "masculine") {
  // Facial hair options limited to ["none", "stubble"]
}

// Archetype-Ethnicity Compatibility
if (identity.ethnicity.startsWith("fantasy_") && identity.archetype === "merchant") {
  // Warning: Fantasy races as merchants may need cultural context
}
```

#### `facialFeatures` Numeric Validation
- All values must be in range [0.0, 1.0]
- Extreme combinations may produce unrealistic results:
  - `jawWidth: 1.0` + `cheekboneHeight: 0.0` = potentially distorted proportions
  - Recommend validation warnings for extreme combinations

#### `camera` Technical Constraints
- **fov Range**: 35-85mm equivalent
  - 35mm = wide angle, may distort facial features
  - 85mm = portrait lens, natural perspective
  - Values outside range may produce unrealistic perspective
- **headTilt Range**: -0.3 to 0.3 radians (-17° to +17°)
  - Extreme tilts may cause composition issues

### Weapon/Item Specific Validation

#### Rarity-Dependent Constraints
```javascript
const rarityConstraints = {
  "common": {
    ornamentation: [0.0, 0.3],
    emissiveGlow: [0.0, 0.2],
    materials: ["steel", "iron", "wood", "bone"]
  },
  "legendary": {
    ornamentation: [0.7, 1.0],
    emissiveGlow: [0.5, 1.0],
    materials: ["mithril", "adamantine", "crystal", "ethereal"]
  }
}
```

#### Material-Surface Compatibility
- **Crystal + Patina**: Crystal materials should not have rust/tarnish patina
- **Wood + Emissive**: Wood materials with high emissive glow need magical justification
- **Bone + Reflections**: Bone materials should have lower reflection values (0.1-0.4)

#### Camera Mode Optimization
- **flat_icon**: Optimized for UI, minimal shadows/effects
- **isometric**: Consistent perspective for game world items
- **hero_render**: Maximum detail and effects allowed

### Environment Concept Validation

#### Atmospheric Consistency
```javascript
// Time of Day + Weather Logic
const validCombinations = {
  "dawn": ["clear", "foggy", "partly_cloudy"],
  "night": ["clear", "rainy", "stormy"], // No "sunny" at night
  "midday": ["clear", "partly_cloudy", "overcast"] // Rare fog at midday
}

// Biome + Weather Constraints  
const biomeWeather = {
  "desert": ["clear", "sandstorm"], // No rain/snow in desert
  "arctic": ["clear", "snowy", "stormy"], // No rain in arctic
  "tropical": ["clear", "rainy", "stormy"] // No snow in tropical
}
```

#### Composition Technical Rules
- **horizonPosition**: 0.33 or 0.66 follow rule of thirds for dynamic composition
- **cameraHeight + Scale**: Aerial cameras work best with "wide" or "epic" scales
- **depthLayers + fogDensity**: High fog density reduces effective depth layers

## Frontend Integration Guidelines

### Real-Time Validation
```typescript
interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
  suggestions: string[];
}

// Validate on every control change
function validateConfiguration(config: AssetConfig): ValidationResult {
  // 1. Schema validation
  // 2. Business logic validation  
  // 3. Performance impact assessment
  // 4. Generate user-friendly suggestions
}
```

### UI Control Mapping
- **Sliders**: Map directly to numeric fields with appropriate ranges
- **Dropdowns**: Populate from enum values with human-readable labels
- **Toggles**: For boolean fields and binary enum choices
- **Conditional Controls**: Show/hide based on other field values

### Live JSON Updates
- Update JSON display in real-time as controls change
- Highlight invalid fields in red
- Show warnings in amber
- Provide auto-correction suggestions

## Backend Validation Pipeline

### Request Validation Flow
1. **Schema Validation**: JSON Schema validation against appropriate schema
2. **Business Rules**: Apply domain-specific validation rules
3. **Security Checks**: Validate seed ranges, prevent injection attacks
4. **Performance Assessment**: Estimate generation time and resource usage
5. **Queue Management**: Route to appropriate FIBO model instance

### Error Response Format
```json
{
  "error": "VALIDATION_FAILED",
  "message": "Configuration validation failed",
  "details": {
    "field": "facialFeatures.jawWidth",
    "value": 1.5,
    "constraint": "Value must be between 0.0 and 1.0",
    "suggestion": "Reduce jawWidth to maximum value of 1.0"
  },
  "code": "FIELD_OUT_OF_RANGE"
}
```

## Performance Optimization Guidelines

### Generation Time Estimates
- **NPC Portrait**: 2-8 seconds depending on detail level and resolution
- **Weapon/Item**: 1-5 seconds, varies by complexity and effects
- **Environment**: 5-15 seconds for high-detail landscapes

### Resource Usage Optimization
- **Batch Generation**: Group similar configurations to optimize GPU usage
- **Progressive Detail**: Start with lower detail for previews, full detail for final
- **Caching Strategy**: Cache common configurations to reduce generation load

## Extensibility Notes

### Adding New Asset Types
1. Create new schema following base schema pattern
2. Add validation rules to backend
3. Create UI controls for new parameters
4. Update routing logic for new asset type

### Schema Versioning Strategy
- **Additive Changes**: New optional fields can be added without version bump
- **Breaking Changes**: Require new schema version (v2, v3, etc.)
- **Backward Compatibility**: Always maintain support for previous versions
- **Migration Path**: Provide automatic migration for deprecated fields

### Custom Parameter Extensions
```json
{
  "extensions": {
    "studio_custom": {
      "project_id": "game_alpha_v2",
      "art_director_notes": "Increase contrast for mobile visibility",
      "pipeline_version": "2.1.3"
    }
  }
}
```

## Quality Assurance Checklist

### Pre-Production Validation
- [ ] All enum values tested with actual FIBO generation
- [ ] Numeric ranges validated for realistic output
- [ ] Cross-field dependencies produce expected results
- [ ] Performance benchmarks established for all configurations
- [ ] Error handling tested for all validation scenarios

### Production Monitoring
- [ ] Track validation failure rates by field
- [ ] Monitor generation success rates by configuration complexity
- [ ] Collect user feedback on validation messaging
- [ ] Performance metrics for different configuration types
- [ ] A/B test validation rule strictness vs. user experience

This validation framework ensures that the FIBO JSON schemas maintain production quality while providing clear, actionable feedback to users and robust error handling for automated systems.