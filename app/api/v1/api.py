from fastapi import APIRouter
from app.api.v1.endpoints import users, items, health, sessions, games

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(games.router, prefix="/games", tags=["games"]) 