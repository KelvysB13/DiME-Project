from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from resources.db import get_async_db
from infrastructure.persistence.repositories.metricas_reputacion import Metricas_reputacionRepository
from application.services.metricas_reputacion import Metricas_reputacionService
from application.dto.metricas_reputacion import Metricas_reputacion as Metricas_reputacionSchema, Metricas_reputacionCreate, Metricas_reputacionUpdate
from application.dto.base import PaginatedResponse

router = APIRouter(prefix="/metricas_reputacions", tags=["metricas_reputacions"])


async def get_metricas_reputacion_service(db: AsyncSession = Depends(get_async_db)) -> Metricas_reputacionService:
    return Metricas_reputacionService(Metricas_reputacionRepository(db))


@router.get("/", response_model=PaginatedResponse,
         summary="Listar metricas_reputacions",
         description="Obtiene lista paginada de metricas_reputacions con búsqueda y ordenamiento")
async def list_metricas_reputacions(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    search: Optional[str] = Query(None, description="Buscar en: nivel_reputacion, insignia"),
    sort_by: Optional[str] = Query(None, description="Ordenar por: id_metricas_reputacion, id_vendedor, fecha_captura, ventas_totales_periodo, total_reclamos, total_mediaciones, total_canceladas, total_envios_incorrectos, nivel_reputacion, insignia"),
    sort_desc: bool = Query(False, description="Orden descendente"),
    service: Metricas_reputacionService = Depends(get_metricas_reputacion_service),
):
    items, total = await service.get_all(skip=skip, limit=limit, search=search, sort_by=sort_by, sort_desc=sort_desc)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{metricas_reputacion_id}", response_model=Metricas_reputacionSchema,
         summary="Obtener Metricas_reputacion por ID",
         responses={404: {'description': 'Metricas_reputacion no encontrado'}})
async def get_metricas_reputacion(metricas_reputacion_id: int, service: Metricas_reputacionService = Depends(get_metricas_reputacion_service)):
    return await service.get_by_id(metricas_reputacion_id)


@router.post("/", response_model=Metricas_reputacionSchema, status_code=status.HTTP_201_CREATED,
          summary="Crear Metricas_reputacion",
          description="Crea un nuevo registro de Metricas_reputacion",
          responses={409: {'description': 'Conflicto'}, 422: {'description': 'Error de validación'}})
async def create_metricas_reputacion(data: Metricas_reputacionCreate, service: Metricas_reputacionService = Depends(get_metricas_reputacion_service)):
    return await service.create(data)


@router.put("/{metricas_reputacion_id}", response_model=Metricas_reputacionSchema,
         summary="Actualizar Metricas_reputacion",
         description="Actualiza un registro existente de Metricas_reputacion",
         responses={404: {'description': 'Metricas_reputacion no encontrado'}})
async def update_metricas_reputacion(metricas_reputacion_id: int, data: Metricas_reputacionUpdate, service: Metricas_reputacionService = Depends(get_metricas_reputacion_service)):
    return await service.update(metricas_reputacion_id, data)


@router.delete("/{metricas_reputacion_id}", status_code=status.HTTP_204_NO_CONTENT,
           summary="Eliminar Metricas_reputacion",
           description="Elimina un registro de Metricas_reputacion",
           responses={404: {'description': 'Metricas_reputacion no encontrado'}})
async def delete_metricas_reputacion(metricas_reputacion_id: int, service: Metricas_reputacionService = Depends(get_metricas_reputacion_service)):
    await service.delete(metricas_reputacion_id)
    return None


@router.post("/{metricas_reputacion_id}/soft-delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_metricas_reputacion(metricas_reputacion_id: int, service: Metricas_reputacionService = Depends(get_metricas_reputacion_service)):
    await service.soft_delete(metricas_reputacion_id)
    return None


@router.post("/{metricas_reputacion_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_metricas_reputacion(metricas_reputacion_id: int, service: Metricas_reputacionService = Depends(get_metricas_reputacion_service)):
    await service.restore(metricas_reputacion_id)
    return None