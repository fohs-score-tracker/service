"""
Player management
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import conint
from redis import Redis

from . import schemas
from .deps import get_redis

router = APIRouter(tags=["Players"])


@router.get(
    "/players", response_model=List[schemas.PlayerResult], summary="List all players"
)
def list_players(redis: Redis = Depends(get_redis)):
    return [schemas.PlayerResult.find(redis, p) for p in redis.smembers("players")]


@router.get(
    "/players/{player_id}",
    response_model=schemas.PlayerResult,
    summary="Lookup by id",
    responses={404: {"description": "Player does not exist"}},
)
def find_player(player_id: conint(gt=0), redis: Redis = Depends(get_redis)):
    if not redis.sismember("players", player_id):
        raise HTTPException(404)
    return schemas.PlayerResult.find(redis, player_id)


@router.delete(
    "/players/{player_id}",
    status_code=204,
    responses={
        404: {"description": "Player does not exist"},
        204: {"description": "Player was successfully deleted"},
    },
    summary="Delete a player with id",
)
def delete_player(player_id: conint(gt=0), redis: Redis = Depends(get_redis)):
    if not redis.sismember("players", player_id):
        raise HTTPException(404)
    prefix = f"player:{player_id}"
    for shot_id in redis.smembers(prefix + ":shots"):
        schemas.Shot.delete(redis, shot_id)
    redis.delete(prefix + ":shots", prefix + ":name")
    redis.srem("players", player_id)
    for team_id in redis.smembers("teams"):
        if redis.sismember(f"team:{team_id}:players", player_id):
            redis.srem(f"team:{team_id}:players", player_id)
    return Response(status_code=204)


@router.post(
    "/players/new",
    response_model=schemas.PlayerResult,
    status_code=201,
    response_description="New Player",
    summary="Create a new player",
)
def new_player(data: schemas.PlayerCreate, redis: Redis = Depends(get_redis)):
    new_id = redis.incr("next_player_id")
    redis.set(f"player:{new_id}:name", data.name)
    redis.sadd("players", new_id)
    return schemas.PlayerResult.find(redis, new_id)


@router.post(
    "/players/{player_id}/shots/new",
    response_model=schemas.PlayerResult,
    response_description="Player with new shot",
    summary="Record a player's shot",
    responses={
        404: {"description": "Player or game does not exist"},
        201: {"description": "Shot was sucessfully added"},
    },
    status_code=201,
)
def add_shot(
    player_id: conint(gt=0),
    data: schemas.ShotCreate,
    redis: Redis = Depends(get_redis),
):
    if not redis.sismember("players", player_id):
        raise HTTPException(404)
    shot_id = redis.incr("next_shot_id")
    if not redis.sismember("games", data.game_id):
        raise HTTPException(404, detail="Game does not exist")
    for key, value in data.dict().items():
        redis.set(f"shot:{shot_id}:{key}", str(value))  # can't use bools
    redis.sadd(f"player:{player_id}:shots", shot_id)
    return schemas.PlayerResult.find(redis, player_id)


@router.delete(
    "/players/{player_id}/shots/{shot_id}",
    summary="Delete a player's shot",
    response_model=schemas.PlayerResult,
    response_description="Player with shot removed",
)
def delete_shot(
    player_id: conint(gt=0), shot_id: conint(gt=0), redis: Redis = Depends(get_redis)
):
    if not redis.sismember(f"player:{player_id}:shots", shot_id):
        raise HTTPException(404)
    schemas.Shot.delete(redis, shot_id)
    redis.srem(f"player:{player_id}:shots", shot_id)
    return schemas.PlayerResult.find(redis, player_id)


@router.patch(
    "/players/{player_id}",
    summary="Edit a player",
    response_model=schemas.PlayerResult,
    response_description="Edited player",
)
def edit_player(
    player_id: conint(gt=0),
    data: schemas.PlayerCreate,
    redis: Redis = Depends(get_redis),
):
    if not redis.sismember("players", player_id):
        raise HTTPException(404)
    redis.set(f"player:{player_id}:name", data.name)
    return schemas.PlayerResult.find(redis, player_id)
