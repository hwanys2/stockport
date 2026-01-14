from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.portfolio import Portfolio as PortfolioModel, PortfolioItem as PortfolioItemModel, Asset as AssetModel
from ..models.user import User
from ..schemas.portfolio import (
    Portfolio, PortfolioCreate, PortfolioDetail,
    PortfolioItemUpdate, PortfolioAnalysis, ItemAnalysis
)
from ..services.auth import get_current_user
from ..services.market import get_current_price, get_multiple_prices

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.post("", response_model=PortfolioDetail, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    portfolio_data: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """포트폴리오 생성"""
    # 목표 비중 합계 검증
    total_weight = sum(item.target_weight for item in portfolio_data.items)
    if abs(total_weight - 100.0) > 0.01:  # 부동소수점 오차 허용
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Total target weight must be 100%, got {total_weight}%"
        )
    
    # 포트폴리오 생성
    new_portfolio = PortfolioModel(
        user_id=current_user.id,
        name=portfolio_data.name,
        initial_invest_amount=portfolio_data.initial_invest_amount,
        description=portfolio_data.description
    )
    db.add(new_portfolio)
    db.flush()  # ID를 얻기 위해
    
    # 각 종목에 대해 현재가 조회 및 수량 계산
    for item_data in portfolio_data.items:
        # 종목 정보 가져오기
        asset = db.query(AssetModel).filter(AssetModel.id == item_data.asset_id).first()
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asset with id {item_data.asset_id} not found"
            )
        
        # 현재가 조회 (entry_price)
        entry_price = get_current_price(asset.symbol)
        if entry_price is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Could not fetch price for {asset.symbol}"
            )
        
        # 초기 수량 계산
        # 종목별 투자액 = 총 투자금 × (목표 비중 / 100)
        item_invest_amount = portfolio_data.initial_invest_amount * (item_data.target_weight / 100.0)
        # 초기 수량 = 종목별 투자액 / entry_price
        initial_quantity = item_invest_amount / entry_price
        
        # PortfolioItem 생성
        new_item = PortfolioItemModel(
            portfolio_id=new_portfolio.id,
            asset_id=item_data.asset_id,
            target_weight=item_data.target_weight,
            tolerance=item_data.tolerance,
            entry_price=entry_price,
            initial_quantity=initial_quantity,
            current_quantity=initial_quantity  # 처음에는 초기 수량과 동일
        )
        db.add(new_item)
    
    db.commit()
    db.refresh(new_portfolio)
    
    return new_portfolio


@router.get("", response_model=List[Portfolio])
def list_portfolios(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """사용자의 포트폴리오 목록 조회"""
    portfolios = db.query(PortfolioModel).filter(
        PortfolioModel.user_id == current_user.id
    ).all()
    return portfolios


@router.get("/{portfolio_id}", response_model=PortfolioDetail)
def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """포트폴리오 상세 조회"""
    portfolio = db.query(PortfolioModel).filter(
        PortfolioModel.id == portfolio_id,
        PortfolioModel.user_id == current_user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    return portfolio


@router.get("/{portfolio_id}/analysis", response_model=PortfolioAnalysis)
def analyze_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """포트폴리오 분석 (현재 비중, 차이, 경고 등)"""
    portfolio = db.query(PortfolioModel).filter(
        PortfolioModel.id == portfolio_id,
        PortfolioModel.user_id == current_user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    # 모든 종목의 현재가 조회
    symbols = [item.asset.symbol for item in portfolio.items]
    current_prices = get_multiple_prices(symbols)
    
    # 각 종목 분석
    items_analysis = []
    total_value = 0.0
    
    for item in portfolio.items:
        current_price = current_prices.get(item.asset.symbol)
        if current_price is None:
            # 가격을 가져올 수 없는 경우 entry_price 사용
            current_price = item.entry_price
        
        # 평가금액 계산
        current_value = item.current_quantity * current_price
        total_value += current_value
    
    # 두 번째 패스: 현재 비중 계산 및 분석
    for item in portfolio.items:
        current_price = current_prices.get(item.asset.symbol) or item.entry_price
        current_value = item.current_quantity * current_price
        
        # 현재 비중
        current_weight = (current_value / total_value * 100) if total_value > 0 else 0
        
        # 차이
        weight_diff = current_weight - item.target_weight
        
        # 허용 범위 벗어남 여부
        is_out_of_range = abs(weight_diff) > item.tolerance
        
        items_analysis.append(ItemAnalysis(
            item_id=item.id,
            asset=item.asset,
            target_weight=item.target_weight,
            current_weight=current_weight,
            weight_diff=weight_diff,
            tolerance=item.tolerance,
            is_out_of_range=is_out_of_range,
            current_quantity=item.current_quantity,
            current_price=current_price,
            current_value=current_value,
            entry_price=item.entry_price,
            initial_quantity=item.initial_quantity
        ))
    
    # 전체 수익률 계산
    total_return = total_value - portfolio.initial_invest_amount
    total_return_pct = (total_return / portfolio.initial_invest_amount * 100) if portfolio.initial_invest_amount > 0 else 0
    
    return PortfolioAnalysis(
        portfolio=portfolio,
        total_value=total_value,
        initial_invest_amount=portfolio.initial_invest_amount,
        total_return=total_return,
        total_return_pct=total_return_pct,
        items=items_analysis
    )


@router.patch("/{portfolio_id}/items/{item_id}", response_model=PortfolioDetail)
def update_portfolio_item_quantity(
    portfolio_id: int,
    item_id: int,
    update_data: PortfolioItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """포트폴리오 종목의 수량 업데이트"""
    # 포트폴리오 소유권 확인
    portfolio = db.query(PortfolioModel).filter(
        PortfolioModel.id == portfolio_id,
        PortfolioModel.user_id == current_user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    # 아이템 찾기
    item = db.query(PortfolioItemModel).filter(
        PortfolioItemModel.id == item_id,
        PortfolioItemModel.portfolio_id == portfolio_id
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio item not found"
        )
    
    # 수량 업데이트
    item.current_quantity = update_data.current_quantity
    db.commit()
    db.refresh(portfolio)
    
    return portfolio


@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """포트폴리오 삭제"""
    portfolio = db.query(PortfolioModel).filter(
        PortfolioModel.id == portfolio_id,
        PortfolioModel.user_id == current_user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    db.delete(portfolio)
    db.commit()
    
    return None

