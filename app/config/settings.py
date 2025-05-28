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

    class Config:
        env_file = ".env"

settings = Settings()
