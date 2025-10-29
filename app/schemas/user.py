from pydantic import BaseModel, EmailStr
from typing import Optional

# ✅ Schema for user registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

# ✅ Schema for reading user data (returned to client)
class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None

    class Config:
        orm_mode = True  # ✅ Allows returning ORM models directly
