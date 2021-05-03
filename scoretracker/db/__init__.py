"""
Database management functions.
"""

from typing import Optional

from sqlalchemy.orm import Session

from .. import schemas
from . import models
from .connection import Base, SessionLocal, engine


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_player(db: Session, player_id: int) -> Optional[models.Player]:
    return db.query(models.Player).filter(models.Player.id == player_id).first()


def create_player(db: Session, player: schemas.PlayerCreate) -> models.Player:
    db_player = models.Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def hash_pw(pwd, salt):
    return hashlib.pbkdf2_hmac(
        'sha256', pwd.encode(), salt.encode(), 50000).hex()
