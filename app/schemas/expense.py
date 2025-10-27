from pydantic import BaseModel
from datetime import date
from typing import Optional

class CategoryRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # Required in Pydantic v2

class ExpenseBase(BaseModel):
    title: str
    amount: float
    date: date
    description: Optional[str] = None
    category_id: int

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[date] = None # type: ignore
    description: Optional[str] = None
    category_id: Optional[int] = None

class ExpenseRead(ExpenseBase):
    id: int
    category: Optional[CategoryRead]  # THIS FIXES THE ERROR

    class Config:
        from_attributes = True  # Replacement for orm_mode in Pydantic v2
