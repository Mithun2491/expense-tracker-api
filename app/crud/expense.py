from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.expense import Expense
from app.models.category import Category

# ✅ Create Expense
def create_expense(db: Session, expense_data: dict):
    exp = Expense(**expense_data)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

# ✅ Get Expense by ID
def get_expense(db: Session, expense_id: int):
    return db.query(Expense).filter(Expense.id == expense_id).first()

# ✅ List Expenses with optional filters
def list_expenses(db: Session, skip: int = 0, limit: int = 100, category_id: int = None, start_date=None, end_date=None):
    query = db.query(Expense)
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    return query.offset(skip).limit(limit).all()

# ✅ Update Expense
def update_expense(db: Session, expense_id: int, expense_data: dict):
    exp = db.query(Expense).filter(Expense.id == expense_id).first()
    if not exp:
        return None
    for key, value in expense_data.items():
        setattr(exp, key, value)
    db.commit()
    db.refresh(exp)
    return exp

# ✅ Delete Expense
def delete_expense(db: Session, expense_id: int):
    exp = db.query(Expense).filter(Expense.id == expense_id).first()
    if not exp:
        return None
    db.delete(exp)
    db.commit()
    return True

# ✅ Monthly Summary
def monthly_summary(db: Session, month: int, year: int):
    return (
        db.query(Category.name, func.sum(Expense.amount))
        .join(Expense, Expense.category_id == Category.id)
        .filter(func.extract('month', Expense.date) == month)
        .filter(func.extract('year', Expense.date) == year)
        .group_by(Category.name)
        .all()
    )
