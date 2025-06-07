#backend/app/routers/product.py

from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.models import Product
from app.core.auth import verify_jwt

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=Product)
def create_product(p: Product, session: Session = Depends(get_session)):
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

@router.get("/", response_model=list[Product])
def list_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()