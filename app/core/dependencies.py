from app.services.user_service import UserService
from app.services.health_service import HealthService
from app.services.session_service import SessionService
from app.services.game_service import GameService
from app.services.contest_service import ContestService
from app.services.otp_service import OTPService
from app.services.league_join_service import LeagueJoinService


def get_user_service() -> UserService:
    """Dependency to get UserService instance"""
    return UserService()



def get_health_service() -> HealthService:
    """Dependency to get HealthService instance"""
    return HealthService()


def get_session_service() -> SessionService:
    """Dependency to get SessionService instance"""
    return SessionService()


def get_game_service() -> GameService:
    """Dependency to get GameService instance"""
    return GameService()


def get_contest_service() -> ContestService:
    """Dependency to get ContestService instance"""
    return ContestService()


def get_otp_service() -> OTPService:
    """Dependency to get OTPService instance"""
    return OTPService()


def get_league_join_service() -> LeagueJoinService:
    """Dependency to get LeagueJoinService instance"""
    return LeagueJoinService() 