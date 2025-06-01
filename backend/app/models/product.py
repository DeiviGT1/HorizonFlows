from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="company.id")
    sku: str
    name: str
    type: str = "goods"           # goods | service
    unit_price: float
    tax_rate: float = 0.07
    stock_min: int = 0            # 0 si es servicio
    created_at: datetime = Field(default_factory=datetime.utcnow)