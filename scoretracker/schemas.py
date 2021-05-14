"""
Pydantic models.
"""
from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, conint
from redis import Redis


class UserProfile(BaseModel):
    name: str
    email: EmailStr
    id: conint(gt=0)

    class Config:
        schema_extra = {
            "title": "User",
            "example": {"name": "Jeff", "id": 1, "email": "jeff@localhost"},
        }


class User(UserProfile):
    password: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "title": "New User",
            "example": {
                "name": "Jeff",
                "password": "********",
                "email": "jeff@example.com",
            },
        }


class PlayerCreate(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "title": "New Player",
            "example": {
                "name": "Jeff",
            },
        }


class ShotCreate(BaseModel):
    x: conint(ge=0, lt=100)
    y: conint(ge=0, lt=50)
    points: conint(gt=0, le=3)  # 1, 2, or 3
    game_id: conint(gt=0)
    missed: bool

    class Config:
        schema_extra = {
            "title": "New Shot",
            "example": {"x": 50, "y": 25, "points": 3, "game_id": 1, "missed": False},
        }


class Shot(BaseModel):
    id: conint(gt=0)
    x: conint(ge=0, lt=100)
    y: conint(ge=0, lt=50)
    points: conint(gt=0, le=3)  # 1, 2, or 3
    game_id: conint(gt=0)
    missed: bool

    @classmethod
    def find(cls, redis: Redis, shot_id: int):
        prefix = f"shot:{shot_id}"
        return cls(
            id=shot_id,
            x=redis.get(prefix + ":x"),
            y=redis.get(prefix + ":y"),
            points=redis.get(prefix + ":points"),
            game_id=redis.get(prefix + ":game_id"),
            missed=redis.get(prefix + ":missed"),
        )

    @classmethod
    def delete(cls, redis: Redis, shot_id: int):
        prefix = f"shot:{shot_id}"
        redis.delete(
            prefix + ":x",
            prefix + ":y",
            prefix + ":points",
            prefix + ":game_id",
            prefix + ":missed",
        )

    def convert(self):
        return ShotResult(**self.dict())


class ShotResult(BaseModel):
    id: conint(gt=0) = Field(..., example=1)
    x: conint(ge=0, lt=100) = Field(..., example=50)
    y: conint(ge=0, lt=50) = Field(..., example=25)
    points: conint(gt=0, le=3) = Field(..., example=1)  # 1, 2, or 3
    missed: bool

    class Config:
        schema_extra = {
            "title": "Shot",
        }

    @classmethod
    def find(cls, redis: Redis, shot_id: int):
        return Shot.find(redis, shot_id).convert()


class Player(BaseModel):
    id: conint(gt=0)
    name: str
    shot_ids: List[conint(gt=0)]

    @classmethod
    def find(cls, redis: Redis, player_id: int):
        return cls(
            id=player_id,
            shot_ids=redis.smembers(f"player:{player_id}:shots"),
            name=redis.get(f"player:{player_id}:name"),
        )

    def convert(self, redis: Redis):
        return PlayerResult(
            id=self.id,
            name=self.name,
            shots=[
                Shot.find(redis, shot_id).convert()
                for shot_id in redis.smembers(f"player:{self.id}:shots")
            ],
        )


class PlayerResult(BaseModel):
    id: conint(gt=0) = Field(..., example=1)
    name: str = Field(..., example="Jeff")
    shots: List[ShotResult]

    @classmethod
    def find(cls, redis: Redis, player_id: int):
        return Player.find(redis, player_id).convert(redis)


class TeamCreate(BaseModel):
    name: str
    players: List[conint(gt=0)] = []
    coaches: List[conint(gt=0)] = []

    class Config:
        schema_extra = {
            "title": "New Team",
            "example": {"name": "Home Team", "players": [1], "coaches": [1]},
        }


class Team(BaseModel):
    id: conint(gt=0)
    name: str
    coaches: List[conint(gt=0)]
    players: List[conint(gt=0)]

    @classmethod
    def find(cls, redis: Redis, team_id: int):
        return cls(
            id=team_id,
            name=redis.get(f"team:{team_id}:name"),
            players=redis.smembers(f"team:{team_id}:players"),
            coaches=redis.smembers(f"team:{team_id}:coaches"),
        )

    def convert(self, redis: Redis) -> TeamResult:
        return TeamResult(
            id=self.id,
            name=self.name,
            players=[PlayerResult.find(redis, p) for p in self.players],
            coaches=[redis.hgetall(f"user:{c}") for c in self.coaches],
        )


class TeamResult(BaseModel):
    id: conint(gt=0) = Field(..., example=1)
    name: str = Field(..., example="Home Team")
    coaches: List[UserProfile]
    players: List[Player]

    @classmethod
    def find(cls, redis: Redis, team_id: int):
        return Team.find(redis, team_id).convert(redis)

    class Config:
        schema_extra = {
            "title": "Team",
        }


class Game(BaseModel):
    id: conint(gt=0)
    team_id: conint(gt=0)
    other_team: str
    date: date

    @staticmethod
    def find(redis: Redis, game_id: int):
        return Game(
            id=game_id,
            team_id=redis.get(f"game:{game_id}:team_id"),
            other_team=redis.get(f"game:{game_id}:other_team"),
            date=redis.get(f"game:{game_id}:date"),
        )

    def convert(self, redis: Redis):
        return GameResult(
            id=self.id,
            team=TeamResult.find(redis, self.team_id),
            other_team=self.other_team,
            date=self.date,
        )


class GameResult(BaseModel):
    id: conint(gt=0) = Field(..., example=1)
    team: TeamResult
    other_team: str = Field(..., example="Away Team")
    date: date

    @staticmethod
    def find(redis: Redis, game_id: int):
        return Game.find(redis, game_id).convert(redis)

    class Config:
        schema_extra = {
            "title": "Game",
        }


class GameCreate(BaseModel):
    team_id: conint(gt=0) = Field(..., example=1)
    other_team: str = Field(..., example="Away Team")
    date: Optional[date] = Field(default_factory=date.today)

    class Config:
        schema_extra = {
            "title": "New Game",
        }
