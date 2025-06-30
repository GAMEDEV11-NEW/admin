from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.dependencies import get_user_service

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users(
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
):
    """Get all users with pagination"""
    return await user_service.get_users(limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """Get a specific user by ID"""
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/mobile/{mobile_no}", response_model=UserResponse)
async def get_user_by_mobile(
    mobile_no: str,
    user_service: UserService = Depends(get_user_service)
):
    """Get a specific user by mobile number"""
    user = await user_service.get_user_by_mobile(mobile_no)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/email/{email}", response_model=UserResponse)
async def get_user_by_email(
    email: str,
    user_service: UserService = Depends(get_user_service)
):
    """Get a specific user by email"""
    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user"""
    return await user_service.create_user(user_data)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    """Update an existing user"""
    user = await user_service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
):
    """Delete a user"""
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        ) 