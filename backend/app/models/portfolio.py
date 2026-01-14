from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Asset(Base):
    """종목 정보 (주식, ETF 등)"""
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)  # 티커 (예: AAPL, TSLA)
    name = Column(String, nullable=False)  # 종목명
    exchange = Column(String, nullable=True)  # 거래소 (선택)
    currency = Column(String, default="USD")  # 통화
    asset_type = Column(String, default="stock")  # stock, etf, crypto 등
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    portfolio_items = relationship("PortfolioItem", back_populates="asset")


class Portfolio(Base):
    """포트폴리오"""
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)  # 포트폴리오 이름
    initial_invest_amount = Column(Float, nullable=False)  # 초기 투자금액
    description = Column(Text, nullable=True)  # 설명 (선택)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="portfolios")
    items = relationship("PortfolioItem", back_populates="portfolio", cascade="all, delete-orphan")


class PortfolioItem(Base):
    """포트폴리오 구성 종목"""
    __tablename__ = "portfolio_items"
    
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    
    # 목표 설정
    target_weight = Column(Float, nullable=False)  # 목표 비중 (%)
    tolerance = Column(Float, default=5.0)  # 허용 오차폭 (%)
    
    # 생성 시점 데이터 (수정 불가)
    entry_price = Column(Float, nullable=False)  # 생성 시점 가격 (고정)
    initial_quantity = Column(Float, nullable=False)  # 초기 수량
    
    # 현재 수량 (사용자가 수정 가능)
    current_quantity = Column(Float, nullable=False)  # 현재 수량
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="items")
    asset = relationship("Asset", back_populates="portfolio_items")

