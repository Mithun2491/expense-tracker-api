# app/core/redis_client.py
import logging
from redis import asyncio as aioredis
from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        self.client = None

    async def connect(self):
        self.client = await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            encoding="utf-8",
            decode_responses=True  # Automatically convert bytes to strings
        )
        logger.info("✅ Redis Connected Successfully")
        print("✅ Redis Connected Successfully")

    async def close(self):
        if self.client:
            try:
                await self.client.close()
                logger.info("❌ Redis Connection Closed")
            except Exception as e:
                logger.error(f"Error closing Redis connection: {e}")

redis_client = RedisClient()
