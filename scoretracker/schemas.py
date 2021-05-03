"""
Pydantic models.
"""

from pydantic import BaseModel


class User(BaseModel):
    full_name: str
    email: str
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "full_name": "Jeff",
                "id": 1,
                "email": "jeff@localhost"
            }
        }


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "full_name": "Jeff",
                "password": "123456",
                "email": "jeff@localhost"
            }
        }


class PlayerCreate(BaseModel):
    full_name: str
     
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "full_name": "Jeff",
            }
        }

class Player(BaseModel):
    id: int 
    full_name: str
    two_pointers: int 
    missed_two_pointers: int 
    three_pointers: int 
    missed_three_pointers: int
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "full_name": "Jeff",
                "two_pointers": 2,
                "missed_two_pointers": 1,
                "three_pointers": 5,
                "missed_three_pointers": 3}
            }
        

