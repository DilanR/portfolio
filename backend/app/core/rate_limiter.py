import time
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.redis import redis_client

RATE_LIMIT = 5
WINDOW = 60  # seconds


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.client is None:
            raise HTTPException(status_code=400, detail="Cannot determine client IP")

        forwarded = request.headers.get("x-forwarded-for")
        ip = forwarded.split(",")[0].strip() if forwarded else request.client.host

        key = f"rate_limit:{ip}"
        now = time.time()
        window_start = now - WINDOW

        pipe = redis_client.pipeline()

        pipe.zremrangebyscore(key, 0, window_start)

        pipe.zadd(key, {str(now): now})

        pipe.zcard(key)

        pipe.expire(key, WINDOW)

        _, _, count, _ = pipe.execute()

        if count > RATE_LIMIT:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded",
                headers={"Retry-After": str(WINDOW)},
            )

        return await call_next(request)
