from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """Base schema for User"""
    email: EmailStr
    name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """Schema for creating User"""
    password: str = Field(..., min_length=8, max_length=100)
    watchlist: Optional[List[str]] = Field(default_factory=list)
    preferred_sectors: Optional[List[str]] = Field(default_factory=list)


class UserUpdate(BaseModel):
    """Schema for updating User"""
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    watchlist: Optional[List[str]] = None
    preferred_sectors: Optional[List[str]] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for User response"""
    id: str
    is_active: bool
    is_verified: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    watchlist: List[str]
    preferred_sectors: List[str]
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""
    email: str
    password: str


class UserPasswordChange(BaseModel):
    """Schema for password change"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)


class UserWatchlistUpdate(BaseModel):
    """Schema for updating user watchlist"""
    watchlist: List[str] = Field(..., max_items=50)


class UserPreferencesUpdate(BaseModel):
    """Schema for updating user preferences"""
    preferred_sectors: Optional[List[str]] = None
    email_notifications: Optional[bool] = None
    price_alerts: Optional[bool] = None
    news_updates: Optional[bool] = None


class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data"""
    email: Optional[str] = None
