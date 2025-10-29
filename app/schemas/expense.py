from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from .category import CategoryRead

# ---------- Base Schema ----------
class ExpenseBase(BaseModel):
    title: str
    amount: float
    date: date
    description: Optional[str] = None
    category_id: Optional[int] = None

# ---------- Create ----------
class ExpenseCreate(ExpenseBase):
    pass

# ---------- Update ----------
class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[date] = None  # type: ignore
    description: Optional[str] = None
    category_id: Optional[int] = None

# ---------- Read ----------
class ExpenseRead(ExpenseBase):
    id: int
    user_id: int  # ✅ Very important for multi-user applications
    category: Optional[CategoryRead] = None  # ✅ Eager relationship
    is_deleted: bool  # ✅ Soft delete visibility
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # ✅ Required in Pydantic v2
