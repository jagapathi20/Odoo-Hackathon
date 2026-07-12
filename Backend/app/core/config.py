from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration.
    Values are read from environment variables (or a `.env` file) and fall
    back to hackathon/dev-safe defaults only when nothing is provided.
    """

    # --- Database ---
    # FIX: previously there was no DATABASE_URL at all, so database.py could
    # never build a real SQLAlchemy engine. SQLite fallback keeps `uvicorn`
    # bootable out of the box for local dev; set a real Postgres DSN via env
    # in staging/production.
    DATABASE_URL: str = "sqlite:///./assetflow.db"

    # --- Auth ---
    JWT_SECRET: str = "test_secret_key_1234567890_hackathon_demo"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- CORS ---
    ALLOWED_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()