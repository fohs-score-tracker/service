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
    redis.sadd("teams", team.id)
    redis.set(current_team + ":name", team.name)
    if team.players:
        redis.sadd(current_team + ":players", *team.players)
    if team.coaches:
        redis.sadd(current_team + ":coaches", *team.coaches)

    return team


@router.get("/teams/{team_id}/", response_model=schemas.Team,
            summary="Lookup by id", responses={404: {"description": "Team does not exist"}})
def get_team(team_id: int, redis: Redis = Depends(get_redis)):
    current_team = f"team:{team_id}"
    if not redis.sismember("teams", team_id):
        raise HTTPException(404)

    return schemas.Team(
        id=team_id,
        name=redis.get(f"{current_team}:name"),
        players=redis.smembers(f"{current_team}:players"),
        coaches=redis.smembers(f"{current_team}:coaches"),
    )


@router.delete("/teams/{team_id}", status_code=204, responses={404: {"description": "Team does not exist"},
               204: {"description": "Team was successfully deleted"}}, summary="Delete a team with id")
def delete_team(team_id: int, redis: Redis = Dep(get_redis)):
    key = f"team:{team_id}"
    if not redis.sismember("teams", team_id):
        raise HTTPException(404)
    else:
        redis.delete(key)
    return Response(status_code=204)
