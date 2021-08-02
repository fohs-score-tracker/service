from ..objects import Error, Player, PlayerResult
from ..utils import get_redis


def create_player(name: str) -> Player:
    redis = get_redis()
    player_id = redis.incr("next_player_id")
    redis.set(f"player:{player_id}:name", name)
    redis.sadd("players", player_id)
    return Player(id=player_id)


def update_player(player_id: int, name: str) -> PlayerResult:
    redis = get_redis()
    if not redis.sismember("players", player_id):
        return PlayerResult(
            player=None, error=Error(field="id", detail="Player does not exist.")
        )
    redis.set(f"player:{player_id}:name", name)
    return PlayerResult(player=Player(id=1), error=None)


def delete_player(player_id: int) -> bool:
    redis = get_redis()
    if not redis.delete(f"player:{player_id}:name"):
        return False
    redis.srem("players", player_id)
    # TODO: delete shots and stuff
    return True
