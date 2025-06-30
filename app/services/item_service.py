import logging
from typing import List, Optional
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.models.item import Item
from app.repositories.item_repository import ItemRepository

logger = logging.getLogger(__name__)


class ItemService:
    """Item business logic service"""
    
    def __init__(self):
        self.item_repository = ItemRepository()
    
    async def get_items(self, skip: int = 0, limit: int = 100) -> List[ItemResponse]:
        """Get all items with pagination"""
        try:
            items = await self.item_repository.get_all(skip=skip, limit=limit)
            return [ItemResponse.from_orm(item) for item in items]
        except Exception as e:
            logger.error(f"Error getting items: {e}")
            raise
    
    async def get_item_by_id(self, item_id: int) -> Optional[ItemResponse]:
        """Get item by ID"""
        try:
            item = await self.item_repository.get_by_id(item_id)
            if item:
                return ItemResponse.from_orm(item)
            return None
        except Exception as e:
            logger.error(f"Error getting item {item_id}: {e}")
            raise
    
    async def create_item(self, item_data: ItemCreate) -> ItemResponse:
        """Create a new item"""
        try:
            # Business logic validation
            if item_data.price < 0:
                raise ValueError("Price cannot be negative")
            
            if item_data.quantity < 0:
                raise ValueError("Quantity cannot be negative")
            
            item = await self.item_repository.create(item_data)
            logger.info(f"Created item with ID: {item.id}")
            return ItemResponse.from_orm(item)
        except Exception as e:
            logger.error(f"Error creating item: {e}")
            raise
    
    async def update_item(self, item_id: int, item_data: ItemUpdate) -> Optional[ItemResponse]:
        """Update an existing item"""
        try:
            item = await self.item_repository.get_by_id(item_id)
            if not item:
                return None
            
            # Business logic validation
            if item_data.price is not None and item_data.price < 0:
                raise ValueError("Price cannot be negative")
            
            if item_data.quantity is not None and item_data.quantity < 0:
                raise ValueError("Quantity cannot be negative")
            
            updated_item = await self.item_repository.update(item_id, item_data)
            logger.info(f"Updated item with ID: {item_id}")
            return ItemResponse.from_orm(updated_item)
        except Exception as e:
            logger.error(f"Error updating item {item_id}: {e}")
            raise
    
    async def delete_item(self, item_id: int) -> bool:
        """Delete an item"""
        try:
            success = await self.item_repository.delete(item_id)
            if success:
                logger.info(f"Deleted item with ID: {item_id}")
            return success
        except Exception as e:
            logger.error(f"Error deleting item {item_id}: {e}")
            raise 