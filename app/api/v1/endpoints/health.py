from fastapi import APIRouter, Depends
from app.services.health_service import HealthService
from app.schemas.health import HealthResponse, DetailedHealthResponse

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint"""
    return HealthResponse(status="healthy")


@router.get("/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check(
    health_service: HealthService = Depends(HealthService)
):
    """Detailed health check with system information"""
    return await health_service.get_detailed_health() 