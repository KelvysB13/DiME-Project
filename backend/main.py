from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from api import api_router
from api.frontend_router import router as frontend_router

app = FastAPI(title="DiME - Diagnóstico Integral de Métricas E-commerce", version="1.0.0")

app.add_middleware(

    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent

app.include_router(api_router, prefix="/api")

app.mount("/assets", StaticFiles(directory=str(BASE_DIR / "assets")), name="assets")
app.mount("/forms", StaticFiles(directory=str(BASE_DIR / "forms")), name="forms")

app.include_router(frontend_router)
