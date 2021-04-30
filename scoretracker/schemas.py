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
