from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .db import SessionLocal
from .utils import get_settings

basic = HTTPBasic()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def basic_auth(auth: HTTPBasicCredentials = Depends(basic)):
    # TODO: validate
    return auth
