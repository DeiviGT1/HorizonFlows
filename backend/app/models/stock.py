# backend/app/models/stock.py
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class StockMovement(SQLModel, table=True):
    """
    Registra CADA cambio de inventario.

    • type  : "in"  (ingreso), "out" (egreso) o "adjust" (ajuste manual)
    • qty   : cantidad positiva (¡no pongas signo!)
    • reference: texto libre (p.ej. "purchase 23", "invoice 15", "manual")
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    qty: int
    type: str = Field(max_length=10)                # "in" | "out" | "adjust"
    reference: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def signed_qty(self) -> int:
        """Devuelve qty con signo según type."""
        return self.qty if self.type == "in" else -self.qty