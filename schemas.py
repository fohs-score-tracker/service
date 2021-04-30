from typing import List, Optional

from pydantic import BaseModel


class PlayerBase(BaseModel):
    id:int


class PlayerCreate(PlayerBase):
    username: str
    full_name: str
    two_pointers: int
    missed_two_pointers: int
    three_pointers: int
    missed_three_pointers: int


class Player(PlayerBase):
    id: int
    username: str
    full_name: str
    two_pointers: int
    missed_two_pointers: int
    three_pointers: int
    missed_three_pointers: int
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: int
    


class UserCreate(UserBase):
    username: str
    full_name: str
    password: str
    email: str
    
    



class User(UserBase):
    id: int
    email: str
    username: str
    full_name: str

    class Config:
        orm_mode = True
