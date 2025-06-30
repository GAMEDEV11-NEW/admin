import logging
from typing import List, Optional
from datetime import datetime
from cassandra.cluster import Session
from app.schemas.game import GameCreate, GameUpdate
from app.core.database import get_cassandra_session

logger = logging.getLogger(__name__)


class GameRepository:
    """Game data access repository for Cassandra"""
    
    def __init__(self):
        self.session: Session = get_cassandra_session()
    
    async def get_all_games(self, limit: int = 100) -> List[dict]:
        """Get all games"""
        try:
            query = "SELECT * FROM games LIMIT %s"
            rows = self.session.execute(query, (limit,))
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all games: {e}")
            raise
    
    async def get_game_by_id(self, game_id: str) -> Optional[dict]:
        """Get game by ID"""
        try:
            query = "SELECT * FROM games WHERE id = %s"
            row = self.session.execute(query, (game_id,)).one()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting game by ID {game_id}: {e}")
            raise
    
    async def get_active_games(self, limit: int = 100) -> List[dict]:
        """Get active games"""
        try:
            query = "SELECT * FROM games WHERE is_active = true LIMIT %s"
            rows = self.session.execute(query, (limit,))
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting active games: {e}")
            raise
    
    async def get_featured_games(self, limit: int = 50) -> List[dict]:
        """Get featured games"""
        try:
            query = "SELECT * FROM games WHERE is_featured = true LIMIT %s"
            rows = self.session.execute(query, (limit,))
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting featured games: {e}")
            raise
    
    async def get_games_by_category(self, category: str, limit: int = 50) -> List[dict]:
        """Get games by category"""
        try:
            query = "SELECT * FROM games WHERE category = %s LIMIT %s"
            rows = self.session.execute(query, (category, limit))
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting games by category {category}: {e}")
            raise
    
    async def create_game(self, game_data: GameCreate) -> dict:
        """Create a new game"""
        try:
            now = datetime.utcnow().isoformat()
            game_id = f"game_{now}_{hash(game_data.name)}"
            
            query = """
                INSERT INTO games (
                    id, name, description, category, icon, banner,
                    min_players, max_players, difficulty, rating,
                    is_active, is_featured, tags, metadata,
                    created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.session.execute(query, (
                game_id,
                game_data.name,
                game_data.description,
                game_data.category,
                game_data.icon,
                game_data.banner,
                game_data.min_players,
                game_data.max_players,
                game_data.difficulty,
                game_data.rating,
                game_data.is_active,
                game_data.is_featured,
                game_data.tags or [],
                game_data.metadata or {},
                now,
                now
            ))
            
            # Return the created game
            return {
                "id": game_id,
                "name": game_data.name,
                "description": game_data.description,
                "category": game_data.category,
                "icon": game_data.icon,
                "banner": game_data.banner,
                "min_players": game_data.min_players,
                "max_players": game_data.max_players,
                "difficulty": game_data.difficulty,
                "rating": game_data.rating,
                "is_active": game_data.is_active,
                "is_featured": game_data.is_featured,
                "tags": game_data.tags or [],
                "metadata": game_data.metadata or {},
                "created_at": now,
                "updated_at": now
            }
        except Exception as e:
            logger.error(f"Error creating game: {e}")
            raise
    
    async def update_game(self, game_id: str, game_data: GameUpdate) -> Optional[dict]:
        """Update an existing game"""
        try:
            now = datetime.utcnow().isoformat()
            
            # Build dynamic update query
            update_fields = []
            values = []
            
            if game_data.name is not None:
                update_fields.append("name = %s")
                values.append(game_data.name)
            
            if game_data.description is not None:
                update_fields.append("description = %s")
                values.append(game_data.description)
            
            if game_data.category is not None:
                update_fields.append("category = %s")
                values.append(game_data.category)
            
            if game_data.icon is not None:
                update_fields.append("icon = %s")
                values.append(game_data.icon)
            
            if game_data.banner is not None:
                update_fields.append("banner = %s")
                values.append(game_data.banner)
            
            if game_data.min_players is not None:
                update_fields.append("min_players = %s")
                values.append(game_data.min_players)
            
            if game_data.max_players is not None:
                update_fields.append("max_players = %s")
                values.append(game_data.max_players)
            
            if game_data.difficulty is not None:
                update_fields.append("difficulty = %s")
                values.append(game_data.difficulty)
            
            if game_data.rating is not None:
                update_fields.append("rating = %s")
                values.append(game_data.rating)
            
            if game_data.is_active is not None:
                update_fields.append("is_active = %s")
                values.append(game_data.is_active)
            
            if game_data.is_featured is not None:
                update_fields.append("is_featured = %s")
                values.append(game_data.is_featured)
            
            if game_data.tags is not None:
                update_fields.append("tags = %s")
                values.append(game_data.tags)
            
            if game_data.metadata is not None:
                update_fields.append("metadata = %s")
                values.append(game_data.metadata)
            
            update_fields.append("updated_at = %s")
            values.append(now)
            
            if not update_fields:
                return None
            
            query = f"""
                UPDATE games 
                SET {', '.join(update_fields)}
                WHERE id = %s
            """
            values.append(game_id)
            
            self.session.execute(query, values)
            
            # Return updated game
            return await self.get_game_by_id(game_id)
        except Exception as e:
            logger.error(f"Error updating game {game_id}: {e}")
            raise
    
    async def delete_game(self, game_id: str) -> bool:
        """Delete a game"""
        try:
            query = "DELETE FROM games WHERE id = %s"
            self.session.execute(query, (game_id,))
            return True
        except Exception as e:
            logger.error(f"Error deleting game {game_id}: {e}")
            raise 