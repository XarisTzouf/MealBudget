from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import orm_models as models
from app.db.schemas import PlanCreate, PlanRead, PlanStats

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("", response_model=PlanRead, status_code=status.HTTP_201_CREATED)
def create_plan(payload: PlanCreate, db: Session = Depends(get_db)) -> PlanRead:
    unique_ids = list(set(payload.meal_ids or []))

    meals = []
    if unique_ids:
        meals = db.query(models.Meal).filter(models.Meal.id.in_(unique_ids)).all()
        if len(meals) != len(unique_ids):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found")

    plan = models.Plan(title=payload.title, budget=payload.budget)
    plan.meals = meals
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return PlanRead.model_validate(plan)


@router.get("/{plan_id}", response_model=PlanRead)
def get_plan(plan_id: int, db: Session = Depends(get_db)) -> PlanRead:
    plan = db.get(models.Plan, plan_id)
    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    return PlanRead.model_validate(plan)


@router.get("/{plan_id}/stats", response_model=PlanStats)
def get_plan_stats(plan_id: int, db: Session = Depends(get_db)) -> PlanStats:
    plan = db.get(models.Plan, plan_id)
    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")

    total_cost = sum((m.cost or 0.0) for m in plan.meals)
    kcal = sum((m.kcal or 0.0) for m in plan.meals)
    protein = sum((m.protein or 0.0) for m in plan.meals)
    fat = sum((m.fat or 0.0) for m in plan.meals)
    carbs = sum((m.carbs or 0.0) for m in plan.meals)

    return PlanStats(
        plan_id=plan.id,
        total_cost=total_cost,
        kcal=kcal,
        protein=protein,
        fat=fat,
        carbs=carbs,
    )
