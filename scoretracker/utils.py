"""
Utility functions.
"""

from typing import Optional

from pydantic import BaseSettings, RedisDsn


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    REDIS_URL: Optional[RedisDsn] = None
    SENDGRID_API_KEY: Optional[str] = None

