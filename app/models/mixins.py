# app/models/mixins.py
import datetime
from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.sql import func

class TimestampMixin:
    """
    Automatically sets created_at and updated_at timestamps.
    - created_at: time when record is created
    - updated_at: time when record is updated
    """
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now(), nullable=False)


class SoftDeleteMixin:
    """
    Adds soft delete functionality.
    - is_deleted: flag to mark record as deleted
    - deleted_at: timestamp when record was marked deleted
    """
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.datetime.utcnow()
