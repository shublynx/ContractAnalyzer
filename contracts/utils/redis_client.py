import redis
from django.conf import settings

# This singleton prevents connection leaks on your Ubuntu server
redis_client = redis.Redis(
    host=getattr(settings, 'REDIS_HOST', 'localhost'),
    port=getattr(settings, 'REDIS_PORT', 6379),
    decode_responses=True
)