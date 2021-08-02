from ..inputs import CreateGame, UpdateGame
from ..objects import Error, Game, GameResult
from ..utils import get_redis


def create_game(game: CreateGame) -> GameResult:
    redis = get_redis()
    if not redis.sismember("teams", game.team_id):
        return GameResult(
            game=None, error=Error(field="teamId", detail="Team does not exist.")
        )
    game_id = redis.incr("next_game_id")
    prefix = f"game:{game_id}"
    redis.set(prefix + ":team_id", game.team_id)
    redis.set(prefix + ":name", game.name)
    redis.set(prefix + ":other_team", game.other_team_name)
    redis.set(prefix + ":date", str(game.date))

    redis.sadd("games", game_id)
    return GameResult(game=Game(id=game_id), error=None)


def update_game(game_id: int, game: UpdateGame) -> GameResult:
    redis = get_redis()
    prefix = f"game:{game_id}"
    if game.team_id is not None:
        if not redis.sismember("teams", game.team_id):
            return GameResult(
                game=None, error=Error(field="teamId", detail="Team does not exist.")
            )
        redis.set(prefix + ":team_id", game.team_id)
    if game.name:
        redis.set(prefix + ":name", game.name)
    if game.other_team_name:
        redis.set(prefix + ":other_team", game.other_team_name)
    if game.date:
        redis.set(prefix + ":date", str(game.date))
    return GameResult(game=Game(id=game_id), error=None)


def delete_game(game_id: int) -> bool:
    redis = get_redis()
    if not redis.sismember("games", game_id):
        return False
    prefix = f"game:{game_id}"
    redis.srem("games", game_id)
    redis.delete(
        prefix + ":team_id", prefix + ":name", prefix + ":other_team", prefix + ":date"
    )
    return True
