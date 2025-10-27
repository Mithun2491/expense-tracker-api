from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from app.deps import get_db, get_current_user
from app.schemas.expense import ExpenseCreate, ExpenseRead, ExpenseUpdate
from app.crud.expense import (
    create_expense,
    get_expense,
    update_expense,
    delete_expense,
    list_expenses,
    monthly_summary
)
from app.crud.category import get_category

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
    dependencies=[Depends(get_current_user)]
)

# ✅ Create Expense
@router.post("/", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create(exp_in: ExpenseCreate, db: Session = Depends(get_db)):
    category = get_category(db, exp_in.category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Category not found")
    return create_expense(db, exp_in.dict())

# ✅ List Expenses with optional filters
@router.get("/", response_model=list[ExpenseRead])
def read_all(
    skip: int = 0,
    limit: int = 100,
    category_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    return list_expenses(db, skip=skip, limit=limit, category_id=category_id, start_date=start_date, end_date=end_date)

# ✅ Monthly Summary (⚠ must be above /{expense_id} route)
@router.get("/summary/monthly")
def monthly(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=1970),
    db: Session = Depends(get_db)
):
    summary = monthly_summary(db, month, year)
    return [{"category": name, "total": total} for name, total in summary]

# ✅ Get Single Expense
@router.get("/{expense_id}", response_model=ExpenseRead)
def read_one(expense_id: int, db: Session = Depends(get_db)):
    exp = get_expense(db, expense_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    return exp

# ✅ Update Expense
@router.put("/{expense_id}", response_model=ExpenseRead)
def update(expense_id: int, updates: ExpenseUpdate, db: Session = Depends(get_db)):
    exp = get_expense(db, expense_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    if updates.category_id:
        if not get_category(db, updates.category_id):
            raise HTTPException(status_code=400, detail="Category not found")
    data = updates.dict(exclude_unset=True)
    return update_expense(db, exp, data)

# ✅ Delete Expense
@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove(expense_id: int, db: Session = Depends(get_db)):
    exp = get_expense(db, expense_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    delete_expense(db, exp)
    return
