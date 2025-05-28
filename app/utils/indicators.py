import pandas as pd

def calculate_ema(prices, period: int = 20):
    series = pd.Series(prices)
    return list(series.ewm(span=period, adjust=False).mean())
