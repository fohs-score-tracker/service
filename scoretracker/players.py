"""
Player management
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import HTTPBasicCredentials
from redis import Redis

from . import schemas
from .deps import basic_auth, get_redis

router = APIRouter(tags=["Players"])


@router.get("/players",
            response_model=List[schemas.Player], summary="List all players")
def list_players(redis: Redis = Depends(get_redis)):
    return [redis.hgetall(key) for key in redis.keys("player:*")]


@router.get("/players/{player_id}",
            response_model=schemas.Player, summary="Lookup by id", responses={404: {"description": "Player does not exist"}})
def find_player(player_id: int, redis: Redis = Depends(get_redis)):
    player = redis.hgetall(f'player:{player_id}')
    if player:
        return player
    else:
        raise HTTPException(404)


@router.delete("/players/{player_id}", status_code=204,
               responses={404: {"description": "Player does not exist"}, 204: {"description": "Player was successfully deleted"}}, summary="Delete a player with id")
def delete_player(player_id: int, redis: Redis = Depends(get_redis)):
    key = f'player:{player_id}'
    if not redis.exists(key):
        raise HTTPException(404)
    else:
        redis.delete(key)
    return Response(status_code=204)


@router.post("/players/new", response_model=schemas.Player,
             status_code=201, response_description="New Player", summary="Create a new player")
def new_player(data: schemas.PlayerCreate,
               redis: Redis = Depends(get_redis)):
    player = schemas.Player(id=redis.incr("next_player_id"), **data.dict())
    redis.hmset(f"player:{player.id}", player.dict())
    return player
