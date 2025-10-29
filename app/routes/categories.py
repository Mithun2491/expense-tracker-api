from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.crud.category import create_category, get_category_by_name, list_categories
from app.schemas.category import CategoryCreate, CategoryRead
from app.models.user import User  # ✅ Import to type-hint current_user

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    dependencies=[Depends(get_current_user)]  # ✅ Secures all routes globally
)

# ✅ Create Category
@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create(cat_in: CategoryCreate, 
           db: Session = Depends(get_db), 
           current_user: User = Depends(get_current_user)):  # ✅ Get logged-in user
    existing = get_category_by_name(db, cat_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    # ✅ Must pass user_id
    return create_category(db, name=cat_in.name, user_id=current_user.id)

# ✅ List Categories
@router.get("/", response_model=list[CategoryRead])
def read_all(skip: int = 0, limit: int = 100, 
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):  # optional, but consistent
    return list_categories(db, skip=skip, limit=limit)
