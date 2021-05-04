from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import players, users

app = FastAPI(title="ScoreTracker", version="0.0.0", openapi_tags=[
    {
        "name": "Users",
        "description": "Operations involving user accounts",
    },
    {
        "name": "Players",
        "description": "Operations involving players"
    }
])

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(users.router)
app.include_router(players.router)
