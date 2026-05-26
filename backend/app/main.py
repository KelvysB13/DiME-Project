from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.auth.routes import router as auth_router

app = FastAPI(title="DiME - Diagnóstico Integral de Métricas E-commerce", version="3.0.0")

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")

app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "3.0.0"}
