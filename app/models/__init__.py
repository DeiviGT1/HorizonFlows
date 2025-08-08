# backend/app/models/__init__.py

# CashDrawerActivity ya no se importa desde .user
from .user import User, Shift, UserRole 
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
# Se importa la definición completa desde .finance
from .finance import Expense, ExpenseCategory, CashDrawerActivity, CashActivityType

__all__ = [
    "User", "Shift", "UserRole",
    "Product", "Category",
    "PurchaseOrder", "PurchaseOrderLine", "GoodsReceipt", "GoodsReceiptLine", "PurchaseOrderStatus",
    "Sale", "SaleLine", "Payment", "PaymentMethod",
    "Customer",
    "Vendor",
    "Expense", "ExpenseCategory", "CashDrawerActivity", "CashActivityType"
]