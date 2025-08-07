# backend/app/models/expense.py

from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship

class Expense(SQLModel, table=True):
    __tablename__ = "expense"

    id: Optional[int] = Field(default=None, primary_key=True)
    vendor_id: int = Field(foreign_key="vendor.id")
    date: datetime = Field(default_factory=datetime.utcnow)
    total: float
    status: str = Field(default="draft")

    # Relación a líneas
    lines: List["ExpenseLine"] = Relationship(back_populates="expense")
    vendor: List["Vendor"] = Relationship(back_populates="expenses")


class ExpenseLine(SQLModel, table=True):
    __tablename__ = "expense_line"

    id: Optional[int] = Field(default=None, primary_key=True)
    expense_id: int = Field(foreign_key="expense.id")
    account_id: int = Field(foreign_key="chart_of_account.id")
    
    amount: float
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Vincula de vuelta a la Expense
    expense: Optional["Expense"] = Relationship(back_populates="lines")