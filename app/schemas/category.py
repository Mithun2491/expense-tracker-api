from pydantic import BaseModel
from typing import Optional

# ✅ Schema used for creating a category
class CategoryCreate(BaseModel):
    name: str

# ✅ Schema returned when reading a category record
class CategoryRead(BaseModel):
    id: int
    name: str
    user_id: Optional[int]  # ✅ Shows which user owns the category

    class Config:
        orm_mode = True
