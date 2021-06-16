"""
Utility functions.
"""

from typing import Optional

from pydantic import BaseSettings, EmailStr, RedisDsn


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    REDIS_URL: Optional[RedisDsn] = None
    SENDGRID_API_KEY: Optional[str] = None
    EMAIL_FROM_ADDRESS: Optional[EmailStr] = None
