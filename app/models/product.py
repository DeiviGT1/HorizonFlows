# backend/app/models/product.py

from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    products: List["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sku: str = Field(unique=True, index=True)
    name: str
    sale_price: float
    purchase_price: float
    stock: int = Field(default=0)
    
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="products")

    vendor_id: Optional[int] = Field(default=None, foreign_key="vendor.id")
    vendor: Optional["Vendor"] = Relationship(back_populates="products")
    
    sale_lines: List["SaleLine"] = Relationship(back_populates="product")
    purchase_order_lines: List["PurchaseOrderLine"] = Relationship(back_populates="product")
    goods_receipt_lines: List["GoodsReceiptLine"] = Relationship(back_populates="product")