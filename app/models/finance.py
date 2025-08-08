# backend/app/models/finance.py

from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import date, datetime
from enum import Enum

class CashActivityType(str, Enum):
    IN = "in"
    OUT = "out"

class ExpenseCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    expenses: List["Expense"] = Relationship(back_populates="category")

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    amount: float
    date: date
    
    category_id: int = Field(foreign_key="expensecategory.id")
    category: ExpenseCategory = Relationship(back_populates="expenses")
    
class CashDrawerActivity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    type: CashActivityType
    amount: float
    reason: str
    
    shift_id: int = Field(foreign_key="shift.id")
    # Referencia hacia adelante para evitar importación circular
    shift: "Shift" = Relationship(back_populates="cash_activities")