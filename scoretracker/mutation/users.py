from ..inputs import CreateUser, UpdateUser
from ..objects import Error, User, UserResult
from ..utils import get_redis


def create_user(user: CreateUser) -> UserResult:
    redis = get_redis()
    for key in redis.scan_iter("user:*"):
        if redis.hget(key, "email") == user.email:
            return UserResult(
                user=None,
                error=Error(
                    field="email", detail="A user with that email already exists."
                ),
            )
    user_id = redis.incr("next_user_id")
    redis.hset(
        f"user:{user_id}",
        mapping={
            "id": user_id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
        },
    )
    return UserResult(error=None, user=User(id=user_id))


def update_user(user_id: int, user: UpdateUser) -> UserResult:
    redis = get_redis()
    key = f"user:{user_id}"
    if not redis.exists(key):
        return UserResult(
            user=None, error=Error(field="id", detail="User does not exist.")
        )
    if user.email is not None:
        for key in redis.scan_iter("user:*"):
            if redis.hget(key, "email") == user.email:
                return UserResult(
                    user=None,
                    error=Error(
                        field="email", detail="A different user already has that email."
                    ),
                )
        redis.hset(key, "email", user.email)
    if user.name is not None:
        redis.hset(key, "name", user.name)
    if user.password is not None:
        redis.hset(key, "password", user.password)
    return UserResult(error=None, user=User(id=user_id))


def delete_user(user_id: int) -> bool:
    return get_redis().delete(f"user:{user_id}") == 1


# TODO: add me endpoint
