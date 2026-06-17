from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from resources.db import get_async_db
from infrastructure.persistence.repositories.pais import PaisRepository
from application.services.pais import PaisService
from application.dto.pais import Pais as PaisSchema, PaisCreate, PaisUpdate
from application.dto.base import PaginatedResponse

router = APIRouter(prefix="/pais", tags=["pais"])


async def get_pais_service(db: AsyncSession = Depends(get_async_db)) -> PaisService:
    return PaisService(PaisRepository(db))


@router.get("/", response_model=PaginatedResponse,
         summary="Listar pais",
         description="Obtiene lista paginada de pais con búsqueda y ordenamiento")
async def list_pais(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    search: Optional[str] = Query(None, description="Buscar en: codigo_pais, nombre_pais"),
    sort_by: Optional[str] = Query(None, description="Ordenar por: codigo_pais, nombre_pais"),
    sort_desc: bool = Query(False, description="Orden descendente"),
    service: PaisService = Depends(get_pais_service),
):
    items, total = await service.get_all(skip=skip, limit=limit, search=search, sort_by=sort_by, sort_desc=sort_desc)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{pais_id}", response_model=PaisSchema,
         summary="Obtener Pais por ID",
         responses={404: {'description': 'Pais no encontrado'}})
async def get_pais(pais_id: str, service: PaisService = Depends(get_pais_service)):
    return await service.get_by_id(pais_id)


@router.post("/", response_model=PaisSchema, status_code=status.HTTP_201_CREATED,
          summary="Crear Pais",
          description="Crea un nuevo registro de Pais",
          responses={409: {'description': 'Conflicto'}, 422: {'description': 'Error de validación'}})
async def create_pais(data: PaisCreate, service: PaisService = Depends(get_pais_service)):
    return await service.create(data)


@router.put("/{pais_id}", response_model=PaisSchema,
         summary="Actualizar Pais",
         description="Actualiza un registro existente de Pais",
         responses={404: {'description': 'Pais no encontrado'}})
async def update_pais(pais_id: str, data: PaisUpdate, service: PaisService = Depends(get_pais_service)):
    return await service.update(pais_id, data)


@router.delete("/{pais_id}", status_code=status.HTTP_204_NO_CONTENT,
           summary="Eliminar Pais",
           description="Elimina un registro de Pais",
           responses={404: {'description': 'Pais no encontrado'}})
async def delete_pais(pais_id: str, service: PaisService = Depends(get_pais_service)):
    await service.delete(pais_id)
    return None


@router.post("/{pais_id}/soft-delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_pais(pais_id: str, service: PaisService = Depends(get_pais_service)):
    await service.soft_delete(pais_id)
    return None


@router.post("/{pais_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_pais(pais_id: str, service: PaisService = Depends(get_pais_service)):
    await service.restore(pais_id)
    return None