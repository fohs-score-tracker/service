
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials

from . import schemas
from .db import Session, create_player, get_player, models
from .deps import basic_auth, get_db



router = APIRouter(tags=["Players"])


@router.get("/players",
            response_model=List[schemas.Player], summary="List all ")
def list_players(db: Session = Depends(get_db)):
    players = []
    for player in db.query(models.Player).all():
        players.append(schemas.Player.from_orm(player))
    return players


@router.get("/players/{player_id}",
            response_model=schemas.Player, summary="Lookup by id", responses={404: {"description": "Player does not exist"}})
def find_player(player_id: int, db: Session = Depends(get_db)):
    player = get_player(db, player_id)
    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player does not exist")
    return player


@router.delete("/players/{player_id}", status_code=204,
               responses={404: {"description": "Player does not exist"}, 204: {"description": "Player was successfully deleted"}}, summary="Delete a player with id")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = get_player(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player does not exist")
    else:
        db.delete(player)
        db.commit()


@router.post("/players/new", response_model=schemas.Player,
              status_code=201, response_description="New player", summary="Create a new player")
def new_player(player: schemas.PlayerCreate,
             db: Session = Depends(get_db)):
    player = create_player(db, player)
    return player
