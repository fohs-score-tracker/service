# """
# Pydantic models.
# """
# from __future__ import annotations

# from datetime import datetime
# from typing import List, Optional

# from pydantic import BaseModel
# from redis import Redis


# class UserProfile(BaseModel):
#     name: str
#     email: str
#     id: int


# class UserResult(BaseModel):
#     user: Optional[UserProfile]
#     error: Optional[str]


# class UserCreate(BaseModel):
#     name: str
#     email: str
#     password: str


# class UserUpdate(BaseModel):
#     name: Optional[str]
#     email: Optional[str]
#     password: Optional[str]


# class PlayerCreate(BaseModel):
#     name: str


# class ShotCreate(BaseModel):
#     x: int
#     y: int
#     points: int
#     game_id: int
#     missed: bool


# class Shot(BaseModel):
#     id: int
#     x: int
#     y: int
#     points: int
#     game_id: int
#     missed: bool

#     @classmethod
#     def delete(cls, redis: Redis, shot_id: int):
#         prefix = f"shot:{shot_id}"
#         redis.delete(
#             prefix + ":x",
#             prefix + ":y",
#             prefix + ":points",
#             prefix + ":game_id",
#             prefix + ":missed",
#         )


# class Player(BaseModel):
#     id: int
#     name: str
#     shot_ids: List[int]

#     @classmethod
#     def find(cls, redis: Redis, player_id: int):
#         return cls(
#             id=player_id,
#             shot_ids=redis.smembers(f"player:{player_id}:shots"),
#             name=redis.get(f"player:{player_id}:name"),
#         )


# class TeamCreate(BaseModel):
#     name: str
#     players: List[int] = []
#     coaches: List[int] = []


# class Team(BaseModel):
#     id: int
#     name: str
#     coaches: List[int]
#     players: List[int]

#     @classmethod
#     def find(cls, redis: Redis, team_id: int):
#         return cls(
#             id=team_id,
#             name=redis.get(f"team:{team_id}:name"),
#             players=redis.smembers(f"team:{team_id}:players"),
#             coaches=redis.smembers(f"team:{team_id}:coaches"),
#         )


# class Game(BaseModel):
#     id: int
#     name: str
#     team_id: int
#     other_team: str
#     date: date

#     @staticmethod
#     def find(redis: Redis, game_id: int):
#         return Game(
#             id=game_id,
#             name=redis.get(f"game:{game_id}:name"),
#             team_id=redis.get(f"game:{game_id}:team_id"),
#             other_team=redis.get(f"game:{game_id}:other_team"),
#             date=redis.get(f"game:{game_id}:date"),
#         )


# class GameCreate(BaseModel):
#     name: str
#     team_id: int
#     other_team: str
#     date: Optional[datetime]

#     class Config:
#         schema_extra = {
#             "title": "New Game",
#         }
