from datetime import timedelta
from functools import lru_cache

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from redis import Redis

from .schemas import User
from .utils import Settings

from passlib.context import CryptContext

oauth_schema = OAuth2PasswordBearer("/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@lru_cache
def get_settings() -> Settings:  # pragma: no cover
    return Settings()


@lru_cache
def get_redis() -> Redis:  # pragma: no cover
    settings = get_settings()
    if settings.REDIS_URL is None:
        return Redis(decode_responses=True)
    return Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_current_user(
    token: str = Depends(oauth_schema), redis: Redis = Depends(get_redis)
):
    key = "token:" + token
    if not redis.exists(key):
        raise HTTPException(401, detail="Invalid or expired token")
    redis.expire(key, timedelta(days=1))
    return User.parse_obj(redis.hgetall(f"user:{redis.get(key)}"))


def hash_user_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
