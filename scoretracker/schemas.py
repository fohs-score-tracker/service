"""
Pydantic models.
"""
from typing import List

from pydantic import BaseModel, EmailStr, conint


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
                "email": "jeff@localhost"
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
    team_name: str
    players: List[int]
    Coach: List[int]


class Team(BaseModel):
    id: conint(gt=0)
    team_name: str
    players: List[int]
    Coach: List[int]
