# backend/app/models/product.py

from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class Product(SQLModel, table=True):
    """
    Representa un producto o servicio que la empresa ofrece.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="business.id")
    sku: Optional[str] = Field(default=None, index=True, description="Stock Keeping Unit")
    name: str
    type: str = Field(default="service", description="Puede ser 'service' o 'good'")
    unit_price: float = 0.0
    tax_rate: float = 0.0

    # Relación (opcional por ahora, pero buena práctica)
    business: "Business" = Relationship(back_populates="products")