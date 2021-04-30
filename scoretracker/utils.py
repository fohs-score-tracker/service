"""
Utility functions.
"""

from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    DATABASE_URL: Optional[str] = None
    ADMIN_PASSWORD: Optional[str] = None


@lru_cache
def get_settings() -> Settings:
    return Settings()