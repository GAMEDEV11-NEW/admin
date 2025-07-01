import logging
from typing import List, Optional
from datetime import datetime
from cassandra.cluster import Session
from app.schemas.contest import ContestCreate, ContestUpdate
from app.core.database import get_cassandra_session

logger = logging.getLogger(__name__)


class ContestRepository:
    """Contest data access repository for Cassandra"""
    
    def __init__(self):
        self.session: Session = get_cassandra_session()
    
    def _row_to_dict(self, row) -> dict:
        """Convert Cassandra row to dictionary"""
        if row is None:
            return None
        return {column: getattr(row, column) for column in row._fields}
    
    async def get_all_contests(self, limit: int = 100) -> List[dict]:
        """Get all contests with pagination"""
        try:
            query = "SELECT * FROM contests LIMIT %s"
            rows = self.session.execute(query, (limit,))
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all contests: {e}")
            raise
    
    async def get_contest_by_id(self, contest_id: str) -> Optional[dict]:
        """Get contest by ID"""
        try:
            query = "SELECT * FROM contests WHERE contest_id = %s"
            row = self.session.execute(query, (contest_id,)).one()
            return self._row_to_dict(row)
        except Exception as e:
            logger.error(f"Error getting contest by ID {contest_id}: {e}")
            raise
    
    async def get_active_contests(self, limit: int = 50) -> List[dict]:
        """Get active contests (where end time is in the future)"""
        try:
            query = "SELECT * FROM contests WHERE contest_endtime > %s LIMIT %s"
            current_time = datetime.utcnow().isoformat()
            rows = self.session.execute(query, (current_time, limit))
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting active contests: {e}")
            raise
    
    async def create_contest(self, contest_data: ContestCreate) -> dict:
        """Create a new contest"""
        try:
            now = datetime.utcnow()
            contest_id = f"contest_{now.timestamp()}_{hash(contest_data.contest_name)}"
            
            query = """
                INSERT INTO contests (
                    contest_id, contest_name, contest_win_price, contest_entryfee,
                    contest_joinuser, contest_activeuser, contest_starttime, contest_endtime
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.session.execute(query, (
                contest_id,
                contest_data.contest_name,
                contest_data.contest_win_price,
                contest_data.contest_entryfee,
                contest_data.contest_joinuser,
                contest_data.contest_activeuser,
                contest_data.contest_starttime,
                contest_data.contest_endtime
            ))
            
            # Return the created contest
            return {
                "contest_id": contest_id,
                "contest_name": contest_data.contest_name,
                "contest_win_price": contest_data.contest_win_price,
                "contest_entryfee": contest_data.contest_entryfee,
                "contest_joinuser": contest_data.contest_joinuser,
                "contest_activeuser": contest_data.contest_activeuser,
                "contest_starttime": contest_data.contest_starttime,
                "contest_endtime": contest_data.contest_endtime
            }
        except Exception as e:
            logger.error(f"Error creating contest: {e}")
            raise
    
    async def update_contest(self, contest_id: str, contest_data: ContestUpdate) -> Optional[dict]:
        """Update an existing contest"""
        try:
            # Build dynamic update query
            update_fields = []
            values = []
            
            if contest_data.contest_name is not None:
                update_fields.append("contest_name = %s")
                values.append(contest_data.contest_name)
            
            if contest_data.contest_win_price is not None:
                update_fields.append("contest_win_price = %s")
                values.append(contest_data.contest_win_price)
            
            if contest_data.contest_entryfee is not None:
                update_fields.append("contest_entryfee = %s")
                values.append(contest_data.contest_entryfee)
            
            if contest_data.contest_joinuser is not None:
                update_fields.append("contest_joinuser = %s")
                values.append(contest_data.contest_joinuser)
            
            if contest_data.contest_activeuser is not None:
                update_fields.append("contest_activeuser = %s")
                values.append(contest_data.contest_activeuser)
            
            if contest_data.contest_starttime is not None:
                update_fields.append("contest_starttime = %s")
                values.append(contest_data.contest_starttime)
            
            if contest_data.contest_endtime is not None:
                update_fields.append("contest_endtime = %s")
                values.append(contest_data.contest_endtime)
            
            if not update_fields:
                return None
            
            query = f"""
                UPDATE contests 
                SET {', '.join(update_fields)}
                WHERE contest_id = %s
            """
            values.append(contest_id)
            
            self.session.execute(query, values)
            
            # Return updated contest
            return await self.get_contest_by_id(contest_id)
        except Exception as e:
            logger.error(f"Error updating contest {contest_id}: {e}")
            raise
    
    async def delete_contest(self, contest_id: str) -> bool:
        """Delete a contest"""
        try:
            query = "DELETE FROM contests WHERE contest_id = %s"
            self.session.execute(query, (contest_id,))
            return True
        except Exception as e:
            logger.error(f"Error deleting contest {contest_id}: {e}")
            raise
    
    async def increment_join_user(self, contest_id: str) -> bool:
        """Increment the number of users who joined the contest"""
        try:
            query = "UPDATE contests SET contest_joinuser = contest_joinuser + 1 WHERE contest_id = %s"
            self.session.execute(query, (contest_id,))
            return True
        except Exception as e:
            logger.error(f"Error incrementing join user for contest {contest_id}: {e}")
            raise
    
    async def increment_active_user(self, contest_id: str) -> bool:
        """Increment the number of active users in the contest"""
        try:
            query = "UPDATE contests SET contest_activeuser = contest_activeuser + 1 WHERE contest_id = %s"
            self.session.execute(query, (contest_id,))
            return True
        except Exception as e:
            logger.error(f"Error incrementing active user for contest {contest_id}: {e}")
            raise 