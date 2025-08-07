# backend/app/models/chart_of_account.py
from enum import Enum
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class AccountType(str, Enum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"

class ChartOfAccount(SQLModel, table=True):
    __tablename__ = "chart_of_account"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(nullable=False, unique=True, index=True, max_length=16)
    name: str = Field(nullable=False, max_length=100)
    type: AccountType = Field(nullable=False)
    parent_id: Optional[int] = Field(default=None, foreign_key="chart_of_account.id")
    description: Optional[str] = None

    children: List["ChartOfAccount"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={"cascade": "all,delete-orphan"}
    )
    parent: Optional["ChartOfAccount"] = Relationship(back_populates="children")