import hashlib
from secrets import token_urlsafe

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    salt = token_urlsafe()
    hashed_password = hash_pw(user.password, salt)
    user
    db_user = models.User(
        email=user.email, password=hashed_password, username=user.username, )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(
        models.Player.id == player_id).first()


def get_player_by_user_first(db: Session, user_id: int):
    return db.query(models.Player).filter(
        models.Player.user_id == user_id).first()


def get_player_by_user_all(db: Session, user_id: int):
    return db.query(models.Player).filter_by(user_id=user_id).all()


def get_player_by_username(db: Session, username: str):
    return db.query(models.Player).filter(
        models.Player.username == username).first()


def hash_pw(pwd, salt):
    return hashlib.pbkdf2_hmac(
        'sha256', pwd.encode(), salt.encode(), 50000).hex()
