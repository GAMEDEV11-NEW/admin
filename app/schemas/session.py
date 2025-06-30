from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SessionBase(BaseModel):
    """Base session schema"""
    mobile_no: str = Field(..., description="Mobile number")
    device_id: str = Field(..., description="Device identifier")
    session_token: str = Field(..., description="Session token")
    user_id: str = Field(..., description="User ID")
    jwt_token: Optional[str] = Field(None, description="JWT token")
    fcm_token: Optional[str] = Field(None, description="FCM token")
    is_active: bool = Field(default=True, description="Session active status")


class SessionCreate(SessionBase):
    """Schema for creating a new session"""
    expires_at: datetime = Field(..., description="Session expiration time")


class SessionUpdate(BaseModel):
    """Schema for updating a session"""
    jwt_token: Optional[str] = Field(None, description="JWT token")
    fcm_token: Optional[str] = Field(None, description="FCM token")
    is_active: Optional[bool] = Field(None, description="Session active status")
    expires_at: Optional[datetime] = Field(None, description="Session expiration time")


class SessionResponse(SessionBase):
    """Schema for session response"""
    created_at: datetime = Field(..., description="Session creation time")
    expires_at: datetime = Field(..., description="Session expiration time")
    updated_at: datetime = Field(..., description="Session last update time")
    
    class Config:
        from_attributes = True 