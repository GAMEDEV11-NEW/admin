import logging
import psutil
import platform
from datetime import datetime
from typing import Dict, Any
from app.schemas.health import DetailedHealthResponse, SystemInfo

logger = logging.getLogger(__name__)


class HealthService:
    """Health monitoring service"""
    
    async def get_detailed_health(self) -> DetailedHealthResponse:
        """Get detailed system health information"""
        try:
            system_info = await self._get_system_info()
            
            return DetailedHealthResponse(
                status="healthy",
                timestamp=datetime.utcnow(),
                system_info=system_info,
                services={
                    "database": await self._check_database_health(),
                    "external_api": await self._check_external_api_health(),
                    "memory": await self._check_memory_health(),
                    "disk": await self._check_disk_health()
                }
            )
        except Exception as e:
            logger.error(f"Error getting detailed health: {e}")
            raise
    
    async def _get_system_info(self) -> SystemInfo:
        """Get system information"""
        return SystemInfo(
            platform=platform.system(),
            platform_version=platform.version(),
            python_version=platform.python_version(),
            cpu_count=psutil.cpu_count(),
            memory_total=psutil.virtual_memory().total,
            uptime=psutil.boot_time()
        )
    
    async def _check_database_health(self) -> Dict[str, Any]:
        """Check database health"""
        try:
            # This would typically check actual database connectivity
            # For now, we'll simulate a healthy database
            return {
                "status": "healthy",
                "response_time": 0.001,
                "connections": 5
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def _check_external_api_health(self) -> Dict[str, Any]:
        """Check external API health"""
        try:
            # This would typically make a request to external APIs
            # For now, we'll simulate a healthy external API
            return {
                "status": "healthy",
                "response_time": 0.05,
                "endpoints": ["/api/v1/users"]
            }
        except Exception as e:
            logger.error(f"External API health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def _check_memory_health(self) -> Dict[str, Any]:
        """Check memory health"""
        try:
            memory = psutil.virtual_memory()
            return {
                "status": "healthy" if memory.percent < 90 else "warning",
                "usage_percent": memory.percent,
                "available": memory.available,
                "total": memory.total
            }
        except Exception as e:
            logger.error(f"Memory health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def _check_disk_health(self) -> Dict[str, Any]:
        """Check disk health"""
        try:
            disk = psutil.disk_usage('/')
            return {
                "status": "healthy" if disk.percent < 90 else "warning",
                "usage_percent": disk.percent,
                "free": disk.free,
                "total": disk.total
            }
        except Exception as e:
            logger.error(f"Disk health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            } 