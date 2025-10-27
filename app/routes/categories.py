from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.crud.category import create_category, get_category_by_name, list_categories
from app.schemas.category import CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
def create(cat_in: CategoryCreate, db: Session = Depends(get_db)):
    existing = get_category_by_name(db, cat_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    return create_category(db, cat_in.name)

@router.get("/", response_model=list[CategoryRead], dependencies=[Depends(get_current_user)])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_categories(db, skip=skip, limit=limit)
