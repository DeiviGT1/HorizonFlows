# backend/app/models/business.py
from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Business(SQLModel, table=True):
    """
    Tu “empresa” raíz. Se almacena en la BD maestra.
    """
    __tablename__ = "business"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    
    # --- Campos nuevos para Multitenancy ---
    slug: str = Field(unique=True, index=True, description="Identificador único para URL/subdominio")
    db_name: str = Field(unique=True, description="Nombre de la base de datos del tenant")
    # --- Fin de campos nuevos ---
    
    tax_id: Optional[str] = Field(default=None, description="RFC / NIF / Tax ID")
    address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    # accounts: List["ChartOfAccount"]      = Relationship(back_populates="business")
    # customers: List["Customer"] = Relationship(back_populates="business")
    # vendors:   List["Vendor"] = Relationship(back_populates="business")
    # entries:   List["JournalEntry"] = Relationship(back_populates="business")
    # invoices:  List["Invoice"]             = Relationship(back_populates="business")
    # expenses:  List["Expense"]             = Relationship(back_populates="business")
    # payments:  List["Payment"]             = Relationship(back_populates="business")
    # categories: List["Category"]           = Relationship(back_populates="business")