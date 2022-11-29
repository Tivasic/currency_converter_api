import aioredis
from typing import Any, NoReturn
import json
from typing import Optional

redis_connection = aioredis.from_url("redis://127.0.0.1:6379")


def cast(
    value: Optional[Any],  # this is a value loaded from redis
    expected_type: str = "str",
) -> Optional[Any]:
    if any([value is None, expected_type is None]):
        return value

    if expected_type == "dict":
        return json.loads(value)
    if expected_type == "str":
        return value.decode("utf-8")


async def get(key: str, expected_type: Optional[str] = "str") -> Any:
    results = await redis_connection.get(key)
    return cast(value=results, expected_type=expected_type)


async def lpush(key: str, value: str) -> None:
    await redis_connection.lpush(key, value)


async def rpoplpush(key: str) -> str:
    return await redis_connection.rpoplpush(key, key)


async def store(key: str, value: Any) -> None:
    if isinstance(value, dict):
        value = json.dumps(value)
    await redis_connection.set(name=key, value=value)


async def store_exp(key: str, time: int, value: dict) -> None:
    await redis_connection.setex(name=key, time=time, value=json.dumps(value))


def ping() -> bool | NoReturn:
    return redis_connection.ping()
