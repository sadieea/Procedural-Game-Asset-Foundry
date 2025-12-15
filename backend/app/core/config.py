"""
Application configuration management using Pydantic Settings.
Handles environment variables, validation, and default values.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    # Application Settings
    APP_NAME: str = "Procedural Game Asset Foundry"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./assets.db"
    
    # Storage Configuration
    STORAGE_TYPE: Literal["local", "s3"] = "local"
    STORAGE_PATH: str = "./storage/assets"
    
    # S3 Configuration
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "game-assets"
    
    # FIBO Model Configuration
    FIBO_MODE: Literal["local", "mock"] = "mock"
    FIBO_COMFYUI_URL: str = "http://127.0.0.1:8188"
    FIBO_WORKFLOW_PATH: str = "./fibo/workflows"
    FIBO_API_KEY: str = ""
    
    # Generation Limits
    MAX_BATCH_SIZE: int = Field(default=10, ge=1, le=50)
    GENERATION_TIMEOUT_SECONDS: int = Field(default=300, ge=30, le=600)
    MAX_CONCURRENT_GENERATIONS: int = Field(default=3, ge=1, le=10)
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.DEBUG
    
    @property
    def database_url_sync(self) -> str:
        """Get synchronous database URL for SQLAlchemy."""
        if self.DATABASE_URL.startswith("sqlite"):
            return self.DATABASE_URL
        # Convert async postgres URL to sync
        return self.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()