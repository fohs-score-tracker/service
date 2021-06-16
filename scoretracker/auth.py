from datetime import timedelta
from secrets import token_urlsafe

from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm, oauth2

from redis import Redis
from . import schemas
from .deps import get_redis, oauth_schema, get_send_grid

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
def password_reset(email: str, redis: Redis = Depends(get_redis)):
    for key in redis.scan_iter("user:*"):
       x = redis.hgetall(key)
       if (x.get("email") == email):
           token = token_urlsafe()
           redis.setex("reset", timedelta(minutes=30), token)
           redis.setex(f"reset:{token}",timedelta(minutes=30), x.get("id"))

           message = Mail(from_email='scoretracker@protonmail.com',to_emails=F"{email}",subject='Sending with Twilio SendGrid is Fun',html_content='<strong>and easy to do anywhere, even with Python</strong>')
           sg = SendGridAPIClient(get_send_grid())
           sg.send(message)
   
@router.post("/users/{token}/passwordreset")
def password_update(token: str, data: schemas.PasswordChange, redis: Redis = Depends(get_redis)):
    for db_token in redis.scan_iter("reset:*"):
        if token == db_token:
            pass