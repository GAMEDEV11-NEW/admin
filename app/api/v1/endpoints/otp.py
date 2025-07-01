from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.services.otp_service import OTPService
from app.schemas.otp import OTPCreate, OTPResponse, OTPUpdate, OTPVerify
from app.core.dependencies import get_otp_service

router = APIRouter()


@router.get("/phone-email/{phone_or_email}", response_model=List[OTPResponse])
async def get_otps_by_phone_email(
    phone_or_email: str,
    limit: int = 50,
    otp_service: OTPService = Depends(get_otp_service)
):
    """Get all OTPs for a phone/email"""
    return await otp_service.get_otps_by_phone_email(phone_or_email, limit=limit)


@router.get("/purpose/{purpose}", response_model=List[OTPResponse])
async def get_otps_by_purpose(
    purpose: str,
    limit: int = 50,
    otp_service: OTPService = Depends(get_otp_service)
):
    """Get all OTPs by purpose"""
    return await otp_service.get_otps_by_purpose(purpose, limit=limit)


@router.get("/verified", response_model=List[OTPResponse])
async def get_verified_otps(
    limit: int = 50,
    otp_service: OTPService = Depends(get_otp_service)
):
    """Get all verified OTPs"""
    return await otp_service.get_verified_otps(limit=limit)


@router.get("/{phone_or_email}/{purpose}", response_model=OTPResponse)
async def get_otp_by_phone_email_and_purpose(
    phone_or_email: str,
    purpose: str,
    otp_service: OTPService = Depends(get_otp_service)
):
    """Get OTP by phone/email and purpose"""
    otp = await otp_service.get_otp_by_phone_email_and_purpose(phone_or_email, purpose)
    if not otp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OTP not found"
        )
    return otp


@router.post("/", response_model=OTPResponse, status_code=status.HTTP_201_CREATED)
async def create_otp(
    otp_data: OTPCreate,
    otp_service: OTPService = Depends(get_otp_service)
):
    """Create a new OTP"""
    return await otp_service.create_otp(otp_data)


@router.put("/{phone_or_email}/{purpose}/{created_at}", response_model=OTPResponse)
async def update_otp(
    phone_or_email: str,
    purpose: str,
    created_at: str,
    otp_data: OTPUpdate,
    otp_service: OTPService = Depends(get_otp_service)
):
    """Update an existing OTP"""
    otp = await otp_service.update_otp(phone_or_email, purpose, created_at, otp_data)
    if not otp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OTP not found"
        )
    return otp


@router.delete("/{phone_or_email}/{purpose}/{created_at}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_otp(
    phone_or_email: str,
    purpose: str,
    created_at: str,
    otp_service: OTPService = Depends(get_otp_service)
):
    """Delete an OTP"""
    success = await otp_service.delete_otp(phone_or_email, purpose, created_at)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OTP not found"
        )


@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_otp(
    verify_data: OTPVerify,
    otp_service: OTPService = Depends(get_otp_service)
):
    """Verify an OTP"""
    is_valid = await otp_service.verify_otp(verify_data)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    return {"message": "OTP verified successfully", "verified": True}


@router.post("/{phone_or_email}/{purpose}/increment-attempt", status_code=status.HTTP_200_OK)
async def increment_attempt_count(
    phone_or_email: str,
    purpose: str,
    otp_service: OTPService = Depends(get_otp_service)
):
    """Increment attempt count for an OTP"""
    success = await otp_service.increment_attempt_count(phone_or_email, purpose)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OTP not found"
        )
    return {"message": "Attempt count incremented successfully"}


@router.delete("/expired", status_code=status.HTTP_200_OK)
async def delete_expired_otps(
    otp_service: OTPService = Depends(get_otp_service)
):
    """Delete expired OTPs"""
    deleted_count = await otp_service.delete_expired_otps()
    return {"message": f"Deleted {deleted_count} expired OTPs", "deleted_count": deleted_count} 