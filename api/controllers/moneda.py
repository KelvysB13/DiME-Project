from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from resources.db import get_async_db
from infrastructure.persistence.repositories.moneda import MonedaRepository
from application.services.moneda import MonedaService
from application.dto.moneda import Moneda as MonedaSchema, MonedaCreate, MonedaUpdate
from application.dto.base import PaginatedResponse

router = APIRouter(prefix="/monedas", tags=["monedas"])


async def get_moneda_service(db: AsyncSession = Depends(get_async_db)) -> MonedaService:
    return MonedaService(MonedaRepository(db))


@router.get("/", response_model=PaginatedResponse,
         summary="Listar monedas",
         description="Obtiene lista paginada de monedas con búsqueda y ordenamiento")
async def list_monedas(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    search: Optional[str] = Query(None, description="Buscar en: codigo_moneda, nombre_moneda, simbolo"),
    sort_by: Optional[str] = Query(None, description="Ordenar por: codigo_moneda, nombre_moneda, simbolo"),
    sort_desc: bool = Query(False, description="Orden descendente"),
    service: MonedaService = Depends(get_moneda_service),
):
    items, total = await service.get_all(skip=skip, limit=limit, search=search, sort_by=sort_by, sort_desc=sort_desc)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{moneda_id}", response_model=MonedaSchema,
         summary="Obtener Moneda por ID",
         responses={404: {'description': 'Moneda no encontrado'}})
async def get_moneda(moneda_id: str, service: MonedaService = Depends(get_moneda_service)):
    return await service.get_by_id(moneda_id)


@router.post("/", response_model=MonedaSchema, status_code=status.HTTP_201_CREATED,
          summary="Crear Moneda",
          description="Crea un nuevo registro de Moneda",
          responses={409: {'description': 'Conflicto'}, 422: {'description': 'Error de validación'}})
async def create_moneda(data: MonedaCreate, service: MonedaService = Depends(get_moneda_service)):
    return await service.create(data)


@router.put("/{moneda_id}", response_model=MonedaSchema,
         summary="Actualizar Moneda",
         description="Actualiza un registro existente de Moneda",
         responses={404: {'description': 'Moneda no encontrado'}})
async def update_moneda(moneda_id: str, data: MonedaUpdate, service: MonedaService = Depends(get_moneda_service)):
    return await service.update(moneda_id, data)


@router.delete("/{moneda_id}", status_code=status.HTTP_204_NO_CONTENT,
           summary="Eliminar Moneda",
           description="Elimina un registro de Moneda",
           responses={404: {'description': 'Moneda no encontrado'}})
async def delete_moneda(moneda_id: str, service: MonedaService = Depends(get_moneda_service)):
    await service.delete(moneda_id)
    return None


@router.post("/{moneda_id}/soft-delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_moneda(moneda_id: str, service: MonedaService = Depends(get_moneda_service)):
    await service.soft_delete(moneda_id)
    return None


@router.post("/{moneda_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_moneda(moneda_id: str, service: MonedaService = Depends(get_moneda_service)):
    await service.restore(moneda_id)
    return None