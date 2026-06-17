import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from config.settings import APP_TITLE, APP_VERSION, ALLOWED_ORIGINS, BASE_DIR
from web.middlewares.logging_middleware import RequestLoggingMiddleware
from web.middlewares.error_transformer import setup_exception_handlers
from web.middlewares.rate_limiter import RateLimiterMiddleware
from web.api_router import api_router
from web.middlewares.auth.auth_middleware import AuthMiddleware

app = FastAPI(title=APP_TITLE, version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimiterMiddleware)
app.add_middleware(AuthMiddleware)

app.include_router(api_router)
setup_exception_handlers(app)

views_dir = os.path.join(BASE_DIR, "views")
if os.path.isdir(views_dir):
    app.mount("/views", StaticFiles(directory=views_dir), name="views")

assets_dir = os.path.join(BASE_DIR, "assets")
if os.path.isdir(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


@app.get("/")
async def root():
    from fastapi.responses import FileResponse
    login_path = os.path.join(views_dir, "public", "login.html")
    if os.path.isfile(login_path):
        return FileResponse(login_path)
    return {"message": "DiME API - Diagnóstico de Métricas de Vendedores", "docs": "/docs"}


@app.get("/dashboard")
async def dashboard():
    from fastapi.responses import FileResponse
    dashboard_path = os.path.join(views_dir, "public", "dashboard.html")
    if os.path.isfile(dashboard_path):
        return FileResponse(dashboard_path)
    return {"error": "Dashboard page not found"}
