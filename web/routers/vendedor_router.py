from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from resources.db import get_async_db
from infrastructure.persistence.repositories.vendedor import VendedorRepository
from application.services.vendedor import VendedorService
from application.dto.vendedor import Vendedor as VendedorSchema, VendedorCreate, VendedorUpdate
from application.dto.base import PaginatedResponse

router = APIRouter(prefix="/vendedors", tags=["vendedors"])


async def get_vendedor_service(db: AsyncSession = Depends(get_async_db)) -> VendedorService:
    return VendedorService(VendedorRepository(db))


@router.get("/", response_model=PaginatedResponse,
         summary="Listar vendedors",
         description="Obtiene lista paginada de vendedors con búsqueda y ordenamiento")
async def list_vendedors(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo de registros"),
    search: str | None = Query(None, description="Buscar en: user_name, nombre_tienda, codigo_pais, moneda_local, email, access_token, refresh_token"),
    sort_by: str | None = Query(None, description="Ordenar por: id_vendedor, user_name, nombre_tienda, codigo_pais, moneda_local, tipo_plan, email, access_token, refresh_token, tiempo_token, esta_activo, fecha_creacion"),
    sort_desc: bool = Query(False, description="Orden descendente"),
    service: VendedorService = Depends(get_vendedor_service),
):
    items, total = await service.get_all(skip=skip, limit=limit, search=search, sort_by=sort_by, sort_desc=sort_desc)
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{vendedor_id}", response_model=VendedorSchema,
         summary="Obtener Vendedor por ID",
         responses={404: {'description': 'Vendedor no encontrado'}})
async def get_vendedor(vendedor_id: int, service: VendedorService = Depends(get_vendedor_service)):
    return await service.get_by_id(vendedor_id)


@router.post("/", response_model=VendedorSchema, status_code=status.HTTP_201_CREATED,
          summary="Crear Vendedor",
          description="Crea un nuevo registro de Vendedor",
          responses={409: {'description': 'Conflicto'}, 422: {'description': 'Error de validación'}})
async def create_vendedor(data: VendedorCreate, service: VendedorService = Depends(get_vendedor_service)):
    return await service.create(data)


@router.put("/{vendedor_id}", response_model=VendedorSchema,
         summary="Actualizar Vendedor",
         description="Actualiza un registro existente de Vendedor",
         responses={404: {'description': 'Vendedor no encontrado'}})
async def update_vendedor(vendedor_id: int, data: VendedorUpdate, service: VendedorService = Depends(get_vendedor_service)):
    return await service.update(vendedor_id, data)


@router.delete("/{vendedor_id}", status_code=status.HTTP_204_NO_CONTENT,
           summary="Eliminar Vendedor",
           description="Elimina un registro de Vendedor",
           responses={404: {'description': 'Vendedor no encontrado'}})
async def delete_vendedor(vendedor_id: int, service: VendedorService = Depends(get_vendedor_service)):
    await service.delete(vendedor_id)
    return None


@router.post("/{vendedor_id}/soft-delete", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_vendedor(vendedor_id: int, service: VendedorService = Depends(get_vendedor_service)):
    await service.soft_delete(vendedor_id)
    return None


@router.post("/{vendedor_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
async def restore_vendedor(vendedor_id: int, service: VendedorService = Depends(get_vendedor_service)):
    await service.restore(vendedor_id)
    return None