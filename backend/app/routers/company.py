from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.db import get_session
from app.models import Company

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("/", response_model=Company)
def create_company(company: Company, session: Session = Depends(get_session)):
    session.add(company)
    session.commit()
    session.refresh(company)
    return company

@router.get("/", response_model=list[Company])
def list_companies(session: Session = Depends(get_session)):
    return session.exec(select(Company)).all()