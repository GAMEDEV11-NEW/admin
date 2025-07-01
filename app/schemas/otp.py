from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class OTPBase(BaseModel):
    """Base OTP schema"""
    phone_or_email: str = Field(..., description="Phone number or email")
    otp_code: str = Field(..., description="OTP code")
    purpose: str = Field(..., description="Purpose of OTP")
    expires_at: str = Field(..., description="Expiration timestamp")
    is_verified: bool = Field(default=False, description="Whether OTP is verified")
    attempt_count: int = Field(default=0, description="Number of verification attempts")


class OTPCreate(OTPBase):
    """Schema for creating a new OTP"""
    pass


class OTPUpdate(BaseModel):
    """Schema for updating an OTP"""
    otp_code: Optional[str] = Field(None, description="OTP code")
    expires_at: Optional[str] = Field(None, description="Expiration timestamp")
    is_verified: Optional[bool] = Field(None, description="Whether OTP is verified")
    attempt_count: Optional[int] = Field(None, description="Number of verification attempts")


class OTPVerify(BaseModel):
    """Schema for OTP verification"""
    phone_or_email: str = Field(..., description="Phone number or email")
    otp_code: str = Field(..., description="OTP code to verify")
    purpose: str = Field(..., description="Purpose of OTP")


class OTPResponse(OTPBase):
    """Schema for OTP response"""
    created_at: str = Field(..., description="Creation timestamp")
    
    model_config = ConfigDict(from_attributes=True) 