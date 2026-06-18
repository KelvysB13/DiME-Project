from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from resources.db import get_async_db
from infrastructure.persistence.repositories.publicacion import PublicacionRepository
from application.services.publicacion import PublicacionService
from application.dto.publicacion import Publicacion as PublicacionSchema, PublicacionCreate, PublicacionUpdate
from application.dto.base import PaginatedResponse

router = APIRouter(prefix="/publicacions", tags=["publicacions"])


async def get_publicacion_service(db: AsyncSession = Depends(get_async_db)) -> PublicacionService:
    return PublicacionService(PublicacionRepository(db))


@router.get("/", response_model=PaginatedResponse,
         summary="Listar publicacions",
         description="Obtiene lista paginada de publicacions con búsqueda y ordenamiento")
async def list_publicacions(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    search: str | None = Query(None, description="Buscar en: ml_item_id, titulo, tipo_publicacion, estado_publicacion"),
    sort_by: str | None = Query(None, description="Ordenar por: id_publicacion, id_vendedor, ml_item_id, titulo, tipo_publicacion, estado_publicacion"),
    sort_desc: bool = Query(False, description="Orden descendente"),
    service: PublicacionService = Depends(get_publicacion_service),
):
    items, total = await service.get_all(skip=skip, limit=limit, search=search, sort_by=sort_by, sort_desc=sort_desc)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{publicacion_id}", response_model=PublicacionSchema,
         summary="Obtener Publicacion por ID",
         responses={404: {'description': 'Publicacion no encontrado'}})
async def get_publicacion(publicacion_id: int, service: PublicacionService = Depends(get_publicacion_service)):
    return await service.get_by_id(publicacion_id)


@router.post("/", response_model=PublicacionSchema, status_code=status.HTTP_201_CREATED,
          summary="Crear Publicacion",
          description="Crea un nuevo registro de Publicacion",
          responses={409: {'description': 'Conflicto'}, 422: {'description': 'Error de validación'}})
async def create_publicacion(data: PublicacionCreate, service: PublicacionService = Depends(get_publicacion_service)):
    return await service.create(data)


@router.put("/{publicacion_id}", response_model=PublicacionSchema,
         summary="Actualizar Publicacion",
         description="Actualiza un registro existente de Publicacion",
         responses={404: {'description': 'Publicacion no encontrado'}})
async def update_publicacion(publicacion_id: int, data: PublicacionUpdate, service: PublicacionService = Depends(get_publicacion_service)):
    return await service.update(publicacion_id, data)


@router.delete("/{publicacion_id}", status_code=status.HTTP_204_NO_CONTENT,
           summary="Eliminar Publicacion",
           description="Elimina un registro de Publicacion",
           responses={404: {'description': 'Publicacion no encontrado'}})
async def delete_publicacion(publicacion_id: int, service: PublicacionService = Depends(get_publicacion_service)):
    await service.delete(publicacion_id)
    return None


@router.post("/{publicacion_id}/soft-delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_publicacion(publicacion_id: int, service: PublicacionService = Depends(get_publicacion_service)):
    await service.soft_delete(publicacion_id)
    return None


@router.post("/{publicacion_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_publicacion(publicacion_id: int, service: PublicacionService = Depends(get_publicacion_service)):
    await service.restore(publicacion_id)
    return None