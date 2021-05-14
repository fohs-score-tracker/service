"""
Player management
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from redis import Redis

from . import schemas
from .deps import get_redis

router = APIRouter(tags=["Players"])


@router.get("/players",
            response_model=List[schemas.Player], summary="List all players")
def list_players(redis: Redis = Depends(get_redis)):
    return [redis.hgetall(key) for key in redis.scan_iter("player:*")]


@router.get("/players/{player_id}",
            response_model=schemas.Player, summary="Lookup by id", responses={404: {"description": "Player does not exist"}})
def find_player(player_id: int, redis: Redis = Depends(get_redis)):
    player = redis.hgetall(f'player:{player_id}')
    if not player:
        raise HTTPException(404)
    return player


@router.delete("/players/{player_id}", status_code=204,
               responses={404: {"description": "Player does not exist"}, 204: {"description": "Player was successfully deleted"}}, summary="Delete a player with id")
def delete_player(player_id: int, redis: Redis = Depends(get_redis)):
    key = f'player:{player_id}'
    if not redis.exists(key):
        raise HTTPException(404)
    redis.delete(key)
    return Response(status_code=204)


@router.post("/players/new", response_model=schemas.Player,
             status_code=201, response_description="New Player", summary="Create a new player")
def new_player(data: schemas.PlayerCreate,
               redis: Redis = Depends(get_redis)):
    player = schemas.Player(id=redis.incr("next_player_id"), **data.dict())
    redis.hmset(f"player:{player.id}", player.dict())
    return player


@router.patch("/players/{player_id}/edit/twopointers/{score}", response_model=schemas.Player,
              status_code=200, response_description="Edit two pointers", summary="Edit two pointers")
def edit_player(player_id: int, score: int, redis: Redis = Depends(get_redis)):
    if not redis.exists(f"player:{player_id}"):
        raise HTTPException(404)
    player_data = redis.hgetall(f"player:{player_id}")
    player = schemas.Player(**player_data)
    player.two_pointers += score
    redis.hmset(f"player:{player.id}", player.dict())
    return player


@router.patch("/players/{player_id}/edit/missedtwopointers/{score}", response_model=schemas.Player,
              status_code=200, response_description="edit missed two pointers", summary="Edit missed two pointers")
def edit_missed_two_pointers(player_id: int, score: int,
                             redis: Redis = Depends(get_redis)):
    if not redis.exists(f"player:{player_id}"):
        raise HTTPException(404)
    player_data = redis.hgetall(F"player:{player_id}")
    player = schemas.Player(**player_data)
    player.missed_two_pointers += score
    redis.hmset(f"player:{player.id}", player.dict())
    return player


@router.patch("/players/{player_id}/edit/threepointers/{score}", response_model=schemas.Player,
              status_code=200, response_description="edit three pointers", summary="Edit three pointers")
def edit_three_pointers(player_id: int, score: int,
                        redis: Redis = Depends(get_redis)):
    if not redis.exists(f"player:{player_id}"):
        raise HTTPException(404)
    player_data = redis.hgetall(f"player:{player_id}")
    player = schemas.Player(**player_data)
    player.three_pointers += score
    redis.hmset(f"player:{player.id}", player.dict())
    return player


@router.patch("/players/{player_id}/edit/missthreepointers/{score}", response_model=schemas.Player,
              status_code=200, response_description="edit missed three pointers", summary="Edit missed three pointers")
def edit_missed_three_pointers(
        player_id: int, score: int, redis: Redis = Depends(get_redis)):
    if not redis.exists(f"player:{player_id}"):
        raise HTTPException(404)
    player_data = redis.hgetall(f"player:{player_id}")
    player = schemas.Player(**player_data)
    player.missed_three_pointers += score
    redis.hmset(f"player:{player.id}", player.dict())
    return player
