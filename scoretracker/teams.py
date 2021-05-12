from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from redis import Redis

from . import schemas
from .deps import get_redis

router = APIRouter(tags=["Teams"])


@router.post("/teams/new", response_model=schemas.TeamResult, status_code=201,
             response_description="New Team", summary="Create a new team")
def new_team(data: schemas.TeamCreate, redis: Redis = Depends(get_redis)):
    team = schemas.Team(id=redis.incr("next_team_id"), **data.dict())
    prefix = f"team:{team.id}"
    redis.sadd("teams", team.id)
    redis.set(prefix + ":name", team.name)
    if team.players:
        redis.sadd(prefix + ":players", *team.players)
    if team.coaches:
        redis.sadd(prefix + ":coaches", *team.coaches)

    return team.convert(redis)


@router.get("/teams",
            response_model=List[schemas.TeamResult], summary="Get a list of all teams")
def all_teams(redis: Redis = Depends(get_redis)):
    return [schemas.TeamResult.find(redis, team_id)
            for team_id in redis.smembers("teams")]


@router.get("/teams/{team_id}", response_model=schemas.TeamResult,
            summary="Lookup by id", responses={404: {"description": "Team does not exist"}})
def get_team(team_id: int, redis: Redis = Depends(get_redis)):
    if not redis.sismember("teams", team_id):
        raise HTTPException(404)

    return schemas.TeamResult.find(redis, team_id)


@router.patch("/teams/{team_id}", response_model=schemas.TeamResult,
              summary="Edit by id", responses={404: {"description": "Team does not exist"}})
def edit_team(team_id: int, data: schemas.TeamCreate,
              redis: Redis = Depends(get_redis)):
    if not redis.sismember("teams", team_id):
        raise HTTPException(404)
    team = schemas.Team(id=team_id, **data.dict())
    prefix = f"team:{team_id}"

    # clear lists before adding
    redis.delete(f"{prefix}:players")
    redis.delete(f"{prefix}:coaches")

    redis.set(f"{prefix}:name", team.name)
    if team.players:
        redis.sadd(f"{prefix}:players", *team.players)
    if team.coaches:
        redis.sadd(f"{prefix}:coaches", *team.coaches)

    return team.convert(redis)


@router.delete("/teams/{team_id}", status_code=204, responses={404: {"description": "Team does not exist"},
                                                               204: {"description": "Team was successfully deleted"}}, summary="Delete a team with id")
def delete_team(team_id: int, redis: Redis = Depends(get_redis)):
    prefix = f"team:{team_id}"
    if not redis.sismember("teams", team_id):
        raise HTTPException(404)
    else:
        redis.srem("teams", team_id)
        redis.delete(prefix + ":name")
        redis.delete(prefix + ":players")
        redis.delete(prefix + ":coaches")
    return Response(status_code=204)
