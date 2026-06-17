from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from resources.db import get_async_db
from infrastructure.persistence.repositories.metricas_calidad_publicacion import Metricas_calidad_publicacionRepository
from application.services.metricas_calidad_publicacion import Metricas_calidad_publicacionService
from application.dto.metricas_calidad_publicacion import Metricas_calidad_publicacion as Metricas_calidad_publicacionSchema, Metricas_calidad_publicacionCreate, Metricas_calidad_publicacionUpdate
from application.dto.base import PaginatedResponse

router = APIRouter(prefix="/metricas_calidad_publicacions", tags=["metricas_calidad_publicacions"])


async def get_metricas_calidad_publicacion_service(db: AsyncSession = Depends(get_async_db)) -> Metricas_calidad_publicacionService:
    return Metricas_calidad_publicacionService(Metricas_calidad_publicacionRepository(db))


@router.get("/", response_model=PaginatedResponse,
         summary="Listar metricas_calidad_publicacions",
         description="Obtiene lista paginada de metricas_calidad_publicacions")
async def list_metricas_calidad_publicacions(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    service: Metricas_calidad_publicacionService = Depends(get_metricas_calidad_publicacion_service),
):
    items, total = await service.get_all(skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{metricas_calidad_publicacion_id}", response_model=Metricas_calidad_publicacionSchema,
         summary="Obtener Metricas_calidad_publicacion por ID",
         responses={404: {'description': 'Metricas_calidad_publicacion no encontrado'}})
async def get_metricas_calidad_publicacion(metricas_calidad_publicacion_id: int, service: Metricas_calidad_publicacionService = Depends(get_metricas_calidad_publicacion_service)):
    return await service.get_by_id(metricas_calidad_publicacion_id)


@router.post("/", response_model=Metricas_calidad_publicacionSchema, status_code=status.HTTP_201_CREATED,
          summary="Crear Metricas_calidad_publicacion",
          description="Crea un nuevo registro de Metricas_calidad_publicacion",
          responses={409: {'description': 'Conflicto'}, 422: {'description': 'Error de validación'}})
async def create_metricas_calidad_publicacion(data: Metricas_calidad_publicacionCreate, service: Metricas_calidad_publicacionService = Depends(get_metricas_calidad_publicacion_service)):
    return await service.create(data)


@router.put("/{metricas_calidad_publicacion_id}", response_model=Metricas_calidad_publicacionSchema,
         summary="Actualizar Metricas_calidad_publicacion",
         description="Actualiza un registro existente de Metricas_calidad_publicacion",
         responses={404: {'description': 'Metricas_calidad_publicacion no encontrado'}})
async def update_metricas_calidad_publicacion(metricas_calidad_publicacion_id: int, data: Metricas_calidad_publicacionUpdate, service: Metricas_calidad_publicacionService = Depends(get_metricas_calidad_publicacion_service)):
    return await service.update(metricas_calidad_publicacion_id, data)


@router.delete("/{metricas_calidad_publicacion_id}", status_code=status.HTTP_204_NO_CONTENT,
           summary="Eliminar Metricas_calidad_publicacion",
           description="Elimina un registro de Metricas_calidad_publicacion",
           responses={404: {'description': 'Metricas_calidad_publicacion no encontrado'}})
async def delete_metricas_calidad_publicacion(metricas_calidad_publicacion_id: int, service: Metricas_calidad_publicacionService = Depends(get_metricas_calidad_publicacion_service)):
    await service.delete(metricas_calidad_publicacion_id)
    return None


@router.post("/{metricas_calidad_publicacion_id}/soft-delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_metricas_calidad_publicacion(metricas_calidad_publicacion_id: int, service: Metricas_calidad_publicacionService = Depends(get_metricas_calidad_publicacion_service)):
    await service.soft_delete(metricas_calidad_publicacion_id)
    return None


@router.post("/{metricas_calidad_publicacion_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_metricas_calidad_publicacion(metricas_calidad_publicacion_id: int, service: Metricas_calidad_publicacionService = Depends(get_metricas_calidad_publicacion_service)):
    await service.restore(metricas_calidad_publicacion_id)
    return None