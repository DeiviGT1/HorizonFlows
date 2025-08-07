# backend/app/main.py

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.tenant_middleware import TenantMiddleware
from app.routers import customer, product, invoice, devtools, business

app = FastAPI(title="HorizonFlows API")

# --- 2. CONFIGURACIÓN DE CORS ---
origins = [
    "http://localhost:3000",  # El origen de tu frontend React
    "http://127.0.0.1:3000", # IP local para el frontend
    "https://horizonflows.com",  # Tu dominio principal de producción
]

app.add_middleware(TenantMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- FIN DE LA CONFIGURACIÓN DE CORS ---

@app.get("/ping")
async def ping():
    return {"status": "pong"}

app.include_router(customer.router)
app.include_router(product.router)
app.include_router(invoice.router)
app.include_router(business.router)

##DEBUG
app.include_router(devtools.router)