from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from resources.db import get_async_db
from infrastructure.persistence.repositories.metricas_costo import Metricas_costoRepository
from application.services.metricas_costo import Metricas_costoService
from application.dto.metricas_costo import Metricas_costo as Metricas_costoSchema, Metricas_costoCreate, Metricas_costoUpdate
from application.dto.base import PaginatedResponse

router = APIRouter(prefix="/metricas_costos", tags=["metricas_costos"])


async def get_metricas_costo_service(db: AsyncSession = Depends(get_async_db)) -> Metricas_costoService:
    return Metricas_costoService(Metricas_costoRepository(db))


@router.get("/", response_model=PaginatedResponse,
         summary="Listar metricas_costos",
         description="Obtiene lista paginada de metricas_costos")
async def list_metricas_costos(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    service: Metricas_costoService = Depends(get_metricas_costo_service),
):
    items, total = await service.get_all(skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{metricas_costo_id}", response_model=Metricas_costoSchema,
         summary="Obtener Metricas_costo por ID",
         responses={404: {'description': 'Metricas_costo no encontrado'}})
async def get_metricas_costo(metricas_costo_id: int, service: Metricas_costoService = Depends(get_metricas_costo_service)):
    return await service.get_by_id(metricas_costo_id)


@router.post("/", response_model=Metricas_costoSchema, status_code=status.HTTP_201_CREATED,
          summary="Crear Metricas_costo",
          description="Crea un nuevo registro de Metricas_costo",
          responses={409: {'description': 'Conflicto'}, 422: {'description': 'Error de validación'}})
async def create_metricas_costo(data: Metricas_costoCreate, service: Metricas_costoService = Depends(get_metricas_costo_service)):
    return await service.create(data)


@router.put("/{metricas_costo_id}", response_model=Metricas_costoSchema,
         summary="Actualizar Metricas_costo",
         description="Actualiza un registro existente de Metricas_costo",
         responses={404: {'description': 'Metricas_costo no encontrado'}})
async def update_metricas_costo(metricas_costo_id: int, data: Metricas_costoUpdate, service: Metricas_costoService = Depends(get_metricas_costo_service)):
    return await service.update(metricas_costo_id, data)


@router.delete("/{metricas_costo_id}", status_code=status.HTTP_204_NO_CONTENT,
           summary="Eliminar Metricas_costo",
           description="Elimina un registro de Metricas_costo",
           responses={404: {'description': 'Metricas_costo no encontrado'}})
async def delete_metricas_costo(metricas_costo_id: int, service: Metricas_costoService = Depends(get_metricas_costo_service)):
    await service.delete(metricas_costo_id)
    return None


@router.post("/{metricas_costo_id}/soft-delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_metricas_costo(metricas_costo_id: int, service: Metricas_costoService = Depends(get_metricas_costo_service)):
    await service.soft_delete(metricas_costo_id)
    return None


@router.post("/{metricas_costo_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_metricas_costo(metricas_costo_id: int, service: Metricas_costoService = Depends(get_metricas_costo_service)):
    await service.restore(metricas_costo_id)
    return None