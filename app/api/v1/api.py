from fastapi import APIRouter
from app.api.v1.endpoints import users, health, contests, otp, league_joins

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(contests.router, prefix="/contests", tags=["contests"])
api_router.include_router(otp.router, prefix="/otp", tags=["otp"])
api_router.include_router(league_joins.router, prefix="/league-joins", tags=["league_joins"]) 