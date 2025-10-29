from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.mixins import TimestampMixin, SoftDeleteMixin  # ✅ path correct


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)  # ✅ Added: store user's full name
    hashed_password = Column(String(255), nullable=False)
    
    categories = relationship("Category", back_populates="user", cascade="all, delete")

    # ✅ Relationships
    expenses = relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
