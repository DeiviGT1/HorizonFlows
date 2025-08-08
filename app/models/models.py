# --- backend/app/models.py ---

from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, date
from enum import Enum

# --- ENUMS (Tipos predefinidos) ---

class UserRole(str, Enum):
    CASHIER = "cashier"
    MANAGER = "manager"
    ADMIN = "admin"

class PaymentMethod(str, Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    OTHER = "other"

class PurchaseOrderStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PARTIALLY_RECEIVED = "partially_received"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class CashActivityType(str, Enum):
    IN = "in"
    OUT = "out"

# --- Módulo 1 y 4: Usuarios y Turnos ---

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.CASHIER)
    
    sales: List["Sale"] = Relationship(back_populates="user")
    shifts: List["Shift"] = Relationship(back_populates="user")
    goods_receipts: List["GoodsReceipt"] = Relationship(back_populates="user")

class Shift(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    starting_cash: float
    ending_cash: Optional[float] = None
    
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="shifts")
    
    cash_activities: List["CashDrawerActivity"] = Relationship(back_populates="shift")

class CashDrawerActivity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    type: CashActivityType
    amount: float
    reason: str
    
    shift_id: int = Field(foreign_key="shift.id")
    shift: "Shift" = Relationship(back_populates="cash_activities")

# --- Módulo 2: Inventario, Productos, Proveedores ---

class Vendor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    contact_person: Optional[str] = None
    
    products: List["Product"] = Relationship(back_populates="vendor")
    purchase_orders: List["PurchaseOrder"] = Relationship(back_populates="vendor")

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
    
    category_id: int = Field(foreign_key="category.id")
    category: Category = Relationship(back_populates="products")

    vendor_id: Optional[int] = Field(default=None, foreign_key="vendor.id")
    vendor: Optional[Vendor] = Relationship(back_populates="products")
    
    sale_lines: List["SaleLine"] = Relationship(back_populates="product")
    purchase_order_lines: List["PurchaseOrderLine"] = Relationship(back_populates="product")
    goods_receipt_lines: List["GoodsReceiptLine"] = Relationship(back_populates="product")

class PurchaseOrder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_date: date = Field(default_factory=date.today)
    expected_delivery_date: Optional[date] = None
    status: PurchaseOrderStatus = Field(default=PurchaseOrderStatus.DRAFT)
    
    vendor_id: int = Field(foreign_key="vendor.id")
    vendor: Vendor = Relationship(back_populates="purchase_orders")

    lines: List["PurchaseOrderLine"] = Relationship(back_populates="purchase_order")
    receipts: List["GoodsReceipt"] = Relationship(back_populates="purchase_order")

class PurchaseOrderLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quantity_ordered: int
    cost_per_item: float # Puede ser diferente al `purchase_price` actual del producto
    
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


# --- Módulo 3 y 1: Clientes y Ventas ---

class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: Optional[str] = Field(default=None, unique=True)
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    
    sales: List["Sale"] = Relationship(back_populates="customer")

class Sale(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    total_amount: float
    
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="sales")

    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    customer: Optional[Customer] = Relationship(back_populates="sales")
    
    lines: List["SaleLine"] = Relationship(back_populates="sale")
    payments: List["Payment"] = Relationship(back_populates="sale")
    
class SaleLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quantity: int
    price_at_sale: float
    
    sale_id: int = Field(foreign_key="sale.id")
    sale: Sale = Relationship(back_populates="lines")

    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="sale_lines")

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    method: PaymentMethod
    
    sale_id: int = Field(foreign_key="sale.id")
    sale: Sale = Relationship(back_populates="payments")

# --- Módulo 5: Finanzas y Gastos ---

class ExpenseCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    expenses: List["Expense"] = Relationship(back_populates="category")

class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    amount: float
    date: date
    
    category_id: int = Field(foreign_key="expensecategory.id")
    category: ExpenseCategory = Relationship(back_populates="expenses")