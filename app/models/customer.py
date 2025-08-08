# backend/app/models/customer.py

from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import date

class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: Optional[str] = Field(default=None, unique=True)
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    
    sales: List["Sale"] = Relationship(back_populates="customer")