from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user/new", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/player/{player_id}/twopointers/{value}")
def add_score(player_id: int, value: int, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return add_score(player_id, value, db)


@app.post("/player/new/", response_model=schemas.Player)
def create_player(Player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.does_player_exist(db, username=Player.username)
    if db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    return create_player(db, Player)


@app.get("/user/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
