import logging
from typing import List, Optional
from app.schemas.item import ItemCreate, ItemUpdate
from app.models.item import Item
from datetime import datetime

logger = logging.getLogger(__name__)


class ItemRepository:
    """Item data access repository"""
    
    def __init__(self):
        # In-memory storage for demonstration
        # In production, this would be replaced with actual database operations
        self._items = {}
        self._next_id = 1
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """Get all items with pagination"""
        try:
            items = list(self._items.values())
            return items[skip:skip + limit]
        except Exception as e:
            logger.error(f"Error getting all items: {e}")
            raise
    
    async def get_by_id(self, item_id: int) -> Optional[Item]:
        """Get item by ID"""
        try:
            return self._items.get(item_id)
        except Exception as e:
            logger.error(f"Error getting item by ID {item_id}: {e}")
            raise
    
    async def create(self, item_data: ItemCreate) -> Item:
        """Create a new item"""
        try:
            item = Item(
                id=self._next_id,
                name=item_data.name,
                description=item_data.description,
                price=item_data.price,
                quantity=item_data.quantity,
                category=item_data.category,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self._items[item.id] = item
            self._next_id += 1
            
            logger.info(f"Created item with ID: {item.id}")
            return item
        except Exception as e:
            logger.error(f"Error creating item: {e}")
            raise
    
    async def update(self, item_id: int, item_data: ItemUpdate) -> Optional[Item]:
        """Update an existing item"""
        try:
            item = self._items.get(item_id)
            if not item:
                return None
            
            # Update only provided fields
            if item_data.name is not None:
                item.name = item_data.name
            if item_data.description is not None:
                item.description = item_data.description
            if item_data.price is not None:
                item.price = item_data.price
            if item_data.quantity is not None:
                item.quantity = item_data.quantity
            if item_data.category is not None:
                item.category = item_data.category
            
            item.updated_at = datetime.utcnow()
            
            logger.info(f"Updated item with ID: {item_id}")
            return item
        except Exception as e:
            logger.error(f"Error updating item {item_id}: {e}")
            raise
    
    async def delete(self, item_id: int) -> bool:
        """Delete an item"""
        try:
            if item_id in self._items:
                del self._items[item_id]
                logger.info(f"Deleted item with ID: {item_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting item {item_id}: {e}")
            raise 