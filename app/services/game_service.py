import logging
from typing import List, Optional
from app.schemas.game import GameCreate, GameResponse, GameUpdate
from app.repositories.game_repository import GameRepository

logger = logging.getLogger(__name__)


class GameService:
    """Game business logic service"""
    
    def __init__(self):
        self.game_repository = GameRepository()
    
    async def get_all_games(self, limit: int = 100) -> List[GameResponse]:
        """Get all games"""
        try:
            games = await self.game_repository.get_all_games(limit=limit)
            return [GameResponse(**game) for game in games]
        except Exception as e:
            logger.error(f"Error getting all games: {e}")
            raise
    
    async def get_game_by_id(self, game_id: str) -> Optional[GameResponse]:
        """Get game by ID"""
        try:
            game = await self.game_repository.get_game_by_id(game_id)
            if game:
                return GameResponse(**game)
            return None
        except Exception as e:
            logger.error(f"Error getting game {game_id}: {e}")
            raise
    
    async def get_active_games(self, limit: int = 100) -> List[GameResponse]:
        """Get active games"""
        try:
            games = await self.game_repository.get_active_games(limit=limit)
            return [GameResponse(**game) for game in games]
        except Exception as e:
            logger.error(f"Error getting active games: {e}")
            raise
    
    async def get_featured_games(self, limit: int = 50) -> List[GameResponse]:
        """Get featured games"""
        try:
            games = await self.game_repository.get_featured_games(limit=limit)
            return [GameResponse(**game) for game in games]
        except Exception as e:
            logger.error(f"Error getting featured games: {e}")
            raise
    
    async def get_games_by_category(self, category: str, limit: int = 50) -> List[GameResponse]:
        """Get games by category"""
        try:
            games = await self.game_repository.get_games_by_category(category, limit=limit)
            return [GameResponse(**game) for game in games]
        except Exception as e:
            logger.error(f"Error getting games by category {category}: {e}")
            raise
    
    async def create_game(self, game_data: GameCreate) -> GameResponse:
        """Create a new game"""
        try:
            # Business logic validation
            if game_data.min_players > game_data.max_players:
                raise ValueError("Minimum players cannot be greater than maximum players")
            
            if game_data.rating < 0 or game_data.rating > 5:
                raise ValueError("Rating must be between 0 and 5")
            
            game = await self.game_repository.create_game(game_data)
            logger.info(f"Created game with ID: {game['id']}")
            return GameResponse(**game)
        except Exception as e:
            logger.error(f"Error creating game: {e}")
            raise
    
    async def update_game(self, game_id: str, game_data: GameUpdate) -> Optional[GameResponse]:
        """Update an existing game"""
        try:
            # Business logic validation
            if game_data.min_players is not None and game_data.max_players is not None:
                if game_data.min_players > game_data.max_players:
                    raise ValueError("Minimum players cannot be greater than maximum players")
            
            if game_data.rating is not None:
                if game_data.rating < 0 or game_data.rating > 5:
                    raise ValueError("Rating must be between 0 and 5")
            
            game = await self.game_repository.update_game(game_id, game_data)
            if game:
                logger.info(f"Updated game with ID: {game_id}")
                return GameResponse(**game)
            return None
        except Exception as e:
            logger.error(f"Error updating game {game_id}: {e}")
            raise
    
    async def delete_game(self, game_id: str) -> bool:
        """Delete a game"""
        try:
            success = await self.game_repository.delete_game(game_id)
            if success:
                logger.info(f"Deleted game with ID: {game_id}")
            return success
        except Exception as e:
            logger.error(f"Error deleting game {game_id}: {e}")
            raise
    
    async def toggle_game_status(self, game_id: str) -> Optional[GameResponse]:
        """Toggle game active status"""
        try:
            game = await self.get_game_by_id(game_id)
            if not game:
                return None
            
            update_data = GameUpdate(is_active=not game.is_active)
            return await self.update_game(game_id, update_data)
        except Exception as e:
            logger.error(f"Error toggling game status {game_id}: {e}")
            raise
    
    async def toggle_featured_status(self, game_id: str) -> Optional[GameResponse]:
        """Toggle game featured status"""
        try:
            game = await self.get_game_by_id(game_id)
            if not game:
                return None
            
            update_data = GameUpdate(is_featured=not game.is_featured)
            return await self.update_game(game_id, update_data)
        except Exception as e:
            logger.error(f"Error toggling featured status {game_id}: {e}")
            raise 