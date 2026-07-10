from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from core.database import get_db
from auth.deps import get_current_user
from models.admin_model import Admin
from schemas.vendedor_schema import VendedorListResponse, VendedorResponse
from services.vendedor_service import (
    list_vendedores,
    toggle_vendedor_status,
    delete_vendedor,
    VendedorNotFoundError,
)

router = APIRouter()


def _verify_admin(current_user: Admin = Depends(get_current_user)) -> Admin:
    if not isinstance(current_user, Admin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo administradores")
    return current_user


@router.get("/admin/vendedores", response_model=VendedorListResponse)
def obtener_vendedores(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search: str = Query("", max_length=100),
    db: Session = Depends(get_db),
    _admin: Admin = Depends(_verify_admin),
):
    return list_vendedores(db, page=page, per_page=per_page, search=search)


@router.patch("/admin/vendedores/{vendedor_id}/toggle-status", response_model=VendedorResponse)
def cambiar_estado_vendedor(
    vendedor_id: int,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(_verify_admin),
):
    try:
        return toggle_vendedor_status(db, vendedor_id)
    except VendedorNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendedor no encontrado")


@router.delete("/admin/vendedores/{vendedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_vendedor(
    vendedor_id: int,
    db: Session = Depends(get_db),
    _admin: Admin = Depends(_verify_admin),
):
    try:
        delete_vendedor(db, vendedor_id)
    except VendedorNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendedor no encontrado")
