"""
Utility functions.
"""

from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_USERNAME: Optional[str] = None
