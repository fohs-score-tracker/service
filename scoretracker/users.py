"""
User management
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import conint
from redis import Redis

from . import schemas
from .deps import get_current_user, get_redis

router = APIRouter(tags=["Users"])


@router.get(
    "/users", response_model=List[schemas.UserProfile], summary="List all users"
)
def list_users(redis: Redis = Depends(get_redis)):
    return [redis.hgetall(key) for key in redis.scan_iter("user:*")]


@router.get("/users/me", response_model=schemas.UserProfile)
def logged_in_user(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@router.get(
    "/users/{user_id}",
    response_model=schemas.UserProfile,
    summary="Lookup by id",
    responses={404: {"description": "User does not exist"}},
)
def find_user(user_id: conint(gt=0), redis: Redis = Depends(get_redis)):
    user = redis.hgetall(f"user:{user_id}")
    if user:
        return user
    raise HTTPException(404)


@router.delete(
    "/users/{user_id}",
    status_code=204,
    responses={
        404: {"description": "User does not exist"},
        204: {"description": "User was successfully deleted"},
    },
    summary="Delete a user with id",
)
def delete_user(user_id: conint(gt=0), redis: Redis = Depends(get_redis)):
    key = f"user:{user_id}"
    if not redis.exists(key):
        raise HTTPException(404)
    redis.delete(key)
    for team_id in redis.smembers("teams"):
        if redis.sismember(f"team:{team_id}:coaches", user_id):
            redis.srem(f"team:{team_id}:coaches", user_id)
    return Response(status_code=204)


@router.post(
    "/users/new",
    response_model=schemas.UserProfile,
    status_code=201,
    response_description="New User",
    summary="Create a new user",
)
def new_user(data: schemas.UserCreate, redis: Redis = Depends(get_redis)):
    user = schemas.User(id=redis.incr("next_user_id"), **data.dict())
    redis.hset(f"user:{user.id}", mapping=user.dict())
    return user


@router.patch(
    "/users/{user_id}",
    response_model=schemas.UserProfile,
    responses={
        404: {"description": "User does not exist"},
        200: {"description": "Updated user"},
    },
    summary="Update user",
)
def update_user(
    data: schemas.UserCreate, user_id: conint(gt=0), redis: Redis = Depends(get_redis)
):
    key = f"user:{user_id}"
    if not redis.exists(key):
        raise HTTPException(404, detail="User does not exist")
    user = schemas.User(id=user_id, **data.dict())
    redis.hset(key, mapping=user.dict())
    return user
