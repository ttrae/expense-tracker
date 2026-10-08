from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date as DateType
import os

app = FastAPI()

DATABASE_URL = "sqlite:///./expenses.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)


class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str
    date: DateType


class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional[DateType] = None


Base.metadata.create_all(bind=engine)


@app.get("/")
def serve_ui():
    return FileResponse(os.path.join("static", "index.html"))


@app.get("/api/expenses")
def get_expenses():
    db = SessionLocal()
    try:
        expenses = db.query(Expense).order_by(Expense.date.desc()).all()
        return [
            {
                "id": e.id,
                "title": e.title,
                "amount": e.amount,
                "category": e.category,
                "date": e.date.isoformat(),
            }
            for e in expenses
        ]
    finally:
        db.close()


@app.post("/api/expenses")
def create_expense(expense: ExpenseCreate):
    db = SessionLocal()
    try:
        new_expense = Expense(
            title=expense.title,
            amount=expense.amount,
            category=expense.category,
            date=expense.date,
        )
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)
        return {
            "id": new_expense.id,
            "title": new_expense.title,
            "amount": new_expense.amount,
            "category": new_expense.category,
            "date": new_expense.date.isoformat(),
        }
    finally:
        db.close()


@app.get("/api/expenses/{expense_id}")
def get_expense(expense_id: int):
    db = SessionLocal()
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        return {
            "id": expense.id,
            "title": expense.title,
            "amount": expense.amount,
            "category": expense.category,
            "date": expense.date.isoformat(),
        }
    finally:
        db.close()


@app.put("/api/expenses/{expense_id}")
def update_expense(expense_id: int, expense: ExpenseUpdate):
    db = SessionLocal()
    try:
        db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if not db_expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        if expense.title is not None:
            db_expense.title = expense.title
        if expense.amount is not None:
            db_expense.amount = expense.amount
        if expense.category is not None:
            db_expense.category = expense.category
        if expense.date is not None:
            db_expense.date = expense.date
        db.commit()
        db.refresh(db_expense)
        return {
            "id": db_expense.id,
            "title": db_expense.title,
            "amount": db_expense.amount,
            "category": db_expense.category,
            "date": db_expense.date.isoformat(),
        }
    finally:
        db.close()


@app.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int):
    db = SessionLocal()
    try:
        expense = db.query(Expense).filter(Expense.id == expense_id).first()
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        db.delete(expense)
        db.commit()
        return {"detail": "Expense deleted"}
    finally:
        db.close()


app.mount("/static", StaticFiles(directory="static"), name="static")
