from typing import List
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Trading AI Recommendation Engine"
    environment: str = "development"
    openai_api_key: str
    database_url: str

    # JWT settings
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Recommendation engine settings
    symbols: List[str] = ["NIFTY", "BANKNIFTY", "RELIANCE"]
    engine_interval: int = 300  # in seconds

    # Kite Connect API
    kite_api_key: str
    kite_api_secret: str
    kite_access_token: str

    # News API
    news_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
