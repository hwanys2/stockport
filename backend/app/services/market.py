import yfinance as yf
from typing import List, Dict, Optional
import time
from urllib.error import HTTPError
import requests
from ..schemas.portfolio import AssetSearch

# 간단한 인메모리 캐시 (서버 재시작 시 초기화)
_asset_cache: Dict[str, Optional[AssetSearch]] = {}
_cache_timestamp: Dict[str, float] = {}
CACHE_TTL = 300  # 5분

# 일반적인 종목 매핑 (이름 -> 티커)
COMMON_STOCKS = {
    # 미국 주식
    'apple': 'AAPL', 'aapl': 'AAPL', '애플': 'AAPL',
    'microsoft': 'MSFT', 'msft': 'MSFT', '마이크로소프트': 'MSFT',
    'tesla': 'TSLA', 'tsla': 'TSLA', '테슬라': 'TSLA',
    'amazon': 'AMZN', 'amzn': 'AMZN', '아마존': 'AMZN',
    'google': 'GOOGL', 'googl': 'GOOGL', '구글': 'GOOGL',
    'meta': 'META', 'meta': 'META', '페이스북': 'META',
    'nvidia': 'NVDA', 'nvda': 'NVDA', '엔비디아': 'NVDA',
    'netflix': 'NFLX', 'nflx': 'NFLX', '넷플릭스': 'NFLX',
    'disney': 'DIS', 'dis': 'DIS', '디즈니': 'DIS',
    'jpmorgan': 'JPM', 'jpm': 'JPM', '모건': 'JPM',
    'visa': 'V', 'v': 'V',
    'mastercard': 'MA', 'ma': 'MA',
    'coca cola': 'KO', 'ko': 'KO', '코카콜라': 'KO',
    
    # 한국 주식
    '삼성': '005930.KS', '삼성전자': '005930.KS', '005930': '005930.KS',
    'sk하이닉스': '000660.KS', '하이닉스': '000660.KS', '000660': '000660.KS',
    'naver': '035420.KS', '네이버': '035420.KS', '035420': '035420.KS',
    'kakao': '035720.KS', '카카오': '035720.KS', '035720': '035720.KS',
    'lg': '003550.KS', 'lg전자': '066570.KS',
    '현대': '005380.KS', '현대차': '005380.KS',
    '기아': '000270.KS',
    '셀트리온': '068270.KS',
    '포스코': '005490.KS',
}


def search_assets(query: str, limit: int = 10) -> List[AssetSearch]:
    """
    종목 검색 (yfinance의 Ticker를 이용)
    yfinance는 검색 API가 없으므로 일반적인 티커들을 시도
    """
    try:
        query_lower = query.lower().strip()
        query_upper = query.upper().strip()
        results = []
        
        # 1. 일반적인 종목 매핑에서 찾기
        found_in_mapping = False
        if query_lower in COMMON_STOCKS:
            symbol = COMMON_STOCKS[query_lower]
            found_in_mapping = True
            print(f"Found {query} in mapping: {symbol}")
            
            # API 호출 전 딜레이 (rate limiting 방지)
            time.sleep(1.0)
            
            asset = _try_get_asset_info(symbol)
            if asset:
                results.append(asset)
                # 매핑에서 찾은 경우 바로 반환 (추가 시도 없음)
                return results[:limit]
        
        # 2. 매핑에 없는 경우에만 직접 티커 시도
        # 한글이 포함된 경우 ticker로 시도하지 않음
        if not found_in_mapping and query.isascii() and query.isalnum():
            # 먼저 기본 심볼만 시도 (미국 주식일 가능성이 높음)
            base_symbol = query_upper
            
            time.sleep(1.0)
            asset = _try_get_asset_info(base_symbol)
            if asset:
                results.append(asset)
                if len(results) >= limit:
                    return results[:limit]
        
        # 3. 숫자로만 이루어진 경우 (한국 주식 코드일 가능성)
        # 예: 005930, 035420
        if not found_in_mapping and query.isdigit():
            korean_symbols = [
                f"{query_upper}.KS",  # 한국 KOSPI
                f"{query_upper}.KQ",  # 한국 KOSDAQ
            ]
            
            for symbol in korean_symbols:
                time.sleep(1.0)
                asset = _try_get_asset_info(symbol)
                if asset:
                    results.append(asset)
                    if len(results) >= limit:
                        break
        
        return results[:limit]
    except Exception as e:
        print(f"Asset search error: {e}")
        import traceback
        traceback.print_exc()
        return []


