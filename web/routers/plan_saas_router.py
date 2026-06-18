from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from resources.db import get_async_db
from infrastructure.persistence.repositories.plan_saas import Plan_saasRepository
from application.services.plan_saas import Plan_saasService
from application.dto.plan_saas import Plan_saas as Plan_saasSchema, Plan_saasCreate, Plan_saasUpdate
from application.dto.base import PaginatedResponse

router = APIRouter(prefix="/plan_saas", tags=["plan_saas"])


async def get_plan_saas_service(db: AsyncSession = Depends(get_async_db)) -> Plan_saasService:
    return Plan_saasService(Plan_saasRepository(db))


@router.get("/", response_model=PaginatedResponse,
         summary="Listar plan_saas",
         description="Obtiene lista paginada de plan_saas con búsqueda y ordenamiento")
async def list_plan_saas(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    search: str | None = Query(None, description="Buscar en: nombre_plan, descripcion"),
    sort_by: str | None = Query(None, description="Ordenar por: id_plan, nombre_plan, descripcion"),
    sort_desc: bool = Query(False, description="Orden descendente"),
    service: Plan_saasService = Depends(get_plan_saas_service),
):
    items, total = await service.get_all(skip=skip, limit=limit, search=search, sort_by=sort_by, sort_desc=sort_desc)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{plan_saas_id}", response_model=Plan_saasSchema,
         summary="Obtener Plan_saas por ID",
         responses={404: {'description': 'Plan_saas no encontrado'}})
async def get_plan_saas(plan_saas_id: int, service: Plan_saasService = Depends(get_plan_saas_service)):
    return await service.get_by_id(plan_saas_id)


@router.post("/", response_model=Plan_saasSchema, status_code=status.HTTP_201_CREATED,
          summary="Crear Plan_saas",
          description="Crea un nuevo registro de Plan_saas",
          responses={409: {'description': 'Conflicto'}, 422: {'description': 'Error de validación'}})
async def create_plan_saas(data: Plan_saasCreate, service: Plan_saasService = Depends(get_plan_saas_service)):
    return await service.create(data)


@router.put("/{plan_saas_id}", response_model=Plan_saasSchema,
         summary="Actualizar Plan_saas",
         description="Actualiza un registro existente de Plan_saas",
         responses={404: {'description': 'Plan_saas no encontrado'}})
async def update_plan_saas(plan_saas_id: int, data: Plan_saasUpdate, service: Plan_saasService = Depends(get_plan_saas_service)):
    return await service.update(plan_saas_id, data)


@router.delete("/{plan_saas_id}", status_code=status.HTTP_204_NO_CONTENT,
           summary="Eliminar Plan_saas",
           description="Elimina un registro de Plan_saas",
           responses={404: {'description': 'Plan_saas no encontrado'}})
async def delete_plan_saas(plan_saas_id: int, service: Plan_saasService = Depends(get_plan_saas_service)):
    await service.delete(plan_saas_id)
    return None


@router.post("/{plan_saas_id}/soft-delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_plan_saas(plan_saas_id: int, service: Plan_saasService = Depends(get_plan_saas_service)):
    await service.soft_delete(plan_saas_id)
    return None


@router.post("/{plan_saas_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_plan_saas(plan_saas_id: int, service: Plan_saasService = Depends(get_plan_saas_service)):
    await service.restore(plan_saas_id)
    return None