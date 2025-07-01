import logging
from typing import List, Optional
from app.schemas.league_join import LeagueJoinCreate, LeagueJoinResponse, LeagueJoinUpdate
from app.repositories.league_join_repository import LeagueJoinRepository

logger = logging.getLogger(__name__)


class LeagueJoinService:
    """League join business logic service"""
    
    def __init__(self):
        self.league_join_repository = LeagueJoinRepository()
    
    async def get_league_joins(self, limit: int = 100) -> List[LeagueJoinResponse]:
        """Get all league joins with pagination"""
        try:
            joins = await self.league_join_repository.get_all_league_joins(limit=limit)
            return [LeagueJoinResponse(**join) for join in joins]
        except Exception as e:
            logger.error(f"Error getting league joins: {e}")
            raise
    
    async def get_league_joins_by_league_id(self, league_id: str, limit: int = 50) -> List[LeagueJoinResponse]:
        """Get all joins for a specific league"""
        try:
            joins = await self.league_join_repository.get_league_joins_by_league_id(league_id, limit=limit)
            return [LeagueJoinResponse(**join) for join in joins]
        except Exception as e:
            logger.error(f"Error getting league joins for league {league_id}: {e}")
            raise
    
    async def get_league_joins_by_status(self, league_id: str, status: str, limit: int = 50) -> List[LeagueJoinResponse]:
        """Get league joins by status for a specific league"""
        try:
            joins = await self.league_join_repository.get_league_joins_by_status(league_id, status, limit=limit)
            return [LeagueJoinResponse(**join) for join in joins]
        except Exception as e:
            logger.error(f"Error getting league joins by status {status} for league {league_id}: {e}")
            raise
    
    async def get_user_league_joins(self, user_id: str, limit: int = 50) -> List[LeagueJoinResponse]:
        """Get all league joins for a specific user"""
        try:
            joins = await self.league_join_repository.get_user_league_joins(user_id, limit=limit)
            return [LeagueJoinResponse(**join) for join in joins]
        except Exception as e:
            logger.error(f"Error getting league joins for user {user_id}: {e}")
            raise
    
    async def get_league_joins_by_invite_code(self, invite_code: str, limit: int = 50) -> List[LeagueJoinResponse]:
        """Get league joins by invite code"""
        try:
            joins = await self.league_join_repository.get_league_joins_by_invite_code(invite_code, limit=limit)
            return [LeagueJoinResponse(**join) for join in joins]
        except Exception as e:
            logger.error(f"Error getting league joins by invite code {invite_code}: {e}")
            raise
    
    async def get_league_join_by_user_and_league(self, user_id: str, league_id: str) -> Optional[LeagueJoinResponse]:
        """Get specific league join by user and league"""
        try:
            join = await self.league_join_repository.get_league_join_by_user_and_league(user_id, league_id)
            if join:
                return LeagueJoinResponse(**join)
            return None
        except Exception as e:
            logger.error(f"Error getting league join for user {user_id} in league {league_id}: {e}")
            raise
    
    async def create_league_join(self, join_data: LeagueJoinCreate) -> LeagueJoinResponse:
        """Create a new league join"""
        try:
            # Business logic validation
            if not join_data.league_id.strip():
                raise ValueError("League ID cannot be empty")
            
            if not join_data.user_id.strip():
                raise ValueError("User ID cannot be empty")
            
            if not join_data.status.strip():
                raise ValueError("Status cannot be empty")
            
            valid_statuses = ["pending", "active", "inactive", "banned", "left"]
            if join_data.status not in valid_statuses:
                raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
            
            valid_roles = ["member", "admin", "moderator", "owner"]
            if join_data.role and join_data.role not in valid_roles:
                raise ValueError(f"Role must be one of: {', '.join(valid_roles)}")
            
            # Check if user is already in this league
            existing_join = await self.league_join_repository.get_league_join_by_user_and_league(
                join_data.user_id, join_data.league_id
            )
            if existing_join:
                raise ValueError(f"User {join_data.user_id} is already in league {join_data.league_id}")
            
            join = await self.league_join_repository.create_league_join(join_data)
            logger.info(f"Created league join for user {join_data.user_id} in league {join_data.league_id}")
            return LeagueJoinResponse(**join)
        except Exception as e:
            logger.error(f"Error creating league join: {e}")
            raise
    
    async def update_league_join(self, league_id: str, status: str, user_id: str, joined_at: str, join_data: LeagueJoinUpdate) -> Optional[LeagueJoinResponse]:
        """Update an existing league join"""
        try:
            join = await self.league_join_repository.get_league_join_by_user_and_league(user_id, league_id)
            if not join:
                return None
            
            # Business logic validation
            if join_data.status is not None:
                valid_statuses = ["pending", "active", "inactive", "banned", "left"]
                if join_data.status not in valid_statuses:
                    raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
            
            if join_data.role is not None:
                valid_roles = ["member", "admin", "moderator", "owner"]
                if join_data.role not in valid_roles:
                    raise ValueError(f"Role must be one of: {', '.join(valid_roles)}")
            
            updated_join = await self.league_join_repository.update_league_join(league_id, status, user_id, joined_at, join_data)
            if updated_join:
                logger.info(f"Updated league join for user {user_id} in league {league_id}")
                return LeagueJoinResponse(**updated_join)
            return None
        except Exception as e:
            logger.error(f"Error updating league join: {e}")
            raise
    
    async def delete_league_join(self, league_id: str, status: str, user_id: str, joined_at: str) -> bool:
        """Delete a league join"""
        try:
            success = await self.league_join_repository.delete_league_join(league_id, status, user_id, joined_at)
            if success:
                logger.info(f"Deleted league join for user {user_id} in league {league_id}")
            return success
        except Exception as e:
            logger.error(f"Error deleting league join: {e}")
            raise
    
    async def update_join_status(self, league_id: str, user_id: str, new_status: str, status_id: str = None) -> Optional[LeagueJoinResponse]:
        """Update the status of a league join"""
        try:
            # Business logic validation
            valid_statuses = ["pending", "active", "inactive", "banned", "left"]
            if new_status not in valid_statuses:
                raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
            
            join = await self.league_join_repository.update_join_status(league_id, user_id, new_status, status_id)
            if join:
                logger.info(f"Updated join status to {new_status} for user {user_id} in league {league_id}")
                return LeagueJoinResponse(**join)
            return None
        except Exception as e:
            logger.error(f"Error updating join status for user {user_id} in league {league_id}: {e}")
            raise
    
    async def get_league_member_count(self, league_id: str, status: str = "active") -> int:
        """Get the count of members in a league with specific status"""
        try:
            count = await self.league_join_repository.get_league_member_count(league_id, status)
            logger.info(f"League {league_id} has {count} members with status {status}")
            return count
        except Exception as e:
            logger.error(f"Error getting member count for league {league_id}: {e}")
            raise 