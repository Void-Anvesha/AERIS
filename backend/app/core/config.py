from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "AERIS"
    api_version: str = "0.1.0"
    database_url: str = "postgresql://aeris_user:aeris_password@localhost:5432/aeris_db"
    postgis_enabled: bool = True
    log_level: str = "INFO"
    google_maps_api_key: Optional[str] = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
