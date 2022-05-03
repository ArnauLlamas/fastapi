from typing import List

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    app_name: str = "Admin Service"

    secret_key: str
    database_url: PostgresDsn

    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    allowed_origins: List[str]
    allowed_hosts: List[str]


settings = Settings()  # type: ignore
