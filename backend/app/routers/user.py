from fastapi import (
    APIRouter,
    HTTPException,
    status
)
from typing import List
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserLogin, 
    UserWatchlistUpdate, UserPreferencesUpdate, Token
)
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """Register a new user"""
    try:
        user = await user_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login_user(login_data: UserLogin):
    """Login user and return token"""
    user = await user_service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # For now, return a simple token. In production, use JWT tokens
    access_token = f"token_{user.id}_{user.email}"
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 100):
    """Get all users with pagination"""
    users = await user_service.get_users(skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get user by ID"""
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_data: UserUpdate):
    """Update user"""
    try:
        user = await user_service.update_user(user_id, user_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """Delete user"""
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


@router.put("/{user_id}/watchlist", response_model=UserResponse)
async def update_watchlist(user_id: str, watchlist_data: UserWatchlistUpdate):
    """Update user's watchlist"""
    user = await user_service.update_watchlist(user_id, watchlist_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/{user_id}/watchlist/{stock_symbol}", response_model=UserResponse)
async def add_to_watchlist(user_id: str, stock_symbol: str):
    """Add stock to user's watchlist"""
    user = await user_service.add_to_watchlist(user_id, stock_symbol)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.delete("/{user_id}/watchlist/{stock_symbol}", response_model=UserResponse)
async def remove_from_watchlist(user_id: str, stock_symbol: str):
    """Remove stock from user's watchlist"""
    user = await user_service.remove_from_watchlist(user_id, stock_symbol)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}/preferences", response_model=UserResponse)
async def update_preferences(user_id: str, preferences_data: UserPreferencesUpdate):
    """Update user's preferences"""
    user = await user_service.update_preferences(user_id, preferences_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/{user_id}/watchlist", response_model=List[str])
async def get_watchlist(user_id: str):
    """Get user's watchlist"""
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user.watchlist
