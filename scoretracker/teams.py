from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import HTTPBasicCredentials
from redis import Redis

from . import schemas
from .deps import basic_auth, get_redis

router = APIRouter(tags=["Teams"])


@router.post("/teams/new", response_model=schemas.Team, status_code=201,
             response_description="New Team", summary="Create a new team")
def new_team(data: schemas.TeamCreate, redis: Redis = Depends(get_redis)):
    team = schemas.Team(id=redis.incr("next_team_id"), **data.dict())
    current_team = f"team:{team.id}"
    redis.set(current_team + ":name", team.name)
    redis.sadd(current_team + ":roster", *team.players)
    redis.sadd(current_team + ":coach", *team.coach)

    return team
