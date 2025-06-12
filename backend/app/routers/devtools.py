from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlalchemy import delete

from app.core.db import get_session
from app.models import InvoiceLine, Invoice, Product, Customer, Business
from app.core.auth import verify_jwt

router = APIRouter(prefix="/dev", tags=["devtools"], dependencies=[Depends(verify_jwt)])

@router.delete("/purge-invoices", summary="PURGA total de facturas")
def purge_invoices(session: Session = Depends(get_session)):
    session.exec(delete(InvoiceLine))
    res = session.exec(delete(Invoice))
    session.commit()
    return {"deleted_invoices": res.rowcount}

@router.delete("/purge-products", summary="PURGA total de productos")
def purge_products(session: Session = Depends(get_session)):
    res = session.exec(delete(Product))
    session.commit()
    return {"deleted_products": res.rowcount}

@router.delete("/purge-customers", summary="PURGA total de clientes")
def purge_customers(session: Session = Depends(get_session)):
    res = session.exec(delete(Customer))
    session.commit()
    return {"deleted_customers": res.rowcount}

@router.delete("/purge-businesses", summary="PURGA total de empresas")
def purge_businesses(session: Session = Depends(get_session)):
    res = session.exec(delete(Business))
    session.commit()
    return {"deleted_businesses": res.rowcount}

@router.delete("/purge-all", summary="PURGA total de datos")
def purge_all(session: Session = Depends(get_session)):
    session.exec(delete(InvoiceLine))
    session.exec(delete(Invoice))
    session.exec(delete(Product))
    session.exec(delete(Customer))
    session.exec(delete(Business))
    session.commit()
    return {"message": "All data purged successfully"}