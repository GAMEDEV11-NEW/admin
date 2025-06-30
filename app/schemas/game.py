from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class GameBase(BaseModel):
    """Base game schema"""
    name: str = Field(..., description="Game name")
    description: Optional[str] = Field(None, description="Game description")
    category: str = Field(..., description="Game category")
    icon: Optional[str] = Field(None, description="Game icon URL")
    banner: Optional[str] = Field(None, description="Game banner URL")
    min_players: int = Field(..., ge=1, description="Minimum players")
    max_players: int = Field(..., ge=1, description="Maximum players")
    difficulty: str = Field(..., description="Game difficulty")
    rating: float = Field(..., ge=0, le=5, description="Game rating")
    is_active: bool = Field(default=True, description="Game active status")
    is_featured: bool = Field(default=False, description="Featured game status")
    tags: Optional[List[str]] = Field(default=[], description="Game tags")
    metadata: Optional[Dict[str, str]] = Field(default={}, description="Game metadata")


class GameCreate(GameBase):
    """Schema for creating a new game"""
    pass


class GameUpdate(BaseModel):
    """Schema for updating a game"""
    name: Optional[str] = Field(None, description="Game name")
    description: Optional[str] = Field(None, description="Game description")
    category: Optional[str] = Field(None, description="Game category")
    icon: Optional[str] = Field(None, description="Game icon URL")
    banner: Optional[str] = Field(None, description="Game banner URL")
    min_players: Optional[int] = Field(None, ge=1, description="Minimum players")
    max_players: Optional[int] = Field(None, ge=1, description="Maximum players")
    difficulty: Optional[str] = Field(None, description="Game difficulty")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Game rating")
    is_active: Optional[bool] = Field(None, description="Game active status")
    is_featured: Optional[bool] = Field(None, description="Featured game status")
    tags: Optional[List[str]] = Field(None, description="Game tags")
    metadata: Optional[Dict[str, str]] = Field(None, description="Game metadata")


class GameResponse(GameBase):
    """Schema for game response"""
    id: str = Field(..., description="Game ID")
    created_at: str = Field(..., description="Game creation time")
    updated_at: str = Field(..., description="Game last update time")
    
    class Config:
        from_attributes = True 