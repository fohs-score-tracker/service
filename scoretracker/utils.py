"""
Utility functions.
"""

from typing import Optional

from pydantic import BaseSettings, RedisDsn
from redis import Redis


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    REDIS_URL: Optional[RedisDsn] = None
