from fastapi import Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from .config import settings

async def setup_rate_limiter():
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis)

rate_limiter = RateLimiter(times=100, seconds=60)