from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.services.league_join_service import LeagueJoinService
from app.schemas.league_join import LeagueJoinCreate, LeagueJoinResponse, LeagueJoinUpdate
from app.core.dependencies import get_league_join_service

router = APIRouter()


@router.get("/", response_model=List[LeagueJoinResponse])
async def get_league_joins(
    limit: int = 100,
    league_join_service: LeagueJoinService = Depends(get_league_join_service)
):
    """Get all league joins with pagination"""
    return await league_join_service.get_league_joins(limit=limit)


@router.get("/league/{league_id}", response_model=List[LeagueJoinResponse])
async def get_league_joins_by_league_id(
    league_id: str,
    limit: int = 50,
    league_join_service: LeagueJoinService = Depends(get_league_join_service)
):
    """Get all joins for a specific league"""
    return await league_join_service.get_league_joins_by_league_id(league_id, limit=limit)


@router.get("/league/{league_id}/status/{status}", response_model=List[LeagueJoinResponse])
async def get_league_joins_by_status(
    league_id: str,
    status: str,
    limit: int = 50,
    league_join_service: LeagueJoinService = Depends(get_league_join_service)
):
    """Get league joins by status for a specific league"""
    return await league_join_service.get_league_joins_by_status(league_id, status, limit=limit)


@router.get("/user/{user_id}", response_model=List[LeagueJoinResponse])
async def get_user_league_joins(
    user_id: str,
    limit: int = 50,
    league_join_service: LeagueJoinService = Depends(get_league_join_service)
):
    """Get all league joins for a specific user"""
    return await league_join_service.get_user_league_joins(user_id, limit=limit)


@router.get("/invite-code/{invite_code}", response_model=List[LeagueJoinResponse])
async def get_league_joins_by_invite_code(
    invite_code: str,
    limit: int = 50,
    league_join_service: LeagueJoinService = Depends(get_league_join_service)
):
    """Get league joins by invite code"""
    return await league_join_service.get_league_joins_by_invite_code(invite_code, limit=limit)


@router.get("/league/{league_id}/user/{user_id}", response_model=LeagueJoinResponse)
async def get_league_join_by_user_and_league(
    league_id: str,
    user_id: str,
    league_join_service: LeagueJoinService = Depends(get_league_join_service)
):
    """Get specific league join by user and league"""
    join = await league_join_service.get_league_join_by_user_and_league(user_id, league_id)
    if not join:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="League join not found"
        )
    return join


@router.post("/", response_model=LeagueJoinResponse, status_code=status.HTTP_201_CREATED)
async def create_league_join(
    join_data: LeagueJoinCreate,
    league_join_service: LeagueJoinService = Depends(get_league_join_service)
):
    """Create a new league join"""
    return await league_join_service.create_league_join(join_data)


@router.put("/{league_id}/{status}/{user_id}/{joined_at}", response_model=LeagueJoinResponse)
async def update_league_join(
    league_id: str,
    status: str,
    user_id: str,
    joined_at: str,
    join_data: LeagueJoinUpdate,
    league_join_service: LeagueJoinService = Depends(get_league_join_service)
):
    """Update an existing league join"""
    join = await league_join_service.update_league_join(league_id, status, user_id, joined_at, join_data)
    if not join:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="League join not found"
        )
    return join


@router.delete("/{league_id}/{status}/{user_id}/{joined_at}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_league_join(
    league_id: str,
    status: str,
    user_id: str,
    joined_at: str,
    league_join_service: LeagueJoinService = Depends(get_league_join_service)
):
    """Delete a league join"""
    success = await league_join_service.delete_league_join(league_id, status, user_id, joined_at)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="League join not found"
        )


@router.put("/league/{league_id}/user/{user_id}/status", response_model=LeagueJoinResponse)
async def update_join_status(
    league_id: str,
    user_id: str,
    new_status: str,
    status_id: str = None,
    league_join_service: LeagueJoinService = Depends(get_league_join_service)
):
    """Update the status of a league join"""
    join = await league_join_service.update_join_status(league_id, user_id, new_status, status_id)
    if not join:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="League join not found"
        )
    return join


@router.get("/league/{league_id}/member-count", status_code=status.HTTP_200_OK)
async def get_league_member_count(
    league_id: str,
    status: str = "active",
    league_join_service: LeagueJoinService = Depends(get_league_join_service)
):
    """Get the count of members in a league with specific status"""
    count = await league_join_service.get_league_member_count(league_id, status)
    return {"league_id": league_id, "status": status, "member_count": count} 