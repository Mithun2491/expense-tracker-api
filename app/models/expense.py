from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.mixins import TimestampMixin, SoftDeleteMixin

class Expense(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # ✅ Relationships
    category = relationship("Category", back_populates="expenses")
    user = relationship("User", back_populates="expenses")

    def __repr__(self):
        return f"<Expense id={self.id} title={self.title} amount={self.amount}>"
