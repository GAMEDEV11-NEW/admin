import logging
from typing import List, Optional
from datetime import datetime
from cassandra.cluster import Session
from app.schemas.session import SessionCreate, SessionUpdate
from app.core.database import get_cassandra_session

logger = logging.getLogger(__name__)


class SessionRepository:
    """Session data access repository for Cassandra"""
    
    def __init__(self):
        self.session: Session = get_cassandra_session()
    
    async def get_sessions_by_mobile_device(self, mobile_no: str, device_id: str) -> List[dict]:
        """Get sessions by mobile number and device ID"""
        try:
            query = """
                SELECT * FROM sessions 
                WHERE mobile_no = %s AND device_id = %s
            """
            rows = self.session.execute(query, (mobile_no, device_id))
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting sessions by mobile/device: {e}")
            raise
    
    async def get_active_session(self, mobile_no: str, device_id: str) -> Optional[dict]:
        """Get active session for mobile and device"""
        try:
            query = """
                SELECT * FROM sessions 
                WHERE mobile_no = %s AND device_id = %s AND is_active = true
                LIMIT 1
            """
            row = self.session.execute(query, (mobile_no, device_id)).one()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting active session: {e}")
            raise
    
    async def create_session(self, session_data: SessionCreate) -> dict:
        """Create a new session"""
        try:
            now = datetime.utcnow()
            query = """
                INSERT INTO sessions (
                    mobile_no, device_id, session_token, user_id, 
                    jwt_token, fcm_token, created_at, expires_at, 
                    is_active, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.session.execute(query, (
                session_data.mobile_no,
                session_data.device_id,
                session_data.session_token,
                session_data.user_id,
                session_data.jwt_token,
                session_data.fcm_token,
                now,
                session_data.expires_at,
                session_data.is_active,
                now
            ))
            
            # Return the created session
            return {
                "mobile_no": session_data.mobile_no,
                "device_id": session_data.device_id,
                "session_token": session_data.session_token,
                "user_id": session_data.user_id,
                "jwt_token": session_data.jwt_token,
                "fcm_token": session_data.fcm_token,
                "created_at": now,
                "expires_at": session_data.expires_at,
                "is_active": session_data.is_active,
                "updated_at": now
            }
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    async def update_session(self, mobile_no: str, device_id: str, session_data: SessionUpdate) -> Optional[dict]:
        """Update an existing session"""
        try:
            now = datetime.utcnow()
            
            # Build dynamic update query
            update_fields = []
            values = []
            
            if session_data.jwt_token is not None:
                update_fields.append("jwt_token = %s")
                values.append(session_data.jwt_token)
            
            if session_data.fcm_token is not None:
                update_fields.append("fcm_token = %s")
                values.append(session_data.fcm_token)
            
            if session_data.is_active is not None:
                update_fields.append("is_active = %s")
                values.append(session_data.is_active)
            
            if session_data.expires_at is not None:
                update_fields.append("expires_at = %s")
                values.append(session_data.expires_at)
            
            update_fields.append("updated_at = %s")
            values.append(now)
            
            if not update_fields:
                return None
            
            query = f"""
                UPDATE sessions 
                SET {', '.join(update_fields)}
                WHERE mobile_no = %s AND device_id = %s
            """
            values.extend([mobile_no, device_id])
            
            self.session.execute(query, values)
            
            # Return updated session
            return await self.get_active_session(mobile_no, device_id)
        except Exception as e:
            logger.error(f"Error updating session: {e}")
            raise
    
    async def deactivate_session(self, mobile_no: str, device_id: str) -> bool:
        """Deactivate a session"""
        try:
            query = """
                UPDATE sessions 
                SET is_active = false, updated_at = %s
                WHERE mobile_no = %s AND device_id = %s
            """
            self.session.execute(query, (datetime.utcnow(), mobile_no, device_id))
            return True
        except Exception as e:
            logger.error(f"Error deactivating session: {e}")
            raise
    
    async def delete_expired_sessions(self) -> int:
        """Delete expired sessions"""
        try:
            now = datetime.utcnow()
            query = """
                DELETE FROM sessions 
                WHERE expires_at < %s
            """
            result = self.session.execute(query, (now,))
            return len(result)
        except Exception as e:
            logger.error(f"Error deleting expired sessions: {e}")
            raise 