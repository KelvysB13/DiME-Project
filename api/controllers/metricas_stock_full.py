from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from resources.db import get_async_db
from infrastructure.persistence.repositories.metricas_stock_full import Metricas_stock_fullRepository
from application.services.metricas_stock_full import Metricas_stock_fullService
from application.dto.metricas_stock_full import Metricas_stock_full as Metricas_stock_fullSchema, Metricas_stock_fullCreate, Metricas_stock_fullUpdate
from application.dto.base import PaginatedResponse

router = APIRouter(prefix="/metricas_stock_fulls", tags=["metricas_stock_fulls"])


async def get_metricas_stock_full_service(db: AsyncSession = Depends(get_async_db)) -> Metricas_stock_fullService:
    return Metricas_stock_fullService(Metricas_stock_fullRepository(db))


@router.get("/", response_model=PaginatedResponse,
         summary="Listar metricas_stock_fulls",
         description="Obtiene lista paginada de metricas_stock_fulls")
async def list_metricas_stock_fulls(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    service: Metricas_stock_fullService = Depends(get_metricas_stock_full_service),
):
    items, total = await service.get_all(skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{metricas_stock_full_id}", response_model=Metricas_stock_fullSchema,
         summary="Obtener Metricas_stock_full por ID",
         responses={404: {'description': 'Metricas_stock_full no encontrado'}})
async def get_metricas_stock_full(metricas_stock_full_id: int, service: Metricas_stock_fullService = Depends(get_metricas_stock_full_service)):
    return await service.get_by_id(metricas_stock_full_id)


@router.post("/", response_model=Metricas_stock_fullSchema, status_code=status.HTTP_201_CREATED,
          summary="Crear Metricas_stock_full",
          description="Crea un nuevo registro de Metricas_stock_full",
          responses={409: {'description': 'Conflicto'}, 422: {'description': 'Error de validación'}})
async def create_metricas_stock_full(data: Metricas_stock_fullCreate, service: Metricas_stock_fullService = Depends(get_metricas_stock_full_service)):
    return await service.create(data)


@router.put("/{metricas_stock_full_id}", response_model=Metricas_stock_fullSchema,
         summary="Actualizar Metricas_stock_full",
         description="Actualiza un registro existente de Metricas_stock_full",
         responses={404: {'description': 'Metricas_stock_full no encontrado'}})
async def update_metricas_stock_full(metricas_stock_full_id: int, data: Metricas_stock_fullUpdate, service: Metricas_stock_fullService = Depends(get_metricas_stock_full_service)):
    return await service.update(metricas_stock_full_id, data)


@router.delete("/{metricas_stock_full_id}", status_code=status.HTTP_204_NO_CONTENT,
           summary="Eliminar Metricas_stock_full",
           description="Elimina un registro de Metricas_stock_full",
           responses={404: {'description': 'Metricas_stock_full no encontrado'}})
async def delete_metricas_stock_full(metricas_stock_full_id: int, service: Metricas_stock_fullService = Depends(get_metricas_stock_full_service)):
    await service.delete(metricas_stock_full_id)
    return None


@router.post("/{metricas_stock_full_id}/soft-delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_metricas_stock_full(metricas_stock_full_id: int, service: Metricas_stock_fullService = Depends(get_metricas_stock_full_service)):
    await service.soft_delete(metricas_stock_full_id)
    return None


@router.post("/{metricas_stock_full_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_metricas_stock_full(metricas_stock_full_id: int, service: Metricas_stock_fullService = Depends(get_metricas_stock_full_service)):
    await service.restore(metricas_stock_full_id)
    return None