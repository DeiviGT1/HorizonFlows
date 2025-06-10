# backend/app/models/vendor.py
from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Vendor(SQLModel, table=True):
    """
    Proveedor externo.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: int  = Field(foreign_key="business.id")
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    business: "Business" = Relationship(back_populates="vendors")
    expenses: List["Expense"] = Relationship(back_populates="vendor")
    payments: List["Payment"] = Relationship(back_populates="vendor")