# backend/app/models/invoice.py
from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Invoice(SQLModel, table=True):
    """
    Venta a cliente. Genera asiento automático.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    business_id: int  = Field(foreign_key="business.id")
    customer_id: int  = Field(foreign_key="customer.id")
    entry_id: Optional[int] = Field(default=None, foreign_key="journal_entry.id")
    date: datetime
    due_date: Optional[datetime] = None
    status: str
    total_amount: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

    business: "Business" = Relationship(back_populates="invoices")
    customer: "Customer" = Relationship(back_populates="invoices")
    entry:    Optional["JournalEntry"] = Relationship(back_populates="invoices")
    lines:    List["InvoiceLine"]    = Relationship(back_populates="invoice")

class InvoiceLine(SQLModel, table=True):
    """
    Línea de factura: vincula cuenta de ingreso y cuentas por cobrar.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int   = Field(foreign_key="invoice.id")
    account_id: int = Field(foreign_key="chart_of_account.id")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    description: Optional[str] = None
    amount: float = 0.0

    invoice: "Invoice" = Relationship(back_populates="lines")
    account: "ChartOfAccount" = Relationship(back_populates="invoice_lines")
    category: Optional["Category"] = Relationship(back_populates="invoice_lines")
    product: Optional["Product"] = Relationship(back_populates="invoice_lines")
    expense_line: Optional["ExpenseLine"] = Relationship(back_populates="invoice_lines")
    journal_line: Optional["JournalLine"] = Relationship(back_populates="invoice_lines")
    vendor: Optional["Vendor"] = Relationship(back_populates="invoice_lines")
    expense: Optional["Expense"] = Relationship(back_populates="invoice_lines")
    payment: Optional["Payment"] = Relationship(back_populates="invoice_lines")