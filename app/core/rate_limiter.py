# app/core/rate_limiter.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from app.core.config import settings
from app.core.redis_client import redis_client

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit = int(settings.RATE_LIMIT_REQUESTS)
        self.window = int(settings.RATE_LIMIT_PERIOD_SECONDS)

    async def dispatch(self, request: Request, call_next):

        # Skip root health check
        if request.url.path == "/":
            return await call_next(request)

        # ✅ Ensure Redis is connected
        if not redis_client.client:
            print("⚠ Redis not connected. Skipping rate limiting.")
            return await call_next(request)

        user_identifier = await self.get_user_identifier(request)
        key = f"rate_limit:{user_identifier}"

        redis = redis_client.client  # ✅ Short reference

        # ✅ Get request count
        current_count = await redis.get(key)
        current_count = int(current_count) if current_count else 0

        if current_count >= self.rate_limit:
            raise HTTPException(
                status_code=429,
                detail=f"Too Many Requests! Limit is {self.rate_limit} per {self.window} seconds."
            )

        # ✅ Increment with proper TTL
        async with redis.pipeline() as pipe:
            pipe.incr(key)
            ttl = await redis.ttl(key)
            if current_count == 0 or ttl is None or ttl < 0:
                pipe.expire(key, self.window)
            await pipe.execute()

        return await call_next(request)

    async def get_user_identifier(self, request: Request) -> str:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                return payload.get("sub") or request.client.host
            except JWTError:
                return request.client.host
        return request.client.host
