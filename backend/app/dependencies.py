from typing import Annotated

from fastapi import Depends

from app.core.config import Settings
from app.services.stock_service import StockService


def get_settings_from_env():
    return Settings()


def get_stock_service():
    return StockService()


# Type alias for dependency injection
SettingsDependency = Annotated[Settings, Depends(get_settings_from_env)]
StockServiceDependency = Annotated[StockService, Depends(get_stock_service)]
