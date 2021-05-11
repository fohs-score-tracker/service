"""
Pydantic models.
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel, EmailStr, conint
from redis import Redis


class UserProfile(BaseModel):
    full_name: str
    email: EmailStr
    id: conint(gt=0)

    class Config:
        schema_extra = {
            "title": "User",
            "example": {
                "full_name": "Jeff",
                "id": 1,
                "email": "jeff@localhost"
            }
        }


class User(UserProfile):
    password: str


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "title": "New User",
            "example": {
                "full_name": "Jeff",
                "password": "********",
                "email": "jeff@example.com"
            }
        }


class PlayerCreate(BaseModel):
    full_name: str

    class Config:
        schema_extra = {
            "title": "New Player",
            "example": {
                "full_name": "Jeff",
            }
        }


class Player(BaseModel):
    id: conint(gt=0)
    full_name: str
    two_pointers: conint(ge=0) = 0
    missed_two_pointers: conint(ge=0) = 0
    three_pointers: conint(ge=0) = 0
    missed_three_pointers: conint(ge=0) = 0

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "full_name": "Jeff",
                "two_pointers": 2,
                "missed_two_pointers": 1,
                "three_pointers": 5,
                "missed_three_pointers": 3
            }
        }


class TeamCreate(BaseModel):
    name: str
    players: List[conint(gt=0)] = []
    coaches: List[conint(gt=0)] = []

    class Config:
        schema_extra = {
            "title": "New Team",
            "example": {
                "name": "Home Team",
                "players": [1],
                "coaches": [1]
            }
        }


class Team(BaseModel):
    id: conint(gt=0)
    name: str
    coaches: List[conint(gt=0)]
    players: List[conint(gt=0)]

    def convert(self, redis: Redis) -> TeamList:
        return TeamList(
            id=self.id,
            name=self.name,
            players=[redis.hgetall(f"player:{p}") for p in self.players],
            coaches=[redis.hgetall(f"user:{c}") for c in self.coaches]
        )


class TeamList(BaseModel):
    id: conint(gt=0)
    name: str
    coaches: List[UserProfile]
    players: List[Player]

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Home Team",
                "players": [Player.Config.schema_extra],
                "coaches": [UserProfile.Config.schema_extra]
            }
        }
