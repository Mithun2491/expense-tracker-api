from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.models.base import Base  # ✅ Use correct Base import from models

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)            # Who performed the action
    action = Column(String(200), nullable=False)        # e.g. "expense.create"
    target_type = Column(String(100), nullable=False)   # e.g. "expense", "category"
    target_id = Column(Integer, nullable=True)          # ID of the entity affected
    data = Column(JSON, nullable=True)                  # Extra metadata (old/new values)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
