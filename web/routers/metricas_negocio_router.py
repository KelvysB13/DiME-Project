from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from resources.db import get_async_db
from infrastructure.persistence.repositories.metricas_negocio import Metricas_negocioRepository
from application.services.metricas_negocio import Metricas_negocioService
from application.dto.metricas_negocio import Metricas_negocio as Metricas_negocioSchema, Metricas_negocioCreate, Metricas_negocioUpdate
from application.dto.base import PaginatedResponse

router = APIRouter(prefix="/metricas_negocios", tags=["metricas_negocios"])


async def get_metricas_negocio_service(db: AsyncSession = Depends(get_async_db)) -> Metricas_negocioService:
    return Metricas_negocioService(Metricas_negocioRepository(db))


@router.get("/", response_model=PaginatedResponse,
         summary="Listar metricas_negocios",
         description="Obtiene lista paginada de metricas_negocios")
async def list_metricas_negocios(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    service: Metricas_negocioService = Depends(get_metricas_negocio_service),
):
    items, total = await service.get_all(skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{metricas_negocio_id}", response_model=Metricas_negocioSchema,
         summary="Obtener Metricas_negocio por ID",
         responses={404: {'description': 'Metricas_negocio no encontrado'}})
async def get_metricas_negocio(metricas_negocio_id: int, service: Metricas_negocioService = Depends(get_metricas_negocio_service)):
    return await service.get_by_id(metricas_negocio_id)


@router.post("/", response_model=Metricas_negocioSchema, status_code=status.HTTP_201_CREATED,
          summary="Crear Metricas_negocio",
          description="Crea un nuevo registro de Metricas_negocio",
          responses={409: {'description': 'Conflicto'}, 422: {'description': 'Error de validación'}})
async def create_metricas_negocio(data: Metricas_negocioCreate, service: Metricas_negocioService = Depends(get_metricas_negocio_service)):
    return await service.create(data)


@router.put("/{metricas_negocio_id}", response_model=Metricas_negocioSchema,
         summary="Actualizar Metricas_negocio",
         description="Actualiza un registro existente de Metricas_negocio",
         responses={404: {'description': 'Metricas_negocio no encontrado'}})
async def update_metricas_negocio(metricas_negocio_id: int, data: Metricas_negocioUpdate, service: Metricas_negocioService = Depends(get_metricas_negocio_service)):
    return await service.update(metricas_negocio_id, data)


@router.delete("/{metricas_negocio_id}", status_code=status.HTTP_204_NO_CONTENT,
           summary="Eliminar Metricas_negocio",
           description="Elimina un registro de Metricas_negocio",
           responses={404: {'description': 'Metricas_negocio no encontrado'}})
async def delete_metricas_negocio(metricas_negocio_id: int, service: Metricas_negocioService = Depends(get_metricas_negocio_service)):
    await service.delete(metricas_negocio_id)
    return None


@router.post("/{metricas_negocio_id}/soft-delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_metricas_negocio(metricas_negocio_id: int, service: Metricas_negocioService = Depends(get_metricas_negocio_service)):
    await service.soft_delete(metricas_negocio_id)
    return None


@router.post("/{metricas_negocio_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_metricas_negocio(metricas_negocio_id: int, service: Metricas_negocioService = Depends(get_metricas_negocio_service)):
    await service.restore(metricas_negocio_id)
    return None