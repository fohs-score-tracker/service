"""
Pydantic models.
"""

from pydantic import BaseModel


class UserProfile(BaseModel):
    full_name: str
    email: str
    id: int

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
    email: str
    password: str

    class Config:
        schema_extra = {
            "title": "New User",
            "example": {
                "full_name": "Jeff",
                "password": "123456",
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
    id: int
    full_name: str
    two_pointers = 0
    missed_two_pointers = 0
    three_pointers = 0
    missed_three_pointers = 0

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
