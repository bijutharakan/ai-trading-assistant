import asyncio
from app.agents.chart_agent import ChartAgent
from app.agents.oi_agent import OIAgent
from app.agents.sentiment_agent import SentimentAgent
from app.agents.image_agent import ImageAgent
from app.services.signal_dispatcher import SignalDispatcher

class RecommendationEngine:
    """
    Core recommendation engine that runs multiple agents and dispatches signals.
    """
    def __init__(self, db, dispatcher: SignalDispatcher, symbols: list[str], interval: int):
        self.db = db
        self.dispatcher = dispatcher
        self.symbols = symbols
        self.interval = interval
        self.chart_agent = ChartAgent()
        self.oi_agent = OIAgent()
        self.sentiment_agent = SentimentAgent()
        self.image_agent = ImageAgent()

    async def run(self):
        while True:
            for symbol in self.symbols:
                # Run all agents concurrently
                chart_task = self.chart_agent.analyze(symbol)
                oi_task = self.oi_agent.analyze(symbol)
                sentiment_task = self.sentiment_agent.analyze(symbol)
                image_task = self.image_agent.analyze(symbol)
                
                chart_res, oi_res, sent_res, img_res = await asyncio.gather(
                    chart_task, oi_task, sentiment_task, image_task
                )

                # Simple merge logic: prioritize chart signal
                if chart_res and chart_res.get("signal"):
                    entry = chart_res.get("price")
                    sl = entry * 0.99 if entry else None
                    target = entry * 1.01 if entry else None
                    confidence = oi_res.get("pcr", 0) * 100 if oi_res and oi_res.get("pcr") is not None else 50
                    signal_data = {
                        "instrument": symbol,
                        "action": chart_res["signal"],
                        "entry": entry,
                        "sl": sl,
                        "target": target,
                        "confidence": confidence,
                        "rationale": f"Chart {chart_res['signal']} at {entry}, PCR={oi_res.get('pcr')}",
                        "metadata": {
                            "chart": chart_res,
                            "oi": oi_res,
                            "sentiment": sent_res,
                            "image": img_res
                        }
                    }
                    await self.dispatcher.dispatch(signal_data)

            await asyncio.sleep(self.interval)
