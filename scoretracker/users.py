"""
User management
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials

from . import schemas
from .db import Session, create_user, get_user, models
from .deps import basic_auth, get_db

router = APIRouter(tags=["Users"])


@router.get("/users",
            response_model=List[schemas.User], summary="List all users")
def list_users(db: Session = Depends(get_db)):
    users = []
    for user in db.query(models.User).all():
        users.append(schemas.User.from_orm(user))
    return users


@router.get("/users/{user_id}",
            response_model=schemas.User, summary="Lookup by id", responses={404: {"description": "User does not exist"}})
def find_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User does not exist")
    return user


@router.delete("/users/{user_id}", status_code=204,
               responses={404: {"description": "User does not exist"}, 204: {"description": "User was successfully deleted"}}, summary="Delete a user with id")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")
    else:
        db.delete(user)
        db.commit()


@ router.post("/users/new", response_model=schemas.User,
              status_code=201, response_description="New User", summary="Create a new user")
def new_user(user: schemas.UserCreate,
             db: Session = Depends(get_db)):
    user = create_user(db, user)
    return user
