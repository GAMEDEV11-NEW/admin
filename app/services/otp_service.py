import logging
from typing import List, Optional
from app.schemas.otp import OTPCreate, OTPResponse, OTPUpdate, OTPVerify
from app.repositories.otp_repository import OTPRepository

logger = logging.getLogger(__name__)


class OTPService:
    """OTP business logic service"""
    
    def __init__(self):
        self.otp_repository = OTPRepository()
    
    async def get_otps_by_phone_email(self, phone_or_email: str, limit: int = 50) -> List[OTPResponse]:
        """Get all OTPs for a phone/email"""
        try:
            otps = await self.otp_repository.get_all_otps_by_phone_email(phone_or_email, limit=limit)
            return [OTPResponse(**otp) for otp in otps]
        except Exception as e:
            logger.error(f"Error getting OTPs for {phone_or_email}: {e}")
            raise
    
    async def get_otps_by_purpose(self, purpose: str, limit: int = 50) -> List[OTPResponse]:
        """Get all OTPs by purpose"""
        try:
            otps = await self.otp_repository.get_otps_by_purpose(purpose, limit=limit)
            return [OTPResponse(**otp) for otp in otps]
        except Exception as e:
            logger.error(f"Error getting OTPs by purpose {purpose}: {e}")
            raise
    
    async def get_verified_otps(self, limit: int = 50) -> List[OTPResponse]:
        """Get all verified OTPs"""
        try:
            otps = await self.otp_repository.get_verified_otps(limit=limit)
            return [OTPResponse(**otp) for otp in otps]
        except Exception as e:
            logger.error(f"Error getting verified OTPs: {e}")
            raise
    
    async def get_otp_by_phone_email_and_purpose(self, phone_or_email: str, purpose: str) -> Optional[OTPResponse]:
        """Get OTP by phone/email and purpose"""
        try:
            otp = await self.otp_repository.get_otp_by_phone_email_and_purpose(phone_or_email, purpose)
            if otp:
                return OTPResponse(**otp)
            return None
        except Exception as e:
            logger.error(f"Error getting OTP for {phone_or_email} with purpose {purpose}: {e}")
            raise
    
    async def create_otp(self, otp_data: OTPCreate) -> OTPResponse:
        """Create a new OTP"""
        try:
            # Business logic validation
            if not otp_data.phone_or_email.strip():
                raise ValueError("Phone or email cannot be empty")
            
            if not otp_data.otp_code.strip():
                raise ValueError("OTP code cannot be empty")
            
            if not otp_data.purpose.strip():
                raise ValueError("Purpose cannot be empty")
            
            # Check if OTP already exists for this phone/email and purpose
            existing_otp = await self.otp_repository.get_otp_by_phone_email_and_purpose(
                otp_data.phone_or_email, otp_data.purpose
            )
            if existing_otp:
                logger.warning(f"OTP already exists for {otp_data.phone_or_email} with purpose {otp_data.purpose}")
            
            otp = await self.otp_repository.create_otp(otp_data)
            logger.info(f"Created OTP for {otp_data.phone_or_email} with purpose {otp_data.purpose}")
            return OTPResponse(**otp)
        except Exception as e:
            logger.error(f"Error creating OTP: {e}")
            raise
    
    async def update_otp(self, phone_or_email: str, purpose: str, created_at: str, otp_data: OTPUpdate) -> Optional[OTPResponse]:
        """Update an existing OTP"""
        try:
            otp = await self.otp_repository.get_otp_by_phone_email_and_purpose(phone_or_email, purpose)
            if not otp:
                return None
            
            # Business logic validation
            if otp_data.otp_code is not None and not otp_data.otp_code.strip():
                raise ValueError("OTP code cannot be empty")
            
            updated_otp = await self.otp_repository.update_otp(phone_or_email, purpose, created_at, otp_data)
            if updated_otp:
                logger.info(f"Updated OTP for {phone_or_email} with purpose {purpose}")
                return OTPResponse(**updated_otp)
            return None
        except Exception as e:
            logger.error(f"Error updating OTP for {phone_or_email}: {e}")
            raise
    
    async def delete_otp(self, phone_or_email: str, purpose: str, created_at: str) -> bool:
        """Delete an OTP"""
        try:
            success = await self.otp_repository.delete_otp(phone_or_email, purpose, created_at)
            if success:
                logger.info(f"Deleted OTP for {phone_or_email} with purpose {purpose}")
            return success
        except Exception as e:
            logger.error(f"Error deleting OTP for {phone_or_email}: {e}")
            raise
    
    async def verify_otp(self, verify_data: OTPVerify) -> bool:
        """Verify an OTP"""
        try:
            # Business logic validation
            if not verify_data.phone_or_email.strip():
                raise ValueError("Phone or email cannot be empty")
            
            if not verify_data.otp_code.strip():
                raise ValueError("OTP code cannot be empty")
            
            if not verify_data.purpose.strip():
                raise ValueError("Purpose cannot be empty")
            
            is_valid = await self.otp_repository.verify_otp(verify_data)
            if is_valid:
                logger.info(f"OTP verified successfully for {verify_data.phone_or_email} with purpose {verify_data.purpose}")
            else:
                logger.warning(f"OTP verification failed for {verify_data.phone_or_email} with purpose {verify_data.purpose}")
            
            return is_valid
        except Exception as e:
            logger.error(f"Error verifying OTP: {e}")
            raise
    
    async def increment_attempt_count(self, phone_or_email: str, purpose: str) -> bool:
        """Increment attempt count for an OTP"""
        try:
            success = await self.otp_repository.increment_attempt_count(phone_or_email, purpose)
            if success:
                logger.info(f"Incremented attempt count for {phone_or_email} with purpose {purpose}")
            return success
        except Exception as e:
            logger.error(f"Error incrementing attempt count for {phone_or_email}: {e}")
            raise
    
    async def delete_expired_otps(self) -> int:
        """Delete expired OTPs"""
        try:
            deleted_count = await self.otp_repository.delete_expired_otps()
            logger.info(f"Deleted {deleted_count} expired OTPs")
            return deleted_count
        except Exception as e:
            logger.error(f"Error deleting expired OTPs: {e}")
            raise 