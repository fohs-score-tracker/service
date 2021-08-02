from typing import List, Optional

import strawberry

from .objects import Game, Player, Team, User
from .utils import get_redis


@strawberry.type
class Query:
    @strawberry.field
    def keys(self) -> List[str]:
        for key in get_redis().scan_iter():
            yield key

    @strawberry.field
    def users(self) -> List[User]:
        for key in get_redis().scan_iter("user:*"):
            yield User(id=key.split(":")[1])

    @strawberry.field
    def user(self, user_id: int) -> Optional[User]:
        if get_redis().exists(f"user:{user_id}"):
            return User(id=user_id)

    @strawberry.field
    def players(self) -> List[Player]:
        for player_id in get_redis().smembers("players"):
            yield Player(id=player_id)

    @strawberry.field
    def player(self, player_id: int) -> Optional[Player]:
        if get_redis().sismember("players", player_id):
            return Player(id=player_id)

    @strawberry.field
    def teams(self) -> List[Team]:
        for team_id in get_redis().smembers("teams"):
            yield Team(id=team_id)

    @strawberry.field
    def team(self, team_id: int) -> Optional[Team]:
        if get_redis().sismember("teams", team_id):
            return Team(id=team_id)

    @strawberry.field
    def games(self) -> List[Game]:
        for game_id in get_redis().smembers("games"):
            yield Game(id=game_id)

    @strawberry.field
    def game(self, game_id: int) -> Optional[Game]:
        if get_redis().sismember("games", game_id):
            return Game(id=game_id)
