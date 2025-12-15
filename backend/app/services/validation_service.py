"""
Strict FIBO JSON Schema Validation Service for Procedural Game Asset Foundry.
Production-ready validation with comprehensive safety checks.

VALIDATION RULES:
- No additional properties allowed
- All enums strictly enforced  
- Numeric ranges validated
- Defaults applied explicitly
- Schema version checked
- Asset type enforced
- If validation fails → generation must NOT run
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import ValidationError as PydanticValidationError
import structlog

from app.core.exceptions import SchemaValidationError, ValidationError
from app.schemas.asset import BatchVariant, GenerationRequest
from app.schemas.fibo import (
    AssetConfig,
    NPCPortraitConfig,
    WeaponItemConfig,
    EnvironmentConfig,
    AssetType,
    validate_asset_config,
    get_default_config,
    ValidationError as FiboValidationError
)

logger = structlog.get_logger()


class ValidationResult:
    """Structured validation result with comprehensive error reporting."""
    
    def __init__(self, success: bool, config: Optional[AssetConfig] = None, 
                 errors: List[str] = None, warnings: List[str] = None):
        self.success = success
        self.config = config
        self.errors = errors or []
        self.warnings = warnings or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        result = {
            "success": self.success,
            "errorType": "SchemaValidationError" if not self.success else None,
            "message": self.errors[0] if self.errors else None,
            "errors": self.errors,
            "warnings": self.warnings
        }
        
        if self.config:
            result["config"] = self.config.dict()
        
        return result


class ValidationService:
    """
    Strict validation service for FIBO configurations.
    
    SAFETY GUARANTEES:
    - All configurations are validated against strict Pydantic schemas
    - No additional properties allowed (extra="forbid")
    - All enums strictly enforced with no partial matches
    - Numeric ranges validated with precise bounds
    - Cross-field dependencies validated
    - Business logic rules applied
    - Generation blocked if ANY validation fails
    """
    
    async def validate_generation_request(self, request: GenerationRequest) -> AssetConfig:
        """
        Validate complete generation request with strict safety checks.
        
        Args:
            request: Generation request to validate
            
        Returns:
            Validated AssetConfig instance
            
        Raises:
            ValidationError: If ANY validation fails
            SchemaValidationError: If schema validation fails
        """
        try:
            logger.info("Validating generation request", asset_type=request.asset_type)
            
            # Validate request structure
            if not request.asset_type:
                raise ValidationError("Asset type is required")
            
            # Validate asset type enum
            valid_types = [AssetType.NPC_PORTRAIT, AssetType.WEAPON_ITEM, AssetType.ENVIRONMENT_CONCEPT]
            if request.asset_type not in valid_types:
                raise ValidationError(
                    f"Invalid asset type: {request.asset_type}. "
                    f"Must be one of: {', '.join(valid_types)}"
                )
            
            # Convert parameters to dict for validation
            if hasattr(request.parameters, 'dict'):
                params_dict = request.parameters.dict()
            else:
                params_dict = dict(request.parameters)
            
            # Ensure asset type matches
            params_dict['assetType'] = request.asset_type
            
            # Strict schema validation
            validation_result = self.validate_config_strict(params_dict)
            
            if not validation_result.success:
                error_msg = "; ".join(validation_result.errors)
                logger.error("Schema validation failed", errors=validation_result.errors)
                raise SchemaValidationError(
                    f"Schema validation failed: {error_msg}",
                    schema_type=request.asset_type,
                    validation_errors=validation_result.errors
                )
            
            # Log warnings but don't block generation
            if validation_result.warnings:
                logger.warning("Validation warnings", warnings=validation_result.warnings)
            
            logger.info("Generation request validated successfully", asset_type=request.asset_type)
            return validation_result.config
            
        except (ValidationError, SchemaValidationError):
            raise
        except Exception as e:
            logger.error("Unexpected validation error", error=str(e))
            raise ValidationError(f"Validation failed: {str(e)}")
    
    def validate_config_strict(self, config_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate FIBO configuration with strict safety checks.
        
        Args:
            config_data: Raw configuration dictionary
            
        Returns:
            ValidationResult with success status, validated config, and any errors
        """
        try:
            # Validate required fields first
            if not isinstance(config_data, dict):
                return ValidationResult(
                    success=False,
                    errors=["Configuration must be a JSON object"]
                )
            
            # Check asset type (STRICT)
            asset_type = config_data.get('assetType')
            if not asset_type:
                return ValidationResult(
                    success=False,
                    errors=["Missing required field: assetType"]
                )
            
            # Validate schema version (STRICT)
            schema_version = config_data.get('schemaVersion', 'v1')
            if schema_version != 'v1':
                return ValidationResult(
                    success=False,
                    errors=[f"Unsupported schema version: {schema_version}. Only 'v1' is supported."]
                )
            
            # Validate using strict Pydantic schemas
            validated_config = validate_asset_config(config_data)
            
            # Additional business logic validation
            warnings = self._validate_business_rules(validated_config)
            
            logger.info("Configuration validated successfully", asset_type=asset_type)
            
            return ValidationResult(
                success=True,
                config=validated_config,
                warnings=warnings
            )
            
        except FiboValidationError as e:
            logger.error("FIBO validation error", error=str(e))
            return ValidationResult(
                success=False,
                errors=[str(e)]
            )
            
        except PydanticValidationError as e:
            logger.error("Pydantic validation error", errors=e.errors())
            errors = []
            for error in e.errors():
                field_path = " -> ".join(str(loc) for loc in error['loc'])
                
                # Enhanced error messages for common issues
                if error['type'] == 'value_error.extra':
                    error_msg = f"Additional property not allowed: {field_path}"
                elif error['type'] == 'value_error.const':
                    error_msg = f"{field_path}: Value must be exactly '{error.get('ctx', {}).get('given')}'"
                elif error['type'] == 'value_error.number.not_ge':
                    limit = error.get('ctx', {}).get('limit_value')
                    error_msg = f"{field_path}: Value must be >= {limit}"
                elif error['type'] == 'value_error.number.not_le':
                    limit = error.get('ctx', {}).get('limit_value')
                    error_msg = f"{field_path}: Value must be <= {limit}"
                elif error['type'] == 'type_error.enum':
                    permitted = error.get('ctx', {}).get('enum_values', [])
                    error_msg = f"{field_path}: Must be one of {permitted}"
                else:
                    error_msg = f"{field_path}: {error['msg']}"
                
                errors.append(error_msg)
            
            return ValidationResult(
                success=False,
                errors=errors
            )
            
        except Exception as e:
            logger.error("Unexpected validation error", error=str(e))
            return ValidationResult(
                success=False,
                errors=[f"Validation failed: {str(e)}"]
            )
    
    def _validate_business_rules(self, config: AssetConfig) -> List[str]:
        """
        Apply business logic validation rules.
        
        Args:
            config: Validated configuration
            
        Returns:
            List of warning messages
        """
        warnings = []
        
        if isinstance(config, NPCPortraitConfig):
            warnings.extend(self._validate_npc_rules(config))
        elif isinstance(config, WeaponItemConfig):
            warnings.extend(self._validate_weapon_rules(config))
        elif isinstance(config, EnvironmentConfig):
            warnings.extend(self._validate_environment_rules(config))
        
        return warnings
    
    def _validate_npc_rules(self, config: NPCPortraitConfig) -> List[str]:
        """Validate NPC-specific business rules."""
        warnings = []
        
        # Age and facial hair compatibility
        if (config.identity.ageRange == "young" and 
            config.facialFeatures.facialHair in ["beard", "full"]):
            warnings.append("Young characters rarely have full beards")
        
        # Extreme feature combinations
        if (config.facialFeatures.jawWidth > 0.9 and 
            config.facialFeatures.cheekboneHeight < 0.2):
            warnings.append("Very wide jaw with low cheekbones may look unnatural")
        
        # FOV and distance compatibility  
        if config.camera.fov < 40 and config.camera.distance == "close":
            warnings.append("Wide angle lens with close distance may distort facial features")
        
        # Head tilt extremes
        if abs(config.camera.headTilt) > 0.2:
            warnings.append("Extreme head tilt may cause composition issues")
        
        # Expression intensity validation
        if (config.expression.emotion == "neutral" and config.expression.intensity > 0.7):
            warnings.append("High intensity with neutral emotion may look unnatural")
        
        return warnings
    
    def _validate_weapon_rules(self, config: WeaponItemConfig) -> List[str]:
        """Validate weapon-specific business rules."""
        warnings = []
        
        # Rarity and ornamentation consistency (STRICT BUSINESS RULE)
        rarity_ornamentation_min = {
            "common": 0.0,
            "uncommon": 0.2,
            "rare": 0.4,
            "epic": 0.6,
            "legendary": 0.8,
            "artifact": 0.8,
            "unique": 0.7
        }
        
        min_ornamentation = rarity_ornamentation_min.get(config.item.rarity, 0.0)
        if config.form.ornamentation < min_ornamentation:
            warnings.append(
                f"{config.item.rarity.title()} items typically have ornamentation >= {min_ornamentation}"
            )
        
        # Material and glow compatibility
        if (config.item.material == "wood" and config.surface.emissiveGlow > 0.5):
            warnings.append("High emissive glow on wood materials may need magical justification")
        
        # Material and patina compatibility (already enforced in schema)
        if (config.item.material == "crystal" and config.surface.patina in ["rust", "verdigris"]):
            warnings.append("Crystal materials don't typically have metallic patina")
        
        # Camera mode and background compatibility
        if (config.camera.mode == "flat_icon" and 
            config.background.type in ["radial_glow", "gradient"]):
            warnings.append("Flat icon mode works best with transparent or solid backgrounds")
        
        # Rarity and glow consistency
        rarity_glow_max = {
            "common": 0.2,
            "uncommon": 0.4,
            "rare": 0.6,
            "epic": 0.8,
            "legendary": 1.0,
            "artifact": 1.0,
            "unique": 0.9
        }
        
        max_glow = rarity_glow_max.get(config.item.rarity, 0.2)
        if config.surface.emissiveGlow > max_glow:
            warnings.append(
                f"{config.item.rarity.title()} items rarely have emissive glow > {max_glow}"
            )
        
        return warnings
    
    def _validate_environment_rules(self, config: EnvironmentConfig) -> List[str]:
        """Validate environment-specific business rules."""
        warnings = []
        
        # God rays require atmospheric particles
        if config.lighting.godRays > 0.5 and config.atmosphere.fogDensity < 0.2:
            warnings.append("God rays are most visible with atmospheric fog or particles")
        
        # Scale and camera height compatibility
        if (config.scene.scale == "epic" and 
            config.composition.cameraHeight == "ground"):
            warnings.append("Epic scale scenes work better with elevated camera positions")
        
        # Time and lighting compatibility
        if (config.atmosphere.timeOfDay == "night" and 
            config.lighting.lightStyle == "natural"):
            warnings.append("Natural lighting at night may be very dark")
        
        # Biome and weather validation (enforced in schema, but warn for edge cases)
        if (config.scene.biome == "desert" and config.atmosphere.weather == "foggy"):
            warnings.append("Fog is unusual in desert biomes")
        
        # Horizon position rule of thirds
        horizon = config.composition.horizonPosition
        if not (0.28 <= horizon <= 0.38 or 0.62 <= horizon <= 0.72):
            warnings.append("Consider placing horizon at rule of thirds (33% or 66%) for dynamic composition")
        
        # Visibility and fog density correlation
        if (config.atmosphere.fogDensity > 0.7 and config.atmosphere.visibility > 0.5):
            warnings.append("High fog density typically reduces visibility")
        
        return warnings
    
    async def validate_batch_variant(
        self,
        base_parameters: AssetConfig,
        variant: BatchVariant,
        asset_type: str,
    ) -> Dict[str, Any]:
        """
        Validate batch variant with strict safety checks.
        
        Args:
            base_parameters: Base configuration
            variant: Variant overrides
            asset_type: Asset type being generated
            
        Returns:
            Validated variant parameters
            
        Raises:
            ValidationError: If variant validation fails
        """
        try:
            # Apply variant overrides to base parameters
            merged_params = await self.apply_parameter_overrides(
                base_parameters=base_parameters,
                overrides=variant.parameters,
                asset_type=asset_type,
            )
            
            # Validate the merged parameters using strict validation
            if hasattr(merged_params, 'dict'):
                params_dict = merged_params.dict()
            else:
                params_dict = dict(merged_params)
            
            validation_result = self.validate_config_strict(params_dict)
            
            if not validation_result.success:
                variant_name = variant.name or "unnamed"
                error_msg = "; ".join(validation_result.errors)
                raise ValidationError(f"Variant '{variant_name}' validation failed: {error_msg}")
            
            return validation_result.config.dict()
            
        except ValidationError:
            raise
        except Exception as e:
            variant_name = variant.name or "unnamed"
            raise ValidationError(f"Variant '{variant_name}' validation failed: {str(e)}")
    
    async def apply_parameter_overrides(
        self,
        base_parameters: Union[AssetConfig, Dict[str, Any]],
        overrides: Dict[str, Any],
        asset_type: str,
    ) -> AssetConfig:
        """
        Apply parameter overrides with strict validation.
        
        Args:
            base_parameters: Base configuration
            overrides: Parameter overrides to apply
            asset_type: Asset type for validation
            
        Returns:
            Updated configuration with overrides applied
            
        Raises:
            ValidationError: If overrides are invalid
        """
        try:
            # Convert to dict if needed
            if hasattr(base_parameters, 'dict'):
                base_dict = base_parameters.dict()
            else:
                base_dict = dict(base_parameters)
            
            # Apply overrides recursively
            merged_dict = self._deep_merge_dicts(base_dict, overrides)
            
            # Ensure asset type is correct
            merged_dict['assetType'] = asset_type
            
            # Validate merged configuration
            validated_config = validate_asset_config(merged_dict)
            return validated_config
                
        except FiboValidationError as e:
            raise ValidationError(f"Parameter override validation failed: {str(e)}")
        except PydanticValidationError as e:
            logger.error("Override validation failed", errors=e.errors())
            raise ValidationError(f"Parameter override validation failed: {e}")
        except Exception as e:
            logger.error("Error applying overrides", error=str(e))
            raise ValidationError(f"Failed to apply parameter overrides: {str(e)}")
    
    def _deep_merge_dicts(self, base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two dictionaries, with overrides taking precedence.
        
        Args:
            base: Base dictionary
            overrides: Override dictionary
            
        Returns:
            Merged dictionary
        """
        result = base.copy()
        
        for key, value in overrides.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge_dicts(result[key], value)
            else:
                result[key] = value
        
        return result
    
    async def validate_seed(self, seed: int) -> int:
        """
        Validate random seed with strict bounds.
        
        Args:
            seed: Seed value to validate
            
        Returns:
            Validated seed value
            
        Raises:
            ValidationError: If seed is invalid
        """
        if not isinstance(seed, int):
            raise ValidationError("Seed must be an integer")
        
        if seed < 1 or seed > 999999999:
            raise ValidationError("Seed must be between 1 and 999,999,999")
        
        return seed
    
    def get_validation_schema(self, asset_type: str) -> Optional[Dict[str, Any]]:
        """
        Get JSON schema for asset type.
        
        Args:
            asset_type: Asset type identifier
            
        Returns:
            JSON schema dictionary or None if invalid
        """
        try:
            if asset_type == AssetType.NPC_PORTRAIT:
                return NPCPortraitConfig.schema()
            elif asset_type == AssetType.WEAPON_ITEM:
                return WeaponItemConfig.schema()
            elif asset_type == AssetType.ENVIRONMENT_CONCEPT:
                return EnvironmentConfig.schema()
            else:
                return None
        except Exception as e:
            logger.error("Failed to get schema", asset_type=asset_type, error=str(e))
            return None
    
    def get_default_configuration(self, asset_type: str) -> Optional[Dict[str, Any]]:
        """
        Get default configuration for asset type.
        
        Args:
            asset_type: Asset type identifier
            
        Returns:
            Default configuration dictionary or None if invalid
        """
        try:
            if asset_type == AssetType.NPC_PORTRAIT:
                config = get_default_config(AssetType.NPC_PORTRAIT)
            elif asset_type == AssetType.WEAPON_ITEM:
                config = get_default_config(AssetType.WEAPON_ITEM)
            elif asset_type == AssetType.ENVIRONMENT_CONCEPT:
                config = get_default_config(AssetType.ENVIRONMENT_CONCEPT)
            else:
                return None
            
            return config.dict()
            
        except Exception as e:
            logger.error("Failed to get default config", asset_type=asset_type, error=str(e))
            return None