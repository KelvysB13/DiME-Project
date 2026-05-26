from fastapi import FastAPI
from app.auth.routes import router as auth_router

app = FastAPI(title="DiME - Diagnóstico Integral de Métricas E-commerce", version="3.0.0")

app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "3.0.0"}
