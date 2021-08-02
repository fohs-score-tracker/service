from ..inputs import CreateTeam, UpdateTeam
from ..objects import Error, Team, TeamResult
from ..utils import get_redis


def create_team(team: CreateTeam) -> TeamResult:
    redis = get_redis()
    if team.players:
        for player_id in team.players:
            if not redis.sismember("players", player_id):
                return TeamResult(
                    team=None,
                    error=Error(
                        field="players",
                        detail=f"Player with ID {player_id} does not exist.",
                    ),
                )
    if team.coaches:
        for coach_id in team.coaches:
            if not redis.exists(f"user:{coach_id}"):
                return TeamResult(
                    team=None,
                    error=Error(
                        field="coaches",
                        detail=f"User with ID {coach_id} does not exist.",
                    ),
                )
    team_id = redis.incr("next_team_id")
    prefix = f"team:{team_id}"
    redis.sadd("teams", team_id)
    if team.players:
        redis.sadd(prefix + ":players", *team.players)
    if team.coaches:
        redis.sadd(prefix + ":coaches", *team.coaches)
    redis.set(prefix + ":name", team.name)
    return TeamResult(team=Team(id=team_id), error=None)


def update_team(team_id: int, team: UpdateTeam) -> TeamResult:
    redis = get_redis()
    if not redis.sismember("teams", team_id):
        return TeamResult(
            team=None, error=Error(field="id", detail="Team does not exist.")
        )
    prefix = f"team:{team_id}"
    if team.name:
        redis.set(prefix + ":name", team.name)
    if team.players is not None:
        redis.delete(prefix + ":players")
        for player_id in team.players:
            if not redis.sismember("players", player_id):
                return TeamResult(
                    team=None,
                    error=Error(
                        field="players",
                        detail=f"Player with ID {player_id} does not exist.",
                    ),
                )
        redis.sadd(prefix + ":players", *team.players)
    if team.coaches is not None:
        redis.delete(prefix + ":coaches")
        for coach_id in team.coaches:
            if not redis.exists(f"user:{coach_id}"):
                return TeamResult(
                    team=None,
                    error=Error(
                        field="coaches",
                        detail=f"User with ID {coach_id} does not exist.",
                    ),
                )
        redis.sadd(prefix + ":coaches", *team.coaches)
    return TeamResult(error=None, team=Team(id=team_id))


def delete_team(team_id: int) -> bool:
    redis = get_redis()
    if not redis.sismember("teams", team_id):
        return False
    redis.srem("teams", team_id)
    prefix = f"team:{team_id}"
    redis.delete(prefix + ":name", prefix + ":players", prefix + ":coaches")
    return True
