from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AERIS"
    api_version: str = "0.1.0"
    database_url: str = "postgresql://aeris_user:aeris_password@localhost:5432/aeris_db"
    postgis_enabled: bool = True
    log_level: str = "INFO"

    # --- Groq / LLM configuration ------------------------------------------
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY", description="Groq API key")
    groq_base_url: str = Field(default="https://api.groq.com/openai/v1", alias="GROQ_BASE_URL")
    groq_model: str = Field(default="llama-3.3-70b-versatile", alias="GROQ_MODEL")
    groq_temperature: float = Field(default=0.4, alias="GROQ_TEMPERATURE")
    groq_max_tokens: int = Field(default=600, alias="GROQ_MAX_TOKENS")
    groq_request_timeout_seconds: float = Field(default=20.0, alias="GROQ_REQUEST_TIMEOUT_SECONDS")

    # --- Decision engine tunables ------------------------------------------
    manual_review_confidence_threshold: float = Field(default=0.70, alias="MANUAL_REVIEW_CONFIDENCE_THRESHOLD")

    # Compatibility properties for casing
    @property
    def GROQ_API_KEY(self) -> str:
        return self.groq_api_key

    @property
    def GROQ_BASE_URL(self) -> str:
        return self.groq_base_url

    @property
    def GROQ_MODEL(self) -> str:
        return self.groq_model

    @property
    def GROQ_TEMPERATURE(self) -> float:
        return self.groq_temperature

    @property
    def GROQ_MAX_TOKENS(self) -> int:
        return self.groq_max_tokens

    @property
    def GROQ_REQUEST_TIMEOUT_SECONDS(self) -> float:
        return self.groq_request_timeout_seconds

    @property
    def MANUAL_REVIEW_CONFIDENCE_THRESHOLD(self) -> float:
        return self.manual_review_confidence_threshold

    @property
    def LOG_LEVEL(self) -> str:
        return self.log_level


settings = Settings()


@lru_cache
def get_settings() -> Settings:
    return settings
