from fastapi import FastAPI

from . import users, players
from .db import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI(title="ScoreTracker", version="0.0.0", openapi_tags=[
    {
        "name": "Users",
        "description": "Operations involving user accounts",
    },
])
app.include_router(users.router)
app.include_router(players.router)