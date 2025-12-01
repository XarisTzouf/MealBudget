
from fastapi import APIRouter, HTTPException, status
from app.core.domain_models import PlanRequest, PlanResponse
from app.core.optimization import solve

router = APIRouter(prefix="/budget", tags=["budget"])

@router.post("/optimize", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def optimize(req: PlanRequest) -> PlanResponse:
    try:
        return solve(req)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="optimization failed")

