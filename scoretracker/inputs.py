from datetime import datetime
from typing import List, Optional

import strawberry


@strawberry.input
class CreateUser:
    name: str
    email: str
    password: str


@strawberry.input
class UpdateUser:
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


@strawberry.input
class CreateTeam:
    name: str
    players: Optional[List[int]] = None
    coaches: Optional[List[int]] = None


@strawberry.input
class UpdateTeam:
    name: Optional[str] = None
    players: Optional[List[int]] = None
    coaches: Optional[List[int]] = None


@strawberry.input
class CreateGame:
    date: datetime
    name: str
    other_team_name: str
    team_id: int


@strawberry.input
class UpdateGame:
    date: Optional[datetime] = None
    name: Optional[str] = None
    other_team_name: Optional[str] = None
    team_id: Optional[int] = None


@strawberry.input
class CreateShot:
    x: int
    y: int
    points: int
    missed: bool
    game_id: int
