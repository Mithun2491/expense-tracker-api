from sqlalchemy.orm import Session
from app.models.expense import Expense

def create_expense(db: Session, expense_data: dict):
    exp = Expense(**expense_data)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

def get_expense(db: Session, expense_id: int):
    return db.query(Expense).filter(Expense.id == expense_id).first()

def list_expenses(db: Session, skip=0, limit=100, category_id=None, start_date=None, end_date=None):
    query = db.query(Expense)
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    return query.offset(skip).limit(limit).all()
