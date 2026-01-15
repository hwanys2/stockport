import FinanceDataReader as fdr
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..schemas.portfolio import AssetSearch


# 한국 주식 종목 리스트 캐시
_krx_stocks_cache = None
_krx_cache_time = None
KRX_CACHE_TTL = 3600  # 1시간

# 미국 주식 주요 종목
US_MAJOR_STOCKS = {
    'aapl': ('AAPL', 'Apple Inc.'),
    'apple': ('AAPL', 'Apple Inc.'),
    '애플': ('AAPL', 'Apple Inc.'),
    
    'msft': ('MSFT', 'Microsoft Corporation'),
    'microsoft': ('MSFT', 'Microsoft Corporation'),
    '마이크로소프트': ('MSFT', 'Microsoft Corporation'),
    
    'googl': ('GOOGL', 'Alphabet Inc.'),
    'google': ('GOOGL', 'Alphabet Inc.'),
    '구글': ('GOOGL', 'Alphabet Inc.'),
    
    'amzn': ('AMZN', 'Amazon.com Inc.'),
    'amazon': ('AMZN', 'Amazon.com Inc.'),
    '아마존': ('AMZN', 'Amazon.com Inc.'),
    
    'tsla': ('TSLA', 'Tesla Inc.'),
    'tesla': ('TSLA', 'Tesla Inc.'),
    '테슬라': ('TSLA', 'Tesla Inc.'),
    
    'meta': ('META', 'Meta Platforms Inc.'),
    'facebook': ('META', 'Meta Platforms Inc.'),
    '메타': ('META', 'Meta Platforms Inc.'),
    '페이스북': ('META', 'Meta Platforms Inc.'),
    
    'nvda': ('NVDA', 'NVIDIA Corporation'),
    'nvidia': ('NVDA', 'NVIDIA Corporation'),
    '엔비디아': ('NVDA', 'NVIDIA Corporation'),
    
    'nflx': ('NFLX', 'Netflix Inc.'),
    'netflix': ('NFLX', 'Netflix Inc.'),
    '넷플릭스': ('NFLX', 'Netflix Inc.'),
    
    'dis': ('DIS', 'The Walt Disney Company'),
    'disney': ('DIS', 'The Walt Disney Company'),
    '디즈니': ('DIS', 'The Walt Disney Company'),
    
    'jpm': ('JPM', 'JPMorgan Chase & Co.'),
    'jpmorgan': ('JPM', 'JPMorgan Chase & Co.'),
    
    'v': ('V', 'Visa Inc.'),
    'visa': ('V', 'Visa Inc.'),
    
    'ma': ('MA', 'Mastercard Incorporated'),
    'mastercard': ('MA', 'Mastercard Incorporated'),
    
    'ko': ('KO', 'The Coca-Cola Company'),
    'coca cola': ('KO', 'The Coca-Cola Company'),
    '코카콜라': ('KO', 'The Coca-Cola Company'),
    
    'pypl': ('PYPL', 'PayPal Holdings Inc.'),
    'paypal': ('PYPL', 'PayPal Holdings Inc.'),
    
    'intc': ('INTC', 'Intel Corporation'),
    'intel': ('INTC', 'Intel Corporation'),
    '인텔': ('INTC', 'Intel Corporation'),
    
    'amd': ('AMD', 'Advanced Micro Devices Inc.'),
    
    'ba': ('BA', 'The Boeing Company'),
    'boeing': ('BA', 'The Boeing Company'),
    '보잉': ('BA', 'The Boeing Company'),
}


def _get_krx_stocks():
    """한국 거래소 전체 종목 리스트 가져오기 (캐시 사용)"""
    global _krx_stocks_cache, _krx_cache_time
    
    # 캐시 확인
    if _krx_stocks_cache is not None and _krx_cache_time is not None:
        if (datetime.now() - _krx_cache_time).seconds < KRX_CACHE_TTL:
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


def search_assets(query: str, limit: int = 10) -> List[AssetSearch]:
    """
    종목 검색 (FinanceDataReader 사용)
    """
    try:
        query_lower = query.lower().strip()
        query_upper = query.upper().strip()
        results = []
        
        # 1. 미국 주식 매핑에서 검색
        if query_lower in US_MAJOR_STOCKS:
            symbol, name = US_MAJOR_STOCKS[query_lower]
            asset = _get_us_stock_info(symbol, name)
            if asset:
                results.append(asset)
        
        # 2. 미국 주식 티커 직접 입력 (영문만, 대문자)
        if len(results) < limit and query.isalpha() and query.isupper():
            asset = _get_us_stock_info(query_upper)
            if asset:
                # 중복 제거
                if not any(r.symbol == asset.symbol for r in results):
                    results.append(asset)
        
        # 3. 한국 주식 검색
        if len(results) < limit:
            krx_stocks = _get_krx_stocks()
            if krx_stocks is not None:
                # 종목명 또는 코드로 검색
                matched = krx_stocks[
                    krx_stocks['Name'].str.contains(query, case=False, na=False) |
                    krx_stocks['Code'].str.contains(query, case=False, na=False)
                ]
                
                for _, row in matched.head(limit - len(results)).iterrows():
                    asset = _get_kr_stock_info(row['Code'], row['Name'])
                    if asset:
                        results.append(asset)
        
        return results[:limit]
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
