import logging
from typing import List, Optional
from datetime import datetime
from uuid import uuid4
from cassandra.cluster import Session
from app.schemas.league_join import LeagueJoinCreate, LeagueJoinUpdate
from app.core.database import get_cassandra_session

logger = logging.getLogger(__name__)


class LeagueJoinRepository:
    """League join data access repository for Cassandra"""
    
    def __init__(self):
        self.session: Session = get_cassandra_session()
    
    def _row_to_dict(self, row) -> dict:
        """Convert Cassandra row to dictionary"""
        if row is None:
            return None
        return {column: getattr(row, column) for column in row._fields}
    
    async def get_all_league_joins(self, limit: int = 100) -> List[dict]:
        """Get all league joins with pagination"""
        try:
            query = "SELECT * FROM league_joins LIMIT %s"
            rows = self.session.execute(query, (limit,))
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all league joins: {e}")
            raise
    
    async def get_league_joins_by_league_id(self, league_id: str, limit: int = 50) -> List[dict]:
        """Get all joins for a specific league"""
        try:
            query = "SELECT * FROM league_joins WHERE league_id = %s LIMIT %s"
            rows = self.session.execute(query, (league_id, limit))
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting league joins for league {league_id}: {e}")
            raise
    
    async def get_league_joins_by_status(self, league_id: str, status: str, limit: int = 50) -> List[dict]:
        """Get league joins by status for a specific league"""
        try:
            query = "SELECT * FROM league_joins WHERE league_id = %s AND status = %s LIMIT %s"
            rows = self.session.execute(query, (league_id, status, limit))
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting league joins by status {status} for league {league_id}: {e}")
            raise
    
    async def get_user_league_joins(self, user_id: str, limit: int = 50) -> List[dict]:
        """Get all league joins for a specific user"""
        try:
            query = "SELECT * FROM league_joins WHERE user_id = %s LIMIT %s"
            rows = self.session.execute(query, (user_id, limit))
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting league joins for user {user_id}: {e}")
            raise
    
    async def get_league_join_by_user_and_league(self, user_id: str, league_id: str) -> Optional[dict]:
        """Get specific league join by user and league"""
        try:
            query = "SELECT * FROM league_joins WHERE league_id = %s AND user_id = %s LIMIT 1"
            row = self.session.execute(query, (league_id, user_id)).one()
            return self._row_to_dict(row)
        except Exception as e:
            logger.error(f"Error getting league join for user {user_id} in league {league_id}: {e}")
            raise
    
    async def get_league_joins_by_invite_code(self, invite_code: str, limit: int = 50) -> List[dict]:
        """Get league joins by invite code"""
        try:
            query = "SELECT * FROM league_joins WHERE invite_code = %s LIMIT %s"
            rows = self.session.execute(query, (invite_code, limit))
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting league joins by invite code {invite_code}: {e}")
            raise
    
    async def create_league_join(self, join_data: LeagueJoinCreate) -> dict:
        """Create a new league join"""
        try:
            now = datetime.utcnow()
            join_id = uuid4()
            
            query = """
                INSERT INTO league_joins (
                    league_id, status, user_id, id, joined_at, updated_at,
                    invite_code, role, extra_data
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.session.execute(query, (
                join_data.league_id,
                join_data.status,
                join_data.user_id,
                join_id,
                now.isoformat(),
                now.isoformat(),
                join_data.invite_code,
                join_data.role,
                join_data.extra_data
            ))
            
            # Return the created league join
            return {
                "league_id": join_data.league_id,
                "status": join_data.status,
                "user_id": join_data.user_id,
                "id": join_id,
                "joined_at": now.isoformat(),
                "updated_at": now.isoformat(),
                "invite_code": join_data.invite_code,
                "role": join_data.role,
                "extra_data": join_data.extra_data
            }
        except Exception as e:
            logger.error(f"Error creating league join: {e}")
            raise
    
    async def update_league_join(self, league_id: str, status: str, user_id: str, joined_at: str, join_data: LeagueJoinUpdate) -> Optional[dict]:
        """Update an existing league join"""
        try:
            # Build dynamic update query
            update_fields = []
            values = []
            
            if join_data.status is not None:
                update_fields.append("status = %s")
                values.append(join_data.status)
            
            if join_data.invite_code is not None:
                update_fields.append("invite_code = %s")
                values.append(join_data.invite_code)
            
            if join_data.role is not None:
                update_fields.append("role = %s")
                values.append(join_data.role)
            
            if join_data.extra_data is not None:
                update_fields.append("extra_data = %s")
                values.append(join_data.extra_data)
            
            if join_data.status_id is not None:
                update_fields.append("status_id = %s")
                values.append(join_data.status_id)
            
            # Always update the updated_at field
            update_fields.append("updated_at = %s")
            values.append(datetime.utcnow().isoformat())
            
            if not update_fields:
                return None
            
            query = f"""
                UPDATE league_joins 
                SET {', '.join(update_fields)}
                WHERE league_id = %s AND status = %s AND user_id = %s AND joined_at = %s
            """
            values.extend([league_id, status, user_id, joined_at])
            
            self.session.execute(query, values)
            
            # Return updated league join
            return await self.get_league_join_by_user_and_league(user_id, league_id)
        except Exception as e:
            logger.error(f"Error updating league join: {e}")
            raise
    
    async def delete_league_join(self, league_id: str, status: str, user_id: str, joined_at: str) -> bool:
        """Delete a league join"""
        try:
            query = """
                DELETE FROM league_joins 
                WHERE league_id = %s AND status = %s AND user_id = %s AND joined_at = %s
            """
            self.session.execute(query, (league_id, status, user_id, joined_at))
            return True
        except Exception as e:
            logger.error(f"Error deleting league join: {e}")
            raise
    
    async def update_join_status(self, league_id: str, user_id: str, new_status: str, status_id: str = None) -> Optional[dict]:
        """Update the status of a league join"""
        try:
            # First get the current join
            current_join = await self.get_league_join_by_user_and_league(user_id, league_id)
            if not current_join:
                return None
            
            # Update the status
            update_data = LeagueJoinUpdate(status=new_status)
            if status_id:
                update_data.status_id = status_id
            
            return await self.update_league_join(
                league_id,
                current_join['status'],
                user_id,
                current_join['joined_at'],
                update_data
            )
        except Exception as e:
            logger.error(f"Error updating join status for user {user_id} in league {league_id}: {e}")
            raise
    
    async def get_league_member_count(self, league_id: str, status: str = "active") -> int:
        """Get the count of members in a league with specific status"""
        try:
            query = "SELECT COUNT(*) as count FROM league_joins WHERE league_id = %s AND status = %s"
            row = self.session.execute(query, (league_id, status)).one()
            return row.count if row else 0
        except Exception as e:
            logger.error(f"Error getting member count for league {league_id}: {e}")
            raise 