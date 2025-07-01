import logging
from typing import List, Optional
from datetime import datetime
from cassandra.cluster import Session
from app.schemas.user import UserCreate, UserUpdate
from app.core.database import get_cassandra_session

logger = logging.getLogger(__name__)


class UserRepository:
    """User data access repository for Cassandra"""
    
    def __init__(self):
        self.session: Session = get_cassandra_session()
    
    def _row_to_dict(self, row) -> dict:
        """Convert Cassandra row to dictionary"""
        if row is None:
            return None
        return {column: getattr(row, column) for column in row._fields}
    
    async def get_all_users(self, limit: int = 100) -> List[dict]:
        """Get all users with pagination"""
        try:
            query = "SELECT * FROM users LIMIT %s"
            rows = self.session.execute(query, (limit,))
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            raise
    
    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID"""
        try:
            query = "SELECT * FROM users WHERE id = %s"
            row = self.session.execute(query, (user_id,)).one()
            return self._row_to_dict(row)
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {e}")
            raise
    
    async def get_user_by_mobile(self, mobile_no: str) -> Optional[dict]:
        """Get user by mobile number"""
        try:
            # Note: This would require a secondary index on mobile_no in production
            query = "SELECT * FROM users WHERE mobile_no = %s ALLOW FILTERING"
            row = self.session.execute(query, (mobile_no,)).one()
            return self._row_to_dict(row)
        except Exception as e:
            logger.error(f"Error getting user by mobile {mobile_no}: {e}")
            raise
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email"""
        try:
            # Note: This would require a secondary index on email in production
            query = "SELECT * FROM users WHERE email = %s ALLOW FILTERING"
            row = self.session.execute(query, (email,)).one()
            return self._row_to_dict(row)
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            raise
    
    async def create_user(self, user_data: UserCreate) -> dict:
        """Create a new user"""
        try:
            now = datetime.utcnow()
            user_id = f"user_{now.timestamp()}_{hash(user_data.mobile_no)}"
            
            query = """
                INSERT INTO users (
                    id, mobile_no, email, full_name, state, referral_code,
                    referred_by, profile_data, language_code, language_name,
                    region_code, timezone, user_preferences, status,
                    created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.session.execute(query, (
                user_id,
                user_data.mobile_no,
                user_data.email,
                user_data.full_name,
                user_data.state,
                user_data.referral_code,
                user_data.referred_by,
                user_data.profile_data,
                user_data.language_code,
                user_data.language_name,
                user_data.region_code,
                user_data.timezone,
                user_data.user_preferences,
                user_data.status,
                now,
                now
            ))
            
            # Return the created user
            return {
                "id": user_id,
                "mobile_no": user_data.mobile_no,
                "email": user_data.email,
                "full_name": user_data.full_name,
                "state": user_data.state,
                "referral_code": user_data.referral_code,
                "referred_by": user_data.referred_by,
                "profile_data": user_data.profile_data,
                "language_code": user_data.language_code,
                "language_name": user_data.language_name,
                "region_code": user_data.region_code,
                "timezone": user_data.timezone,
                "user_preferences": user_data.user_preferences,
                "status": user_data.status,
                "created_at": now,
                "updated_at": now
            }
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[dict]:
        """Update an existing user"""
        try:
            now = datetime.utcnow()
            
            # Build dynamic update query
            update_fields = []
            values = []
            
            if user_data.mobile_no is not None:
                update_fields.append("mobile_no = %s")
                values.append(user_data.mobile_no)
            
            if user_data.email is not None:
                update_fields.append("email = %s")
                values.append(user_data.email)
            
            if user_data.full_name is not None:
                update_fields.append("full_name = %s")
                values.append(user_data.full_name)
            
            if user_data.state is not None:
                update_fields.append("state = %s")
                values.append(user_data.state)
            
            if user_data.referral_code is not None:
                update_fields.append("referral_code = %s")
                values.append(user_data.referral_code)
            
            if user_data.referred_by is not None:
                update_fields.append("referred_by = %s")
                values.append(user_data.referred_by)
            
            if user_data.profile_data is not None:
                update_fields.append("profile_data = %s")
                values.append(user_data.profile_data)
            
            if user_data.language_code is not None:
                update_fields.append("language_code = %s")
                values.append(user_data.language_code)
            
            if user_data.language_name is not None:
                update_fields.append("language_name = %s")
                values.append(user_data.language_name)
            
            if user_data.region_code is not None:
                update_fields.append("region_code = %s")
                values.append(user_data.region_code)
            
            if user_data.timezone is not None:
                update_fields.append("timezone = %s")
                values.append(user_data.timezone)
            
            if user_data.user_preferences is not None:
                update_fields.append("user_preferences = %s")
                values.append(user_data.user_preferences)
            
            if user_data.status is not None:
                update_fields.append("status = %s")
                values.append(user_data.status)
            
            update_fields.append("updated_at = %s")
            values.append(now)
            
            if not update_fields:
                return None
            
            query = f"""
                UPDATE users 
                SET {', '.join(update_fields)}
                WHERE id = %s
            """
            values.append(user_id)
            
            self.session.execute(query, values)
            
            # Return updated user
            return await self.get_user_by_id(user_id)
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            raise
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        try:
            query = "DELETE FROM users WHERE id = %s"
            self.session.execute(query, (user_id,))
            return True
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            raise 