from functools import lru_cache

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from redis import Redis

from .schemas import User
from .utils import Settings

basic = HTTPBasic()


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_redis() -> Redis:
    settings = get_settings()
    if settings.REDIS_URL is None:
        return Redis(decode_responses=True)
    return Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_current_user(
    creds: HTTPBasicCredentials = Depends(basic), redis: Redis = Depends(get_redis)
):
    for key in redis.scan_iter("user:*"):
        user = User.parse_obj(redis.hgetall(key))
        if user.email == creds.username:
            if user.password == creds.password:
                return user
            raise HTTPException(401, "Invalid password")
    raise HTTPException(401, "User does not exist")
