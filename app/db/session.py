from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# ✅ PostgreSQL Engine (no need for sqlite check)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Ensures the connection is valid
    pool_size=10,        # Connection pool size for performance
    max_overflow=20      # Extra connections allowed beyond pool_size
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
