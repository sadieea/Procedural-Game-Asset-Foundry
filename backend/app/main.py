"""
Main FastAPI application entry point.
Production-grade setup with proper middleware, error handling, and monitoring.
"""

import logging
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import api_router
from app.core.config import get_settings
from app.core.database import init_db
from app.core.exceptions import AssetGenerationError, ValidationError
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    logger = structlog.get_logger()
    logger.info("Starting Procedural Game Asset Foundry Backend")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Procedural Game Asset Foundry Backend")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    
    # Setup structured logging
    setup_logging(settings.LOG_LEVEL, settings.DEBUG)
    
    app = FastAPI(
        title="Procedural Game Asset Foundry API",
        description="Production-grade JSON-native asset generation for game developers",
        version="0.1.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )
    
    # Add middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next) -> Response:
        start_time = time.time()
        
        logger = structlog.get_logger()
        logger.info(
            "Request started",
            method=request.method,
            url=str(request.url),
            client_ip=request.client.host if request.client else None,
        )
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(
            "Request completed",
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            process_time=f"{process_time:.3f}s",
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response
    
    # Add global exception handlers
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "validation_error",
                "message": str(exc),
                "details": exc.details if hasattr(exc, 'details') else None,
            },
        )
    
    @app.exception_handler(AssetGenerationError)
    async def generation_exception_handler(request: Request, exc: AssetGenerationError):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "generation_error",
                "message": str(exc),
                "asset_type": exc.asset_type if hasattr(exc, 'asset_type') else None,
            },
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger = structlog.get_logger()
        logger.error(
            "Unhandled exception",
            exception=str(exc),
            exception_type=type(exc).__name__,
            url=str(request.url),
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "internal_server_error",
                "message": "An unexpected error occurred",
            },
        )
    
    # Include API routes
    app.include_router(api_router, prefix="/api")
    
    # Mount static files for generated assets
    import os
    from pathlib import Path
    
    # Resolve storage path relative to backend directory
    backend_dir = Path(__file__).parent.parent
    storage_path = backend_dir / settings.STORAGE_PATH
    
    # Ensure storage directory exists
    storage_path.mkdir(parents=True, exist_ok=True)
    
    logger = structlog.get_logger()
    logger.info("Mounting static files", storage_path=str(storage_path))
    
    if storage_path.exists():
        app.mount("/storage", StaticFiles(directory=str(storage_path)), name="storage")
        logger.info("Static files mounted successfully")
    else:
        logger.warning("Storage path does not exist", path=str(storage_path))
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint for monitoring."""
        return {
            "status": "healthy",
            "service": "procedural-game-asset-foundry",
            "version": "0.1.0",
            "timestamp": time.time(),
        }
    
    return app


# Create the application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower(),
    )