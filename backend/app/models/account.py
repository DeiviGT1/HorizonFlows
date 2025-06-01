# backend/app/models/account.py
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class AccountEntry(SQLModel, table=True):
    """
    Movimientos de la cuenta corriente del cliente.

    • debit  : aumenta lo que el cliente debe (facturas).
    • credit : reduce lo que el cliente debe (pagos).
    - Usa UNO de los dos campos por fila.
    """
    id: Optional[int] = Field(default=None, primary_key=True)

    customer_id: int = Field(foreign_key="customer.id")
    invoice_id: Optional[int] = Field(default=None, foreign_key="invoice.id")

    debit: float = 0.0
    credit: float = 0.0

    note: Optional[str] = Field(default=None)       # "Cash", "Card", etc.
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def signed_amount(self) -> float:
        """Devuelve monto con signo: +debit, -credit."""
        return self.debit - self.credit