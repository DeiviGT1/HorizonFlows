# backend/app/models/user.py

from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    CASHIER = "cashier"
    MANAGER = "manager"
    ADMIN = "admin"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.CASHIER)
    
    sales: List["Sale"] = Relationship(back_populates="user")
    shifts: List["Shift"] = Relationship(back_populates="user")
    goods_receipts: List["GoodsReceipt"] = Relationship(back_populates="user")

class Shift(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    starting_cash: float
    ending_cash: Optional[float] = None
    
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="shifts")
    
    # Referencia hacia adelante para evitar importación circular
    cash_activities: List["CashDrawerActivity"] = Relationship(back_populates="shift")
