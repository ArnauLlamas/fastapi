"""Application settings"""
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """Application settings class"""

    app_name: str = "Admin Service"

    secret_key: str
    database_url: PostgresDsn

    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
