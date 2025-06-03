# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- 1. IMPORTA ESTO
from app.routers import company, customer, product, invoice, devtools

app = FastAPI(title="HorizonFlows API")

# --- 2. CONFIGURACIÓN DE CORS ---
origins = [
    "http://localhost:3000",  # El origen de tu frontend React
    "http://127.0.0.1:3000", # IP local para el frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"], # Permite todas las cabeceras
)
# --- FIN DE LA CONFIGURACIÓN DE CORS ---

@app.get("/ping")
async def ping():
    return {"status": "pong"}

app.include_router(company.router)
app.include_router(customer.router)
app.include_router(product.router)
app.include_router(invoice.router)

##DEBUG
app.include_router(devtools.router)