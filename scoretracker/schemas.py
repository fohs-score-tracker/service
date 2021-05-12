"""
Pydantic models.
"""
from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, conint
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

    @classmethod
    def find(cls, redis: Redis, team_id: int):
        return cls(id=team_id,
                   name=redis.get(f"team:{team_id}:name"),
                   players=redis.smembers(f"team:{team_id}:players"),
                   coaches=redis.smembers(f"team:{team_id}:coaches"))

    def convert(self, redis: Redis) -> TeamResult:
        return TeamResult(
            id=self.id,
            name=self.name,
            players=[redis.hgetall(f"player:{p}") for p in self.players],
            coaches=[redis.hgetall(f"user:{c}") for c in self.coaches]
        )


class TeamResult(BaseModel):
    id: conint(gt=0)
    name: str
    coaches: List[UserProfile]
    players: List[Player]

    @classmethod
    def find(cls, redis: Redis, team_id: int):
        return Team.find(redis, team_id).convert(redis)

    class Config:
        schema_extra = {
            "title": "Team",
            "example": {
                "id": 1,
                "name": "Home Team",
                "players": [Player.Config.schema_extra["example"]],
                "coaches": [UserProfile.Config.schema_extra["example"]]
            }
        }


class Game(BaseModel):
    id: conint(gt=0)
    team_id: conint(gt=0)
    other_team: str
    date: date

    @staticmethod
    def find(redis: Redis, game_id: int):
        return Game(id=game_id,
                    team_id=redis.get(f'game:{game_id}:team_id'),
                    other_team=redis.get(f'game:{game_id}:other_team'),
                    date=redis.get(f'game:{game_id}:date'))

    def convert(self, redis: Redis):
        return GameResult(id=self.id,
                          team=TeamResult.find(redis, self.team_id),
                          other_team=self.other_team,
                          date=self.date)


class GameResult(BaseModel):
    id: conint(gt=0)
    team: TeamResult
    other_team: str
    date: date

    @staticmethod
    def find(redis: Redis, game_id: int):
        return Game.find(redis, game_id).convert(redis)

    class Config:
        schema_extra = {
            "title": "Game",
            "example": {
                "id": 1,
                "team": TeamResult.Config.schema_extra["example"],
                "other_team": "Away Team",
                "date": date.fromtimestamp(0)
            }
        }


class GameCreate(BaseModel):
    team_id: conint(gt=0)
    other_team: str
    date: Optional[date] = Field(default_factory=date.today)

    class Config:
        schema_extra = {
            "title": "New Game",
            "example": {
                "team_id": 1,
                "other_team": "Away Team"
            }
        }
