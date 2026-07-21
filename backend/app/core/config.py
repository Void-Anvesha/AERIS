from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AERIS"
    api_version: str = "0.1.0"
    database_url: str = "postgresql://aeris_user:aeris_password@localhost:5432/aeris_db"
    postgis_enabled: bool = True
    log_level: str = "INFO"


settings = Settings()
