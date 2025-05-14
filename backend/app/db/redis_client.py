import redis
from app.config import settings

def get_redis_client():
    try:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=int(settings.REDIS_PORT),
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
        redis_client.ping()  # Test connection
        return redis_client
    except redis.ConnectionError as e:
        print(f"Redis connection failed: {e}")
        raise

redis_client = get_redis_client()