# backend/app/models/category.py

from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum

class CategoryType(str, Enum):
    expense = "expense"
    income = "income"
    both = "both"


class Category(SQLModel, table=True):
    """
    Categorías para agrupar líneas de ExpenseLine e InvoiceLine,
    con soporte opcional para jerarquía padre-hijo.
    """
    __tablename__ = "category"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    type: CategoryType = Field(sa_column_kwargs={"default": CategoryType.both})
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id")

    # Relaciones jerárquicas
    parent: Optional["Category"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Category.id"}
    )
    children: List["Category"] = Relationship(back_populates="parent")

    # Relaciones a las líneas de gasto e ingreso
    expense_lines: List["ExpenseLine"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    invoice_lines: List["InvoiceLine"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    account: Optional["ChartOfAccount"] = Relationship(back_populates="category")