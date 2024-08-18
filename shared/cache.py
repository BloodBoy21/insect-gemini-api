from redis import Redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
REDIS_TLS = os.getenv("REDIS_TLS", "False") == "True"
cache = None


def init_redis():
    global cache
    try:
        print(
            f"Connecting to Redis at {REDIS_HOST}:{REDIS_PORT}, db={REDIS_DB}, tls={REDIS_TLS}"
        )
        cache = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            ssl=REDIS_TLS,
        )
        if Redis.ping(cache):
            print("Redis is running")
        else:
            print("Redis is not running")
    except Exception as e:
        print("Error connecting to Redis", e)


def get_redis() -> Redis:
    global cache
    if not cache:
        init_redis()
    return cache
