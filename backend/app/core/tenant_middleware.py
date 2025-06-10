# backend/app/core/tenant_middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .db import set_tenant, get_master_session
from sqlmodel import select
from app.models.business import Business

async def _db_name_from_subdomain(host: str) -> str:
    # p.e. acme.erp.com → 'acme'
    sub = host.split(".")[0]
    async with get_master_session() as s:
        q = await s.exec(select(Business.db_name).where(Business.slug == sub))
        return q.one()  # lanza 404 si no existe

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        host = request.headers.get("host", "")
        db_name = await _db_name_from_subdomain(host)
        set_tenant(db_name)
        return await call_next(request)