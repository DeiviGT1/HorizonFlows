# backend/app/models/__init__.py

from .user import User, Shift, CashDrawerActivity, UserRole
from .product import Product, Category
from .inventory import (
    PurchaseOrder,
    PurchaseOrderLine,
    GoodsReceipt,
    GoodsReceiptLine,
    PurchaseOrderStatus,
)
from .sales import Sale, SaleLine, Payment, PaymentMethod
from .customer import Customer
from .vendor import Vendor
from .finance import Expense, ExpenseCategory, CashActivityType

# Opcional: define qué se importa con 'from app.models import *'
__all__ = [
    "User", "Shift", "CashDrawerActivity", "UserRole",
    "Product", "Category",
    "PurchaseOrder", "PurchaseOrderLine", "GoodsReceipt", "GoodsReceiptLine", "PurchaseOrderStatus",
    "Sale", "SaleLine", "Payment", "PaymentMethod",
    "Customer",
    "Vendor",
    "Expense", "ExpenseCategory", "CashActivityType"
]