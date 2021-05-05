"""
User management
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import HTTPBasicCredentials
from redis import Redis

from . import schemas
from .deps import basic_auth, get_redis

router = APIRouter(tags=["Users"])


@router.get("/users",
            response_model=List[schemas.UserProfile], summary="List all users")
def list_users(redis: Redis = Depends(get_redis)):
    return [redis.hgetall(key) for key in redis.scan_iter("user:*")]


@router.get("/users/{user_id}",
            response_model=schemas.UserProfile, summary="Lookup by id", responses={404: {"description": "User does not exist"}})
def find_user(user_id: int, redis: Redis = Depends(get_redis)):
    user = redis.hgetall(f'user:{user_id}')
    if user:
        return user
    else:
        raise HTTPException(404)


@router.delete("/users/{user_id}", status_code=204,
               responses={404: {"description": "User does not exist"}, 204: {"description": "User was successfully deleted"}}, summary="Delete a user with id")
def delete_user(user_id: int, redis: Redis = Depends(get_redis)):
    key = f'user:{user_id}'
    if not redis.exists(key):
        raise HTTPException(404)
    else:
        redis.delete(key)
    return Response(status_code=204)


@router.post("/users/new", response_model=schemas.UserProfile,
             status_code=201, response_description="New User", summary="Create a new user")
def new_user(data: schemas.UserCreate,
             redis: Redis = Depends(get_redis)):
    user = schemas.User(id=redis.incr("next_user_id"), **data.dict())
    redis.hmset(f"user:{user.id}", user.dict())
    return user
