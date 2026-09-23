from functools import lru_cache
from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):

    app_name: str = "EduGenie"

    # ---------------------------------------------------------
    # Gemini
    # ---------------------------------------------------------

    gemini_api_key: str = ""

    gemini_model: str = "gemini-2.5-flash"


    # ---------------------------------------------------------
    # Local explanation model
    # ---------------------------------------------------------

    # Disabled because Gemini will handle explanations.
    # This avoids downloading/loading LaMini locally.
    local_explainer_enabled: bool = False

    local_explainer_model: str = (
        "MBZUAI/LaMini-Flan-T5-783M"
    )


    # ---------------------------------------------------------
    # Server
    # ---------------------------------------------------------

    host: str = "127.0.0.1"

    port: int = 8000

    reload: bool = True


    # ---------------------------------------------------------
    # CORS
    # ---------------------------------------------------------

    cors_origins: str = "*"


    # ---------------------------------------------------------
    # Environment configuration
    # ---------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


    # ---------------------------------------------------------
    # Gemini API status
    # ---------------------------------------------------------

    @property
    def gemini_configured(self) -> bool:

        return bool(
            self.gemini_api_key.strip()
        )


# -------------------------------------------------------------
# Cached settings
# -------------------------------------------------------------

@lru_cache
def get_settings() -> Settings:

    return Settings()


settings = get_settings()