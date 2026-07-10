from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "views" / "public"
ADMIN_DIR = Path(__file__).resolve().parent.parent.parent / "views" / "admin"

PAGE_ROUTES = {

    "/": "home.html",
    "/auth/login": "login.html",
    "/auth/register": "register.html",
    "/me/dashboard": "user_dashboard.html",
    "/me/settings": "user_settings.html",
    "/faq": "faq.html",
    "/admin/dashboard": "admin_dashboard.html",
}

def _make_route(file: str):

    async def _serve():
        if file == "admin_dashboard.html":
            return HTMLResponse((ADMIN_DIR / file).read_text(encoding="utf-8"))
        return HTMLResponse((FRONTEND_DIR / file).read_text(encoding="utf-8"))
    
    return _serve

for route_path, filename in PAGE_ROUTES.items():

    router.add_api_route(
        
        route_path,
        _make_route(filename),
        methods=["GET"],
        include_in_schema=False,
    )
