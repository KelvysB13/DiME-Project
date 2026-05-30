from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api_router import api_router

app = FastAPI(title="DiME - Diagnóstico Integral de Métricas E-commerce", version="1.0.0")

app.include_router(api_router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}