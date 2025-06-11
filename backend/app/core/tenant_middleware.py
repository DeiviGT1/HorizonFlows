# backend/app/core/tenant_middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import HTTPException

# Cambiamos las importaciones para que funcionen en este contexto
from .db import set_tenant, get_master_session 
from sqlmodel import select
from app.models.business import Business

class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        host = request.headers.get("host", "").split(":")[0] # 'acme.localhost:8000' -> 'acme.localhost'
        subdomain = host.split(".")[0]

        # Excluir rutas que no necesitan tenant (ej. docs, health checks)
        if request.url.path in ["/docs", "/openapi.json", "/ping"]:
             return await call_next(request)

        try:
            # Usamos el generador de sesión maestro
            with next(get_master_session()) as s:
                business = s.exec(select(Business).where(Business.slug == subdomain)).first()
            
            if not business:
                # Opcional: podrías devolver un JSON en lugar de una página de error
                raise HTTPException(status_code=404, detail="Tenant not found")

            # Si encontramos la empresa, establecemos su motor de BD
            set_tenant(business.db_name)

        except Exception as e:
            # Considera logging del error 'e'
            return Response(f"Could not identify tenant: {subdomain}", status_code=404)

        return await call_next(request)