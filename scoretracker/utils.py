# from datetime import timedelta
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, RedisDsn
from redis import Redis


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    REDIS_URL: Optional[RedisDsn] = None


@lru_cache
def get_settings() -> Settings:  # pragma: no cover
    return Settings()


@lru_cache
def get_redis() -> Redis:  # pragma: no cover
    settings = get_settings()
    if settings.REDIS_URL is None:
        return Redis(decode_responses=True)
    return Redis.from_url(settings.REDIS_URL, decode_responses=True)


# def get_current_user(
#     token: str = Depends(oauth_schema), redis: Redis = Depends(get_redis)
# ):
#     key = "token:" + token
#     if not redis.exists(key):
#         raise HTTPException(401, detail="Invalid or expired token")
#     redis.expire(key, timedelta(days=1))
#     return User.parse_obj(redis.hgetall(f"user:{redis.get(key)}"))
