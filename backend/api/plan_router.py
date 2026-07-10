from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.plan_schema import PlanCreate, PlanUpdate, PlanResponse, PlanListResponse
from services.plan_service import (obtener_plans as service_obtener_plans, obtener_plan_por_id, crear_plan, actualizar_plan, eliminar_plan, PlanNotFoundError, PlanNameAlreadyExistsError)

router = APIRouter()

@router.get("/plans", response_model=PlanListResponse)
def obtener_plans(db: Session = Depends(get_db)):

    planes = service_obtener_plans(db)
    return PlanListResponse(planes=planes)

@router.get("/plans/{plan_id}", response_model=PlanResponse)
def obtener_plan(plan_id: int, db: Session = Depends(get_db)):

    try:
        return obtener_plan_por_id(db, plan_id)
    
    except PlanNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan no encontrado")

@router.post("/plans", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def crear(payload: PlanCreate, db: Session = Depends(get_db)):

    try:
        return crear_plan(db, payload)
    
    except PlanNameAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un plan con ese nombre")

@router.put("/plans/{plan_id}", response_model=PlanResponse)
def actualizar(plan_id: int, payload: PlanUpdate, db: Session = Depends(get_db)):

    try:
        return actualizar_plan(db, plan_id, payload)
    
    except PlanNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan no encontrado")
    
    except PlanNameAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un plan con ese nombre")

@router.delete("/plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(plan_id: int, db: Session = Depends(get_db)):

    try:
        eliminar_plan(db, plan_id)
        
    except PlanNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan no encontrado")
