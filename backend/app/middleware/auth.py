
from fastapi import HTTPException
from starlette.requests import Request
import jwt

from app.core.config import Settings

settings = Settings()


async def authorize_token(request: Request, call_next):
    excluded_paths = ["/health", "/", "/docs", "/openapi.json", "/users/login", "/users/register", '/stocks/companies']
    if request.url.path in excluded_paths or request.method == "OPTIONS":
        response = await call_next(request)
        return response

    authorization = request.headers.get('authorization')
    print('authorization', authorization)
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    token = authorization.split("Bearer ")[1]
    print('token', token)
    if not token:
        raise HTTPException(status_code=401, detail="Empty token")
    print('token is not empty')
    try:
        decoded_token = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        print('decoded_token', decoded_token)
        if not decoded_token:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        # Add user info to request state
        request.state.user = {
            "id": decoded_token.get('user_id', decoded_token.get('id')),
            "name": decoded_token.get('name'),
            "email": decoded_token.get('email'),
            "watchlist": decoded_token.get('watchlist', []),
            "preferred_sectors": decoded_token.get('preferred_sectors', [])
        }
        print('request.state.user', request.state.user)
        return await call_next(request)
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=401, detail="Authentication failed", headers={"WWW-Authenticate": "Bearer"})
