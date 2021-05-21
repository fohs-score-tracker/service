from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import games, players, teams, users

app = FastAPI(
    title="ScoreTracker",
    version="0.0.0",
    openapi_tags=[
        {
            "name": "Users",
            "description": "Add user accounts",
        },
        {"name": "Players", "description": "Register and manage players"},
        {"name": "Teams", "description": "Organize players in teams"},
        {"name": "Games", "description": "Record games"},
    ],
)

origins = [
    "https://fohs-score-tracker.github.io",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(players.router)
app.include_router(teams.router)
app.include_router(games.router)
