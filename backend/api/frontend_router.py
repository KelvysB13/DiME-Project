from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

VIEWS_DIR = Path(__file__).resolve().parent.parent.parent / "views"
FRONTEND_DIR = VIEWS_DIR / "public"
ADMIN_DIR = VIEWS_DIR / "admin"

PAGE_ROUTES = {

    "/": (FRONTEND_DIR, "home.html"),
    "/auth/login": (FRONTEND_DIR, "login.html"),
    "/auth/register": (FRONTEND_DIR, "register.html"),
    "/me/dashboard": (FRONTEND_DIR, "user_dashboard.html"),
    "/me/settings": (FRONTEND_DIR, "user_settings.html"),
    "/faq": (FRONTEND_DIR, "faq.html"),
    "/admin/dashboard": (ADMIN_DIR, "admin_dashboard.html"),
}

def _make_route(base_dir: Path, file: str):

    async def _serve():
        return HTMLResponse((base_dir / file).read_text(encoding="utf-8"))

    return _serve

for route_path, (base_dir, filename) in PAGE_ROUTES.items():

    router.add_api_route(

        route_path,
        _make_route(base_dir, filename),
        methods=["GET"],
        include_in_schema=False,
    )
