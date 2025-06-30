from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.services.game_service import GameService
from app.schemas.game import GameCreate, GameResponse, GameUpdate
from app.core.dependencies import get_game_service

router = APIRouter()


@router.get("/", response_model=List[GameResponse])
async def get_all_games(
    limit: int = 100,
    game_service: GameService = Depends(get_game_service)
):
    """Get all games"""
    return await game_service.get_all_games(limit=limit)


@router.get("/active", response_model=List[GameResponse])
async def get_active_games(
    limit: int = 100,
    game_service: GameService = Depends(get_game_service)
):
    """Get active games"""
    return await game_service.get_active_games(limit=limit)


@router.get("/featured", response_model=List[GameResponse])
async def get_featured_games(
    limit: int = 50,
    game_service: GameService = Depends(get_game_service)
):
    """Get featured games"""
    return await game_service.get_featured_games(limit=limit)


@router.get("/category/{category}", response_model=List[GameResponse])
async def get_games_by_category(
    category: str,
    limit: int = 50,
    game_service: GameService = Depends(get_game_service)
):
    """Get games by category"""
    return await game_service.get_games_by_category(category, limit=limit)


@router.get("/{game_id}", response_model=GameResponse)
async def get_game(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """Get a specific game by ID"""
    game = await game_service.get_game_by_id(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return game


@router.post("/", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
async def create_game(
    game_data: GameCreate,
    game_service: GameService = Depends(get_game_service)
):
    """Create a new game"""
    return await game_service.create_game(game_data)


@router.put("/{game_id}", response_model=GameResponse)
async def update_game(
    game_id: str,
    game_data: GameUpdate,
    game_service: GameService = Depends(get_game_service)
):
    """Update an existing game"""
    game = await game_service.update_game(game_id, game_data)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return game


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """Delete a game"""
    success = await game_service.delete_game(game_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )


@router.post("/{game_id}/toggle-status", response_model=GameResponse)
async def toggle_game_status(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """Toggle game active status"""
    game = await game_service.toggle_game_status(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return game


@router.post("/{game_id}/toggle-featured", response_model=GameResponse)
async def toggle_featured_status(
    game_id: str,
    game_service: GameService = Depends(get_game_service)
):
    """Toggle game featured status"""
    game = await game_service.toggle_featured_status(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return game 