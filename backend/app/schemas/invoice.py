from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, conint, condecimal

class InvoiceLineIn(BaseModel):
    product_id: int
    qty: conint(gt=0)
    unit_price: condecimal(gt=0, max_digits=12, decimal_places=2)

class InvoiceIn(BaseModel):
    business_id: int          # ⬅️  renombrado
    customer_id: int
    lines: List[InvoiceLineIn]

class InvoiceOut(BaseModel):
    id: int
    business_id: int
    customer_id: int
    date: datetime
    due_date: Optional[datetime]
    status: str
    total_amount: Decimal
    has_pdf: bool = False

    class Config:
        orm_mode = True