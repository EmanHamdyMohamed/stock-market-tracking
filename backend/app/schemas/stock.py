from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StockBase(BaseModel):
    """Base schema for Stock"""
    symbol: str
    """Stock symbol (e.g., AAPL, GOOGL)"""
    name: str
    """Company name"""
    price: float
    """Current stock price"""
    change_percent: Optional[float]
    """Percentage change from previous close"""
    volume: Optional[int]
    """Trading volume"""
    market_cap: Optional[float]
    """Market capitalization"""
    sector: Optional[str]
    """Stock sector (e.g., Technology, Healthcare)"""
    

class StockCreate(StockBase):
    """Schema for creating Stock"""
    pass


class StockUpdate(BaseModel):
    """Schema for updating Stock"""
    symbol: Optional[str]
    name: Optional[str]
    price: Optional[float]
    change_percent: Optional[float]
    volume: Optional[int]
    market_cap: Optional[float]
    sector: Optional[str]


class StockResponse(StockBase):
    """Schema for Stock response"""
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
