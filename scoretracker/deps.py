from functools import lru_cache

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from redis import Redis

from .utils import Settings

basic = HTTPBasic()


def basic_auth(auth: HTTPBasicCredentials = Depends(basic)):
    return auth


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_redis() -> Redis:
    settings = get_settings()
    if settings.REDIS_URL is None:
        return Redis(decode_responses=True)
    else:
        return Redis.from_url(settings.REDIS_URL, decode_responses=True)
