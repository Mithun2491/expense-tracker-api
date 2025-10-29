# app/models/base.py
from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.orm import declared_attr
from sqlalchemy.ext.declarative import as_declarative

@as_declarative()
class Base:
    id: int
    __name__: str

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)
