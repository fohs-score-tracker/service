from typing import List, Optional

from pydantic import BaseModel

class PlayerBase(BaseModel):
    pass 

class PlayerCreate(PlayerBase):
    username: str
    full_name: str
    two_pointers: int
    missed_two_pointers: int #
    three_pointers: int
    missed_three_pointers: int
    


class Player(UserBase):
    id: int
    username: str
    full_name: str

    class Config:
        orm_mode = True



class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    username: str
    fullname: str
    pw_hash:  str
    pw_salt: str


class User(UserBase):
    id: int
    username: str
    full_name: str

    class Config:
        orm_mode = True
