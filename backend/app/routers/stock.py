from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.stock import StockCreate, StockUpdate, StockResponse
from app.services.stock_service import StockService

router = APIRouter(prefix="/stocks", tags=["Stocks"])

# Dependency to get service instance
def get_stock_service() -> StockService:
    return StockService()

@router.post("/", response_model=StockResponse)
async def create_stock(
    stock_data: StockCreate,
    service: StockService = Depends(get_stock_service)
):
    """Create a new Stock"""
    return await service.create_stock(stock_data)

@router.get("/", response_model=List[StockResponse])
async def get_stocks(
    skip: int = 0,
    limit: int = 100,
    service: StockService = Depends(get_stock_service)
):
    """Get all Stocks with pagination"""
    return await service.get_stocks(skip=skip, limit=limit)

@router.get("/{id}", response_model=StockResponse)
async def get_stock(
    id: int,
    service: StockService = Depends(get_stock_service)
):
    """Get a Stock by ID"""
    stock = await service.get_stock(id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@router.put("/{id}", response_model=StockResponse)
async def update_stock(
    id: int,
    stock_data: StockUpdate,
    service: StockService = Depends(get_stock_service)
):
    """Update a Stock"""
    stock = await service.update_stock(id, stock_data)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock

@router.delete("/{id}")
async def delete_stock(
    id: int,
    service: StockService = Depends(get_stock_service)
):
    """Delete a Stock"""
    success = await service.delete_stock(id)
    if not success:
        raise HTTPException(status_code=404, detail="Stock not found")
    return {"message": "Stock deleted successfully"}