def _try_get_asset_info(symbol: str, max_retries: int = 3) -> Optional[AssetSearch]:
    """티커 심볼로 종목 정보 가져오기 (재시도 로직 및 캐싱 포함)"""
    # 캐시 확인
    if symbol in _asset_cache:
        cache_time = _cache_timestamp.get(symbol, 0)
        if time.time() - cache_time < CACHE_TTL:
            print(f"Cache hit for {symbol}")
            return _asset_cache[symbol]
    
    for attempt in range(max_retries):
        try:
            ticker = yf.Ticker(symbol)
            
            # fast_info 사용 (더 빠름)
            try:
                fast_info = ticker.fast_info
                if fast_info and hasattr(fast_info, 'lastPrice'):
                    price = fast_info.lastPrice
                    if price and price > 0:
                        # info에서 이름 가져오기
                        info = ticker.info
                        name = info.get('longName') or info.get('shortName') or symbol
                        result = AssetSearch(
                            symbol=symbol,
                            name=name,
                            exchange=info.get('exchange', ''),
                            current_price=float(price)
                        )
                        # 캐시에 저장
                        _asset_cache[symbol] = result
                        _cache_timestamp[symbol] = time.time()
                        return result
            except (HTTPError, requests.exceptions.HTTPError) as e:
                status_code = getattr(e, 'code', None) or getattr(e.response, 'status_code', None)
                if status_code == 429:  # Too Many Requests
                    wait_time = (2 ** attempt) * 2  # 지수 백오프: 2초, 4초, 8초
                    if attempt < max_retries - 1:
                        print(f"Rate limited for {symbol}, waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                    return None
                # 다른 HTTP 에러는 무시하고 다음 시도
                pass
            except Exception:
                pass
            
            # fast_info 실패 시 info 사용
            try:
                info = ticker.info
                if not info:
                    return None
                
                # 유효한 티커인지 확인 (심볼이 있고 가격 정보가 있는지)
                if 'symbol' not in info:
                    return None
                
                price = (
                    info.get('currentPrice') or 
                    info.get('regularMarketPrice') or 
                    info.get('previousClose')
                )
                
                if not price or price <= 0:
                    return None
                
                name = info.get('longName') or info.get('shortName') or symbol
                
                result = AssetSearch(
                    symbol=info.get('symbol', symbol),
                    name=name,
                    exchange=info.get('exchange', ''),
                    current_price=float(price)
                )
                # 캐시에 저장
                _asset_cache[symbol] = result
                _cache_timestamp[symbol] = time.time()
                return result
            except (HTTPError, requests.exceptions.HTTPError) as e:
                status_code = getattr(e, 'code', None) or getattr(e.response, 'status_code', None)
                if status_code == 429:  # Too Many Requests
                    wait_time = (2 ** attempt) * 2  # 지수 백오프: 2초, 4초, 8초
                    if attempt < max_retries - 1:
                        print(f"Rate limited for {symbol}, waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                    return None
                return None
                
        except (HTTPError, requests.exceptions.HTTPError) as e:
            status_code = getattr(e, 'code', None) or getattr(e.response, 'status_code', None)
            if status_code == 429:  # Too Many Requests
                wait_time = (2 ** attempt) * 2  # 지수 백오프: 2초, 4초, 8초
                if attempt < max_retries - 1:
                    print(f"Rate limited for {symbol}, waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
                return None
            # 특정 티커 실패는 무시 (다른 티커 시도)
            return None
        except Exception as e:
            # 429 에러가 아닌 다른 에러는 즉시 반환
            error_str = str(e)
            if "429" in error_str or "Too Many Requests" in error_str:
                wait_time = (2 ** attempt) * 2  # 지수 백오프: 2초, 4초, 8초
                if attempt < max_retries - 1:
                    print(f"Rate limited for {symbol}, waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
            # 특정 티커 실패는 무시 (다른 티커 시도)
            # 실패도 캐시하여 반복 시도 방지 (짧은 TTL)
            _asset_cache[symbol] = None
            _cache_timestamp[symbol] = time.time()
            return None
    
    # 모든 재시도 실패, 캐시에 저장
    _asset_cache[symbol] = None
    _cache_timestamp[symbol] = time.time()
    return None


def get_current_price(symbol: str, max_retries: int = 3) -> Optional[float]:
    """
    특정 종목의 현재가 조회 (재시도 로직 포함)
    """
    for attempt in range(max_retries):
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
        except (HTTPError, requests.exceptions.HTTPError) as e:
            status_code = getattr(e, 'code', None) or getattr(e.response, 'status_code', None)
            if status_code == 429:  # Too Many Requests
                wait_time = (2 ** attempt) * 2  # 지수 백오프: 2초, 4초, 8초
                if attempt < max_retries - 1:
                    print(f"Rate limited for {symbol} price fetch, waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
                return None
            print(f"Price fetch error for {symbol}: {e}")
            return None
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "Too Many Requests" in error_str:
                wait_time = (2 ** attempt) * 2  # 지수 백오프: 2초, 4초, 8초
                if attempt < max_retries - 1:
                    print(f"Rate limited for {symbol} price fetch, waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
            print(f"Price fetch error for {symbol}: {e}")
            return None
    
    return None


def get_multiple_prices(symbols: List[str]) -> Dict[str, Optional[float]]:
    """
    여러 종목의 현재가를 한번에 조회
    """
    prices = {}
    for symbol in symbols:
        prices[symbol] = get_current_price(symbol)
    return prices

