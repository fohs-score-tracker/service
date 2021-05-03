from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import users
from .db import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI(title="ScoreTracker", version="0.0.0", openapi_tags=[
    {
        "name": "Users",
        "description": "Operations involving user accounts",
    },
])
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
