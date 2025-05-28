from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Trading AI Recommendation Engine"
    environment: str = "development"
    openai_api_key: str
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
