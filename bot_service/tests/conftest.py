import pytest
from fakeredis.aioredis import FakeRedis


@pytest.fixture
async def fake_redis():
    """Фикстура с фейковым async Redis."""
    redis = FakeRedis(decode_responses=True)
    yield redis
    await redis.flushall()
    await redis.aclose()