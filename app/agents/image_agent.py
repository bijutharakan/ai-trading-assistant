import asyncio
from app.services.data_fetcher import DataFetcher
from app.utils.image_parser import parse_chart_image

class ImageAgent:
    """
    Agent to capture and parse chart images via headless browser.
    """
    def __init__(self):
        self.fetcher = DataFetcher()

    async def analyze(self, symbol: str):
        image_bytes = await self.fetcher.get_chart_image(symbol)
        indicators = parse_chart_image(image_bytes)
        return {"instrument": symbol, "image_indicators": indicators}
