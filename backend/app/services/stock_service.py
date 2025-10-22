from typing import List, Optional
from app.schemas.stock import StockCreate, StockUpdate, StockResponse
from app.models.stock import Stock
from mongoengine.errors import DoesNotExist, ValidationError


class StockService:
    """Service layer for Stock operations using MongoEngine"""
    
    PREDEFINED_COMPANIES = [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        {"symbol": "GOOGL", "name": "Alphabet Inc."},
        {"symbol": "AMZN", "name": "Amazon.com Inc."},
        {"symbol": "TSLA", "name": "Tesla Inc."},
        {"symbol": "META", "name": "Meta Platforms Inc."},
        {"symbol": "NVDA", "name": "NVIDIA Corporation"},
        {"symbol": "JPM", "name": "JPMorgan Chase & Co."},
        {"symbol": "V", "name": "Visa Inc."},
        {"symbol": "WMT", "name": "Walmart Inc."}
    ]
    
    def __init__(self):
        self.predefined_companies = self.get_predefined_companies()
        # self.predefined_companies_db = self.get_predefined_companies_db()

    def get_predefined_companies(self) -> List[Stock]:
        """Get predefined companies"""
        return [Stock(**company) for company in self.PREDEFINED_COMPANIES]
    
    # def get_predefined_companies_db(self) -> List[Stock]:
    #     """Get predefined companies"""
    #     return [Stock(**company) for company in self.predefined_companies_db]
    
    async def create_stock(self, stock_data: StockCreate) -> StockResponse:
        """Create a new Stock"""
        try:
            # Convert Pydantic model to dict and create MongoEngine document
            stock_dict = stock_data.model_dump()
            db_stock = Stock(**stock_dict)
            db_stock.save()
            
            # Convert back to response format
            return StockResponse(
                id=str(db_stock.id),
                symbol=db_stock.symbol,
                name=db_stock.name,
                price=db_stock.price,
                change_percent=db_stock.change_percent,
                volume=db_stock.volume,
                market_cap=db_stock.market_cap,
                sector=db_stock.sector,
                created_at=db_stock.created_at,
                updated_at=db_stock.updated_at
            )
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")
    
    async def get_stock(self, stock_id: str) -> Optional[StockResponse]:
        """Get a Stock by ID"""
        try:
            db_stock = Stock.objects.get(id=stock_id)
            return StockResponse(
                id=str(db_stock.id),
                symbol=db_stock.symbol,
                name=db_stock.name,
                price=db_stock.price,
                change_percent=db_stock.change_percent,
                volume=db_stock.volume,
                market_cap=db_stock.market_cap,
                sector=db_stock.sector,
                created_at=db_stock.created_at,
                updated_at=db_stock.updated_at
            )
        except DoesNotExist:
            return None
    
    async def get_stocks(self, skip: int = 0, limit: int = 100) -> List[StockResponse]:
        """Get all Stocks with pagination"""
        db_stocks = Stock.objects.skip(skip).limit(limit).order_by('-created_at')
        
        return [
            StockResponse(
                id=str(stock.id),
                symbol=stock.symbol,
                name=stock.name,
                price=stock.price,
                change_percent=stock.change_percent,
                volume=stock.volume,
                market_cap=stock.market_cap,
                sector=stock.sector,
                created_at=stock.created_at,
                updated_at=stock.updated_at
            )
            for stock in db_stocks
        ]
    
    async def update_stock(self, stock_id: str, stock_data: StockUpdate) -> Optional[StockResponse]:
        """Update a Stock"""
        try:
            db_stock = Stock.objects.get(id=stock_id)
            
            # Update only provided fields
            update_data = stock_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_stock, field, value)
            
            db_stock.save()
            
            return StockResponse(
                id=str(db_stock.id),
                symbol=db_stock.symbol,
                name=db_stock.name,
                price=db_stock.price,
                change_percent=db_stock.change_percent,
                volume=db_stock.volume,
                market_cap=db_stock.market_cap,
                sector=db_stock.sector,
                created_at=db_stock.created_at,
                updated_at=db_stock.updated_at
            )
        except DoesNotExist:
            return None
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")
    
    async def delete_stock(self, stock_id: str) -> bool:
        """Delete a Stock"""
        try:
            db_stock = Stock.objects.get(id=stock_id)
            db_stock.delete()
            return True
        except DoesNotExist:
            return False
    
    async def get_stock_by_symbol(self, symbol: str) -> Optional[StockResponse]:
        """Get a Stock by symbol"""
        try:
            db_stock = Stock.objects.get(symbol=symbol.upper())
            return StockResponse(
                id=str(db_stock.id),
                symbol=db_stock.symbol,
                name=db_stock.name,
                price=db_stock.price,
                change_percent=db_stock.change_percent,
                volume=db_stock.volume,
                market_cap=db_stock.market_cap,
                sector=db_stock.sector,
                created_at=db_stock.created_at,
                updated_at=db_stock.updated_at
            )
        except DoesNotExist:
            return None
