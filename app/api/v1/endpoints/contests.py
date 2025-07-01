from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.services.contest_service import ContestService
from app.schemas.contest import ContestCreate, ContestResponse, ContestUpdate
from app.core.dependencies import get_contest_service

router = APIRouter()


@router.get("/", response_model=List[ContestResponse])
async def get_contests(
    limit: int = 100,
    contest_service: ContestService = Depends(get_contest_service)
):
    """Get all contests with pagination"""
    return await contest_service.get_contests(limit=limit)


@router.get("/active", response_model=List[ContestResponse])
async def get_active_contests(
    limit: int = 50,
    contest_service: ContestService = Depends(get_contest_service)
):
    """Get active contests"""
    return await contest_service.get_active_contests(limit=limit)


@router.get("/{contest_id}", response_model=ContestResponse)
async def get_contest(
    contest_id: str,
    contest_service: ContestService = Depends(get_contest_service)
):
    """Get a specific contest by ID"""
    contest = await contest_service.get_contest_by_id(contest_id)
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found"
        )
    return contest


@router.post("/", response_model=ContestResponse, status_code=status.HTTP_201_CREATED)
async def create_contest(
    contest_data: ContestCreate,
    contest_service: ContestService = Depends(get_contest_service)
):
    """Create a new contest"""
    return await contest_service.create_contest(contest_data)


@router.put("/{contest_id}", response_model=ContestResponse)
async def update_contest(
    contest_id: str,
    contest_data: ContestUpdate,
    contest_service: ContestService = Depends(get_contest_service)
):
    """Update an existing contest"""
    contest = await contest_service.update_contest(contest_id, contest_data)
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found"
        )
    return contest


@router.delete("/{contest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contest(
    contest_id: str,
    contest_service: ContestService = Depends(get_contest_service)
):
    """Delete a contest"""
    success = await contest_service.delete_contest(contest_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found"
        )


@router.post("/{contest_id}/increment-join", status_code=status.HTTP_200_OK)
async def increment_join_user(
    contest_id: str,
    contest_service: ContestService = Depends(get_contest_service)
):
    """Increment the number of users who joined the contest"""
    success = await contest_service.increment_join_user(contest_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found"
        )
    return {"message": "Join count incremented successfully"}


@router.post("/{contest_id}/increment-active", status_code=status.HTTP_200_OK)
async def increment_active_user(
    contest_id: str,
    contest_service: ContestService = Depends(get_contest_service)
):
    """Increment the number of active users in the contest"""
    success = await contest_service.increment_active_user(contest_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contest not found"
        )
    return {"message": "Active user count incremented successfully"} 