from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AERIS"
    api_version: str = "0.1.0"
    database_url: str = "postgresql://aeris_user:aeris_password@localhost:5432/aeris_db"
    postgis_enabled: bool = True
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def __init__(self, **values: str) -> None:
        super().__init__(**values)
        if self.database_url.startswith("postgres://"):
            self.database_url = self.database_url.replace("postgres://", "postgresql://", 1)


settings = Settings()
