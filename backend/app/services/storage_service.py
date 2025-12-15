"""
Storage service for managing asset files.
Mock implementation for development.
"""

from typing import Dict


class StorageService:
    """Service for managing asset storage."""
    
    async def get_storage_info(self) -> Dict:
        """Get storage information (mock implementation)."""
        return {
            "type": "local",
            "available_space": "10GB",
            "used_space": "1GB"
        }