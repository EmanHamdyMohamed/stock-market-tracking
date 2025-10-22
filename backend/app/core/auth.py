from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.user_service import UserService
from app.schemas.user import UserResponse

security = HTTPBearer()
user_service = UserService()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
    """Get current authenticated user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Simple token parsing - in production, use JWT
        token = credentials.credentials
        if not token.startswith("token_"):
            raise credentials_exception
        
        # Extract user info from token
        parts = token.split("_")
        if len(parts) != 3:
            raise credentials_exception
        
        user_id = parts[1]
        username = parts[2]
        
        # Get user from database
        user = await user_service.get_user(user_id)
        if user is None or user.username != username:
            raise credentials_exception
        
        return user
        
    except Exception:
        raise credentials_exception


async def get_current_active_user(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def get_current_admin_user(current_user: UserResponse = Depends(get_current_active_user)) -> UserResponse:
    """Get current admin user"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
