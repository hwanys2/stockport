from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


# Asset schemas
class AssetCreate(BaseModel):
    symbol: str
    name: str
    exchange: Optional[str] = None
    currency: str = "USD"
    asset_type: str = "stock"


class Asset(BaseModel):
    id: int
    symbol: str
    name: str
    exchange: Optional[str]
    currency: str
    asset_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class AssetSearch(BaseModel):
    symbol: str
    name: str
    exchange: Optional[str] = None
    current_price: Optional[float] = None


# Portfolio Item schemas
class PortfolioItemCreate(BaseModel):
    asset_id: int
    target_weight: float = Field(..., gt=0, le=100)
    tolerance: float = Field(default=5.0, ge=0, le=50)


class PortfolioItemUpdate(BaseModel):
    current_quantity: float = Field(..., ge=0)


class PortfolioItem(BaseModel):
    id: int
    portfolio_id: int
    asset_id: int
    target_weight: float
    tolerance: float
    entry_price: float
    initial_quantity: float
    current_quantity: float
    created_at: datetime
    asset: Asset
    
    class Config:
        from_attributes = True


# Portfolio schemas
class PortfolioCreate(BaseModel):
    name: str
    initial_invest_amount: float = Field(..., gt=0)
    description: Optional[str] = None
    items: List[PortfolioItemCreate]


class Portfolio(BaseModel):
    id: int
    user_id: int
    name: str
    initial_invest_amount: float
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class PortfolioDetail(Portfolio):
    items: List[PortfolioItem]


# Analysis schemas (for current weight calculation)
class ItemAnalysis(BaseModel):
    item_id: int
    asset: Asset
    target_weight: float
    current_weight: float
    weight_diff: float
    tolerance: float
    is_out_of_range: bool
    current_quantity: float
    current_price: float
    current_value: float
    entry_price: float
    initial_quantity: float


class PortfolioAnalysis(BaseModel):
    portfolio: Portfolio
    total_value: float
    initial_invest_amount: float
    total_return: float
    total_return_pct: float
    items: List[ItemAnalysis]

