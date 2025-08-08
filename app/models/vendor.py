# backend/app/models/vendor.py

from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

class Vendor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    contact_person: Optional[str] = None
    
    products: List["Product"] = Relationship(back_populates="vendor")
    purchase_orders: List["PurchaseOrder"] = Relationship(back_populates="vendor")