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
    db_user = models.User(
        email=user.email, pw_hash=hashed_password, username=user.username, full_name=user.full_name)

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(
        models.Player.username == player_id).first()


def get_player_by_user_first(db: Session, user_id: int):
    return db.query(models.Player).filter(
        models.Player.user_id == user_id).first()


def get_player_by_user_all(db: Session, user_id: int):
    return db.query(models.Player).filter_by(user_id=user_id).all()


def get_player_by_username(db: Session, username: str):
    return db.query(models.Player).filter(
        models.Player.username == username).first()


def add_score_to_player(db: Session, player:models.Player, score: int):
    player.two_pointers += score
    db.add(player)
    db.commit()
    db.refresh(db_user)
    return db_user



#def create_player(db: Session, player: schemas.Player):
 #   db_player = models.Player(
#        full_name=player.full_name, username=player.username, two_pointers=player.two_pointers, three_pointers=player.three_pointers)
 #   db.add(db_player)

 #   db.commit()

#    db.refresh(db_player)

#    return db_player
#

def hash_pw(pwd, salt):
    return hashlib.pbkdf2_hmac(
        'sha256', pwd.encode(), salt.encode(), 50000).hex()
