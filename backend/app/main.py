#backend/app/main.py

from app.routers import company, customer, product
from fastapi import FastAPI

app = FastAPI(title="HorizonFlows API")

@app.get("/ping")
async def ping():
    return {"status": "pong"}

app.include_router(company.router) 
app.include_router(customer.router) 
app.include_router(product.router)