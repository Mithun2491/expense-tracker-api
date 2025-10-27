from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.routes import auth, categories, expenses

app = FastAPI(title="Expense Tracker API")

# create tables (simple approach; for prod use alembic migrations)
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(expenses.router)
