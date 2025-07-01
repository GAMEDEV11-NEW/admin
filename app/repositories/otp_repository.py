import logging
from typing import List, Optional
from datetime import datetime, timedelta
from cassandra.cluster import Session
from app.schemas.otp import OTPCreate, OTPUpdate, OTPVerify
from app.core.database import get_cassandra_session

logger = logging.getLogger(__name__)


class OTPRepository:
    """OTP data access repository for Cassandra"""
    
    def __init__(self):
        self.session: Session = get_cassandra_session()
    
    def _row_to_dict(self, row) -> dict:
        """Convert Cassandra row to dictionary"""
        if row is None:
            return None
        return {column: getattr(row, column) for column in row._fields}
    
    async def get_otp_by_phone_email_and_purpose(self, phone_or_email: str, purpose: str) -> Optional[dict]:
        """Get OTP by phone/email and purpose"""
        try:
            query = """
                SELECT * FROM otp_store 
                WHERE phone_or_email = %s AND purpose = %s 
                LIMIT 1
            """
            row = self.session.execute(query, (phone_or_email, purpose)).one()
            return self._row_to_dict(row)
        except Exception as e:
            logger.error(f"Error getting OTP for {phone_or_email} with purpose {purpose}: {e}")
            raise
    
    async def get_all_otps_by_phone_email(self, phone_or_email: str, limit: int = 50) -> List[dict]:
        """Get all OTPs for a phone/email"""
        try:
            query = "SELECT * FROM otp_store WHERE phone_or_email = %s LIMIT %s"
            rows = self.session.execute(query, (phone_or_email, limit))
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting OTPs for {phone_or_email}: {e}")
            raise
    
    async def get_otps_by_purpose(self, purpose: str, limit: int = 50) -> List[dict]:
        """Get all OTPs by purpose"""
        try:
            query = "SELECT * FROM otp_store WHERE purpose = %s LIMIT %s"
            rows = self.session.execute(query, (purpose, limit))
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting OTPs by purpose {purpose}: {e}")
            raise
    
    async def get_verified_otps(self, limit: int = 50) -> List[dict]:
        """Get all verified OTPs"""
        try:
            query = "SELECT * FROM otp_store WHERE is_verified = true LIMIT %s"
            rows = self.session.execute(query, (limit,))
            return [self._row_to_dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting verified OTPs: {e}")
            raise
    
    async def create_otp(self, otp_data: OTPCreate) -> dict:
        """Create a new OTP"""
        try:
            now = datetime.utcnow()
            
            query = """
                INSERT INTO otp_store (
                    phone_or_email, otp_code, created_at, expires_at,
                    purpose, is_verified, attempt_count
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.session.execute(query, (
                otp_data.phone_or_email,
                otp_data.otp_code,
                now.isoformat(),
                otp_data.expires_at,
                otp_data.purpose,
                otp_data.is_verified,
                otp_data.attempt_count
            ))
            
            # Return the created OTP
            return {
                "phone_or_email": otp_data.phone_or_email,
                "otp_code": otp_data.otp_code,
                "created_at": now.isoformat(),
                "expires_at": otp_data.expires_at,
                "purpose": otp_data.purpose,
                "is_verified": otp_data.is_verified,
                "attempt_count": otp_data.attempt_count
            }
        except Exception as e:
            logger.error(f"Error creating OTP: {e}")
            raise
    
    async def update_otp(self, phone_or_email: str, purpose: str, created_at: str, otp_data: OTPUpdate) -> Optional[dict]:
        """Update an existing OTP"""
        try:
            # Build dynamic update query
            update_fields = []
            values = []
            
            if otp_data.otp_code is not None:
                update_fields.append("otp_code = %s")
                values.append(otp_data.otp_code)
            
            if otp_data.expires_at is not None:
                update_fields.append("expires_at = %s")
                values.append(otp_data.expires_at)
            
            if otp_data.is_verified is not None:
                update_fields.append("is_verified = %s")
                values.append(otp_data.is_verified)
            
            if otp_data.attempt_count is not None:
                update_fields.append("attempt_count = %s")
                values.append(otp_data.attempt_count)
            
            if not update_fields:
                return None
            
            query = f"""
                UPDATE otp_store 
                SET {', '.join(update_fields)}
                WHERE phone_or_email = %s AND purpose = %s AND created_at = %s
            """
            values.extend([phone_or_email, purpose, created_at])
            
            self.session.execute(query, values)
            
            # Return updated OTP
            return await self.get_otp_by_phone_email_and_purpose(phone_or_email, purpose)
        except Exception as e:
            logger.error(f"Error updating OTP for {phone_or_email}: {e}")
            raise
    
    async def delete_otp(self, phone_or_email: str, purpose: str, created_at: str) -> bool:
        """Delete an OTP"""
        try:
            query = """
                DELETE FROM otp_store 
                WHERE phone_or_email = %s AND purpose = %s AND created_at = %s
            """
            self.session.execute(query, (phone_or_email, purpose, created_at))
            return True
        except Exception as e:
            logger.error(f"Error deleting OTP for {phone_or_email}: {e}")
            raise
    
    async def verify_otp(self, verify_data: OTPVerify) -> bool:
        """Verify an OTP"""
        try:
            # Get the OTP
            otp = await self.get_otp_by_phone_email_and_purpose(
                verify_data.phone_or_email, 
                verify_data.purpose
            )
            
            if not otp:
                return False
            
            # Check if OTP is expired
            expires_at = datetime.fromisoformat(otp['expires_at'])
            if datetime.utcnow() > expires_at:
                return False
            
            # Check if OTP code matches
            if otp['otp_code'] != verify_data.otp_code:
                # Increment attempt count
                new_attempt_count = otp.get('attempt_count', 0) + 1
                await self.update_otp(
                    verify_data.phone_or_email,
                    verify_data.purpose,
                    otp['created_at'],
                    OTPUpdate(attempt_count=new_attempt_count)
                )
                return False
            
            # Mark as verified
            await self.update_otp(
                verify_data.phone_or_email,
                verify_data.purpose,
                otp['created_at'],
                OTPUpdate(is_verified=True)
            )
            
            return True
        except Exception as e:
            logger.error(f"Error verifying OTP: {e}")
            raise
    
    async def increment_attempt_count(self, phone_or_email: str, purpose: str) -> bool:
        """Increment attempt count for an OTP"""
        try:
            otp = await self.get_otp_by_phone_email_and_purpose(phone_or_email, purpose)
            if not otp:
                return False
            
            new_attempt_count = otp.get('attempt_count', 0) + 1
            await self.update_otp(
                phone_or_email,
                purpose,
                otp['created_at'],
                OTPUpdate(attempt_count=new_attempt_count)
            )
            return True
        except Exception as e:
            logger.error(f"Error incrementing attempt count for {phone_or_email}: {e}")
            raise
    
    async def delete_expired_otps(self) -> int:
        """Delete expired OTPs and return count of deleted records"""
        try:
            current_time = datetime.utcnow().isoformat()
            query = "SELECT * FROM otp_store WHERE expires_at < %s"
            expired_otps = self.session.execute(query, (current_time,))
            
            deleted_count = 0
            for otp in expired_otps:
                await self.delete_otp(
                    otp.phone_or_email,
                    otp.purpose,
                    otp.created_at
                )
                deleted_count += 1
            
            return deleted_count
        except Exception as e:
            logger.error(f"Error deleting expired OTPs: {e}")
            raise 