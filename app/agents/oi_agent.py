import asyncio
from app.services.data_fetcher import DataFetcher

class OIAgent:
    """
    Agent to analyze option chain and open interest data.
    """
    def __init__(self):
        self.fetcher = DataFetcher()

    async def analyze(self, symbol: str):
        data = await self.fetcher.get_option_chain(symbol)
        # TODO: parse option chain, compute PCR, max pain, unusual OI changes
        pcr = data.get("put_call_ratio")
        # Placeholder logic
        signal = None
        if pcr and pcr > 1.2:
            signal = "BEARISH"
        elif pcr and pcr < 0.8:
            signal = "BULLISH"
        return {"instrument": symbol, "signal": signal, "pcr": pcr}
