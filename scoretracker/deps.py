from functools import lru_cache

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from redis import Redis

from .utils import Settings

basic = HTTPBasic()


def basic_auth(auth: HTTPBasicCredentials = Depends(basic)):
    # TODO: validate
    return auth


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_redis() -> Redis:
    settings = get_settings()
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        username=settings.REDIS_USERNAME,
        decode_responses=True
    )
