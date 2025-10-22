from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Request
)
import jwt
from datetime import datetime, timezone, timedelta
from typing import List
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin, 
    UserWatchlistUpdate,
    UserPreferencesUpdate,
    Token
)
from app.services.user_service import UserService
from app.dependencies import SettingsDependency


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
async def login_user(
    login_data: UserLogin,
    settings: SettingsDependency
):
    """Login user and return token"""
    user: UserResponse = await user_service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=15)
    # datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_EXPIRATION_TIME)
    payload = {
        "user_id": user.id,
        "email": user.email,
        "name": user.name,
        "watchlist": user.watchlist,
        "preferred_sectors": user.preferred_sectors,
        "exp": expiration_time
    }
    print(payload)
    access_token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        # headers=headers
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=expiration_time
    )


@router.get("/me", response_model=UserResponse)
async def get_user_profile(
    request: Request,
    settings: SettingsDependency
):
    """Get user profile"""
    try:
        user = request.state.user
        
        print('user', user)
        db_user = await user_service.get_user(user['id'])
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user_response = UserResponse(
            id=user['id'],
            email=user['email'],
            name=user['name'],
            watchlist=db_user.watchlist,
            preferred_sectors=db_user.preferred_sectors,
            is_active=db_user.is_active,
            is_verified=db_user.is_verified,
            is_admin=db_user.is_admin,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            last_login=db_user.last_login,
        )
        return user_response
    except Exception as e:
        print('error', e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )


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
