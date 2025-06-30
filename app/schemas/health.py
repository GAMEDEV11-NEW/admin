from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime


class HealthResponse(BaseModel):
    """Basic health response schema"""
    status: str = Field(..., description="Health status")


class SystemInfo(BaseModel):
    """System information schema"""
    platform: str = Field(..., description="Operating system platform")
    platform_version: str = Field(..., description="Platform version")
    python_version: str = Field(..., description="Python version")
    cpu_count: int = Field(..., description="Number of CPU cores")
    memory_total: int = Field(..., description="Total memory in bytes")
    uptime: float = Field(..., description="System uptime in seconds")


class DetailedHealthResponse(BaseModel):
    """Detailed health response schema"""
    status: str = Field(..., description="Overall health status")
    timestamp: datetime = Field(..., description="Health check timestamp")
    system_info: SystemInfo = Field(..., description="System information")
    services: Dict[str, Any] = Field(..., description="Individual service health status") 