from datetime import timedelta
from secrets import token_urlsafe

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm, oauth2
from redis import Redis
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from . import schemas
from .deps import Settings, get_redis, get_settings, oauth_schema

router = APIRouter(tags=["Tokens"])


@router.post("/token", summary="Login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), redis: Redis = Depends(get_redis)
):
    """**Note:** Token expires in 30 minutes of inactivity."""
    for key in redis.scan_iter("user:*"):
        if redis.hget(key, "email") == form_data.username:
            if redis.hget(key, "password") == form_data.password:
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


@router.post("/users/{email}/reset")
def password_reset(
    email: str,
    redis: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
):
    for key in redis.scan_iter("user:*"):
        x = redis.hgetall(key)
        if x.get("email") == email:
            token = token_urlsafe()
            redis.setex("reset", timedelta(minutes=30), token)
            redis.setex(f"reset:{token}", timedelta(minutes=30), x.get("id"))
            message = Mail(
                from_email="scoretracker@protonmail.com",
                to_emails=f"{email}",
                subject="password reset",
                html_content=f"<strong>Here is the link for your password reset</strong> <br> <a href='{token}' ",
            )
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            sg.send(message)


@router.post("/users/{email}/reset/confirm")
def password_update(
    token: str = Body(...),
    email: str,
    redis: Redis = Depends(get_redis),
    password: str = Body(...),
):
    for db_token in redis.scan_iter("reset:*"):
        if token == db_token:
            user_id = redis.hget(f"reset:{db_token}")
            user_key = f"user:{user_id}"
            user_data = redis.hgetall(user_key)
            user = schemas.User(**user_data.dict(), id=user_id)
            redis.hset(user_key, mapping=user.dict())
