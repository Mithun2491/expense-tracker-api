from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from app.models.expense import Expense
from app.models.category import Category


# ✅ Create Expense (User-specific, validates category ownership)
def create_expense(db: Session, expense_data: dict, user_id: int):
    """
    Creates an expense for the logged-in user and validates category ownership.
    """
    category = db.query(Category).filter(
        Category.id == expense_data.get("category_id"),
        Category.user_id == user_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist or does not belong to the user."
        )

    expense = Expense(**expense_data, user_id=user_id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


# ✅ Get Expense by ID (User-restricted)
def get_expense(db: Session, expense_id: int, user_id: int):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user_id
    ).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found."
        )
    return expense


# ✅ List Expenses (Supports filters: category/date range)
def list_expenses(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    category_id: int = None,
    start_date=None,
    end_date=None
):
    query = db.query(Expense).filter(Expense.user_id == user_id)

    if category_id:
        query = query.filter(Expense.category_id == category_id)
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)

    return query.order_by(Expense.date.desc()).offset(skip).limit(limit).all()


# ✅ Update Expense (User-restricted)
def update_expense(db: Session, expense_id: int, expense_data: dict, user_id: int):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user_id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found or does not belong to this user."
        )

    for key, value in expense_data.items():
        if hasattr(expense, key):
            setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return expense


# ✅ Delete Expense (Soft delete support ready)
def delete_expense(db: Session, expense_id: int, user_id: int):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user_id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found or already deleted."
        )

    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully."}


# ✅ Monthly Summary (User-specific by month/year)
def monthly_summary(db: Session, month: int, year: int, user_id: int):
    """
    Returns total spending per category for the given month and year.
    """
    summary = (
        db.query(Category.name, func.sum(Expense.amount).label("total_spent"))
        .join(Expense, Expense.category_id == Category.id)
        .filter(Expense.user_id == user_id)
        .filter(func.extract('month', Expense.date) == month)
        .filter(func.extract('year', Expense.date) == year)
        .group_by(Category.name)
        .all()
    )

    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No expenses found for this period."
        )

    return [{"category": name, "total_spent": total} for name, total in summary]
