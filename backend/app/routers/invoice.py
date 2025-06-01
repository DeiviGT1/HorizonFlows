from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from typing import List

from app.core.db import get_session
from app.models import Invoice
from app.schemas.invoice import InvoiceIn, InvoiceOut
from app.services.invoice_service import InvoiceService
from pathlib import Path

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("/", response_model=Invoice)
def create_invoice(data: InvoiceIn, session: Session = Depends(get_session)):
    try:
        return InvoiceService.create(data.dict(), session)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/{inv_id}/pdf")
def download_pdf(inv_id: int):
    path = Path(f"/storage/invoices/{inv_id}.pdf")
    if not path.exists():
        raise HTTPException(404, "PDF not found")
    return FileResponse(path, media_type="application/pdf", filename=path.name)

@router.get("/", response_model=List[Invoice])
def list_invoices(session: Session = Depends(get_session)):
    """
    Devuelve todas las facturas almacenadas.
    """
    invoices = session.exec(select(Invoice)).all()
    return invoices

##PRUEBA

@router.get("/{inv_id}", response_model=InvoiceOut)
def get_invoice(inv_id: int, session: Session = Depends(get_session)):
    inv = session.get(Invoice, inv_id)
    if not inv:
        raise HTTPException(404, "Invoice not found")

    # construye un objeto de salida
    return InvoiceOut.from_orm(
        inv,
        update={"has_pdf": Path(f"/storage/invoices/{inv_id}.pdf").exists()}
    )