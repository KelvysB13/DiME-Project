from fastapi import APIRouter, Depends
from auth.deps import get_current_user
from models.vendedor_model import Vendedor
from services.metabase_embed_service import get_diagnostico_embed_urls

router = APIRouter()


@router.get("/metabase/embed-urls")
def metabase_embed_urls(current_user: Vendedor = Depends(get_current_user)):
    return get_diagnostico_embed_urls(current_user.id_vendedor)
