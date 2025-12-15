"""
Custom exception classes for the asset generation system.
Provides structured error handling with proper context.
"""

from typing import Any, Dict, Optional


class AssetFoundryError(Exception):
    """Base exception for all asset foundry errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ValidationError(AssetFoundryError):
    """Raised when input validation fails."""
    
    def __init__(
        self, 
        message: str, 
        field: Optional[str] = None, 
        value: Optional[Any] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, details)
        self.field = field
        self.value = value


class SchemaValidationError(ValidationError):
    """Raised when JSON schema validation fails."""
    
    def __init__(
        self, 
        message: str, 
        schema_type: str,
        validation_errors: Optional[list] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, details=details)
        self.schema_type = schema_type
        self.validation_errors = validation_errors or []


class AssetGenerationError(AssetFoundryError):
    """Raised when asset generation fails."""
    
    def __init__(
        self, 
        message: str, 
        asset_type: Optional[str] = None,
        generation_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, details)
        self.asset_type = asset_type
        self.generation_id = generation_id


class FiboModelError(AssetGenerationError):
    """Raised when FIBO model inference fails."""
    
    def __init__(
        self, 
        message: str, 
        model_type: Optional[str] = None,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, details=details)
        self.model_type = model_type
        self.error_code = error_code


class StorageError(AssetFoundryError):
    """Raised when asset storage operations fail."""
    
    def __init__(
        self, 
        message: str, 
        storage_type: Optional[str] = None,
        asset_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, details)
        self.storage_type = storage_type
        self.asset_id = asset_id


class DatabaseError(AssetFoundryError):
    """Raised when database operations fail."""
    
    def __init__(
        self, 
        message: str, 
        operation: Optional[str] = None,
        table: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, details)
        self.operation = operation
        self.table = table


class RateLimitError(AssetFoundryError):
    """Raised when rate limits are exceeded."""
    
    def __init__(
        self, 
        message: str, 
        limit_type: Optional[str] = None,
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, details)
        self.limit_type = limit_type
        self.retry_after = retry_after


class ConfigurationError(AssetFoundryError):
    """Raised when configuration is invalid or missing."""
    
    def __init__(
        self, 
        message: str, 
        config_key: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, details)
        self.config_key = config_key


class GenerationError(AssetFoundryError):
    """Raised when image generation fails."""
    
    def __init__(
        self, 
        message: str, 
        asset_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, details)
        self.asset_type = asset_type