"""
Database configuration and session management.
SQLAlchemy setup with async support and proper connection handling.
"""

from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

# Create declarative base for models
Base = declarative_base()

# Global variables for database engines and sessions
engine = None
async_engine = None
SessionLocal = None
AsyncSessionLocal = None


def init_sync_db() -> None:
    """Initialize synchronous database engine and session."""
    global engine, SessionLocal
    
    settings = get_settings()
    
    engine = create_engine(
        settings.database_url_sync,
        connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
        echo=settings.DEBUG,
    )
    
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )


async def init_async_db() -> None:
    """Initialize asynchronous database engine and session."""
    global async_engine, AsyncSessionLocal
    
    settings = get_settings()
    
    # Convert sync URL to async for SQLite
    async_url = settings.DATABASE_URL
    if async_url.startswith("sqlite:///"):
        async_url = async_url.replace("sqlite:///", "sqlite+aiosqlite:///")
    
    async_engine = create_async_engine(
        async_url,
        echo=settings.DEBUG,
    )
    
    AsyncSessionLocal = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def init_db() -> None:
    """Initialize database and create tables."""
    # Initialize both sync and async engines
    init_sync_db()
    await init_async_db()
    
    # Import models to ensure they're registered
    from app.models.asset import Asset, AssetMetadata, GenerationHistory
    
    # Create tables
    if async_engine:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session with proper cleanup."""
    if not AsyncSessionLocal:
        await init_async_db()
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_sync_session():
    """Get synchronous database session with proper cleanup."""
    if not SessionLocal:
        init_sync_db()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def close_db() -> None:
    """Close database connections."""
    global engine, async_engine
    
    if async_engine:
        await async_engine.dispose()
    
    if engine:
        engine.dispose()