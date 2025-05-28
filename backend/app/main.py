from fastapi import FastAPI

app = FastAPI(title="HorizonFlows API")

@app.get("/ping")
async def ping():
    return {"status": "pong"}