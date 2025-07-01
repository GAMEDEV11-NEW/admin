import logging
from typing import List, Optional
from app.schemas.contest import ContestCreate, ContestResponse, ContestUpdate
from app.repositories.contest_repository import ContestRepository

logger = logging.getLogger(__name__)


class ContestService:
    """Contest business logic service"""
    
    def __init__(self):
        self.contest_repository = ContestRepository()
    
    async def get_contests(self, limit: int = 100) -> List[ContestResponse]:
        """Get all contests with pagination"""
        try:
            contests = await self.contest_repository.get_all_contests(limit=limit)
            return [ContestResponse(**contest) for contest in contests]
        except Exception as e:
            logger.error(f"Error getting contests: {e}")
            raise
    
    async def get_contest_by_id(self, contest_id: str) -> Optional[ContestResponse]:
        """Get contest by ID"""
        try:
            contest = await self.contest_repository.get_contest_by_id(contest_id)
            if contest:
                return ContestResponse(**contest)
            return None
        except Exception as e:
            logger.error(f"Error getting contest {contest_id}: {e}")
            raise
    
    async def get_active_contests(self, limit: int = 50) -> List[ContestResponse]:
        """Get active contests"""
        try:
            contests = await self.contest_repository.get_active_contests(limit=limit)
            return [ContestResponse(**contest) for contest in contests]
        except Exception as e:
            logger.error(f"Error getting active contests: {e}")
            raise
    
    async def create_contest(self, contest_data: ContestCreate) -> ContestResponse:
        """Create a new contest"""
        try:
            # Business logic validation
            if contest_data.contest_joinuser < 0:
                raise ValueError("Join user count cannot be negative")
            
            if contest_data.contest_activeuser < 0:
                raise ValueError("Active user count cannot be negative")
            
            contest = await self.contest_repository.create_contest(contest_data)
            logger.info(f"Created contest with ID: {contest['contest_id']}")
            return ContestResponse(**contest)
        except Exception as e:
            logger.error(f"Error creating contest: {e}")
            raise
    
    async def update_contest(self, contest_id: str, contest_data: ContestUpdate) -> Optional[ContestResponse]:
        """Update an existing contest"""
        try:
            contest = await self.contest_repository.get_contest_by_id(contest_id)
            if not contest:
                return None
            
            # Business logic validation
            if contest_data.contest_joinuser is not None and contest_data.contest_joinuser < 0:
                raise ValueError("Join user count cannot be negative")
            
            if contest_data.contest_activeuser is not None and contest_data.contest_activeuser < 0:
                raise ValueError("Active user count cannot be negative")
            
            updated_contest = await self.contest_repository.update_contest(contest_id, contest_data)
            if updated_contest:
                logger.info(f"Updated contest with ID: {contest_id}")
                return ContestResponse(**updated_contest)
            return None
        except Exception as e:
            logger.error(f"Error updating contest {contest_id}: {e}")
            raise
    
    async def delete_contest(self, contest_id: str) -> bool:
        """Delete a contest"""
        try:
            success = await self.contest_repository.delete_contest(contest_id)
            if success:
                logger.info(f"Deleted contest with ID: {contest_id}")
            return success
        except Exception as e:
            logger.error(f"Error deleting contest {contest_id}: {e}")
            raise
    
    async def increment_join_user(self, contest_id: str) -> bool:
        """Increment the number of users who joined the contest"""
        try:
            success = await self.contest_repository.increment_join_user(contest_id)
            if success:
                logger.info(f"Incremented join user count for contest: {contest_id}")
            return success
        except Exception as e:
            logger.error(f"Error incrementing join user for contest {contest_id}: {e}")
            raise
    
    async def increment_active_user(self, contest_id: str) -> bool:
        """Increment the number of active users in the contest"""
        try:
            success = await self.contest_repository.increment_active_user(contest_id)
            if success:
                logger.info(f"Incremented active user count for contest: {contest_id}")
            return success
        except Exception as e:
            logger.error(f"Error incrementing active user for contest {contest_id}: {e}")
            raise 