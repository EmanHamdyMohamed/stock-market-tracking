from typing import List, Optional
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserWatchlistUpdate,
    UserPreferencesUpdate
)
from app.models.user import User
from mongoengine.errors import (
    DoesNotExist,
    ValidationError,
    NotUniqueError
)
from datetime import datetime


class UserService:
    """Service layer for User operations using MongoEngine"""
    
    def __init__(self):
        pass
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new User"""
        try:
            # Check if email already exists
            if User.objects(email=user_data.email).first():
                raise ValueError("Email already exists")
            
            # Create new user
            db_user = User(
                email=user_data.email,
                name=user_data.name,
                watchlist=user_data.watchlist or [],
                preferred_sectors=user_data.preferred_sectors or []
            )
            
            # Set password hash
            db_user.set_password(user_data.password)
            db_user.save()
            
            return self._user_to_response(db_user)
            
        except NotUniqueError as e:
            raise ValueError(f"User with this email already exists: {e}")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")
    
    async def get_user(self, user_id: str) -> Optional[UserResponse]:
        """Get a User by ID"""
        try:
            db_user = User.objects.get(id=user_id)
            return self._user_to_response(db_user)
        except DoesNotExist:
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get a User by email"""
        try:
            db_user = User.objects.get(email=email)
            return self._user_to_response(db_user)
        except DoesNotExist:
            return None
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        """Get all Users with pagination"""
        db_users = User.objects.skip(skip).limit(limit).order_by('-created_at')
        return [self._user_to_response(user) for user in db_users]
    
    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[UserResponse]:
        """Update a User"""
        try:
            db_user = User.objects.get(id=user_id)
            
            # Update only provided fields
            update_data = user_data.model_dump(exclude_unset=True)
            
            # Handle password separately
            if 'password' in update_data:
                db_user.set_password(update_data.pop('password'))
            
            # Update other fields
            for field, value in update_data.items():
                if hasattr(db_user, field):
                    setattr(db_user, field, value)
            
            db_user.save()
            return self._user_to_response(db_user)
            
        except DoesNotExist:
            return None
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")
        except NotUniqueError as e:
            raise ValueError(f"Email already exists: {e}")
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete a User"""
        try:
            db_user = User.objects.get(id=user_id)
            db_user.delete()
            return True
        except DoesNotExist:
            return False
    
    async def authenticate_user(self, email: str, password: str) -> Optional[UserResponse]:
        """Authenticate user with email and password"""
        try:
            db_user = User.objects.get(email=email)
            if db_user.check_password(password) and db_user.is_active:
                # Update last login
                db_user.last_login = datetime.utcnow()
                db_user.save()
                return self._user_to_response(db_user)
            return None
        except DoesNotExist:
            return None
    
    async def update_watchlist(self, user_id: str, watchlist_data: UserWatchlistUpdate) -> Optional[UserResponse]:
        """Update user's watchlist"""
        try:
            db_user = User.objects.get(id=user_id)
            db_user.watchlist = watchlist_data.watchlist
            db_user.save()
            return self._user_to_response(db_user)
        except DoesNotExist:
            return None
    
    async def update_preferences(self, user_id: str, preferences_data: UserPreferencesUpdate) -> Optional[UserResponse]:
        """Update user's preferences"""
        try:
            db_user = User.objects.get(id=user_id)
            
            if preferences_data.preferred_sectors is not None:
                db_user.preferred_sectors = preferences_data.preferred_sectors
            
            # Update notification settings
            if preferences_data.email_notifications is not None:
                db_user.notification_settings['email_notifications'] = preferences_data.email_notifications
            if preferences_data.price_alerts is not None:
                db_user.notification_settings['price_alerts'] = preferences_data.price_alerts
            if preferences_data.news_updates is not None:
                db_user.notification_settings['news_updates'] = preferences_data.news_updates
            
            db_user.save()
            return self._user_to_response(db_user)
        except DoesNotExist:
            return None
    
    async def add_to_watchlist(self, user_id: str, stock_symbol: str) -> Optional[UserResponse]:
        """Add stock to user's watchlist"""
        try:
            db_user = User.objects.get(id=user_id)
            if stock_symbol.upper() not in db_user.watchlist:
                db_user.watchlist.append(stock_symbol.upper())
                db_user.save()
            return self._user_to_response(db_user)
        except DoesNotExist:
            return None
    
    async def remove_from_watchlist(self, user_id: str, stock_symbol: str) -> Optional[UserResponse]:
        """Remove stock from user's watchlist"""
        try:
            db_user = User.objects.get(id=user_id)
            if stock_symbol.upper() in db_user.watchlist:
                db_user.watchlist.remove(stock_symbol.upper())
                db_user.save()
            return self._user_to_response(db_user)
        except DoesNotExist:
            return None
    
    def _user_to_response(self, db_user: User) -> UserResponse:
        """Convert MongoEngine User to UserResponse"""
        return UserResponse(
            id=str(db_user.id),
            email=db_user.email,
            name=db_user.name,
            is_active=db_user.is_active,
            is_verified=db_user.is_verified,
            is_admin=db_user.is_admin,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            last_login=db_user.last_login,
            watchlist=db_user.watchlist,
            preferred_sectors=db_user.preferred_sectors
        )
