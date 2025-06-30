import logging
from typing import List, Optional
from datetime import datetime, timedelta
import uuid
from app.schemas.session import SessionCreate, SessionResponse, SessionUpdate
from app.repositories.session_repository import SessionRepository

logger = logging.getLogger(__name__)


class SessionService:
    """Session business logic service"""
    
    def __init__(self):
        self.session_repository = SessionRepository()
    
    async def get_user_sessions(self, mobile_no: str, device_id: str) -> List[SessionResponse]:
        """Get all sessions for a user and device"""
        try:
            sessions = await self.session_repository.get_sessions_by_mobile_device(mobile_no, device_id)
            return [SessionResponse(**session) for session in sessions]
        except Exception as e:
            logger.error(f"Error getting user sessions: {e}")
            raise
    
    async def get_active_session(self, mobile_no: str, device_id: str) -> Optional[SessionResponse]:
        """Get active session for user and device"""
        try:
            session = await self.session_repository.get_active_session(mobile_no, device_id)
            if session:
                return SessionResponse(**session)
            return None
        except Exception as e:
            logger.error(f"Error getting active session: {e}")
            raise
    
    async def create_session(self, mobile_no: str, device_id: str, user_id: str, 
                           jwt_token: Optional[str] = None, fcm_token: Optional[str] = None,
                           expires_in_hours: int = 24) -> SessionResponse:
        """Create a new session"""
        try:
            # Deactivate any existing active sessions for this user/device
            await self.deactivate_session(mobile_no, device_id)
            
            # Create new session
            session_data = SessionCreate(
                mobile_no=mobile_no,
                device_id=device_id,
                session_token=str(uuid.uuid4()),
                user_id=user_id,
                jwt_token=jwt_token,
                fcm_token=fcm_token,
                expires_at=datetime.utcnow() + timedelta(hours=expires_in_hours),
                is_active=True
            )
            
            session = await self.session_repository.create_session(session_data)
            logger.info(f"Created session for user {user_id} on device {device_id}")
            return SessionResponse(**session)
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    async def update_session(self, mobile_no: str, device_id: str, 
                           session_data: SessionUpdate) -> Optional[SessionResponse]:
        """Update an existing session"""
        try:
            session = await self.session_repository.update_session(mobile_no, device_id, session_data)
            if session:
                logger.info(f"Updated session for {mobile_no} on device {device_id}")
                return SessionResponse(**session)
            return None
        except Exception as e:
            logger.error(f"Error updating session: {e}")
            raise
    
    async def deactivate_session(self, mobile_no: str, device_id: str) -> bool:
        """Deactivate a session"""
        try:
            success = await self.session_repository.deactivate_session(mobile_no, device_id)
            if success:
                logger.info(f"Deactivated session for {mobile_no} on device {device_id}")
            return success
        except Exception as e:
            logger.error(f"Error deactivating session: {e}")
            raise
    
    async def refresh_session(self, mobile_no: str, device_id: str, 
                            expires_in_hours: int = 24) -> Optional[SessionResponse]:
        """Refresh session expiration"""
        try:
            session_data = SessionUpdate(
                expires_at=datetime.utcnow() + timedelta(hours=expires_in_hours)
            )
            return await self.update_session(mobile_no, device_id, session_data)
        except Exception as e:
            logger.error(f"Error refreshing session: {e}")
            raise
    
    async def validate_session(self, mobile_no: str, device_id: str, 
                             session_token: str) -> Optional[SessionResponse]:
        """Validate session token"""
        try:
            session = await self.get_active_session(mobile_no, device_id)
            if session and session.session_token == session_token:
                # Check if session is expired
                if session.expires_at > datetime.utcnow():
                    return session
                else:
                    # Session expired, deactivate it
                    await self.deactivate_session(mobile_no, device_id)
            return None
        except Exception as e:
            logger.error(f"Error validating session: {e}")
            raise
    
    async def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions"""
        try:
            count = await self.session_repository.delete_expired_sessions()
            logger.info(f"Cleaned up {count} expired sessions")
            return count
        except Exception as e:
            logger.error(f"Error cleaning up expired sessions: {e}")
            raise 