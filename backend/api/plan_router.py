from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.plan_schema import PlanListResponse
from services.plan_service import get_planes

router = APIRouter()

@router.get("/planes", response_model=PlanListResponse)
def listar_planes(db: Session = Depends(get_db)):
    planes = get_planes(db)
    return PlanListResponse(planes=planes)
