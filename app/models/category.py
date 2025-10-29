from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.mixins import TimestampMixin, SoftDeleteMixin

class Category(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)

    # ✅ If you want categories to be user-specific (recommended for real apps):
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # ✅ Relationship back to user
    user = relationship("User", back_populates="categories")

    # ✅ Relationship to expenses
    expenses = relationship("Expense", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category id={self.id} name={self.name}>"
