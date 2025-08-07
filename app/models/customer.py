# backend/app/models/customer.py
from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class Customer(SQLModel, table=True):
    """
    Cliente externo.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: int  = Field(foreign_key="business.id")
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    business: "Business" = Relationship(back_populates="customers")
    invoices: List["Invoice"] = Relationship(back_populates="customer")
    payments: List["Payment"] = Relationship(back_populates="customer")