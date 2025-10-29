from sqlalchemy.orm import Session
from app.models.category import Category

def create_category(db: Session, name: str, user_id: int):
    """
    Create a new category for a specific user.
    """
    cat = Category(name=name, user_id=user_id)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()

def list_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()
