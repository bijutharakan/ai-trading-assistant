import asyncio
from datetime import datetime, timedelta
import httpx
from kiteconnect import KiteConnect
from newsapi import NewsApiClient
from app.config.settings import settings

class DataFetcher:
    """Fetch market data and other sources asynchronously."""
    def __init__(self):
        # Kite Connect SDK (synchronous) wrapped in async
        self.kite = KiteConnect(api_key=settings.kite_api_key)
        self.kite.set_access_token(settings.kite_access_token)
        # News API client
        self.news_client = NewsApiClient(api_key=settings.news_api_key)
        # HTTPX async client for NSE endpoints or other
        self.http = httpx.AsyncClient()

    async def get_ohlc(self, symbol: str, interval: str = "5minute"):
        """Fetch historical OHLC for the last 24h"""
        to_date = datetime.now()
        from_date = to_date - timedelta(days=1)
        # KiteConnect.historical_data is sync, run in executor
        data = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.kite.historical_data(
                instrument_token=self._get_instrument_token(symbol),
                from_date=from_date,
                to_date=to_date,
                interval=interval
            )
        )
        # Convert to ohlc dict
        ohlc = {'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
        for bar in data:
            ohlc['open'].append(bar['open'])
            ohlc['high'].append(bar['high'])
            ohlc['low'].append(bar['low'])
            ohlc['close'].append(bar['close'])
            ohlc['volume'].append(bar['volume'])
        return ohlc

    async def get_option_chain(self, symbol: str):
        """Fetch option chain and compute put-call ratio via NSE public API."""
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "application/json"
        }
        resp = await self.http.get(url, headers=headers)
        data = resp.json()
        records = data.get('records', {}).get('data', [])
        call_oi = sum(item.get('CE', {}).get('openInterest', 0) for item in records)
        put_oi = sum(item.get('PE', {}).get('openInterest', 0) for item in records)
        pcr = put_oi / call_oi if call_oi else None
        return {'put_call_ratio': pcr, 'records': records}

    async def get_news(self, symbol: str):
        """Fetch top 5 recent news headlines for symbol."""
        resp = self.news_client.get_everything(
            q=symbol,
            language="en",
            sort_by="publishedAt",
            page_size=5
        )
        return [article['title'] for article in resp.get('articles', [])]

    async def get_chart_image(self, symbol: str):
        """Capture chart screenshot; stub to integrate headless browser."""
        # TODO: implement headless browser screenshot (e.g. pyppeteer)
        return b""

    def _get_instrument_token(self, symbol: str) -> int:
        """Map symbol to Kite instrument token. Stub - set token mapping in settings."""
        token_map = {
            "NIFTY": 256265,         # example tokens
            "BANKNIFTY": 260105,
            "RELIANCE": 738561
        }
        return token_map.get(symbol)
