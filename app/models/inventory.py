# backend/app/models/inventory.py

from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, date
from enum import Enum
from .user import User
from .product import Product

class PurchaseOrderStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PARTIALLY_RECEIVED = "partially_received"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PurchaseOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_date: date = Field(default_factory=date.today)
    expected_delivery_date: Optional[date] = None
    status: PurchaseOrderStatus = Field(default=PurchaseOrderStatus.DRAFT)
    
    vendor_id: int = Field(foreign_key="vendor.id")
    vendor: "Vendor" = Relationship(back_populates="purchase_orders")

    lines: List["PurchaseOrderLine"] = Relationship(back_populates="purchase_order")
    receipts: List["GoodsReceipt"] = Relationship(back_populates="purchase_order")

class PurchaseOrderLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quantity_ordered: int
    cost_per_item: float
    
    purchase_order_id: int = Field(foreign_key="purchaseorder.id")
    purchase_order: PurchaseOrder = Relationship(back_populates="lines")

    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="purchase_order_lines")

class GoodsReceipt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    receipt_date: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
    
    purchase_order_id: int = Field(foreign_key="purchaseorder.id")
    purchase_order: PurchaseOrder = Relationship(back_populates="receipts")

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="goods_receipts")

    lines: List["GoodsReceiptLine"] = Relationship(back_populates="receipt")

class GoodsReceiptLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quantity_received: int
    
    receipt_id: int = Field(foreign_key="goodsreceipt.id")
    receipt: GoodsReceipt = Relationship(back_populates="lines")
    
    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="goods_receipt_lines")