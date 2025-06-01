from datetime import datetime
from slugify import slugify
from jinja2 import Environment, FileSystemLoader
import pdfkit
from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select

from app.models import Invoice, InvoiceLine, Product, Customer
from app.core.db import get_session

env = Environment(loader=FileSystemLoader("app/templates"))

PDF_DIR = Path("/storage/invoices")      # volumen del compose
PDF_DIR.mkdir(parents=True, exist_ok=True)

# 1️⃣ configura pdfkit con la ruta exacta
WKHTML_PATH = "/usr/bin/wkhtmltopdf"     # ajusta si which dio otra ruta
config = pdfkit.configuration(wkhtmltopdf=WKHTML_PATH)

class InvoiceService:
    @staticmethod
    def create(data, session: Session) -> Invoice:
        """data = {"company_id":1,"customer_id":2,"lines":[{"product_id":1,"qty":2},...]}"""

        # --- 1. Validar existencia de customer y productos ----------
        customer = session.get(Customer, data["customer_id"])
        if not customer:
            raise ValueError("Customer not found")

        products = {p.id: p for p in session.exec(
            select(Product).where(Product.id.in_([l["product_id"] for l in data["lines"]]))
        ).all()}
        if len(products) != len(data["lines"]):
            raise ValueError("One or more products not found")

        # --- 2. Calcular totales ------------------------------------
        lines = []
        subtotal = 0
        for l in data["lines"]:
            p = products[l["product_id"]]
            total = l["qty"] * p.unit_price
            lines.append(InvoiceLine(
                product_id=p.id, qty=l["qty"],
                unit_price=p.unit_price, line_total=total
            ))
            subtotal += total

        tax = round(subtotal * 0.07, 2)    # simple fijo; adapta según p.tax_rate
        grand = round(subtotal + tax, 2)

        # --- 3. Transacción ----------------------------------------
        try:
            invoice = Invoice(
                company_id=data["company_id"],
                customer_id=customer.id,
                date=datetime.utcnow(),
                subtotal=subtotal,
                tax=tax,
                total=grand,
                status="draft",
                lines=lines
            )
            session.add(invoice)
            session.commit()
            session.refresh(invoice)
        except SQLAlchemyError:
            session.rollback()
            raise

        # --- 4. Generar PDF ----------------------------------------
        InvoiceService.generate_pdf(invoice, customer, products)
        return invoice

    @staticmethod
    def generate_pdf(inv: Invoice, customer: Customer, products: dict):
        tpl = env.get_template("invoice.html")
        html = tpl.render(
            invoice=inv,
            customer=customer,
            company={"name": "HorizonFlows Demo"},
            lines=[dict(l, product=products[l.product_id]) for l in inv.lines],
        )

        filename = f"{inv.id}.pdf"        # nombre sencillo ─ coincide con GET
        out_path = PDF_DIR / filename

        # 2️⃣ genera el PDF
        pdfkit.from_string(html, str(out_path), configuration=config)