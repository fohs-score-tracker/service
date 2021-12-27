from datetime import timedelta
from secrets import token_urlsafe

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm, oauth2
from redis import Redis

from .deps import get_redis, oauth_schema, verify_password

router = APIRouter(tags=["Tokens"])


@router.post("/token", summary="Login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), redis: Redis = Depends(get_redis)
):
    """**Note:** Token expires after 1 day of inactivity."""
    for key in redis.scan_iter("user:*"):
        if redis.hget(key, "email") == form_data.username:
            hash_pw = redis.hget(key, "password")
            if verify_password(form_data.password, hash_pw):
                token = token_urlsafe()
                token_key = "token:" + token
                redis.set(token_key, redis.hget(key, "id"), ex=timedelta(days=1))
                return {"token_type": "bearer", "access_token": token}
            raise HTTPException(401, detail="Invalid password")
    raise HTTPException(401, detail="User does not exist")


@router.post("/token/revoke", summary="Logout", status_code=204)
def logout(token: str = Depends(oauth_schema), redis: Redis = Depends(get_redis)):
    redis.delete("token:" + token)
    return Response(status_code=204)
