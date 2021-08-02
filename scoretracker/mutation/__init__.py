import strawberry

from ..utils import get_redis
from . import games, players, shots, teams, users


@strawberry.type
class Mutation:
    create_user = strawberry.field(users.create_user)
    update_user = strawberry.field(users.update_user)
    delete_user = strawberry.field(users.delete_user)

    create_player = strawberry.field(players.create_player)
    update_player = strawberry.field(players.update_player)
    delete_player = strawberry.field(players.delete_player)

    create_team = strawberry.field(teams.create_team)
    update_team = strawberry.field(teams.update_team)
    delete_team = strawberry.field(teams.delete_team)

    create_game = strawberry.field(games.create_game)
    update_game = strawberry.field(games.update_game)
    delete_game = strawberry.field(games.delete_game)

    create_shot = strawberry.field(shots.create_shot)

    @strawberry.field
    def flush_database(self) -> bool:
        get_redis().flushdb()
        return True
