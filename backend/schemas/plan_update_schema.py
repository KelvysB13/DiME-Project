from pydantic import BaseModel, Field


class PlanChangeRequest(BaseModel):
    tipo_plan: int = Field(..., ge=1, description="ID del nuevo plan")
