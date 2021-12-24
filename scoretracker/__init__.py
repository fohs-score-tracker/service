from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import auth, games, players, users

app = FastAPI(
    title="ScoreTracker",
    version="0.0.0",
    openapi_tags=[
        {
            "name": "Users",
            "description": "Add user accounts",
        },
        {"name": "Players", "description": "Register and manage players"},
        {"name": "Games", "description": "Record games"},
        {"name": "Tokens", "description": "Request and revoke session tokens"},
    ],
    docs_url="/",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(players.router)
app.include_router(games.router)
app.include_router(auth.router)
