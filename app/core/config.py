from functools import lru_cache

from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.app_env: str = os.getenv("APP_ENV", "development")
        self.port: int = int(os.getenv("PORT", "8000"))


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance.

    Returns:
        The process-wide `Settings` instance, constructed once and cached
        via `lru_cache`. [VERIFY] because of caching, changes to
        environment variables after the first call won't be reflected
        within the same process.
    """
    return Settings()