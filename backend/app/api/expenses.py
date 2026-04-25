from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from app.db import models
from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

class ExpenseCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0)
    date: date

class ExpenseRead(ExpenseCreate):
    id: int
    class Config:
        orm_mode = True

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ExpenseRead], tags=["Expenses"])
def get_expenses(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Get a paginated list of expenses."""
    return db.query(models.Expense).offset(skip).limit(limit).all()

@router.post("/", response_model=ExpenseRead, tags=["Expenses"])
def add_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    """Add a new expense."""
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.delete("/{expense_id}", tags=["Expenses"])
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """Delete an expense by ID."""
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"ok": True}