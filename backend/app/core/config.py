from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # MongoDB settings
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_database: str = "stock_market_db"
    
    # API settings
    api_title: str = "Stock Market Backend API"
    api_version: str = "1.0.0"
    debug: bool = False
    
    # CORS settings
    cors_origins: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
