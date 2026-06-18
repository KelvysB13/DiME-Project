from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from resources.db import get_async_db
from infrastructure.persistence.repositories.reportes_diagnostico import Reportes_diagnosticoRepository
from application.services.reportes_diagnostico import Reportes_diagnosticoService
from application.dto.reportes_diagnostico import Reportes_diagnostico as Reportes_diagnosticoSchema, Reportes_diagnosticoCreate, Reportes_diagnosticoUpdate
from application.dto.base import PaginatedResponse

router = APIRouter(prefix="/reportes_diagnosticos", tags=["reportes_diagnosticos"])


async def get_reportes_diagnostico_service(db: AsyncSession = Depends(get_async_db)) -> Reportes_diagnosticoService:
    return Reportes_diagnosticoService(Reportes_diagnosticoRepository(db))


@router.get("/", response_model=PaginatedResponse,
         summary="Listar reportes_diagnosticos",
         description="Obtiene lista paginada de reportes_diagnosticos con búsqueda y ordenamiento")
async def list_reportes_diagnosticos(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    search: str | None = Query(None, description="Buscar en: resumen_ejecutivo"),
    sort_by: str | None = Query(None, description="Ordenar por: id_reporte, id_vendedor, fecha_generacion, fecha_inicio_periodo, fecha_fin_periodo, resumen_ejecutivo, plan_accion"),
    sort_desc: bool = Query(False, description="Orden descendente"),
    service: Reportes_diagnosticoService = Depends(get_reportes_diagnostico_service),
):
    items, total = await service.get_all(skip=skip, limit=limit, search=search, sort_by=sort_by, sort_desc=sort_desc)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{reportes_diagnostico_id}", response_model=Reportes_diagnosticoSchema,
         summary="Obtener Reportes_diagnostico por ID",
         responses={404: {'description': 'Reportes_diagnostico no encontrado'}})
async def get_reportes_diagnostico(reportes_diagnostico_id: int, service: Reportes_diagnosticoService = Depends(get_reportes_diagnostico_service)):
    return await service.get_by_id(reportes_diagnostico_id)


@router.post("/", response_model=Reportes_diagnosticoSchema, status_code=status.HTTP_201_CREATED,
          summary="Crear Reportes_diagnostico",
          description="Crea un nuevo registro de Reportes_diagnostico",
          responses={409: {'description': 'Conflicto'}, 422: {'description': 'Error de validación'}})
async def create_reportes_diagnostico(data: Reportes_diagnosticoCreate, service: Reportes_diagnosticoService = Depends(get_reportes_diagnostico_service)):
    return await service.create(data)


@router.put("/{reportes_diagnostico_id}", response_model=Reportes_diagnosticoSchema,
         summary="Actualizar Reportes_diagnostico",
         description="Actualiza un registro existente de Reportes_diagnostico",
         responses={404: {'description': 'Reportes_diagnostico no encontrado'}})
async def update_reportes_diagnostico(reportes_diagnostico_id: int, data: Reportes_diagnosticoUpdate, service: Reportes_diagnosticoService = Depends(get_reportes_diagnostico_service)):
    return await service.update(reportes_diagnostico_id, data)


@router.delete("/{reportes_diagnostico_id}", status_code=status.HTTP_204_NO_CONTENT,
           summary="Eliminar Reportes_diagnostico",
           description="Elimina un registro de Reportes_diagnostico",
           responses={404: {'description': 'Reportes_diagnostico no encontrado'}})
async def delete_reportes_diagnostico(reportes_diagnostico_id: int, service: Reportes_diagnosticoService = Depends(get_reportes_diagnostico_service)):
    await service.delete(reportes_diagnostico_id)
    return None


@router.post("/{reportes_diagnostico_id}/soft-delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_reportes_diagnostico(reportes_diagnostico_id: int, service: Reportes_diagnosticoService = Depends(get_reportes_diagnostico_service)):
    await service.soft_delete(reportes_diagnostico_id)
    return None


@router.post("/{reportes_diagnostico_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_reportes_diagnostico(reportes_diagnostico_id: int, service: Reportes_diagnosticoService = Depends(get_reportes_diagnostico_service)):
    await service.restore(reportes_diagnostico_id)
    return None