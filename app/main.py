# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.redis_client import redis_client
from app.core.rate_limiter import RateLimitMiddleware
from app.db.base import Base
from app.db.session import engine
from app.routes import auth, categories, expenses

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔌 Initializing Redis...")
    await redis_client.connect()

    if redis_client.client:
        print("✅ Redis connected, rate limiting is enabled!")
    else:
        print("⚠ Redis NOT connected. Rate Limiting will be disabled.")

    if settings.DEBUG:
        print("🛠 Creating database tables (development only)...")
        Base.metadata.create_all(bind=engine)

    print("✅ Startup complete!")
    yield  # <-- this is important, control passes to FastAPI here

    print("❌ Closing Redis...")
    await redis_client.close()

# ✅ Create FastAPI app with lifespan
app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# ✅ Add rate limiting middleware
app.add_middleware(RateLimitMiddleware)

# ✅ Include all routers
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(expenses.router)

@app.get("/", summary="Health Check")
async def root():
    return {"message": "🚀 Expense Tracker API is running!"}
