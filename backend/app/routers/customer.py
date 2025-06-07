from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.models import Customer
from app.core.auth import verify_jwt

router = APIRouter(prefix="/customers", tags=["customers"], dependencies=[Depends(verify_jwt)])

@router.post("/", response_model=Customer)
def create_customer(c: Customer, session: Session = Depends(get_session)):
    session.add(c)
    session.commit()
    session.refresh(c)
    return c

@router.get("/", response_model=list[Customer])
def list_customers(session: Session = Depends(get_session)):
    return session.exec(select(Customer)).all()