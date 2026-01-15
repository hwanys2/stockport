import FinanceDataReader as fdr
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..schemas.portfolio import AssetSearch


# 종목 리스트 캐시
_krx_stocks_cache = None
_krx_cache_time = None
_us_stocks_cache = None
_us_cache_time = None
CACHE_TTL = 3600  # 1시간


def _get_krx_stocks():
    """한국 거래소 전체 종목 리스트 가져오기 (캐시 사용)"""
    global _krx_stocks_cache, _krx_cache_time
    
    # 캐시 확인
    if _krx_stocks_cache is not None and _krx_cache_time is not None:
        if (datetime.now() - _krx_cache_time).seconds < CACHE_TTL:
            return _krx_stocks_cache
    
    try:
        # KOSPI + KOSDAQ 전체 종목 가져오기
        krx_stocks = fdr.StockListing('KRX')
        _krx_stocks_cache = krx_stocks
        _krx_cache_time = datetime.now()
        return krx_stocks
    except Exception as e:
        print(f"KRX stock listing error: {e}")
        return None


def _get_us_stocks():
    """미국 전체 종목 리스트 가져오기 (캐시 사용)"""
    global _us_stocks_cache, _us_cache_time
    
    # 캐시 확인
    if _us_stocks_cache is not None and _us_cache_time is not None:
        if (datetime.now() - _us_cache_time).seconds < CACHE_TTL:
            return _us_stocks_cache
    
    try:
        # NASDAQ + NYSE 전체 종목 가져오기
        import pandas as pd
        
        nasdaq = fdr.StockListing('NASDAQ')
        nyse = fdr.StockListing('NYSE')
        
        # 두 리스트 합치기
        us_stocks = pd.concat([nasdaq, nyse], ignore_index=True)
        
        _us_stocks_cache = us_stocks
        _us_cache_time = datetime.now()
        return us_stocks
    except Exception as e:
        print(f"US stock listing error: {e}")
        return None


def search_assets(query: str, limit: int = 10) -> List[AssetSearch]:
    """
    종목 검색 (FinanceDataReader 사용 - 모든 종목 검색 가능)
    """
    try:
        query = query.strip()
        query_upper = query.upper()
        results = []
        
        # 1. 한국 주식 검색 (KRX 전체)
        krx_stocks = _get_krx_stocks()
        if krx_stocks is not None:
            # 종목명 또는 코드로 검색
            matched = krx_stocks[
                krx_stocks['Name'].str.contains(query, case=False, na=False) |
                krx_stocks['Code'].str.contains(query, case=False, na=False)
            ]
            
            for _, row in matched.head(limit).iterrows():
                asset = _get_kr_stock_info(row['Code'], row['Name'])
                if asset:
                    results.append(asset)
                    if len(results) >= limit:
                        return results
        
        # 2. 미국 주식 검색 (NASDAQ + NYSE 전체)
        if len(results) < limit:
            us_stocks = _get_us_stocks()
            if us_stocks is not None:
                # Symbol 또는 Name으로 검색
                matched = us_stocks[
                    us_stocks['Symbol'].str.contains(query_upper, case=False, na=False) |
                    us_stocks['Name'].str.contains(query, case=False, na=False)
                ]
                
                for _, row in matched.head(limit - len(results)).iterrows():
                    symbol = row['Symbol']
                    name = row['Name']
                    asset = _get_us_stock_info(symbol, name)
                    if asset:
                        results.append(asset)
                        if len(results) >= limit:
                            return results
        
        return results
    except Exception as e:
        print(f"Asset search error: {e}")
        import traceback
        traceback.print_exc()
        return []


def _get_us_stock_info(symbol: str, name: str = None) -> Optional[AssetSearch]:
    """미국 주식 정보 가져오기 (FinanceDataReader)"""
    try:
        # 최근 5일 데이터 가져오기 (휴장일 대비)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        df = fdr.DataReader(symbol, start_date, end_date)
        
        if df is None or df.empty:
            return None
        
        # 가장 최근 종가
        latest_price = float(df['Close'].iloc[-1])
        
        if latest_price <= 0:
            return None
        
        # 이름이 없으면 심볼 사용
        if not name:
            name = symbol
        
        return AssetSearch(
            symbol=symbol,
            name=name,
            exchange='US',
            current_price=latest_price
        )
    except Exception as e:
        print(f"US stock info error for {symbol}: {e}")
        return None


def _get_kr_stock_info(code: str, name: str) -> Optional[AssetSearch]:
    """한국 주식 정보 가져오기 (FinanceDataReader)"""
    try:
        # 최근 5일 데이터 가져오기
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        df = fdr.DataReader(code, start_date, end_date)
        
        if df is None or df.empty:
            return None
        
        # 가장 최근 종가
        latest_price = float(df['Close'].iloc[-1])
        
        if latest_price <= 0:
            return None
        
        # 심볼 형식: 코드 (한국 주식은 코드만 사용)
        symbol = code
        
        return AssetSearch(
            symbol=symbol,
            name=name,
            exchange='KRX',
            current_price=latest_price
        )
    except Exception as e:
        print(f"KR stock info error for {code}: {e}")
        return None


def get_current_price(symbol: str) -> Optional[float]:
    """
    특정 종목의 현재가 조회 (최근 종가)
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        df = fdr.DataReader(symbol, start_date, end_date)
        
        if df is None or df.empty:
            return None
        
        latest_price = float(df['Close'].iloc[-1])
        return latest_price if latest_price > 0 else None
    except Exception as e:
        print(f"Price fetch error for {symbol}: {e}")
        return None


def get_multiple_prices(symbols: List[str]) -> Dict[str, Optional[float]]:
    """
    여러 종목의 현재가를 한번에 조회
    """
    prices = {}
    for symbol in symbols:
        prices[symbol] = get_current_price(symbol)
    return prices
