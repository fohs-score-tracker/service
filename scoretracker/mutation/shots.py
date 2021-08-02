from ..inputs import CreateShot
from ..objects import Error, Shot, ShotResult
from ..utils import get_redis


def create_shot(player_id: int, shot: CreateShot) -> ShotResult:
    redis = get_redis()
    if not redis.sismember("players", player_id):
        return ShotResult(
            shot=None, error=Error(field="player_id", detail="Player does not exist")
        )
    if not redis.sismember("games", shot.game_id):
        return ShotResult(
            shot=None, error=Error(field="game_id", detail="Game does not exist")
        )
    shot_id = redis.incr("next_shot_id")
    prefix = f"shot:{shot_id}"
    redis.set(prefix + ":x", shot.x)
    redis.set(prefix + ":y", shot.y)
    redis.set(prefix + ":points", shot.points)
    redis.set(prefix + ":missed", int(shot.missed))
    redis.set(prefix + ":game_id", shot.game_id)
    redis.sadd(f"player:{player_id}:shots", shot_id)
    return ShotResult(error=None, shot=Shot(id=shot_id))
