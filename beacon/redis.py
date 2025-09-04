import redis
import os


def get_redis():
    pool = redis.ConnectionPool().form_url(os.environ.get("REDIS_URL"))
    return redis.Redis().from_pool(pool)
