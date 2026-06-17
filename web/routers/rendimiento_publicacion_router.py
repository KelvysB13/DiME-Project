from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from resources.db import get_async_db
from infrastructure.persistence.repositories.rendimiento_publicacion import Rendimiento_publicacionRepository
from application.services.rendimiento_publicacion import Rendimiento_publicacionService
from application.dto.rendimiento_publicacion import Rendimiento_publicacion as Rendimiento_publicacionSchema, Rendimiento_publicacionCreate, Rendimiento_publicacionUpdate
from application.dto.base import PaginatedResponse

router = APIRouter(prefix="/rendimiento_publicacions", tags=["rendimiento_publicacions"])


async def get_rendimiento_publicacion_service(db: AsyncSession = Depends(get_async_db)) -> Rendimiento_publicacionService:
    return Rendimiento_publicacionService(Rendimiento_publicacionRepository(db))


@router.get("/", response_model=PaginatedResponse,
         summary="Listar rendimiento_publicacions",
         description="Obtiene lista paginada de rendimiento_publicacions")
async def list_rendimiento_publicacions(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    service: Rendimiento_publicacionService = Depends(get_rendimiento_publicacion_service),
):
    items, total = await service.get_all(skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{rendimiento_publicacion_id}", response_model=Rendimiento_publicacionSchema,
         summary="Obtener Rendimiento_publicacion por ID",
         responses={404: {'description': 'Rendimiento_publicacion no encontrado'}})
async def get_rendimiento_publicacion(rendimiento_publicacion_id: int, service: Rendimiento_publicacionService = Depends(get_rendimiento_publicacion_service)):
    return await service.get_by_id(rendimiento_publicacion_id)


@router.post("/", response_model=Rendimiento_publicacionSchema, status_code=status.HTTP_201_CREATED,
          summary="Crear Rendimiento_publicacion",
          description="Crea un nuevo registro de Rendimiento_publicacion",
          responses={409: {'description': 'Conflicto'}, 422: {'description': 'Error de validación'}})
async def create_rendimiento_publicacion(data: Rendimiento_publicacionCreate, service: Rendimiento_publicacionService = Depends(get_rendimiento_publicacion_service)):
    return await service.create(data)


@router.put("/{rendimiento_publicacion_id}", response_model=Rendimiento_publicacionSchema,
         summary="Actualizar Rendimiento_publicacion",
         description="Actualiza un registro existente de Rendimiento_publicacion",
         responses={404: {'description': 'Rendimiento_publicacion no encontrado'}})
async def update_rendimiento_publicacion(rendimiento_publicacion_id: int, data: Rendimiento_publicacionUpdate, service: Rendimiento_publicacionService = Depends(get_rendimiento_publicacion_service)):
    return await service.update(rendimiento_publicacion_id, data)


@router.delete("/{rendimiento_publicacion_id}", status_code=status.HTTP_204_NO_CONTENT,
           summary="Eliminar Rendimiento_publicacion",
           description="Elimina un registro de Rendimiento_publicacion",
           responses={404: {'description': 'Rendimiento_publicacion no encontrado'}})
async def delete_rendimiento_publicacion(rendimiento_publicacion_id: int, service: Rendimiento_publicacionService = Depends(get_rendimiento_publicacion_service)):
    await service.delete(rendimiento_publicacion_id)
    return None


@router.post("/{rendimiento_publicacion_id}/soft-delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_rendimiento_publicacion(rendimiento_publicacion_id: int, service: Rendimiento_publicacionService = Depends(get_rendimiento_publicacion_service)):
    await service.soft_delete(rendimiento_publicacion_id)
    return None


@router.post("/{rendimiento_publicacion_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_rendimiento_publicacion(rendimiento_publicacion_id: int, service: Rendimiento_publicacionService = Depends(get_rendimiento_publicacion_service)):
    await service.restore(rendimiento_publicacion_id)
    return None