import os
import redis

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),  # change for Docker later
    port=6379,
    decode_responses=True,
)
