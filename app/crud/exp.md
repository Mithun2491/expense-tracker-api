from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List, Tuple
from app.models.expense import Expense
from app.models.category import Category

def create_expense(db: Session, expense_data):
    exp = Expense(**expense_data)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

def update_expense(db: Session, expense: Expense, updates: dict):
    for key, val in updates.items():
        setattr(expense, key, val)
    db.commit()
    db.refresh(expense)
    return expense

def delete_expense(db: Session, expense: Expense):
    db.delete(expense)
    db.commit()

def get_expense(db: Session, expense_id: int):
    return db.query(Expense).filter(Expense.id == expense_id).first()

def list_expenses(db: Session, skip: int =0, limit: int =100, category_id: int = None, start_date=None, end_date=None):
    q = db.query(Expense)
    if category_id:
        q = q.filter(Expense.category_id == category_id)
    if start_date:
        q = q.filter(Expense.date >= start_date)
    if end_date:
        q = q.filter(Expense.date <= end_date)
    return q.order_by(Expense.date.desc()).offset(skip).limit(limit).all()

def monthly_summary(db: Session, month: int, year: int):
    # returns list of (category_name, total_amount)
    q = (
        db.query(Category.name, func.sum(Expense.amount).label("total"))
        .join(Expense, Expense.category_id == Category.id)
        .filter(func.strftime("%m", Expense.date) == f"{month:02d}")
        .filter(func.strftime("%Y", Expense.date) == str(year))
        .group_by(Category.name)
        .all()
    )
    return q
