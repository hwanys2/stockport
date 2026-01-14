from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.portfolio import Asset as AssetModel
from ..models.user import User
from ..schemas.portfolio import Asset, AssetCreate, AssetSearch
from ..services.auth import get_current_user
from ..services.market import search_assets, get_current_price

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("/search", response_model=List[AssetSearch])
def search_assets_route(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user)
):
    """종목 검색"""
    results = search_assets(q, limit)
    return results


@router.post("", response_model=Asset, status_code=status.HTTP_201_CREATED)
def create_asset(
    asset_data: AssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """종목 추가 (DB에 저장)"""
    # 이미 존재하는지 확인
    existing_asset = db.query(AssetModel).filter(
        AssetModel.symbol == asset_data.symbol
    ).first()
    
    if existing_asset:
        return existing_asset
    
    # 새 종목 생성
    new_asset = AssetModel(**asset_data.model_dump())
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    
    return new_asset


@router.get("/{asset_id}", response_model=Asset)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """종목 상세 조회"""
    asset = db.query(AssetModel).filter(AssetModel.id == asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    return asset


@router.get("/{asset_id}/price")
def get_asset_price(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """종목 현재가 조회"""
    asset = db.query(AssetModel).filter(AssetModel.id == asset_id).first()
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    
    price = get_current_price(asset.symbol)
    if price is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not fetch price for this asset"
        )
    
    return {"symbol": asset.symbol, "price": price}

