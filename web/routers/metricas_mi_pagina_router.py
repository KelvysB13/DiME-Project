from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from resources.db import get_async_db
from infrastructure.persistence.repositories.metricas_mi_pagina import Metricas_mi_paginaRepository
from application.services.metricas_mi_pagina import Metricas_mi_paginaService
from application.dto.metricas_mi_pagina import Metricas_mi_pagina as Metricas_mi_paginaSchema, Metricas_mi_paginaCreate, Metricas_mi_paginaUpdate
from application.dto.base import PaginatedResponse

router = APIRouter(prefix="/metricas_mi_paginas", tags=["metricas_mi_paginas"])


async def get_metricas_mi_pagina_service(db: AsyncSession = Depends(get_async_db)) -> Metricas_mi_paginaService:
    return Metricas_mi_paginaService(Metricas_mi_paginaRepository(db))


@router.get("/", response_model=PaginatedResponse,
         summary="Listar metricas_mi_paginas",
         description="Obtiene lista paginada de metricas_mi_paginas")
async def list_metricas_mi_paginas(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    service: Metricas_mi_paginaService = Depends(get_metricas_mi_pagina_service),
):
    items, total = await service.get_all(skip=skip, limit=limit)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{metricas_mi_pagina_id}", response_model=Metricas_mi_paginaSchema,
         summary="Obtener Metricas_mi_pagina por ID",
         responses={404: {'description': 'Metricas_mi_pagina no encontrado'}})
async def get_metricas_mi_pagina(metricas_mi_pagina_id: int, service: Metricas_mi_paginaService = Depends(get_metricas_mi_pagina_service)):
    return await service.get_by_id(metricas_mi_pagina_id)


@router.post("/", response_model=Metricas_mi_paginaSchema, status_code=status.HTTP_201_CREATED,
          summary="Crear Metricas_mi_pagina",
          description="Crea un nuevo registro de Metricas_mi_pagina",
          responses={409: {'description': 'Conflicto'}, 422: {'description': 'Error de validación'}})
async def create_metricas_mi_pagina(data: Metricas_mi_paginaCreate, service: Metricas_mi_paginaService = Depends(get_metricas_mi_pagina_service)):
    return await service.create(data)


@router.put("/{metricas_mi_pagina_id}", response_model=Metricas_mi_paginaSchema,
         summary="Actualizar Metricas_mi_pagina",
         description="Actualiza un registro existente de Metricas_mi_pagina",
         responses={404: {'description': 'Metricas_mi_pagina no encontrado'}})
async def update_metricas_mi_pagina(metricas_mi_pagina_id: int, data: Metricas_mi_paginaUpdate, service: Metricas_mi_paginaService = Depends(get_metricas_mi_pagina_service)):
    return await service.update(metricas_mi_pagina_id, data)


@router.delete("/{metricas_mi_pagina_id}", status_code=status.HTTP_204_NO_CONTENT,
           summary="Eliminar Metricas_mi_pagina",
           description="Elimina un registro de Metricas_mi_pagina",
           responses={404: {'description': 'Metricas_mi_pagina no encontrado'}})
async def delete_metricas_mi_pagina(metricas_mi_pagina_id: int, service: Metricas_mi_paginaService = Depends(get_metricas_mi_pagina_service)):
    await service.delete(metricas_mi_pagina_id)
    return None


@router.post("/{metricas_mi_pagina_id}/soft-delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_metricas_mi_pagina(metricas_mi_pagina_id: int, service: Metricas_mi_paginaService = Depends(get_metricas_mi_pagina_service)):
    await service.soft_delete(metricas_mi_pagina_id)
    return None


@router.post("/{metricas_mi_pagina_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_metricas_mi_pagina(metricas_mi_pagina_id: int, service: Metricas_mi_paginaService = Depends(get_metricas_mi_pagina_service)):
    await service.restore(metricas_mi_pagina_id)
    return None