from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.models import Customer

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=Customer)
def create_customer(c: Customer, session: Session = Depends(get_session)):
    session.add(c)
    session.commit()
    session.refresh(c)
    return c

@router.get("/", response_model=list[Customer])
def list_customers(session: Session = Depends(get_session)):
    return session.exec(select(Customer)).all()