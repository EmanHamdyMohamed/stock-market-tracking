from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    # MongoDB settings
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_database: str = "stock_market_db"
    
    # API settings
    api_title: str = "Stock Market Backend API"
    api_version: str = "1.0.0"
    debug: bool = Field(default=False, description="Debug mode")
    
    @field_validator('debug', mode='before')
    @classmethod
    def parse_debug(cls, v):
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'on')
        return bool(v)
    
    # CORS settings
    # cors_origins: list[str] = Field(default_factory=list, description="List of CORS origins")
    CORS_ORIGINS: list[str] = Field(default=["http://localhost:3000", "http://localhost:3001"], description="List of CORS origins")
    
    # JWT settings
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_TIME: int = 24 * 60 * 60  # 24 hours in seconds
    
    TWELVE_DATA_SECRET_KEY: str = "your-secret-key"
    TWELVE_DATA_SECRET_API_KEY: str = "your-secret-key"
    
    # Environment settings
    # ENV: str = "local"
    
    class Config:
        env_file = ".env.local"
        case_sensitive = False


settings = Settings()
