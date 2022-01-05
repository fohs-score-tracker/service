from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import conint
from redis import Redis

from scoretracker import players

from . import schemas
from .deps import get_redis

router = APIRouter(tags=["Games"])


@router.post(
    "/games/new",
    summary="Record a new game",
    response_description="New Game",
    response_model=schemas.GameResult,
    status_code=201,
)
def new_game(data: schemas.GameCreate, redis: Redis = Depends(get_redis)):
    game = schemas.Game(id=redis.incr("next_game_id"), **data.dict())

    prefix = f"game:{game.id}"
    if not redis.exists(f"user:{game.user_id}"):
        raise HTTPException(404, detail="User does not exist.")
    redis.set(prefix + ":user-id", game.user_id)

    redis.set(prefix + ":name", game.name)
    redis.set(prefix + ":other_team", game.other_team)
    redis.set(prefix + ":date", str(game.date))

    for player_id in game.player_ids:
        if not redis.sismember("players", player_id):
            raise HTTPException(404, detail="Player does not exist.")
        redis.sadd(f"{prefix}:player-ids", player_id)

    redis.sadd("games", game.id)
    return game.convert(redis)


@router.get(
    "/games/{game_id}", summary="Get game by id", response_model=schemas.GameResult
)
def get_game(game_id: conint(gt=0), redis: Redis = Depends(get_redis)):
    if not redis.sismember("games", game_id):
        raise HTTPException(404)
    return schemas.GameResult.find(redis, game_id)


@router.get("/games", summary="Get all games", response_model=List[schemas.GameResult])
def all_games(redis: Redis = Depends(get_redis)):
    return [
        schemas.GameResult.find(redis, game_id) for game_id in redis.smembers("games")
    ]


@router.patch(
    "/games/{game_id}",
    summary="Edit a game",
    response_model=schemas.GameResult,
    responses={
        200: {"description": "Game is edited"},
        404: {"description": "Data does not exist to edit game"},
    },
)
def edit_game(
    data: schemas.GameCreate, game_id: conint(gt=0), redis: Redis = Depends(get_redis)
):
    if not redis.sismember("games", game_id):
        raise HTTPException(404)
    game = schemas.Game(id=game_id, **data.dict())
    prefix = f"game:{game.id}"
    if not redis.exists(f"user:{game.user_id}"):
        raise HTTPException(404, detail="User does not exist.")
    redis.set(prefix + ":user-id", game.user_id)
    redis.set(prefix + ":name", game.name)
    redis.set(prefix + ":other_team", game.other_team)
    redis.set(prefix + ":date", str(game.date))

    for player_id in game.player_ids:
        if not redis.sismember("players", player_id):
            raise HTTPException(404)
        redis.sadd(f"{prefix}:player-ids", player_id)

    redis.sadd("games", game.id)
    return game.convert(redis)


@router.delete(
    "/games/{game_id}",
    summary="Delete game by Id",
    status_code=204,
    responses={
        404: {"description": "Game does not exist"},
        204: {"description": "Game was successfully deleted"},
    },
)
def delete_game(game_id: conint(gt=0), redis: Redis = Depends(get_redis)):
    prefix = f"game:{game_id}"
    if not redis.sismember("games", game_id):
        raise HTTPException(404)
    else:
        redis.srem("games", game_id)
        redis.delete(prefix + ":name")
        redis.delete(prefix + ":other_team")
        redis.delete(prefix + ":date")
        redis.delete(prefix + "user_id")
        redis.delete(prefix + "player-ids")
    return Response(status_code=204)
