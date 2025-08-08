# backend/app/models/payment.py
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Payment(SQLModel, table=True):
    """
    Pago o cobro (cliente o proveedor). Genera asiento.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: int  = Field(foreign_key="business.id")
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    vendor_id:   Optional[int] = Field(default=None, foreign_key="vendor.id")
    entry_id:    Optional[int] = Field(default=None, foreign_key="journal_entry.id")
    date:        datetime
    amount:      float
    method:      Optional[str] = None
    reference:   Optional[str] = None
    created_at:  datetime      = Field(default_factory=datetime.utcnow)

    business: "Business"          = Relationship(back_populates="payments")
    customer: Optional["Customer"] = Relationship(back_populates="payments")
    vendor:   Optional["Vendor"]   = Relationship(back_populates="payments")
    entry:    Optional["JournalEntry"] = Relationship(back_populates="payments")