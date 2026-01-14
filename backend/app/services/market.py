import yfinance as yf
from typing import List, Dict, Optional
from ..schemas.portfolio import AssetSearch


def search_assets(query: str, limit: int = 10) -> List[AssetSearch]:
    """
    종목 검색 (yfinance의 Ticker를 이용)
    실제 운영 환경에서는 더 나은 검색 API 사용 권장
    """
    try:
        # 여러 주요 거래소에서 검색 시도
        symbols = [
            query.upper(),
            f"{query.upper()}.KS",  # 한국 KOSPI
            f"{query.upper()}.KQ",  # 한국 KOSDAQ
        ]
        
        results = []
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                # 유효한 티커인지 확인
                if info and 'symbol' in info:
                    results.append(AssetSearch(
                        symbol=info.get('symbol', symbol),
                        name=info.get('longName') or info.get('shortName', symbol),
                        exchange=info.get('exchange'),
                        current_price=info.get('currentPrice') or info.get('regularMarketPrice')
                    ))
            except:
                continue
        
        return results[:limit]
    except Exception as e:
        print(f"Asset search error: {e}")
        return []


def get_current_price(symbol: str) -> Optional[float]:
    """
    특정 종목의 현재가 조회
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # 여러 가격 필드 시도
        price = (
            info.get('currentPrice') or 
            info.get('regularMarketPrice') or
            info.get('previousClose')
        )
        
        return float(price) if price else None
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

