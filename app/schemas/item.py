from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    """Base item schema"""
    name: str = Field(..., min_length=1, max_length=200, description="Item name")
    description: Optional[str] = Field(None, max_length=1000, description="Item description")
    price: float = Field(..., ge=0, description="Item price")
    quantity: int = Field(..., ge=0, description="Item quantity in stock")
    category: str = Field(..., min_length=1, max_length=100, description="Item category")


class ItemCreate(ItemBase):
    """Schema for creating a new item"""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Item name")
    description: Optional[str] = Field(None, max_length=1000, description="Item description")
    price: Optional[float] = Field(None, ge=0, description="Item price")
    quantity: Optional[int] = Field(None, ge=0, description="Item quantity in stock")
    category: Optional[str] = Field(None, min_length=1, max_length=100, description="Item category")


class ItemResponse(ItemBase):
    """Schema for item response"""
    id: int = Field(..., description="Item ID")
    created_at: datetime = Field(..., description="Item creation timestamp")
    updated_at: datetime = Field(..., description="Item last update timestamp")
    
    class Config:
        from_attributes = True 