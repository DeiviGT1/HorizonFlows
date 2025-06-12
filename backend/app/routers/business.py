# backend/app/routers/business.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
from app.core.db import get_master_session
from app.models import Business
from app.core.auth import verify_jwt

router = APIRouter(
    prefix="/business", 
    tags=["business"], 
    dependencies=[Depends(verify_jwt)]
)

@router.get("/current", response_model=Business)
def get_current_business(request: Request, session: Session = Depends(get_master_session)):
    """
    Returns the business object for the current tenant,
    identified by the subdomain in the host header.
    """
    host = request.headers.get("host", "").split(":")[0]
    subdomain = host.split(".")[0]

    if not subdomain:
        raise HTTPException(status_code=400, detail="Could not identify subdomain from host.")

    business = session.exec(select(Business).where(Business.slug == subdomain)).first()
    
    if not business:
        raise HTTPException(status_code=404, detail=f"Business with slug '{subdomain}' not found.")
        
    return business