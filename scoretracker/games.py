from typing import List

from fastapi import APIRouter, Depends, HTTPException
from redis import Redis

from . import schemas
from .deps import get_redis

router = APIRouter(tags=["Games"])


@router.post("/games/new", summary="Record a new game",
             response_description="New Game", response_model=schemas.GameResult)
def new_game(data: schemas.GameCreate, redis: Redis = Depends(get_redis)):
    game = schemas.Game(id=redis.incr("next_game_id"), **data.dict())

    prefix = f"game:{game.id}"
    redis.set(prefix + ":team_id", game.team_id)
    redis.set(prefix + ":other_team", game.other_team)
    redis.set(prefix + ":date", str(game.date))

    redis.sadd("games", game.id)
    return game.convert(redis)


@router.get("/games/{game_id}", summary="Get game by id",
            response_model=schemas.GameResult)
def get_game(game_id: int, redis: Redis = Depends(get_redis)):
    if not redis.sismember("games", game_id):
        raise HTTPException(404)
    return schemas.GameResult.find(redis, game_id)


@router.get("/games", summary="Get all games",
            response_model=List[schemas.GameResult])
def all_games(redis: Redis = Depends(get_redis)):
    return [schemas.GameResult.find(redis, game_id)
            for game_id in redis.smembers("games")]
