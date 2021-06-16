from datetime import timedelta
from secrets import token_urlsafe

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from redis import Redis
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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


@router.post(
    "/reset/{email}", summary="Request a password reset token", status_code=204
)
def get_reset_token(
    email: str,
    redis: Redis = Depends(get_redis),
    settings: Settings = Depends(get_settings),
):
    if not settings.SENDGRID_API_KEY or not settings.EMAIL_FROM_ADDRESS:
        raise HTTPException(
            status_code=500,
            detail="Password resets have not been configured on this server yet.",
        )
    for key in redis.scan_iter("user:*"):
        if redis.hget(key, "email") != email:
            continue
        user_id = redis.hget(key, "id")
        token = token_urlsafe()
        redis.set(f"reset:{user_id}", token, ex=timedelta(hours=1))
        message = Mail(
            from_email=settings.EMAIL_FROM_ADDRESS,
            to_emails=f"{email}",
            subject="FOHS ScoreTracker password reset",
            html_content=f"Your password reset token is <code>{token}</code>",
        )
        client = SendGridAPIClient(settings.SENDGRID_API_KEY)
        client.send(message)
        return Response(status_code=204)


@router.post(
    "/reset/{email}/confirm",
    summary="Reset a password using a password reset token",
    status_code=204,
)
def reset_password(
    email: str,
    token: str = Body(...),
    password: str = Body(...),
    redis: Redis = Depends(get_redis),
):
    for key in redis.scan_iter("user:*"):
        if redis.hget(key, "email") != email:
            continue
        user_id = redis.hget(key, "id")
        if redis.get(f"reset:{user_id}") != token:
            raise HTTPException(400, "Invalid reset token")
        redis.hset(key, "password", password)
        return Response(status_code=204)
