from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import strawberry

from .utils import get_redis


@strawberry.type
class Error:
    field: Optional[str]
    detail: str


@strawberry.type
class User:
    id: int

    @strawberry.field
    def name(self) -> str:
        return get_redis().hget(f"user:{self.id}", "name") or "No name"

    @strawberry.field
    def email(self) -> str:
        return get_redis().hget(f"user:{self.id}", "email") or "No email"


@strawberry.type
class UserResult:
    user: Optional[User]
    error: Optional[Error]


@strawberry.type
class Player:
    id: int

    @strawberry.field
    def name(self) -> str:
        return get_redis().get(f"player:{self.id}:name") or "No name"

    @strawberry.field
    def shots(self) -> List[Shot]:
        for shot_id in get_redis().smembers(f"player:{self.id}:shots"):
            yield Shot(id=int(shot_id))


@strawberry.type
class PlayerResult:
    player: Optional[Player]
    error: Optional[Error]


@strawberry.type
class Shot:
    id: int

    @strawberry.field
    def x(self) -> int:  # pylint: disable=invalid-name
        return get_redis().get(f"shot:{self.id}:x") or 0

    @strawberry.field
    def y(self) -> int:  # pylint: disable=invalid-name
        return get_redis().get(f"shot:{self.id}:y") or 0

    @strawberry.field
    def points(self) -> int:
        return get_redis().get(f"shot:{self.id}:points") or 0

    @strawberry.field
    def game(self) -> Game:
        return Game(id=get_redis().get(f"shot:{self.id}:game_id"))

    @strawberry.field
    def missed(self) -> bool:
        return int(get_redis().get(f"shot:{self.id}:missed") or 0)

    @strawberry.field
    def made(self) -> bool:
        return not self.missed()  # lol


@strawberry.type
class ShotResult:
    shot: Optional[Shot]
    error: Optional[Error]


@strawberry.type
class Game:
    id: int

    @strawberry.field
    def date(self) -> datetime:
        return datetime.fromisoformat(
            get_redis().get(f"game:{self.id}:date")
        ) or datetime.utcfromtimestamp(0)

    @strawberry.field
    def team(self) -> Team:
        return Team(id=get_redis().get(f"game:{self.id}:team_id"))

    @strawberry.field
    def name(self) -> str:
        return get_redis().get(f"game:{self.id}:name") or "No name"

    @strawberry.field
    def other_team_name(self) -> str:
        return get_redis().get(f"game:{self.id}:other_team") or "No name"


@strawberry.type
class GameResult:
    game: Optional[Game]
    error: Optional[Error]


@strawberry.type
class Team:
    id: int

    @strawberry.field
    def name(self) -> str:
        return get_redis().get(f"team:{self.id}:name") or "No name"

    @strawberry.field
    def players(self) -> List[Player]:
        for player_id in get_redis().smembers(f"team:{self.id}:players"):
            yield Player(id=player_id)

    @strawberry.field
    def coaches(self) -> List[User]:
        for user_id in get_redis().smembers(f"team:{self.id}:coaches"):
            yield User(id=user_id)


@strawberry.type
class TeamResult:
    team: Optional[Team]
    error: Optional[Error]
