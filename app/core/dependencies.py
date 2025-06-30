from app.services.user_service import UserService
from app.services.item_service import ItemService
from app.services.health_service import HealthService
from app.services.session_service import SessionService
from app.services.game_service import GameService


def get_user_service() -> UserService:
    """Dependency to get UserService instance"""
    return UserService()


def get_item_service() -> ItemService:
    """Dependency to get ItemService instance"""
    return ItemService()


def get_health_service() -> HealthService:
    """Dependency to get HealthService instance"""
    return HealthService()


def get_session_service() -> SessionService:
    """Dependency to get SessionService instance"""
    return SessionService()


def get_game_service() -> GameService:
    """Dependency to get GameService instance"""
    return GameService() 