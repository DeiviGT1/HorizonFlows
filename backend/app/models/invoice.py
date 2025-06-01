from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class InvoiceLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoice.id")
    product_id: int = Field(foreign_key="product.id")
    qty: int
    unit_price: float
    line_total: float

class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="company.id")
    customer_id: int = Field(foreign_key="customer.id")
    date: datetime = Field(default_factory=datetime.utcnow)
    subtotal: float
    tax: float
    total: float
    status: str = "draft"            # draft | sent | paid
    lines: List[InvoiceLine] = Relationship(back_populates=None)