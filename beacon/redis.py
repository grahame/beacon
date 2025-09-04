import redis
from .settings import settings


def get_redis():
    pool = redis.ConnectionPool().from_url(settings.redis_location)
    return redis.Redis().from_pool(pool)
