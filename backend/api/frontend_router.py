from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "views"

PAGE_ROUTES = {

    # Rutas Públicas
    "/": ("public", "home.html"),
    "/auth/login": ("public", "login.html"),
    "/auth/register": ("public", "register.html"),
    "/me/dashboard": ("public", "user_dashboard.html"),
    "/me/settings": ("public", "user_settings.html"),
    "/faq": ("public", "faq.html"),
    
    # Rutas de Administración
    "/admin/dashboard": ("admin", "admin_dashboard.html"),
}

def _make_route(folder: str, file: str):

    async def _serve():
        file_path = FRONTEND_DIR / folder / file
        return HTMLResponse(file_path.read_text(encoding="utf-8"))
    
    return _serve

for route_path, (folder, filename) in PAGE_ROUTES.items():

    router.add_api_route(
        
        route_path,
        _make_route(folder, filename),
        methods=["GET"],
        include_in_schema=False,
    )
