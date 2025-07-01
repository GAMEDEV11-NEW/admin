from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    mobile_no: str = Field(..., description="User mobile number")
    email: Optional[str] = Field(None, description="User email address")
    full_name: str = Field(..., min_length=1, max_length=100, description="User full name")
    state: Optional[str] = Field(None, description="User state")
    referral_code: Optional[str] = Field(None, description="User referral code")
    referred_by: Optional[str] = Field(None, description="Referred by user")
    profile_data: Optional[str] = Field(None, description="User profile data")
    language_code: Optional[str] = Field(None, description="Language code")
    language_name: Optional[str] = Field(None, description="Language name")
    region_code: Optional[str] = Field(None, description="Region code")
    timezone: Optional[str] = Field(None, description="User timezone")
    user_preferences: Optional[str] = Field(None, description="User preferences")
    status: str = Field(default="active", description="User status")


class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    mobile_no: Optional[str] = Field(None, description="User mobile number")
    email: Optional[str] = Field(None, description="User email address")
    full_name: Optional[str] = Field(None, min_length=1, max_length=100, description="User full name")
    state: Optional[str] = Field(None, description="User state")
    referral_code: Optional[str] = Field(None, description="User referral code")
    referred_by: Optional[str] = Field(None, description="Referred by user")
    profile_data: Optional[str] = Field(None, description="User profile data")
    language_code: Optional[str] = Field(None, description="Language code")
    language_name: Optional[str] = Field(None, description="Language name")
    region_code: Optional[str] = Field(None, description="Region code")
    timezone: Optional[str] = Field(None, description="User timezone")
    user_preferences: Optional[str] = Field(None, description="User preferences")
    status: Optional[str] = Field(None, description="User status")


class UserResponse(BaseModel):
    """Schema for user response"""
    id: str = Field(..., description="User ID")
    mobile_no: str = Field(..., description="User mobile number")
    email: Optional[str] = Field(None, description="User email address")
    full_name: Optional[str] = Field(None, min_length=1, max_length=100, description="User full name")
    state: Optional[str] = Field(None, description="User state")
    referral_code: Optional[str] = Field(None, description="User referral code")
    referred_by: Optional[str] = Field(None, description="Referred by user")
    profile_data: Optional[str] = Field(None, description="User profile data")
    language_code: Optional[str] = Field(None, description="Language code")
    language_name: Optional[str] = Field(None, description="Language name")
    region_code: Optional[str] = Field(None, description="Region code")
    timezone: Optional[str] = Field(None, description="User timezone")
    user_preferences: Optional[str] = Field(None, description="User preferences")
    status: str = Field(default="active", description="User status")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime = Field(..., description="User last update timestamp")
    
    model_config = ConfigDict(from_attributes=True) 