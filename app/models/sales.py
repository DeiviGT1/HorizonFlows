# backend/app/models/sales.py

from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from enum import Enum
from .user import User
from .product import Product
from .customer import Customer

class PaymentMethod(str, Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    OTHER = "other"

class Sale(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    total_amount: float
    
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="sales")

    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    customer: Optional[Customer] = Relationship(back_populates="sales")
    
    lines: List["SaleLine"] = Relationship(back_populates="sale")
    payments: List["Payment"] = Relationship(back_populates="sale")
    
class SaleLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quantity: int
    price_at_sale: float
    
    sale_id: int = Field(foreign_key="sale.id")
    sale: Sale = Relationship(back_populates="lines")

    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="sale_lines")

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    method: PaymentMethod
    
    sale_id: int = Field(foreign_key="sale.id")
    sale: Sale = Relationship(back_populates="payments")