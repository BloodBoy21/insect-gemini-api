from shared.cache import get_redis
import json
from logging import getLogger

logger = getLogger(__name__)

CACHE_EXPIRATION = 60 * 60 * 24  # 24 hours
cache = get_redis()


def add_data_to_cache(key: str, data: dict):
    try:
        cache.lpush(key, json.dumps(data))
        if cache.llen(key) == 1:
            cache.expire(key, CACHE_EXPIRATION)
    except Exception as e:
        logger.error(str(e))
        return False


def get_user_data(user_id: str):
    try:
        data = cache.lrange(user_id, 0, -1)
        return [json.loads(d) for d in data]
    except Exception as e:
        logger.error(str(e))
        return []


def exits_user_data(user_id: str):
    try:
        return cache.exists(user_id)
    except Exception as e:
        logger.error(str(e))
        return False


def reset_user_data(user_id: str):
    try:
        cache.delete(user_id)
        return True
    except Exception as e:
        logger.error(str(e))
        return False
