from pydantic import BaseModel
from typing import List

from app.models import Invoice

class InvoiceLineIn(BaseModel):
    product_id: int
    qty: int

class InvoiceIn(BaseModel):
    company_id: int
    customer_id: int
    lines: List[InvoiceLineIn]
    
class InvoiceOut(Invoice):
    has_pdf: bool

    class Config:
        orm_mode = True