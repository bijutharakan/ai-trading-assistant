import asyncio
from app.services.data_fetcher import DataFetcher
from app.utils.indicators import calculate_ema

class ChartAgent:
    def __init__(self):
        self.fetcher = DataFetcher()

    async def analyze(self, symbol: str):
        data = await self.fetcher.get_ohlc(symbol)
        ema = calculate_ema(data["close"], period=20)
        last_price = data["close"][-1] if data["close"] else None
        if last_price and ema and last_price > ema[-1]:
            return {"instrument": symbol, "signal": "LONG", "price": last_price}
        return None
