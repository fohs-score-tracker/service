
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials

from . import schemas
from .db import Session, create_user, get_user, models
from .deps import basic_auth, get_db



router = APIRouter(tags=["Users"])