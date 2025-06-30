import logging
from typing import List, Optional
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    """User business logic service"""
    
    def __init__(self):
        self.user_repository = UserRepository()
    
    async def get_users(self, limit: int = 100) -> List[UserResponse]:
        """Get all users with pagination"""
        try:
            users = await self.user_repository.get_all_users(limit=limit)
            return [UserResponse(**user) for user in users]
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            raise
    
    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get user by ID"""
        try:
            user = await self.user_repository.get_user_by_id(user_id)
            if user:
                return UserResponse(**user)
            return None
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            raise
    
    async def get_user_by_mobile(self, mobile_no: str) -> Optional[UserResponse]:
        """Get user by mobile number"""
        try:
            user = await self.user_repository.get_user_by_mobile(mobile_no)
            if user:
                return UserResponse(**user)
            return None
        except Exception as e:
            logger.error(f"Error getting user by mobile {mobile_no}: {e}")
            raise
    
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get user by email"""
        try:
            user = await self.user_repository.get_user_by_email(email)
            if user:
                return UserResponse(**user)
            return None
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            raise
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user"""
        try:
            # Business logic validation
            if await self.user_repository.get_user_by_mobile(user_data.mobile_no):
                raise ValueError("Mobile number already registered")
            
            if user_data.email and await self.user_repository.get_user_by_email(user_data.email):
                raise ValueError("Email already registered")
            
            user = await self.user_repository.create_user(user_data)
            logger.info(f"Created user with ID: {user['id']}")
            return UserResponse(**user)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[UserResponse]:
        """Update an existing user"""
        try:
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                return None
            
            # Business logic validation
            if user_data.mobile_no and user_data.mobile_no != user['mobile_no']:
                if await self.user_repository.get_user_by_mobile(user_data.mobile_no):
                    raise ValueError("Mobile number already registered")
            
            if user_data.email and user_data.email != user['email']:
                if await self.user_repository.get_user_by_email(user_data.email):
                    raise ValueError("Email already registered")
            
            updated_user = await self.user_repository.update_user(user_id, user_data)
            if updated_user:
                logger.info(f"Updated user with ID: {user_id}")
                return UserResponse(**updated_user)
            return None
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            raise
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        try:
            success = await self.user_repository.delete_user(user_id)
            if success:
                logger.info(f"Deleted user with ID: {user_id}")
            return success
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            raise 