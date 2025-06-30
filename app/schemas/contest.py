from pydantic import BaseModel, Field
from typing import Optional


class ContestBase(BaseModel):
    """Base contest schema"""
    contest_name: str = Field(..., description="Contest name")
    contest_win_price: str = Field(..., description="Contest win price")
    contest_entryfee: str = Field(..., description="Contest entry fee")
    contest_joinuser: int = Field(..., ge=0, description="Number of joined users")
    contest_activeuser: int = Field(..., ge=0, description="Number of active users")
    contest_starttime: str = Field(..., description="Contest start time")
    contest_endtime: str = Field(..., description="Contest end time")


class ContestCreate(ContestBase):
    """Schema for creating a new contest"""
    pass


class ContestUpdate(BaseModel):
    """Schema for updating a contest"""
    contest_name: Optional[str] = Field(None, description="Contest name")
    contest_win_price: Optional[str] = Field(None, description="Contest win price")
    contest_entryfee: Optional[str] = Field(None, description="Contest entry fee")
    contest_joinuser: Optional[int] = Field(None, ge=0, description="Number of joined users")
    contest_activeuser: Optional[int] = Field(None, ge=0, description="Number of active users")
    contest_starttime: Optional[str] = Field(None, description="Contest start time")
    contest_endtime: Optional[str] = Field(None, description="Contest end time")


class ContestResponse(ContestBase):
    """Schema for contest response"""
    contest_id: str = Field(..., description="Contest ID")
    
    class Config:
        from_attributes = True 