from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID


class LeagueJoinBase(BaseModel):
    """Base league join schema"""
    league_id: str = Field(..., description="League ID")
    status: str = Field(..., description="Join status")
    user_id: str = Field(..., description="User ID")
    invite_code: Optional[str] = Field(None, description="Invite code")
    role: Optional[str] = Field(default="member", description="User role in league")
    extra_data: Optional[str] = Field(None, description="Extra data")


class LeagueJoinCreate(LeagueJoinBase):
    """Schema for creating a new league join"""
    pass


class LeagueJoinUpdate(BaseModel):
    """Schema for updating a league join"""
    status: Optional[str] = Field(None, description="Join status")
    invite_code: Optional[str] = Field(None, description="Invite code")
    role: Optional[str] = Field(None, description="User role in league")
    extra_data: Optional[str] = Field(None, description="Extra data")
    status_id: Optional[str] = Field(None, description="Status ID")


class LeagueJoinResponse(LeagueJoinBase):
    """Schema for league join response"""
    id: UUID = Field(..., description="Join ID")
    joined_at: str = Field(..., description="Join timestamp")
    updated_at: str = Field(..., description="Last update timestamp")
    status_id: Optional[str] = Field(None, description="Status ID")
    
    model_config = ConfigDict(from_attributes=True) 