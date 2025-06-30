from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.services.item_service import ItemService
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.core.dependencies import get_item_service

router = APIRouter()


@router.get("/", response_model=List[ItemResponse])
async def get_items(
    skip: int = 0,
    limit: int = 100,
    item_service: ItemService = Depends(get_item_service)
):
    """Get all items with pagination"""
    return await item_service.get_items(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    item_service: ItemService = Depends(get_item_service)
):
    """Get a specific item by ID"""
    item = await item_service.get_item_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: ItemCreate,
    item_service: ItemService = Depends(get_item_service)
):
    """Create a new item"""
    return await item_service.create_item(item_data)


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_data: ItemUpdate,
    item_service: ItemService = Depends(get_item_service)
):
    """Update an existing item"""
    item = await item_service.update_item(item_id, item_data)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    item_service: ItemService = Depends(get_item_service)
):
    """Delete an item"""
    success = await item_service.delete_item(item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        ) 