from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional

from app.deps import get_db, get_current_user
from app.schemas.expense import ExpenseCreate, ExpenseRead, ExpenseUpdate
from app.crud.expense import (
    create_expense,
    get_expense,
    update_expense,
    delete_expense,
    list_expenses,
    monthly_summary,
)
from app.crud.category import get_category

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

# ✅ CREATE EXPENSE
@router.post("/", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense_route(
    exp_in: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new expense for the logged-in user."""
    category = get_category(db, exp_in.category_id)
    if not category or category.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist or does not belong to you"
        )

    return create_expense(db, exp_in.dict(), current_user.id)


# ✅ GET SINGLE EXPENSE
@router.get("/{expense_id}", response_model=ExpenseRead)
def get_expense_route(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Fetch a single expense for the logged-in user."""
    expense = get_expense(db, expense_id, current_user.id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


# ✅ LIST EXPENSES (Filter by date/category)
@router.get("/", response_model=List[ExpenseRead])
def list_expenses_route(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    start_date: Optional[date] = Query(None, description="Start date filter"),
    end_date: Optional[date] = Query(None, description="End date filter"),
):
    """List all expenses of the logged-in user with optional filters."""
    return list_expenses(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date
    )


# ✅ UPDATE EXPENSE
@router.put("/{expense_id}", response_model=ExpenseRead)
def update_expense_route(
    expense_id: int,
    exp_in: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update an expense owned by the logged-in user."""
    expense = update_expense(db, expense_id, exp_in.dict(exclude_unset=True), current_user.id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found or not owned by user")
    return expense


# ✅ DELETE EXPENSE
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense_route(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete an expense owned by the logged-in user."""
    success = delete_expense(db, expense_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found or not owned by user")
    return {"message": "Expense deleted successfully"}


# ✅ MONTHLY SUMMARY
@router.get("/summary/", summary="Monthly expense summary by category")
def monthly_summary_route(
    month: int = Query(..., ge=1, le=12, description="Month number (1–12)"),
    year: int = Query(..., description="Year (e.g., 2025)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Summarize expenses by category for a given month and year."""
    summary = monthly_summary(db, month, year, current_user.id)
    return [
        {"category": category_name, "total_amount": total}
        for category_name, total in summary
    ]
